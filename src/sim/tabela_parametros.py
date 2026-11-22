"""Tabela dos parâmetros do modelo base (seções 4.1, 4.2 e 6.3).

Lê os valores do código (src/sim/grupo.py, src/analysis/calibracao.py) e dos
resultados já gerados (parametros_fixos.csv, calibracao_theta.csv), sem rodar
simulação. Saída: results/parametros_modelo.csv.

Uso: python -m src.sim.tabela_parametros
"""
from dataclasses import fields
from pathlib import Path

import pandas as pd

from src.sim.grupo import Parametros
from src.analysis import calibracao

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results"

ORIGEM_FIXA = "fixo no código, sem calibração"
DESCR = {
    "mu_theta": ("mu_theta", "média de log theta_i (F_theta lognormal)", ORIGEM_FIXA),
    "sd_theta": ("sd_theta", "desvio de log theta_i", ORIGEM_FIXA),
    "a_lam": ("a_lambda", "parâmetro a da Beta de F_lambda", ORIGEM_FIXA),
    "b_lam": ("b_lambda", "parâmetro b da Beta de F_lambda", ORIGEM_FIXA),
    "lam_max": ("lambda_barra", "escala da liquidez (fração de C)", ORIGEM_FIXA),
    "phi1": ("phi_1", "peso da urgência na política", ORIGEM_FIXA),
    "phi2": ("phi_2", "peso do prazo restante na política", ORIGEM_FIXA),
    "atraso_exclusao": ("-", "vencimentos sem pagamento até a exclusão", "Res. 285, art. 32, II"),
    "vagas_sorteio": ("kappa_g", "sorteios de ativas previstos por assembleia", "regulamentos (ESTADO §5 item 26)"),
    "vagas_excluidos": ("-", "restituições garantidas por assembleia, havendo saldo", "regulamentos (ESTADO §5 item 26)"),
}


def main():
    fixos = pd.read_csv(RES / "parametros_fixos.csv")
    base = calibracao.base_parametros(fixos, forma="sobra")
    linhas = []
    for f in fields(Parametros):
        if f.name in DESCR:
            sim, d, o = DESCR[f.name]
            linhas.append(dict(parametro=f.name, simbolo=sim, descricao=d, valor=getattr(base, f.name), origem=o))
    linhas.append(dict(parametro="emb_max", simbolo="b_barra_e", descricao="teto do lance embutido",
                       valor=base.emb_max, origem="regulamentos Itaú cl. 14.6 e Santander cl. 72"))
    linhas.append(dict(parametro="rho", simbolo="rho", descricao="probabilidade de recolocação da vaga",
                       valor=base.rho, origem="painel A (parametros_fixos.csv)"))
    th = pd.read_csv(RES / "calibracao_theta.csv")
    simb = {"phi0": "phi_0", "teto_restituicao": "r_barra", "pi": "eta"}
    for _, r in th.iterrows():
        linhas.append(dict(parametro=r["parametro"], simbolo=simb[r["parametro"]], descricao="calibrado por SMM",
                           valor=r["valor"], origem="calibracao_theta.csv"))
    out = pd.DataFrame(linhas)
    out.to_csv(RES / "parametros_modelo.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
