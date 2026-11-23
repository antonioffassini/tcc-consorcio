"""Tabela dos parâmetros do modelo base (seções 4.1, 4.2 e 6.3).

Lê os valores do código (src/sim/grupo.py, src/analysis/calibracao.py) e dos
resultados já gerados (parametros_fixos.csv, calibracao_theta.csv), sem rodar
simulação. Saída: results/parametros_modelo.csv.

Uso: python -m src.sim.tabela_parametros
"""
from dataclasses import fields, replace

import numpy as np
from pathlib import Path

import pandas as pd

from src.sim.grupo import Parametros
from src.analysis import calibracao

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "results"

ORIGEM_FIXA = "fixo no código, sem calibração"
DESCR = {
    "mu_theta": ("mu_theta", "média de log theta_i (F_theta lognormal; mediana 0,2)", "âncora financeira (ESTADO §4, 22/11)"),
    "sd_theta": ("sd_theta", "desvio de log theta_i", ORIGEM_FIXA),
    "a_lam": ("a_lambda", "parâmetro a da Beta de F_lambda", ORIGEM_FIXA),
    "b_lam": ("b_lambda", "parâmetro b da Beta de F_lambda", ORIGEM_FIXA),
    "lam_max": ("lambda_barra", "escala da liquidez (fração de C)", ORIGEM_FIXA),
    "phi2": ("phi_2", "peso do prazo restante na política", ORIGEM_FIXA),
    "atraso_exclusao": ("-", "vencimentos sem pagamento até a exclusão", "Res. 285, art. 32, II"),
    "vagas_sorteio": ("kappa_g", "sorteios de ativas previstos por assembleia", "regulamentos (ESTADO §5 item 26)"),
    "vagas_excluidos": ("-", "restituições garantidas por assembleia, havendo saldo", "regulamentos (ESTADO §5 item 26)"),
}


def main():
    fixos = pd.read_csv(RES / "parametros_fixos.csv")
    base = replace(calibracao.base_parametros(fixos, forma="sobra_reg"), mu_theta=float(np.log(0.2)))
    linhas = []
    for f in fields(Parametros):
        if f.name in DESCR:
            sim, d, o = DESCR[f.name]
            linhas.append(dict(parametro=f.name, simbolo=sim, descricao=d, valor=getattr(base, f.name), origem=o))
    linhas.append(dict(parametro="emb_max", simbolo="b_barra_e", descricao="teto do lance embutido",
                       valor=base.emb_max, origem="regulamentos Itaú cl. 14.6 e Santander (maio/2026) cl. 9.1.7.3"))
    linhas.append(dict(parametro="rho", simbolo="rho", descricao="probabilidade de recolocação da vaga",
                       valor=base.rho, origem="painel A (parametros_fixos.csv)"))
    th = pd.read_csv(RES / "calibracao_theta.csv")
    simb = {"phi0": "phi_0", "teto_restituicao": "r_barra", "pi": "eta", "phi1": "phi_1"}
    linhas.append(dict(parametro="eta0", simbolo="eta_0", descricao="P(sorteio da sobra) nas administradoras sem regulamento lido",
                       valor=0.75, origem="3 de 4 regulamentos que tratam da sobra (ESTADO §4, 22/11)"))
    for _, r in th.iterrows():
        linhas.append(dict(parametro=r["parametro"], simbolo=simb[r["parametro"]], descricao="calibrado por SMM",
                           valor=r["valor"], origem="calibracao_theta.csv"))
    out = pd.DataFrame(linhas)
    out.to_csv(RES / "parametros_modelo.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
