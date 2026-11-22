"""Tabelas derivadas para o texto (caps. 7 e 8), sem simulação nova.

1. results/h3_relativas.csv — diferenças de H3 contra M0 em % do nível de M0,
   com os limites do IC de 95%, por forma (sobra = base; fracao = modelo de 16/11).
2. results/versoes_modelo.csv — os mesmos momentos nas três versões do modelo
   (protótipo de 26/10, modelo de 16/11, modelo revisado de 19/11).
3. results/h3_robustez_relativas.csv — robustez de H3 (10 sorteios de Theta) em % do
   nível de M0, com o resumo por mecanismo (mínimo, máximo, contagem de dominância pontual).

Uso: python -m src.analysis.tabelas_texto
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results"
ARQ = RES / "arquivo_2026-11-16"
CRIT = ["W", "E", "S", "Rst", "espera_media", "frac_lance"]


def relativas():
    linhas = []
    for forma in ("sobra", "fracao"):
        niv = pd.read_csv(RES / f"h3_metricas_{forma}.csv").set_index("mecanismo").loc["M0"]
        dif = pd.read_csv(RES / f"h3_diferencas_{forma}.csv").set_index("mecanismo")
        for mec, r in dif.iterrows():
            if mec == "M0":
                continue
            for c in CRIT:
                base = niv[c]
                linhas.append(dict(forma=forma, mecanismo=mec, criterio=c, nivel_M0=base,
                                   diferenca=r[c], ic_inf=r[f"{c}_ic_inf"], ic_sup=r[f"{c}_ic_sup"],
                                   pct=100 * r[c] / base, pct_ic_inf=100 * r[f"{c}_ic_inf"] / base,
                                   pct_ic_sup=100 * r[f"{c}_ic_sup"] / base))
    out = pd.DataFrame(linhas).round(6)
    out.to_csv(RES / "h3_relativas.csv", index=False)
    return out


def versoes():
    p = pd.read_csv(RES / "sim_primeira_rodada.csv").set_index("momento")
    het = pd.read_csv(RES / "sim_heterogeneidade.csv")
    het = het[het.config == "A_prototipo"].set_index("momento")
    v1 = pd.read_csv(ARQ / "calibracao_momentos.csv").set_index("momento")
    v2 = pd.read_csv(RES / "calibracao_momentos.csv").set_index("momento")
    h1 = pd.read_csv(ARQ / "h2_teste.csv").set_index("item")
    h2 = pd.read_csv(RES / "h2_teste.csv").set_index("item")
    dado = pd.read_csv(RES / "fatos_momentos.csv").set_index("nome")["valor"]
    rows = [
        ("frac_lance_media", dado["frac_lance_media"], p.loc["frac_lance", "simulado"],
         v1.loc["frac_lance_media", "simulado_direto"], v2.loc["frac_lance_media", "simulado_direto"]),
        ("frac_lance_dp", dado["frac_lance_dp"], p.loc["frac_lance_dp_entre_grupos", "simulado"],
         v1.loc["frac_lance_dp", "simulado_direto"], v2.loc["frac_lance_dp", "simulado_direto"]),
        ("taxa_contempl_q50", dado["taxa_contempl_q50"], p.loc["taxa_contempl_mediana", "simulado"],
         v1.loc["taxa_contempl_q50", "simulado_direto"], v2.loc["taxa_contempl_q50", "simulado_direto"]),
        ("frac_sorteio_excluidos", v2.loc["frac_sorteio_excluidos", "dado"], het.loc["frac_sorteio_excluidos", "simulado"],
         None, v2.loc["frac_sorteio_excluidos", "simulado_direto"]),
        ("spearman_lance_tamanho", dado["spearman_lance_tamanho"], None,
         h1.loc["spearman_lance_tamanho", "simulado"], h2.loc["spearman_lance_tamanho", "simulado"]),
        ("frac_sem_contempl", dado["frac_sem_contempl"], p.loc["frac_sem_contempl", "simulado"],
         h1.loc["frac_sem_contempl", "simulado"], h2.loc["frac_sem_contempl", "simulado"]),
        ("wald_J", None, None, h1.loc["wald_conjunto", "t"], h2.loc["wald_conjunto", "t"]),
        ("wald_p", None, None, h1.loc["wald_conjunto", "simulado"], h2.loc["wald_conjunto", "simulado"]),
    ]
    out = pd.DataFrame(rows, columns=["momento", "dado", "prototipo_2610", "modelo_1611", "modelo_1911"])
    out.to_csv(RES / "versoes_modelo.csv", index=False)
    return out


def robustez_relativas():
    linhas, resumo = [], []
    for forma in ("sobra", "fracao"):
        niv = pd.read_csv(RES / f"h3_metricas_{forma}.csv").set_index("mecanismo").loc["M0"]
        rob = pd.read_csv(RES / f"h3_robustez_{forma}.csv")
        for c in ("W", "E", "S", "Rst"):
            rob[f"pct_{c}"] = 100 * rob[c] / niv[c]
        rob.insert(0, "forma", forma)
        linhas.append(rob)
        for mec, g in rob.groupby("mecanismo"):
            d = dict(forma=forma, mecanismo=mec, n=len(g), dominancias=int(g["domina_pontual"].sum()))
            for c in ("W", "E", "S", "Rst"):
                d[f"pct_{c}_min"], d[f"pct_{c}_max"] = g[f"pct_{c}"].min(), g[f"pct_{c}"].max()
            resumo.append(d)
    out = pd.concat(linhas).round(6)
    out.to_csv(RES / "h3_robustez_relativas.csv", index=False)
    res = pd.DataFrame(resumo).round(4)
    res.to_csv(RES / "h3_robustez_resumo.csv", index=False)
    return res


if __name__ == "__main__":
    print(relativas().to_string(index=False))
    print(versoes().to_string(index=False))
    print(robustez_relativas().to_string(index=False))
