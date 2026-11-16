"""Passo 1 (15/11): efeito de cada revisão do modelo sobre os momentos de calibração.

Uso: python -m src.sim.rodada_heterogeneidade --proc data/processed --out results

Gera results/parametros_fixos.csv (h por idade, rho, teto do embutido),
results/sim_heterogeneidade.csv (efeito acumulado de cada revisão) e
results/sim_forma_heterogeneidade.csv (momentos por nível contratual, nas duas
formas candidatas, para a escolha da forma). Parâmetros comportamentais de chute (os
padrão de `Parametros`), sem calibração. Os momentos de teste de H2
(spearman_lance_tamanho, frac_sem_contempl) NÃO são calculados aqui: ficam
guardados até o critério de rejeição estar escrito (passo 3).
"""
import argparse
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from . import painel
from .grupo import Parametros

EMB_MAX = 0.25   # teto do lance embutido: hipótese, a conferir em regulamentos (ESTADO §3)
NU_CHUTE = 0.5
PSI_CHUTE = (0.7, 0.3)   # (m_s, sigma_s)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc", default="data/processed", type=Path)
    ap.add_argument("--out", default="results", type=Path)
    ap.add_argument("--grupos-por-adm", default=12, type=int)
    ap.add_argument("--processos", default=2, type=int)
    a_ = ap.parse_args(argv)
    a, b = painel.carrega(a_.proc)
    fixos = painel.parametros_fixos(a)
    fixos = pd.concat([fixos, pd.DataFrame([dict(parametro="emb_max", valor=EMB_MAX, limite_inf=np.nan,
                                                 limite_sup=np.nan, n=0)])], ignore_index=True)
    fixos.to_csv(a_.out / "parametros_fixos.csv", index=False)
    f = fixos.set_index("parametro")["valor"]
    des = painel.monta_desenho(a, b, a_.grupos_por_adm, seed=0)

    proto = Parametros(h=0.005)
    excl = replace(proto, h=0.0, h_idade=painel.h_idade_de(fixos), rho=float(f["rho"]), atraso_exclusao=3)
    emb = replace(excl, emb_max=EMB_MAX)
    configs = [("A_prototipo", proto, (1,), (0.0,), "kappa"),
               ("B_inadimplencia_exclusao_idade_recolocacao", excl, (1,), (0.0,), "kappa"),
               ("C_mais_embutido", emb, (1,), (0.0,), "kappa"),
               ("D_mais_kappa_poisson", emb, painel.KAPPAS, (NU_CHUTE,), "kappa"),
               ("E_mais_fracao_capacidade", emb, painel.GRADE_S, PSI_CHUTE, "fracao")]

    real = pd.read_csv(a_.out / "fatos_momentos.csv").set_index("nome")["valor"]
    bp = b[(b["regime"] == "pos285") & (b["contempl_trim"] >= painel.MIN_CONTEMPL)]
    real_diag = bp["excluidos_contempl_trim"].sum() / (bp["excluidos_contempl_trim"].sum() + bp["sorteio_trim"].sum())
    L, cache = [], {}
    for nome, par, ks, psi, forma in configs:
        chave = (id(par), ks, forma)
        if chave not in cache:
            cache[chave] = painel.simula_desenho(des, par, kappas=ks, processos=a_.processos, forma=forma)
        sims = cache[chave]
        m = painel.momentos_calibracao(des, sims, psi, forma=forma)
        w = painel.pesos(forma, psi, ks)
        exc = sum(wk * sims[k][:, 3].sum() for k, wk in zip(ks, w))
        sor = sum(wk * sims[k][:, 1].sum() for k, wk in zip(ks, w))
        m["frac_sorteio_excluidos"] = exc / max(exc + sor, 1e-12)
        for k, v in m.items():
            L.append(dict(config=nome, momento=k, simulado=round(v, 4)))
    t = pd.DataFrame(L)
    ref = {"frac_lance_media": real["frac_lance_media"], "frac_lance_dp": real["frac_lance_dp"],
           "taxa_contempl_q50": real["taxa_contempl_q50"], "frac_sorteio_excluidos": round(real_diag, 4)}
    t["real"] = t["momento"].map(ref)
    t["papel"] = np.where(t["momento"] == "frac_sorteio_excluidos", "diagnostico", "calibracao")
    t["grupos_simulados"] = len(des.grupos)
    t["psi"] = t["config"].map({c[0]: "/".join(str(x) for x in c[3]) for c in configs})
    t.to_csv(a_.out / "sim_heterogeneidade.csv", index=False)
    # momentos por nível, nas duas formas (base: config C)
    F = []
    for forma in painel.FORMAS:
        ks = painel.niveis_de(forma)
        chave = (id(emb), ks, forma)
        sims = cache.get(chave) or painel.simula_desenho(des, emb, kappas=ks, processos=a_.processos, forma=forma)
        for k in ks:
            m = painel.momentos_calibracao(des, {k: sims[k]}, (0.0,) if forma == "kappa" else (k, 1e-6), forma=forma)
            F.append(dict(forma=forma, nivel=k, **{x: round(y, 4) for x, y in m.items()}))
    F = pd.DataFrame(F)
    F.to_csv(a_.out / "sim_forma_heterogeneidade.csv", index=False)
    print(fixos.to_string(index=False)); print(t.to_string(index=False)); print(F.to_string(index=False))


if __name__ == "__main__":
    main()
