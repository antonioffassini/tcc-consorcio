"""Passo 4: comparação M0 × M1 × M2 com o Theta calibrado (H3).

Uso (da raiz do TCC):
  python -m src.analysis.comparacao --forma sobra     # modelo revisado (base)
  python -m src.analysis.comparacao --forma fracao    # modelo de 16/11 (sensibilidade)

Critérios e regra de decisão: ESTADO §4, 19/11 (escritos antes desta rodada).
  W  bem-estar: média de U_i = exp(-theta_i w_i/12)(1 - e_i) - l_i (1 - exp(-theta_i r_i/12))
     sobre as cotas não excluídas (não contemplada até T conta como contemplada em T);
  E  desvio-padrão da espera w_i (meses da entrada à contemplação), mesmas cotas;
  S  fração das assembleias em que o sorteio previsto não ocorre por falta de saldo;
  Rst meses médios entre exclusão e restituição (encerramento = T).
Política de lance igual em todos os mecanismos (limitação: crítica de Lucas).
Saídas: results/h3_metricas_<forma>.csv, results/h3_diferencas_<forma>.csv,
        results/h3_robustez_<forma>.csv, results/h3_config_<forma>.csv.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

from src.analysis.calibracao import SEMENTE, carrega_pkl
from src.sim import painel
from src.sim.grupo import CONTEMPLADA, EXCLUIDA, RESTITUIDA, INADIMPLENTE, simula
from src.sim.regras import M0, M2, m1_espera

CRITERIOS = {"W": +1, "E": -1, "S": -1, "Rst": -1}   # +1: maior é melhor; -1: menor é melhor
BETAS = (0.5, 1.0, 2.0)


def mecanismos():
    L = [("M0", M0)] + [(f"M1_beta{b:g}", m1_espera(b)) for b in BETAS] + [("M2", M2)]
    return L


def metricas_grupo(r, T) -> dict:
    x = r.extra
    sit, ent, tc = x["situacao"], x["entrada"], x["t_cont"]
    excl = (sit == EXCLUIDA) | (sit == RESTITUIDA) | (sit == INADIMPLENTE) | (x["t_excl"] >= 0)
    ok = ~excl
    tcont = np.where(tc >= 0, tc, T - 1)
    w = (tcont + 1 - ent)[ok].astype(float)
    th = x["theta"][ok]; e = x["emb"][ok]; l = x["livre"][ok]
    rr = (T - 1 - tcont)[ok].astype(float)
    U = np.exp(-th * w / 12.0) * (1.0 - e) - l * (1.0 - np.exp(-th * rr / 12.0))
    te, tr = x["t_excl"], x["t_rest"]
    m = te >= 0
    rst = np.where(tr[m] >= 0, tr[m], T) - te[m]
    return dict(W=float(U.mean()) if len(U) else np.nan, E=float(w.std()) if len(w) else np.nan,
                S=float(r.extra["falha_sorteio"].mean()), Rst=float(rst.mean()) if m.any() else np.nan,
                espera_media=float(w.mean()) if len(w) else np.nan, n_cotas=int(ok.sum()), n_excl=int(m.sum()),
                frac_lance=float(r.contempl_lance.sum() / max(r.contempl_lance.sum() + r.contempl_sorteio.sum(), 1)))


def _roda(args):
    par, seed, mec = args
    r = simula(par, seed=seed, mecanismo=mec)
    return metricas_grupo(r, par.T)


def roda_comparacao(des_list, base, theta_sim: dict, pesos_niv, forma, processos=2, rep_seeds=None, log=print):
    """Uma linha por (réplica, grupo, mecanismo)."""
    niv = painel.niveis_de(forma)
    linhas = []
    for r, des in enumerate(des_list):
        rng = np.random.default_rng(SEMENTE + 101 * r if rep_seeds is None else rep_seeds[r])
        nivel_adm = rng.choice(np.asarray(niv, float), size=len(des.adms), p=pesos_niv)
        tarefas, chaves = [], []
        for nome, mec in mecanismos():
            for g in des.grupos.itertuples():
                par = painel.ajusta(replace(base, **theta_sim), forma, nivel_adm[g.adm], g.N, g.T)
                tarefas.append((par, g.seed + 7919 * r, mec))
                chaves.append(dict(replica=r, mecanismo=nome, gid=g.gid, cnpj=g.cnpj, adm=g.adm, peso=g.peso))
        if processos > 1:
            with Pool(processos) as p:
                outs = p.map(_roda, tarefas, chunksize=8)
        else:
            outs = [_roda(t) for t in tarefas]
        linhas += [dict(**k, **o) for k, o in zip(chaves, outs)]
        log(f"  réplica {r}: {len(tarefas)} vidas de grupo")
    return pd.DataFrame(linhas)


def _media(df, col):
    d = df[["peso", col]].dropna()
    return float(np.average(d[col], weights=d["peso"])) if len(d) else np.nan


def resume(df: pd.DataFrame, B: int, seed: int):
    """Níveis por mecanismo e diferenças pareadas contra M0, com IC por bootstrap de administradoras."""
    crit = list(CRITERIOS) + ["espera_media", "frac_lance"]
    base = df[df["mecanismo"] == "M0"].set_index(["replica", "gid"])
    adms = df["cnpj"].unique()
    rng = np.random.default_rng(seed)
    idx_boot = [rng.choice(len(adms), len(adms), replace=True) for _ in range(B)]
    por_adm = {c: i for i, c in enumerate(adms)}
    L, D = [], []
    for nome, sub in df.groupby("mecanismo", sort=False):
        s = sub.set_index(["replica", "gid"])
        dif = s[crit].sub(base[crit]).assign(peso=s["peso"], cnpj=s["cnpj"])
        lin = dict(mecanismo=nome); dl = dict(mecanismo=nome)
        cod = dif["cnpj"].map(por_adm).values
        for c in crit:
            lin[c] = _media(s, c)
            dl[c] = _media(dif, c)
            bs_niv, bs_dif = [], []
            for ib in idx_boot:
                cnt = np.bincount(ib, minlength=len(adms))[cod]
                wv = s["peso"].values * cnt; dv = dif["peso"].values * cnt
                v = s[c].values; dvv = dif[c].values
                mk = ~np.isnan(v) & (wv > 0); md = ~np.isnan(dvv) & (dv > 0)
                bs_niv.append(np.average(v[mk], weights=wv[mk]) if mk.any() else np.nan)
                bs_dif.append(np.average(dvv[md], weights=dv[md]) if md.any() else np.nan)
            lin[c + "_ic_inf"], lin[c + "_ic_sup"] = np.nanpercentile(bs_niv, [2.5, 97.5])
            dl[c + "_ic_inf"], dl[c + "_ic_sup"] = np.nanpercentile(bs_dif, [2.5, 97.5])
        L.append(lin); D.append(dl)
    niveis, difs = pd.DataFrame(L), pd.DataFrame(D)
    # regra de dominância (ESTADO §4, 19/11)
    for i, row in difs.iterrows():
        if row["mecanismo"] == "M0":
            continue
        melhora = piora = []
        melhora, piora = [], []
        for c, sgn in CRITERIOS.items():
            lo, hi = sgn * row[c + "_ic_inf"], sgn * row[c + "_ic_sup"]
            lo, hi = min(lo, hi), max(lo, hi)
            if lo > 0:
                melhora.append(c)
            if hi < 0:
                piora.append(c)
        difs.loc[i, "melhora"] = ",".join(melhora); difs.loc[i, "piora"] = ",".join(piora)
        difs.loc[i, "domina_M0"] = bool(melhora) and not piora
    return niveis, difs


def robustez(df_list, nivel_m0: dict) -> pd.DataFrame:
    """Para cada sorteio de Theta: diferenças pontuais e dominância com limiar de 1% do nível de M0."""
    L = []
    for k, df in enumerate(df_list):
        base = df[df["mecanismo"] == "M0"].set_index(["replica", "gid"])
        for nome, sub in df.groupby("mecanismo", sort=False):
            if nome == "M0":
                continue
            s = sub.set_index(["replica", "gid"])
            lin = dict(sorteio_theta=k, mecanismo=nome)
            melhora, piora = [], []
            for c, sgn in CRITERIOS.items():
                d = _media(s[[c]].sub(base[[c]]).assign(peso=s["peso"]), c)
                lin[c] = d
                lim = 0.01 * abs(nivel_m0[c]) if nivel_m0[c] else 1e-12
                if sgn * d > lim:
                    melhora.append(c)
                if sgn * d < -lim:
                    piora.append(c)
            lin["melhora"] = ",".join(melhora); lin["piora"] = ",".join(piora)
            lin["domina_pontual"] = bool(melhora) and not piora
            L.append(lin)
    return pd.DataFrame(L)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--proc", default="data/processed", type=Path)
    ap.add_argument("--forma", default="sobra", choices=["sobra", "fracao"])
    ap.add_argument("--B", default=500, type=int)
    ap.add_argument("--n-theta", default=10, type=int)
    ap.add_argument("--processos", default=2, type=int)
    a = ap.parse_args(argv)
    P = carrega_pkl(a.proc, a.forma)
    sup, th, th_b = P["sup"], np.asarray(P["theta"]), np.asarray(P["th_b"])
    d_sim = len(sup.nomes)
    niv = painel.niveis_de(sup.forma)

    def separa(t):
        return dict(zip(sup.nomes, map(float, t[:d_sim]))), painel.pesos(sup.forma, tuple(t[d_sim:]), niv)

    ts, wn = separa(th)
    print(f"[{a.forma}] Theta = {dict(zip(sup.nomes + ['mistura'], list(th)))}", flush=True)
    df = roda_comparacao(sup.des, sup.base, ts, wn, sup.forma, processos=a.processos,
                         log=lambda s: print(s, flush=True))
    niveis, difs = resume(df, a.B, SEMENTE)
    niveis.round(6).to_csv(Path("results") / f"h3_metricas_{a.forma}.csv", index=False)
    difs.round(6).to_csv(Path("results") / f"h3_diferencas_{a.forma}.csv", index=False)
    print(niveis.round(4).to_string(index=False)); print(difs.round(4).to_string(index=False), flush=True)
    # robustez à incerteza de calibração
    rng = np.random.default_rng(SEMENTE + 7)
    escolha = rng.choice(len(th_b), size=min(a.n_theta, len(th_b)), replace=False)
    nivel_m0 = niveis.set_index("mecanismo").loc["M0"].to_dict()
    dfs = []
    for k, i in enumerate(escolha):
        tsk, wk = separa(th_b[i])
        dfs.append(roda_comparacao(sup.des[:1], sup.base, tsk, wk, sup.forma, processos=a.processos,
                                   rep_seeds=[SEMENTE + 1000 + k], log=lambda s: None))
        print(f"  robustez {k + 1}/{len(escolha)}", flush=True)
    rob = robustez(dfs, nivel_m0)
    rob["indice_bootstrap"] = rob["sorteio_theta"].map(dict(enumerate(map(int, escolha))))
    rob.round(6).to_csv(Path("results") / f"h3_robustez_{a.forma}.csv", index=False)
    resumo = rob.groupby("mecanismo")["domina_pontual"].agg(["sum", "count"]).reset_index()
    resumo["robusta"] = resumo["sum"] >= 0.8 * resumo["count"]
    print(resumo.to_string(index=False))
    cfg = dict(forma=a.forma, theta=dict(zip(sup.nomes, map(float, th[:d_sim]))), pesos_niveis=list(map(float, wn)),
               replicas=len(sup.des), grupos=int(sum(len(d.grupos) for d in sup.des)), B=a.B,
               n_theta=len(escolha), mecanismos=[n for n, _ in mecanismos()], criterios=CRITERIOS,
               politica="fixa entre mecanismos (crítica de Lucas); [DECISÃO PENDENTE: papel do RL na comparação]",
               robustez=resumo.to_dict(orient="records"))
    pd.DataFrame([dict(chave=k, valor=json.dumps(v, ensure_ascii=False, default=str)) for k, v in cfg.items()]).to_csv(
        Path("results") / f"h3_config_{a.forma}.csv", index=False)


if __name__ == "__main__":
    main()
