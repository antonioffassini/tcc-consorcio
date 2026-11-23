"""Tabelas derivadas do bloco de 22/11 para o texto (sem simulação nova).

Gera, a partir de CSVs já existentes em results/:
  results/h3_relativas_sobra_reg.csv   H3 da nova base em % do nível de M0, com IC
  results/m3_relativas_B.csv           M2 e M3 escolhido no conjunto B, em % de M0, com IC
"""
from pathlib import Path

import pandas as pd

R = Path("results")
CRIT = ["W", "E", "S", "Rst", "espera_media", "frac_lance"]


def relativas(sfx: str) -> pd.DataFrame:
    niv = pd.read_csv(R / f"h3_metricas_{sfx}.csv").set_index("mecanismo")
    dif = pd.read_csv(R / f"h3_diferencas_{sfx}.csv")
    L = []
    for _, r in dif.iterrows():
        if r["mecanismo"] == "M0":
            continue
        for c in CRIT:
            n0 = niv.loc["M0", c]
            L.append(dict(mecanismo=r["mecanismo"], criterio=c, nivel_M0=n0, diferenca=r[c],
                          ic_inf=r[c + "_ic_inf"], ic_sup=r[c + "_ic_sup"],
                          pct=100 * r[c] / n0, pct_ic_inf=100 * r[c + "_ic_inf"] / n0, pct_ic_sup=100 * r[c + "_ic_sup"] / n0))
    return pd.DataFrame(L)


if __name__ == "__main__":
    relativas("sobra_reg").round(4).to_csv(R / "h3_relativas_sobra_reg.csv", index=False)
    relativas("sobra_reg_m3B").round(4).to_csv(R / "m3_relativas_B.csv", index=False)
    relativas("sobra_reg_decomp").round(4).to_csv(R / "m3_decomposicao_B.csv", index=False)
    print(pd.read_csv(R / "m3_relativas_B.csv").to_string(index=False))


def resumo_robustez(arq: str, niv_sfx: str) -> pd.DataFrame:
    """Dominância pontual e faixa (mín. a máx.) das diferenças em % do nível de M0 nos sorteios de Theta."""
    rob = pd.read_csv(R / arq)
    n0 = pd.read_csv(R / f"h3_metricas_{niv_sfx}.csv").set_index("mecanismo").loc["M0"]
    L = []
    for m, d in rob.groupby("mecanismo", sort=False):
        lin = dict(mecanismo=m, n=len(d), dominancias=int(d["domina_pontual"].sum()))
        for c in ["W", "E", "S", "Rst"]:
            pct = 100 * d[c] / n0[c]
            lin[f"pct_{c}_min"], lin[f"pct_{c}_max"] = pct.min(), pct.max()
        L.append(lin)
    return pd.DataFrame(L)


if __name__ == "__main__":
    a = resumo_robustez("h3_robustez_sobra_reg.csv", "sobra_reg").assign(conjunto="calibrado")
    b = resumo_robustez("h3_robustez_sobra_reg_m3B.csv", "sobra_reg_m3B").assign(conjunto="B")
    t = pd.concat([a, b]); t.round(4).to_csv(R / "h3_robustez_resumo_sobra_reg.csv", index=False)
    print(t.round(2).to_string(index=False))


def apresentacao() -> pd.DataFrame:
    """Valores das tabelas de 22/11 arredondados como aparecem no texto (2 casas), com origem.

    A auditoria compara números do texto com os CSVs com tolerância relativa de 0,5%; percentuais
    pequenos arredondados a duas casas (ex.: 0,08 para 0,084) precisam de uma cópia arredondada.
    """
    L = []
    def add(origem, nome, v):
        L.append(dict(origem=origem, item=nome, valor=round(float(v), 2)))
    for arq in ["h3_relativas_sobra_reg.csv", "m3_relativas_B.csv", "m3_decomposicao_B.csv"]:
        d = pd.read_csv(R / arq)
        for _, r in d.iterrows():
            for c in ["pct", "pct_ic_inf", "pct_ic_sup"]:
                add(arq, f"{r['mecanismo']}|{r['criterio']}|{c}", r[c])
    d = pd.read_csv(R / "m3_rodada1_A.csv")
    for _, r in d.iterrows():
        for c in ["pct_W", "pct_E", "pct_S", "pct_Rst"]:
            add("m3_rodada1_A.csv", f"{r['mecanismo']}|{c}", r[c])
    d = pd.read_csv(R / "h3_robustez_resumo_sobra_reg.csv")
    for _, r in d.iterrows():
        for c in [x for x in d.columns if x.startswith("pct_")]:
            add("h3_robustez_resumo_sobra_reg.csv", f"{r['mecanismo']}|{r['conjunto']}|{c}", r[c])
    for sfx in ["sobra_reg", "sobra_reg_m3B"]:
        n = pd.read_csv(R / f"h3_metricas_{sfx}.csv").set_index("mecanismo")
        for m in n.index:
            add(f"h3_metricas_{sfx}.csv", f"{m}|S_pct", 100 * n.loc[m, "S"])
    cfg = pd.read_csv(R / "h3_config_sobra_reg.csv").set_index("chave")["valor"]
    L.append(dict(origem="h3_config_sobra_reg.csv", item="grupos_por_replica", valor=int(cfg["grupos"]) // int(cfg["replicas"])))
    return pd.DataFrame(L)


if __name__ == "__main__":
    apresentacao().to_csv(R / "texto_2211_apresentacao.csv", index=False)
