"""Etapa 2: fatos estilizados e momentos, calculados só a partir dos painéis.

Uso: python -m src.analysis.momentos --proc data/processed --out results
Gera results/fatos_momentos.csv e results/g1_identificacao.csv.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

MIN_CONTEMPL = 30  # filtro: administradora×trimestre com >= 30 contemplações


def _linha(fato, nome, definicao, valor, n, grao):
    return dict(fato=fato, nome=nome, definicao=definicao, valor=round(float(valor), 4), n=int(n), grao=grao)


def calcula(a: pd.DataFrame, b: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    L = []
    bp = b[(b["regime"] == "pos285") & (b["contempl_trim"] >= MIN_CONTEMPL)].copy()
    f = bp["frac_lance"]
    F1 = "O lance domina a contemplação, mas a intensidade varia muito entre administradoras"
    G_B = "administradora×trimestre (pós-285, >=30 contemplações)"
    L += [_linha(F1, "frac_lance_media", "média de lance/(lance+sorteio)", f.mean(), len(f), G_B),
          _linha(F1, "frac_lance_dp", "desvio-padrão de frac_lance", f.std(), len(f), G_B),
          _linha(F1, "frac_lance_min", "mínimo de frac_lance", f.min(), len(f), G_B),
          _linha(F1, "frac_lance_max", "máximo de frac_lance", f.max(), len(f), G_B),
          _linha(F1, "frac_lance_agregada", "soma(lance)/soma(lance+sorteio)",
                 bp["lance_trim"].sum() / bp["contempl_trim"].sum(), len(f), G_B)]
    # variância entre e dentro
    m = bp.groupby("cnpj")["frac_lance"].transform("mean")
    v_tot = f.var(ddof=0); v_dentro = ((f - m) ** 2).mean(); v_entre = ((m - f.mean()) ** 2).mean()
    L += [_linha(F1, "var_total", "variância total de frac_lance", v_tot, len(f), G_B),
          _linha(F1, "var_entre_adm", "variância das médias por administradora (ponderada por obs.)", v_entre, len(f), G_B),
          _linha(F1, "var_dentro_adm", "variância em torno da média da administradora", v_dentro, len(f), G_B),
          _linha(F1, "frac_var_entre", "var_entre/var_total", v_entre / v_tot, len(f), G_B)]
    # sem RS
    fx = b[(b["regime"] == "pos285") & (b["contempl_trim_ex_rs"] >= MIN_CONTEMPL)]["frac_lance_ex_rs"]
    L.append(_linha(F1, "frac_lance_media_ex_rs", "média de frac_lance sem o RS (sensibilidade)", fx.mean(), len(fx), G_B))
    # correlações com características dos grupos (painel A, mediana por administradora no trimestre)
    car = a.groupby(["cnpj", "trimestre"]).agg(tam_med=("cotas_total", "median"), prazo_med=("prazo", "median"))
    j = bp.set_index(["cnpj", "trimestre"]).join(car, how="inner")
    F2 = "Administradoras de grupos maiores contemplam mais por lance"
    for c, nome in [("tam_med", "spearman_lance_tamanho"), ("prazo_med", "spearman_lance_prazo")]:
        r = stats.spearmanr(j["frac_lance"], j[c]).statistic
        L.append(_linha(F2, nome, f"Spearman(frac_lance, mediana de {c} dos grupos da adm.)", r, len(j),
                        "administradora×trimestre, com painel A"))
    # contemplação mensal
    F3 = "Contemplar é raro e irregular no nível do grupo"
    G_A = "grupo×mês (pós-285, ativas>0)"
    aa = a[a["ativas"] > 0]
    t = aa["taxa_contemplacao"]
    for q in [0.25, 0.5, 0.75, 0.9]:
        L.append(_linha(F3, f"taxa_contempl_q{int(q*100)}", f"quantil {q} de contempladas_mes/ativas", t.quantile(q), len(t), G_A))
    L += [_linha(F3, "taxa_contempl_media", "média de contempladas_mes/ativas", t.mean(), len(t), G_A),
          _linha(F3, "frac_sem_contempl", "fração de grupo×mês com contempladas_mes = 0", aa["sem_contemplacao"].mean(), len(aa), G_A)]
    # momentos adicionais (justificativa no README da análise)
    F4 = "A saída por exclusão é contínua e do mesmo grão da contemplação"
    e = (aa["excluidas_mes"] / aa["ativas"]).dropna()
    L += [_linha(F4, "taxa_exclusao_mediana", "mediana de excluidas_mes/ativas", e.median(), len(e), G_A),
          _linha(F4, "taxa_exclusao_media", "média de excluidas_mes/ativas", e.mean(), len(e), G_A)]
    F5 = "A contemplação por grupo cai ao longo da vida do grupo"
    aa = aa.assign(fase=pd.cut(aa["assembleia"] / aa["prazo"], [0, 1/3, 2/3, 10], labels=["inicio", "meio", "fim"]))
    for fase, x in aa.groupby("fase", observed=True)["taxa_contemplacao"]:
        L.append(_linha(F5, f"taxa_contempl_mediana_{fase}", f"mediana da taxa no terço '{fase}' do prazo", x.median(), len(x), G_A))
    mom = pd.DataFrame(L)

    # G1: identificação — há variação entre administradoras?
    gm = bp.groupby("cnpj")["frac_lance"]
    grupos = [g.values for _, g in gm if len(g) >= 2]
    H = stats.kruskal(*grupos)
    icc = v_entre / v_tot
    g1 = pd.DataFrame([
        dict(teste="administradoras_com_2+_trimestres", estatistica=len(grupos), p_valor=np.nan, criterio="n >= 20", passa=len(grupos) >= 20),
        dict(teste="kruskal_wallis_frac_lance_por_adm", estatistica=round(H.statistic, 2), p_valor=H.pvalue, criterio="p < 0,01", passa=H.pvalue < 0.01),
        dict(teste="fracao_variancia_entre_adm", estatistica=round(icc, 4), p_valor=np.nan, criterio=">= 0,5", passa=icc >= 0.5),
        dict(teste="amplitude_frac_lance", estatistica=round(f.max() - f.min(), 4), p_valor=np.nan, criterio=">= 0,3", passa=(f.max() - f.min()) >= 0.3),
        dict(teste="spearman_lance_tamanho_abs", estatistica=round(abs(mom.set_index("nome").loc["spearman_lance_tamanho", "valor"]), 4), p_valor=np.nan, criterio=">= 0,3", passa=abs(mom.set_index("nome").loc["spearman_lance_tamanho", "valor"]) >= 0.3),
    ])
    return mom, g1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc", default="data/processed", type=Path)
    ap.add_argument("--out", default="results", type=Path)
    a_ = ap.parse_args(argv)
    a = pd.read_parquet(a_.proc / "painel_a_grupo_mes.parquet")
    b = pd.read_parquet(a_.proc / "painel_b_adm_trimestre.parquet")
    mom, g1 = calcula(a, b)
    mom.to_csv(a_.out / "fatos_momentos.csv", index=False)
    g1.to_csv(a_.out / "g1_identificacao.csv", index=False)
    print(mom[["nome", "valor", "n"]].to_string(index=False)); print(g1.to_string(index=False))


if __name__ == "__main__":
    main()
