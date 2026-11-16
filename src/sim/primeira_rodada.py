"""Primeira rodada do protótipo, com parâmetros de chute (sem calibração).

Uso: python -m src.sim.primeira_rodada --out results
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .grupo import Parametros, momentos_simulados, simula


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="results", type=Path)
    ap.add_argument("--grupos", default=300, type=int)
    a = ap.parse_args(argv)
    par = Parametros(N=600, T=200, h=0.005)
    ms, esp, serie = [], [], np.zeros((a.grupos, par.T))
    for s in range(a.grupos):
        r = simula(par, seed=s)
        ms.append(momentos_simulados(r))
        esp.append(np.nanmean(r.espera))
        tot = r.contempl_sorteio + r.contempl_lance
        serie[s] = np.where(tot > 0, r.contempl_lance / np.maximum(tot, 1), np.nan)
    m = pd.DataFrame(ms)
    real = pd.read_csv(a.out / "fatos_momentos.csv").set_index("nome")["valor"]
    tab = pd.DataFrame([
        dict(momento="frac_lance", simulado=m.frac_lance.mean(), real=real["frac_lance_media"]),
        dict(momento="frac_lance_dp_entre_grupos", simulado=m.frac_lance.std(), real=real["frac_lance_dp"]),
        dict(momento="taxa_contempl_mediana", simulado=m.taxa_contempl_mediana.mean(), real=real["taxa_contempl_q50"]),
        dict(momento="frac_sem_contempl", simulado=m.frac_sem_contempl.mean(), real=real["frac_sem_contempl"]),
    ]).round(4)
    tab["grupos_simulados"] = a.grupos
    tab.to_csv(a.out / "sim_primeira_rodada.csv", index=False)
    perfil = pd.DataFrame({"terco": ["inicio", "meio", "fim"],
                           "frac_lance_sim": [np.nanmean(serie[:, i:j]) for i, j in [(0, 67), (67, 134), (134, 200)]]}).round(4)
    perfil.to_csv(a.out / "sim_primeira_rodada_perfil.csv", index=False)
    print(tab.to_string(index=False)); print(perfil.to_string(index=False))
    print("espera média (meses):", round(float(np.mean(esp)), 1))


if __name__ == "__main__":
    main()
