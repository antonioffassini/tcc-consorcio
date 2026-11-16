"""Constrói os painéis do TCC a partir de data/raw/bacen.

Uso (alvo ``make painel``)::

    python -m src.pipeline.build_panel --raw data/raw --out data/processed

Saídas
------
data/processed/painel_a_grupo_mes.parquet
    Painel A, grupo × mês, segmento imóveis, data-base >= 2024-07
    (vigência da Res. BCB 285/2023, ESTADO.md §5 item 6).
data/processed/painel_b_adm_trimestre.parquet
    Painel B, administradora × trimestre, segmento imóveis, todas as
    data-bases (2017-03 a 2026-03) com coluna ``regime``; UFs agregadas.
data/processed/conciliacao.parquet
    Conferências cruzadas entre arquivos (usadas pelos testes).
results/qualidade_dados.csv
    Relatório de qualidade (formato longo).

Nada em ``data/raw`` é escrito.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from . import leitura as lt

INICIO_REGIME = 202407  # Res. BCB 285/2023, art. 59 (red. Res. BCB 362/2023)
INICIO_REGIME_TRIM = 202409  # primeiro trimestre inteiro sob a Res. 285
SEGMENTO_IMOVEIS = 1
# Res. BCB 381/2024: medidas temporárias para consorciados do RS, até 31/12/2024.
# Enchentes a partir do fim de abril de 2024: a janela de sensibilidade cobre
# as data-bases de 2024-05 a 2024-12 (mensal) e 2024-06 a 2024-12 (trimestral).
RS_JANELA_MES = (202405, 202412)
RS_JANELA_TRIM = (202406, 202412)
RS_LIMIAR_EXPOSICAO = 0.5

CONTAGENS_GRUPO = [
    "ativas_em_dia", "ativas_contempl_inad", "ativas_nao_contempl_inad",
    "contempladas_mes", "excluidas_estoque", "ativas_quitadas", "credito_pendente",
]
CONTAGENS_UF = [
    "ativos_lance_acum", "ativos_sorteio_acum", "ativos_nao_contemplados",
    "excluidos_contempl_acum", "excluidos_nao_contemplados", "lance_trim",
    "sorteio_trim", "excluidos_contempl_trim", "adesoes_trim",
]


class Qualidade:
    """Acumula linhas do relatório de qualidade (formato longo)."""

    def __init__(self) -> None:
        self.linhas: list[dict] = []

    def add(self, escopo, metrica, valor, arquivo="", data_base="", detalhe=""):
        self.linhas.append(dict(escopo=escopo, arquivo=arquivo, data_base=data_base,
                                metrica=metrica, valor=valor, detalhe=detalhe))

    def df(self) -> pd.DataFrame:
        return pd.DataFrame(self.linhas,
                            columns=["escopo", "arquivo", "data_base", "metrica", "valor", "detalhe"])


def _periodo(aaaamm: pd.Series) -> pd.PeriodIndex:
    return pd.PeriodIndex(aaaamm.astype(int).astype(str), freq="M")


def _sequencia_meses(ini: int, fim: int, passo: int = 1) -> list[int]:
    p = pd.period_range(pd.Period(str(ini), "M"), pd.Period(str(fim), "M"), freq="M")
    return [int(x.strftime("%Y%m")) for x in p[::passo]]


def valida(df: pd.DataFrame, chave: list[str], contagens: list[str], arquivo_db: str,
           q: Qualidade, escopo: str, arquivo: str) -> pd.DataFrame:
    """Aplica as regras de descarte e registra cada motivo no relatório."""
    q.add(escopo, "linhas_lidas", len(df), arquivo, arquivo_db)
    q.add(escopo, "celulas_nulas", int(df.isna().sum().sum()), arquivo, arquivo_db,
          ";".join(f"{c}={n}" for c, n in df.isna().sum().items() if n))
    regras = [
        ("segmento_diferente_de_imoveis", df["segmento"] != SEGMENTO_IMOVEIS),
        ("data_base_diferente_do_arquivo", df["data_base"] != int(arquivo_db)),
        ("chave_nula", df[chave].isna().any(axis=1)),
        ("contagem_nula", df[contagens].isna().any(axis=1)),
        ("contagem_negativa", (df[contagens] < 0).any(axis=1)),
    ]
    descarte = pd.Series(False, index=df.index)
    for motivo, m in regras:
        m = m.fillna(True) & ~descarte
        if m.any():
            q.add(escopo, "linhas_descartadas", int(m.sum()), arquivo, arquivo_db, motivo)
        descarte |= m
    df = df[~descarte]
    dup = df.duplicated(chave, keep="first")
    q.add(escopo, "duplicatas_por_chave", int(dup.sum()), arquivo, arquivo_db, "+".join(chave))
    if dup.any():
        q.add(escopo, "linhas_descartadas", int(dup.sum()), arquivo, arquivo_db, "duplicata")
    q.add(escopo, "linhas_descartadas_total", int(descarte.sum() + dup.sum()), arquivo, arquivo_db,
          "motivos em linhas_descartadas" if (descarte.any() or dup.any()) else "nenhuma")
    q.add(escopo, "linhas_aproveitadas", int((~dup).sum()), arquivo, arquivo_db)
    return df[~dup].copy()


# --------------------------------------------------------------------------
# Painel B — administradora × trimestre (arquivo por UF)
# --------------------------------------------------------------------------
def agrega_uf(uf: pd.DataFrame) -> pd.DataFrame:
    """Agrega as UFs por (data_base, cnpj), mantendo colunas do RS à parte."""
    uf = uf.copy()
    uf["ativos_total"] = uf[["ativos_lance_acum", "ativos_sorteio_acum",
                             "ativos_nao_contemplados"]].sum(axis=1)
    cols = CONTAGENS_UF + ["ativos_total"]
    chave = ["data_base", "cnpj"]
    b = uf.groupby(chave, as_index=False).agg(
        nome_adm=("nome_adm", "last"), n_ufs=("uf", "nunique"),
        **{c: (c, "sum") for c in cols})
    rs = (uf[uf["uf"] == "RS"].groupby(chave)[["lance_trim", "sorteio_trim", "ativos_total"]]
          .sum().add_suffix("_rs"))
    b = b.merge(rs, left_on=chave, right_index=True, how="left")
    for c in ["lance_trim_rs", "sorteio_trim_rs", "ativos_total_rs"]:
        b[c] = b[c].fillna(0).astype("int64")
    return b


def deriva_b(b: pd.DataFrame) -> pd.DataFrame:
    b = b.copy()
    b["contempl_trim"] = b["lance_trim"] + b["sorteio_trim"]
    b["frac_lance"] = b["lance_trim"] / b["contempl_trim"].replace(0, np.nan)
    ex = (b["lance_trim"] - b["lance_trim_rs"]) + (b["sorteio_trim"] - b["sorteio_trim_rs"])
    b["contempl_trim_ex_rs"] = ex
    b["frac_lance_ex_rs"] = (b["lance_trim"] - b["lance_trim_rs"]) / ex.replace(0, np.nan)
    b["rs_exposicao"] = b["ativos_total_rs"] / b["ativos_total"].replace(0, np.nan)
    b["regime"] = np.where(b["data_base"] >= INICIO_REGIME_TRIM, "pos285", "pre285")
    b["flag_rs_2024"] = b["data_base"].between(*RS_JANELA_TRIM)
    b["flag_rs_2024_exposta"] = b["flag_rs_2024"] & (b["rs_exposicao"] >= RS_LIMIAR_EXPOSICAO)
    b["trimestre"] = _periodo(b["data_base"]).asfreq("Q").astype(str)
    return b


# --------------------------------------------------------------------------
# Painel A — grupo × mês
# --------------------------------------------------------------------------
def deriva_a(g: pd.DataFrame) -> pd.DataFrame:
    """Variáveis derivadas do painel por grupo. Espera todas as data-bases
    necessárias (inclusive o mês anterior ao início, para as diferenças)."""
    g = g.sort_values(["cnpj", "grupo", "data_base"]).copy()
    g["ativas"] = g["ativas_em_dia"] + g["ativas_contempl_inad"] + g["ativas_nao_contempl_inad"]
    g["cotas_total"] = g["ativas"] + g["excluidas_estoque"]
    g["meses_restantes"] = g["prazo"] - g["assembleia"]
    g["taxa_contemplacao"] = g["contempladas_mes"] / g["ativas"].replace(0, np.nan)
    per = _periodo(g["data_base"])
    g["_ord"] = per.year * 12 + per.month
    gb = g.groupby(["cnpj", "grupo"], sort=False)
    consecutivo = (g["_ord"] - gb["_ord"].shift()) == 1
    g["flag_mes_anterior_ausente"] = ~consecutivo
    g["excluidas_var"] = gb["excluidas_estoque"].diff().where(consecutivo)
    g["excluidas_mes"] = g["excluidas_var"].clip(lower=0)
    g["flag_excluidas_var_negativa"] = g["excluidas_var"] < 0
    g["flag_ativas_zero"] = g["ativas"] == 0
    g["flag_assembleia_maior_prazo"] = g["assembleia"] > g["prazo"]
    g["sem_contemplacao"] = g["contempladas_mes"] == 0
    g["regime"] = np.where(g["data_base"] >= INICIO_REGIME, "pos285", "pre285")
    g["trimestre"] = per.asfreq("Q").astype(str)
    return g.drop(columns="_ord")


def anexa_rs(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Exposição da administradora ao RS (fração das cotas ativas de imóveis
    domiciliadas no RS), tomada do trimestre do arquivo por UF que contém o mês."""
    ex = b[["trimestre", "cnpj", "rs_exposicao"]]
    a = a.merge(ex, on=["trimestre", "cnpj"], how="left")
    a["flag_rs_2024"] = a["data_base"].between(*RS_JANELA_MES) & (
        a["rs_exposicao"] >= RS_LIMIAR_EXPOSICAO)
    return a


ORDEM_A = [
    "cnpj", "nome_adm", "grupo", "data_base", "trimestre", "regime", "assembleia", "prazo",
    "meses_restantes", "valor_bem", "taxa_adm", "indice_correcao", "ativas", "ativas_em_dia",
    "ativas_contempl_inad", "ativas_nao_contempl_inad", "ativas_quitadas", "credito_pendente",
    "contempladas_mes", "taxa_contemplacao", "sem_contemplacao", "excluidas_estoque",
    "excluidas_var", "excluidas_mes", "cotas_total", "rs_exposicao", "flag_rs_2024",
    "flag_mes_anterior_ausente", "flag_excluidas_var_negativa", "flag_ativas_zero",
    "flag_assembleia_maior_prazo",
]


def lacunas(df: pd.DataFrame, chave: list[str], passo: int) -> pd.DataFrame:
    """Meses (ou trimestres) faltantes entre a primeira e a última aparição de cada chave."""
    per = _periodo(df["data_base"])
    o = pd.Series(per.year * 12 + per.month, index=df.index)
    x = o.groupby([df[c] for c in chave]).agg(["min", "max", "count"])
    x["esperado"] = (x["max"] - x["min"]) // passo + 1
    x["faltantes"] = x["esperado"] - x["count"]
    return x


def constroi(raw: Path, out: Path, results: Path) -> dict[str, pd.DataFrame]:
    q = Qualidade()
    mensais, ufs = lt.lista_zips(raw)

    # Arquivos esperados vs presentes
    if mensais:
        esp = _sequencia_meses(min(map(int, mensais)), max(map(int, mensais)))
        falt = [m for m in esp if str(m) not in mensais]
        q.add("arquivos", "meses_mensais_faltantes", len(falt), detalhe=",".join(map(str, falt)))
    if ufs:
        esp = _sequencia_meses(min(map(int, ufs)), max(map(int, ufs)), 3)
        falt = [m for m in esp if str(m) not in ufs]
        q.add("arquivos", "trimestres_uf_faltantes", len(falt), detalhe=",".join(map(str, falt)))

    # ---- leitura e validação: grupos e segmentos consolidados
    grupos, segs, cabecalhos = [], [], set()
    for aaaamm, p in mensais.items():
        r = lt.le_mensal(p, aaaamm, "grupos")
        if r is None:
            q.add("grupos", "membro_ausente", 1, p.name, aaaamm, "Bens_Imoveis_Grupos.csv")
            continue
        cabecalhos.add((tuple(r.colunas_ausentes), tuple(r.colunas_extras)))
        if r.colunas_ausentes or r.colunas_extras:
            q.add("grupos", "leiaute_divergente", 1, r.arquivo, aaaamm,
                  f"ausentes={r.colunas_ausentes};extras={r.colunas_extras}")
        grupos.append(valida(r.df, ["cnpj", "grupo", "data_base"], CONTAGENS_GRUPO + ["prazo", "assembleia"],
                             aaaamm, q, "grupos", r.arquivo))
        s = lt.le_mensal(p, aaaamm, "segmentos")
        if s is not None:
            segs.append(s.df[s.df["segmento"] == SEGMENTO_IMOVEIS])
    g_all = pd.concat(grupos, ignore_index=True)
    seg = pd.concat(segs, ignore_index=True)

    ufl = []
    for aaaamm, p in ufs.items():
        r = lt.le_uf(p, aaaamm)
        if r is None:
            q.add("uf", "membro_ausente", 1, p.name, aaaamm, "Consorcios_UF.csv")
            continue
        cabecalhos.add((tuple(r.colunas_ausentes), tuple(r.colunas_extras)))
        if r.colunas_ausentes or r.colunas_extras:
            q.add("uf", "leiaute_divergente", 1, r.arquivo, aaaamm,
                  f"ausentes={r.colunas_ausentes};extras={r.colunas_extras}")
        df = r.df
        fora = df["segmento"] != SEGMENTO_IMOVEIS
        q.add("uf", "linhas_lidas_todos_segmentos", len(df), r.arquivo, aaaamm)
        q.add("uf", "linhas_fora_do_recorte", int(fora.sum()), r.arquivo, aaaamm,
              "segmento diferente de imóveis (fora do escopo, não é erro)")
        ufl.append(valida(df[~fora], ["data_base", "cnpj", "uf"], CONTAGENS_UF, aaaamm, q, "uf", r.arquivo))
    uf = pd.concat(ufl, ignore_index=True)

    # ---- checagem de leiaute (IN BCB 525/2024)
    q.add("leiaute", "cabecalhos_divergentes", int(any(a or e for a, e in cabecalhos)),
          detalhe="todos os arquivos com o cabeçalho do dicionário vigente desde 2017-03"
          if not any(a or e for a, e in cabecalhos) else "ver linhas leiaute_divergente")
    g_all = deriva_a(g_all)
    cont = (g_all[g_all["data_base"] >= 202307].groupby("data_base")
            .agg(n=("grupo", "size"), consec=("flag_mes_anterior_ausente", lambda s: 1 - s.mean()),
                 sem_contempl=("sem_contemplacao", "mean"), excl_neg=("flag_excluidas_var_negativa", "mean")))
    for db, r in cont.iterrows():
        q.add("leiaute", "continuidade_grupos", round(float(r["consec"]), 4), "", db,
              f"n_grupos={int(r['n'])};frac_sem_contemplacao={r['sem_contempl']:.4f};"
              f"frac_excl_var_neg={r['excl_neg']:.4f}")

    # ---- Painel B
    b = deriva_b(agrega_uf(uf))
    b = b.sort_values(["data_base", "cnpj"]).reset_index(drop=True)

    # ---- Painel A
    a = g_all[g_all["data_base"] >= INICIO_REGIME].copy()
    a = anexa_rs(a, b)[ORDEM_A].sort_values(["cnpj", "grupo", "data_base"]).reset_index(drop=True)

    # ---- relatórios de painel
    for nome, df, chave, passo in [("painel_a", a, ["cnpj", "grupo"], 1),
                                   ("painel_b", b, ["cnpj"], 3)]:
        q.add(nome, "observacoes", len(df))
        q.add(nome, "administradoras", int(df["cnpj"].nunique()))
        q.add(nome, "data_bases", int(df["data_base"].nunique()),
              detalhe=f"{df['data_base'].min()}-{df['data_base'].max()}")
        q.add(nome, "celulas_nulas", int(df.isna().sum().sum()),
              detalhe=";".join(f"{c}={n}" for c, n in df.isna().sum().items() if n))
        q.add(nome, "duplicatas_por_chave", int(df.duplicated(chave + ["data_base"]).sum()),
              detalhe="+".join(chave + ["data_base"]))
        lac = lacunas(df, chave, passo)
        q.add(nome, "chaves_com_lacuna", int((lac["faltantes"] > 0).sum()), detalhe="+".join(chave))
        q.add(nome, "periodos_faltantes_internos", int(lac["faltantes"].sum()),
              detalhe="períodos ausentes entre a 1ª e a última aparição de cada chave")
    q.add("painel_a", "grupos", int(a.groupby(["cnpj", "grupo"]).ngroups))
    for f in [c for c in a.columns if c.startswith("flag_")]:
        q.add("painel_a", f, int(a[f].sum()), detalhe="sinalizado, não descartado")
    for f in ["flag_rs_2024", "flag_rs_2024_exposta"]:
        q.add("painel_b", f, int(b[f].sum()), detalhe="sinalizado, não descartado")

    # Administradoras com mês ausente no painel A (relatório nominal)
    adm_mes = a.groupby("cnpj")["data_base"].apply(set)
    meses_a = sorted(a["data_base"].unique())
    for cnpj, ms in adm_mes.items():
        ini, fim = min(ms), max(ms)
        falt = [m for m in meses_a if ini <= m <= fim and m not in ms]
        if falt:
            q.add("painel_a", "administradora_mes_ausente", len(falt), detalhe=f"cnpj={cnpj};meses={','.join(map(str, falt))}")
    # Quedas bruscas de grupos de uma administradora de um mês para o outro
    ng = a.groupby(["cnpj", "data_base"]).size().unstack(fill_value=0)
    for cnpj, row in ng.iterrows():
        v = row.values
        for i in range(1, len(v) - 1):
            if v[i - 1] >= 20 and v[i] < 0.5 * v[i - 1] and v[i + 1] >= 0.8 * v[i - 1]:
                q.add("painel_a", "administradora_queda_transitoria_de_grupos", int(v[i - 1] - v[i]),
                      "", int(ng.columns[i]), f"cnpj={cnpj};grupos {v[i-1]}->{v[i]}->{v[i+1]}")

    # ---- conciliações
    soma_g = g_all.groupby(["cnpj", "data_base"])[["contempladas_mes", "ativas_em_dia", "excluidas_estoque"]].sum()
    seg_i = seg.set_index(["cnpj", "data_base"])[["contempladas_mes", "ativas_em_dia", "excluidas_estoque",
                                                   "contempladas_acum", "ativas_nao_contempladas"]]
    c1 = soma_g.join(seg_i, rsuffix="_consolidado", how="inner").reset_index()
    c1["tipo"] = "grupos_vs_consolidado_mensal"
    soma_uf = b.set_index(["cnpj", "data_base"])[["ativos_lance_acum", "ativos_sorteio_acum",
                                                  "ativos_nao_contemplados"]]
    c2 = soma_uf.join(seg_i[["contempladas_acum", "ativas_nao_contempladas"]], how="inner").reset_index()
    c2["tipo"] = "uf_vs_consolidado_trimestral"
    conc = pd.concat([c1, c2], ignore_index=True)
    for col in ["contempladas_mes", "ativas_em_dia", "excluidas_estoque"]:
        ok = (c1[col] == c1[col + "_consolidado"]).mean()
        q.add("conciliacao", f"grupos_vs_consolidado_{col}_igual", round(float(ok), 4),
              detalhe=f"fração de administradora×mês com soma dos grupos = Segmentos_Consolidados (n={len(c1)})")
    acum = c2["ativos_lance_acum"] + c2["ativos_sorteio_acum"]
    q.add("conciliacao", "uf_vs_consolidado_contempladas_acum_igual",
          round(float((acum == c2["contempladas_acum"]).mean()), 4),
          detalhe=f"lance+sorteio acumulados (soma das UFs) = acumulado consolidado (n={len(c2)})")
    q.add("conciliacao", "uf_vs_consolidado_nao_contempladas_igual",
          round(float((c2["ativos_nao_contemplados"] == c2["ativas_nao_contempladas"]).mean()), 4),
          detalhe=f"n={len(c2)}")
    # fluxo: contemplações no trimestre (UF) vs soma de 3 meses do painel por grupo
    tri = g_all.groupby(["cnpj", "trimestre"])["contempladas_mes"].sum().rename("contempl_grupos_3m")
    c3 = b.set_index(["cnpj", "trimestre"])[["contempl_trim", "excluidos_contempl_trim", "data_base"]].join(tri, how="inner")
    c3 = c3[c3["data_base"] >= INICIO_REGIME_TRIM]
    razao = c3["contempl_trim"].sum() / c3["contempl_grupos_3m"].sum()
    q.add("conciliacao", "uf_trim_vs_grupos_3m_razao_agregada", round(float(razao), 4),
          detalhe="soma(lance+sorteio no trimestre, UF) / soma(contempladas no mês, grupos, 3 meses); regime pós-285")

    out.mkdir(parents=True, exist_ok=True)
    results.mkdir(parents=True, exist_ok=True)
    a.to_parquet(out / "painel_a_grupo_mes.parquet", index=False)
    b.to_parquet(out / "painel_b_adm_trimestre.parquet", index=False)
    conc.to_parquet(out / "conciliacao.parquet", index=False)
    qd = q.df()
    qd.to_csv(results / "qualidade_dados.csv", index=False)
    return {"a": a, "b": b, "conciliacao": conc, "qualidade": qd}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raw", default="data/raw", type=Path)
    ap.add_argument("--out", default="data/processed", type=Path)
    ap.add_argument("--results", default="results", type=Path)
    args = ap.parse_args(argv)
    r = constroi(args.raw, args.out, args.results)
    a, b = r["a"], r["b"]
    print(f"Painel A: {len(a)} obs., {a.groupby(['cnpj', 'grupo']).ngroups} grupos, "
          f"{a['cnpj'].nunique()} administradoras, {a['data_base'].min()}-{a['data_base'].max()}")
    print(f"Painel B: {len(b)} obs., {b['cnpj'].nunique()} administradoras, "
          f"{b['data_base'].min()}-{b['data_base'].max()}")
    print(f"Relatório: {args.results / 'qualidade_dados.csv'} ({len(r['qualidade'])} linhas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
