"""Treino e avaliação dos agentes de aprendizado (H1 e H4; ESTADO §4, 22/11).

Uso (da raiz):
  python -m src.analysis.agentes_rl treino --mecanismo M0 --semente 0
  python -m src.analysis.agentes_rl treino --mecanismo M2 --semente 0 --aquece results/agentes/Q_M0_s0.npy
  python -m src.analysis.agentes_rl h1
  python -m src.analysis.agentes_rl h4
Saídas em results/agentes/.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

from src.analysis import comparacao as cp
from src.analysis.calibracao import SEMENTE, _carrega, carrega_pkl
from src.sim import painel
from src.sim.agentes import ACOES, Agente
from src.sim.grupo import simula
from src.sim.regras import resolve, M0, M2, m3x

OUT = Path("results") / "agentes"
M3_ESCOLHIDO = "M3rs_p0.05"
MECS = {"M0": M0, "M2": M2, M3_ESCOLHIDO: m3x("M3x_p0.05_b0_s1")}
N_GRUPOS_TREINO = 30
MAX_EP, VERIFICA, LIMIAR = 4000, 250, 0.95
TENTATIVA2 = dict(max_ep=20000, verifica=500)   # ESTADO §4, 22/11: mesmo critério, passo por média amostral
SUF = "_t2"   # tentativa 2 (ESTADO §4, 22/11)
Q0 = 1.0   # inicialização otimista (Banchio e Skrzypacz, 2022): acima de qualquer U_i observado


def base_e_desenho():
    P = carrega_pkl("data/processed", "sobra_reg")
    sup, th = P["sup"], P["theta"]
    base = replace(sup.base, **dict(zip(sup.nomes, map(float, th))))
    return base, sup


def treino(args):
    OUT.mkdir(parents=True, exist_ok=True)
    base, sup = base_e_desenho()
    g = sup.des[0].grupos.sample(N_GRUPOS_TREINO, random_state=args.semente)
    Q = np.load(args.aquece) if args.aquece else None
    ag = Agente(base, seed=args.semente, Q=None if Q is None else Q.copy(), alfa=(0.0 if args.tentativa == 2 else 0.1))
    max_ep, verifica = (TENTATIVA2["max_ep"], TENTATIVA2["verifica"]) if args.tentativa == 2 else (MAX_EP, VERIFICA)
    if Q is None:
        ag.Q[:] = Q0
    mec = MECS[args.mecanismo] if args.mecanismo in MECS else resolve(args.mecanismo)
    ant, hist = ag.gulosa(), []
    convergiu = False
    for ep in range(1, max_ep + 1):
        horiz = 3000 if args.tentativa == 1 else 15000
        ag.eps = max(0.02, 0.3 - (0.28 * ep / horiz)) if not args.aquece else max(0.02, 0.1 - 0.08 * ep / (horiz / 2))
        x = g.iloc[ep % len(g)]
        par = painel.ajusta(base, "sobra_reg", 1, int(x["N"]), int(x["T"]), int(x["sobra"]))
        r = simula(par, seed=10_000 * args.semente + ep, mecanismo=mec, politica=ag)
        ag.atualiza(r, par.T)
        if ep % verifica == 0:
            atual = ag.gulosa()
            massa = ag.visitas / max(ag.visitas.sum(), 1)
            estavel = float(massa[atual == ant].sum())
            hist.append(dict(episodio=ep, eps=ag.eps, estavel=estavel, estados_visitados=int((ag.visitas > 0).sum()),
                             lance_medio_guloso=float((ACOES[atual] * massa).sum())))
            print(hist[-1], flush=True)
            ant = atual
            if estavel >= LIMIAR and ep >= (1000 if args.tentativa == 1 else (7500 if args.aquece else 15000)):
                convergiu = True
                break
    tag = f"{args.mecanismo}_s{args.semente}" + ("" if args.tentativa == 1 else "_t2")
    np.save(OUT / f"Q_{tag}.npy", ag.Q); np.save(OUT / f"visitas_{tag}.npy", ag.visitas)
    h = pd.DataFrame(hist); h["convergiu"] = convergiu; h.to_csv(OUT / f"treino_{tag}.csv", index=False)
    print("convergiu" if convergiu else "NÃO convergiu", tag)


def h1(args):
    """Lance guloso aprendido sob M0 contra a previsão estática b_st = min(lambda + emb_max, v)."""
    base, _ = base_e_desenho()
    L = []
    for s in (0, 1):
        f = OUT / f"Q_M0_s{s}{SUF}.npy"
        if not f.exists():
            continue
        ag = Agente(base, seed=s, Q=np.load(f), visitas=np.load(OUT / f"visitas_M0_s{s}{SUF}.npy"), treino=False, eps=0)
        rng = np.random.default_rng(99)
        n = 200_000
        from src.sim.grupo import sorteia_theta
        th = sorteia_theta(rng, base, n); lam = rng.beta(base.a_lam, base.b_lam, n) * base.lam_max
        rest = rng.random(n); corte = rng.choice([0.0, 0.1, 0.2, 0.4], n)
        # avalia nos estados visitados, ponderando pela frequência de visita no treino
        massa = ag.visitas / ag.visitas.sum()
        guloso = ACOES[ag.Q.argmax(axis=1)]
        # previsão estática média por estado (Monte Carlo sobre tipos que caem no estado)
        sid = ag.estado(th, lam, rest, 0.0) // 4 * 4   # o corte não entra na previsão estática
        T_med = 200.0
        w_bar = rest * T_med / 2
        v = 1 - np.exp(-th * w_bar / 12)
        bst = np.minimum(lam + base.emb_max, v)
        prev = pd.Series(bst).groupby(sid).mean()
        dif = []
        for e in np.flatnonzero(massa > 0):
            p = prev.get(e // 4 * 4, np.nan)
            dif.append((massa[e], abs(guloso[e] - p), guloso[e], p))
        d = pd.DataFrame(dif, columns=["massa", "abs_dif", "lance_aprendido", "lance_estatico"]).dropna()
        mad = float(np.average(d["abs_dif"], weights=d["massa"]))
        L.append(dict(semente=s, dif_abs_media=mad, lance_aprendido_medio=float(np.average(d["lance_aprendido"], weights=d["massa"])),
                      lance_estatico_medio=float(np.average(d["lance_estatico"], weights=d["massa"])),
                      limiar=0.05, H1_aceita=bool(mad > 0.05)))
    t = pd.DataFrame(L); t.round(4).to_csv(OUT / "h1_teste.csv", index=False); print(t.round(4).to_string(index=False))


def _roda_ag(a):
    par, seed, mec, Q = a
    ag = Agente(par, seed=0, Q=Q, treino=False, eps=0.0)
    r = simula(par, seed=seed, mecanismo=mec, politica=ag)
    return cp.metricas_grupo(r, par.T)


def h4(args):
    """H3 refeita com a política gulosa aprendida sob cada mecanismo, no conjunto B."""
    base, sup = base_e_desenho()
    a, b, _ = _carrega("data/processed")
    des = [painel.atribui_sobra(painel.monta_desenho(a, b, 12, seed=s), painel.ETA0, seed=s) for s in (10, 11, 12)]
    Qs = {m: np.load(OUT / f"Q_{m}_s0{SUF}.npy") for m in MECS if (OUT / f"Q_{m}_s0{SUF}.npy").exists()}
    linhas = []
    for r_, d in enumerate(des):
        tarefas, chaves = [], []
        for nome, Q in Qs.items():
            for gg in d.grupos.itertuples():
                par = painel.ajusta(base, "sobra_reg", 1, gg.N, gg.T, gg.sobra)
                tarefas.append((par, gg.seed + 7919 * r_, MECS[nome], Q))
                chaves.append(dict(replica=r_, mecanismo=nome, gid=gg.gid, cnpj=gg.cnpj, adm=gg.adm, peso=gg.peso))
        with Pool(2) as p:
            outs = p.map(_roda_ag, tarefas, chunksize=8)
        linhas += [dict(**k, **o) for k, o in zip(chaves, outs)]
        print(f"  réplica {r_}", flush=True)
    df = pd.DataFrame(linhas)
    niveis, difs = cp.resume(df, 500, SEMENTE)
    niveis.round(6).to_csv(OUT / "h4_metricas.csv", index=False); difs.round(6).to_csv(OUT / "h4_diferencas.csv", index=False)
    print(niveis.round(4).to_string(index=False)); print(difs.round(4).to_string(index=False))


def h5(args):
    """Família M4 com lance aprendido (ESTADO §4, 23/11): conjunto A (escolha) ou B (teste)."""
    base, sup = base_e_desenho()
    nomes = ["M0"] + [n for n in args.mecs.split(",") if n and n != "M0"]
    if args.conjunto == "A":
        des = [sup.des[0]]
    else:
        a, b, _ = _carrega("data/processed")
        des = [painel.atribui_sobra(painel.monta_desenho(a, b, 12, seed=s), painel.ETA0, seed=s) for s in (10, 11, 12)]
    Qs = {m: np.load(OUT / f"Q_{m}_s{args.semente}{SUF}.npy") for m in nomes}
    linhas = []
    for r_, d in enumerate(des):
        tarefas, chaves = [], []
        for nome, Q in Qs.items():
            mec = MECS[nome] if nome in MECS else resolve(nome)
            for gg in d.grupos.itertuples():
                par = painel.ajusta(base, "sobra_reg", 1, gg.N, gg.T, gg.sobra)
                tarefas.append((par, gg.seed + 7919 * r_, mec, Q))
                chaves.append(dict(replica=r_, mecanismo=nome, gid=gg.gid, cnpj=gg.cnpj, adm=gg.adm, peso=gg.peso))
        with Pool(2) as p:
            outs = p.map(_roda_ag, tarefas, chunksize=8)
        linhas += [dict(**k, **o) for k, o in zip(chaves, outs)]
        print(f"  réplica {r_}", flush=True)
    df = pd.DataFrame(linhas)
    niveis, difs = cp.resume(df, 500, SEMENTE)
    sfx = f"_{args.conjunto}" + ("" if args.semente == 0 else f"_s{args.semente}")
    niveis.round(6).to_csv(OUT / f"h5_metricas{sfx}.csv", index=False)
    difs.round(6).to_csv(OUT / f"h5_diferencas{sfx}.csv", index=False)
    print(niveis.round(4).to_string(index=False)); print(difs.round(4).to_string(index=False))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("comando", choices=["treino", "h1", "h4", "h5"])
    ap.add_argument("--conjunto", default="A", choices=["A", "B"])
    ap.add_argument("--mecs", default="")
    ap.add_argument("--mecanismo", default="M0")
    ap.add_argument("--semente", default=0, type=int)
    ap.add_argument("--aquece", default="")
    ap.add_argument("--tentativa", default=1, type=int)
    a = ap.parse_args(argv)
    {"treino": treino, "h1": h1, "h4": h4, "h5": h5}[a.comando](a)


if __name__ == "__main__":
    main()


def h1_detalhe():
    """Lance aprendido (guloso) e previsão estática por quintil de urgência e faixa do prazo restante, semente 0."""
    from src.sim.grupo import sorteia_theta
    base, _ = base_e_desenho()
    ag = Agente(base, seed=0, Q=np.load(OUT / f"Q_M0_s0{SUF}.npy"), visitas=np.load(OUT / f"visitas_M0_s0{SUF}.npy"),
                treino=False, eps=0)
    rng = np.random.default_rng(99); n = 200_000
    th = sorteia_theta(rng, base, n); lam = rng.beta(base.a_lam, base.b_lam, n) * base.lam_max; rest = rng.random(n)
    bst = np.minimum(lam + base.emb_max, 1 - np.exp(-th * rest * 200.0 / 2 / 12))
    sid = ag.estado(th, lam, rest, 0.0)
    guloso = ACOES[ag.Q.argmax(axis=1)]
    massa_total = ag.visitas.reshape(-1, 4).sum(axis=1)          # soma sobre a faixa do corte
    g_med = (ag.visitas.reshape(-1, 4) * guloso.reshape(-1, 4)).sum(axis=1) / np.maximum(massa_total, 1)
    df = pd.DataFrame(dict(tq=np.searchsorted(ag.c_th, th), rb=np.searchsorted([0.25, 0.5, 0.75], rest),
                           bst=bst, aprendido=g_med[sid // 4]))
    t = df.groupby(["tq", "rb"]).agg(lance_estatico=("bst", "mean"), lance_aprendido=("aprendido", "mean")).reset_index()
    t["diferenca"] = t["lance_aprendido"] - t["lance_estatico"]
    t.round(4).to_csv(OUT / "h1_detalhe.csv", index=False); print(t.round(3).to_string(index=False))


def h4_relativas():
    """H4 em % do nível de M0 (com cópia arredondada a 2 casas para o texto)."""
    niv = pd.read_csv(OUT / "h4_metricas.csv").set_index("mecanismo"); dif = pd.read_csv(OUT / "h4_diferencas.csv")
    L = []
    for _, r in dif.iterrows():
        if r["mecanismo"] == "M0":
            continue
        for c in ["W", "E", "S", "Rst", "espera_media", "frac_lance"]:
            n0 = niv.loc["M0", c]
            L.append(dict(mecanismo=r["mecanismo"], criterio=c, nivel_M0=n0, diferenca=r[c], ic_inf=r[c + "_ic_inf"],
                          ic_sup=r[c + "_ic_sup"], pct=100 * r[c] / n0, pct_ic_inf=100 * r[c + "_ic_inf"] / n0,
                          pct_ic_sup=100 * r[c + "_ic_sup"] / n0, pct_2c=round(100 * r[c] / n0, 2),
                          pct_ic_inf_2c=round(100 * r[c + "_ic_inf"] / n0, 2), pct_ic_sup_2c=round(100 * r[c + "_ic_sup"] / n0, 2)))
    pd.DataFrame(L).round(4).to_csv(OUT / "h4_relativas.csv", index=False)
