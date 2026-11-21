"""Calibração por método de momentos simulados (SMM) e teste de H2.

Uso (da raiz do TCC):
  python -m src.analysis.calibracao identificacao              # jacobiano (modelo de 16/11)
  python -m src.analysis.calibracao calibra --forma sobra      # modelo revisado (19/11)
  python -m src.analysis.calibracao calibra --forma fracao     # modelo de 16/11 (sensibilidade)
  python -m src.analysis.calibracao h2 --forma sobra           # só depois do critério (ESTADO §4, 16/11)

Desenho (ESTADO §4, 15/11, 16/11 e 19/11):
  - forma "sobra" (base desde 19/11): sorteio de excluídas separado (uma restituição
    garantida e outras até `teto_restituicao` por assembleia); fração pi das
    administradoras faz sorteio da sobra; teto do embutido 0,30.
    Theta = (phi0, teto_restituicao, pi); momentos de calibração = mu_cal + frac_sorteio_excluidos.
  - forma "fracao" (16/11, sensibilidade): sorteio comum, s_j ~ LogNormal(log m_s, sigma_s),
    embutido 0,25. Theta = (phi0, m_s, sigma_s); momentos = mu_cal.
  - mu_tes = (spearman_lance_tamanho, frac_sem_contempl): fora da função objetivo.
  - W = diag(1 / Var_boot), variâncias por bootstrap de administradoras (painéis A e B juntos).
  - Simulação: R réplicas, cada uma com seu desenho de grupos; agregadas na função objetivo.
  - Superfície: parâmetros de simulação numa grade (1 ou 2 dimensões) com interpolação
    multilinear das saídas por nível contratual; o parâmetro da mistura entra exato.
    O ponto calibrado é conferido por simulação direta.
  - Erro-padrão: bootstrap dos momentos de dados re-otimizado na superfície, mais a
    variância entre réplicas (cada réplica calibrada separadamente).
"""
from __future__ import annotations

import argparse
import itertools
import json
import pickle
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats

from src.sim import painel
from src.sim.grupo import Parametros

CAL = ["frac_lance_media", "frac_lance_dp", "taxa_contempl_q50"]
CAL_SOBRA = CAL + ["frac_sorteio_excluidos"]
TES = ["spearman_lance_tamanho", "frac_sem_contempl"]
SEMENTE = 20261116
EMB_MAX = 0.25          # modelo de 16/11
EMB_MAX_REV = 0.30      # revisão de 19/11 (Itaú cl. 14.6; Santander cl. 72)
PONTO_PARTIDA = dict(phi0=0.10, lam_max=0.6, m_s=0.7, sigma_s=0.3)
PASSOS = dict(phi0=0.05, lam_max=0.2, m_s=0.1, sigma_s=0.1)
GRADES = dict(phi0=np.round(np.linspace(-0.30, 0.30, 11), 3),
              lam_max=np.round(np.linspace(0.05, 1.05, 11), 3))
GRADES_FORMA = {
    "fracao": {"phi0": GRADES["phi0"]},
    "sobra": {"phi0": np.array([-0.30, -0.20, -0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.20, 0.30]),
              "teto_restituicao": np.array([0.0, 0.10, 0.20, 0.35, 0.70, 1.50])},
}
LIMITES = dict(phi0=(-0.30, 0.30), lam_max=(0.05, 1.05), m_s=(0.05, 2.5), sigma_s=(0.01, 1.5),
               teto_restituicao=(0.0, 1.5), pi=(0.0, 1.0), nu=(0.0, 5.0))
MISTURA = {"fracao": ["m_s", "sigma_s"], "sobra": ["pi"], "kappa": ["nu"]}
CAL_FORMA = {"fracao": CAL, "sobra": CAL_SOBRA}


# ================================================================ dados

class Dados:
    """Momentos de dados e bootstrap por administradora (clusters)."""

    def __init__(self, a: pd.DataFrame, b: pd.DataFrame):
        bp = b[(b["regime"] == "pos285") & (b["contempl_trim"] >= painel.MIN_CONTEMPL)]
        car = a.groupby(["cnpj", "trimestre"]).agg(tam_med=("cotas_total", "median")).reset_index()
        j = bp[["cnpj", "trimestre", "frac_lance"]].merge(car, on=["cnpj", "trimestre"], how="inner")
        aa = a[a["ativas"] > 0]
        self.adms = np.unique(np.concatenate([bp["cnpj"].unique(), aa["cnpj"].unique()]))
        idx = {c: k for k, c in enumerate(self.adms)}
        self.b_adm = bp["cnpj"].map(idx).values; self.f = bp["frac_lance"].values
        self.b_exc = bp["excluidos_contempl_trim"].fillna(0).values.astype(float)
        self.b_sor = bp["sorteio_trim"].fillna(0).values.astype(float)
        self.j_adm = j["cnpj"].map(idx).values; self.j_f = j["frac_lance"].values; self.j_t = j["tam_med"].values
        self.a_adm = aa["cnpj"].map(idx).values
        self.tx = aa["taxa_contemplacao"].values; self.sem = aa["sem_contemplacao"].values.astype(float)
        o = np.argsort(self.tx, kind="stable"); self.tx_o, self.tx_adm_o = self.tx[o], self.a_adm[o]

    def momentos(self, c=None) -> dict:
        """c = contagem de cada administradora na reamostragem (None = amostra original)."""
        if c is None:
            return dict(frac_lance_media=self.f.mean(), frac_lance_dp=self.f.std(ddof=1),
                        taxa_contempl_q50=float(np.quantile(self.tx, 0.5)),
                        spearman_lance_tamanho=stats.spearmanr(self.j_f, self.j_t).statistic,
                        frac_sem_contempl=self.sem.mean(),
                        frac_sorteio_excluidos=self.b_exc.sum() / (self.b_exc.sum() + self.b_sor.sum()))
        wb = c[self.b_adm].astype(float); n = wb.sum()
        m = (wb * self.f).sum() / n
        dp = np.sqrt(((wb * (self.f - m) ** 2).sum()) / (n - 1))
        wa = c[self.tx_adm_o].astype(float); cw = np.cumsum(wa) / wa.sum()
        q50 = float(self.tx_o[np.searchsorted(cw, 0.5)])
        rep = np.repeat(np.arange(len(self.j_f)), c[self.j_adm])
        sp = stats.spearmanr(self.j_f[rep], self.j_t[rep]).statistic
        ws = c[self.a_adm].astype(float)
        ex = (wb * self.b_exc).sum(); so = (wb * self.b_sor).sum()
        return dict(frac_lance_media=m, frac_lance_dp=dp, taxa_contempl_q50=q50,
                    spearman_lance_tamanho=sp, frac_sem_contempl=(ws * self.sem).sum() / ws.sum(),
                    frac_sorteio_excluidos=ex / (ex + so))

    def bootstrap(self, B: int, seed: int) -> pd.DataFrame:
        rng = np.random.default_rng(seed)
        L = []
        for _ in range(B):
            c = np.bincount(rng.integers(0, len(self.adms), len(self.adms)), minlength=len(self.adms))
            L.append(self.momentos(c))
        return pd.DataFrame(L)


# ================================================================ simulação

def base_parametros(fixos: pd.DataFrame, forma: str = "fracao") -> Parametros:
    f = fixos.set_index("parametro")["valor"]
    base = Parametros(h=0.0, h_idade=painel.h_idade_de(fixos), rho=float(f["rho"]), atraso_exclusao=3,
                      emb_max=EMB_MAX)
    if forma == "sobra":
        base = replace(base, emb_max=EMB_MAX_REV, sorteio_excluidos="separado", vagas_excluidos=1)
    return base


@dataclass
class Bloco:
    """Saídas de uma réplica num ponto da grade, para todos os níveis contratuais."""
    F: np.ndarray       # (n_niv, n_alvo) fração de lance por administradora×trimestre
    TX: np.ndarray      # (n_niv, n_gm) taxa por grupo×mês (nan se ativas = 0)
    Z: np.ndarray       # (n_niv, n_gm) 1 se grupo×mês sem contemplação (nan se ativas = 0)
    EXC: np.ndarray     # (n_niv,) restituições a excluídas, total
    SOR: np.ndarray     # (n_niv,) sorteios de ativas, total
    EXA: np.ndarray = None   # (n_niv, n_alvo) restituições por administradora×trimestre do alvo
    SOA: np.ndarray = None   # (n_niv, n_alvo) sorteios de ativas por administradora×trimestre do alvo


def _somas_alvo(des: painel.Desenho, s: np.ndarray) -> tuple:
    o = des.obs.assign(sorteio=s[:, 1], rest=s[:, 3]).merge(des.grupos[["gid", "cnpj"]], on="gid")
    g = o.groupby(["cnpj", "trimestre"])[["sorteio", "rest"]].sum().reset_index()
    m = des.alvo_b[["cnpj", "trimestre"]].merge(g, on=["cnpj", "trimestre"], how="left").fillna(0)
    return m["rest"].values.astype(float), m["sorteio"].values.astype(float)


def roda_bloco(des: painel.Desenho, par: Parametros, rep: int, processos: int, forma: str = "fracao") -> Bloco:
    niv = painel.niveis_de(forma)
    sims = painel.simula_desenho(des, par, kappas=niv, processos=processos, rep=rep, forma=forma)
    F, TX, Z, E, S, EA, SA = [], [], [], [], [], [], []
    for k in niv:
        s = sims[k]
        F.append(painel._frac_adm_trim(des, s)["frac"].values)
        at = s[:, 2].astype(float); tot = s[:, 0] + s[:, 1]
        with np.errstate(invalid="ignore", divide="ignore"):
            TX.append(np.where(at > 0, tot / at, np.nan)); Z.append(np.where(at > 0, (tot == 0).astype(float), np.nan))
        E.append(s[:, 3].sum()); S.append(s[:, 1].sum())
        ea, sa = _somas_alvo(des, s); EA.append(ea); SA.append(sa)
    return Bloco(np.array(F), np.array(TX), np.array(Z), np.array(E, float), np.array(S, float),
                 np.array(EA), np.array(SA))


def _lin(x0, x1, t):
    """Interpolação linear que não propaga NaN de um só lado: se um extremo é NaN, usa o outro."""
    if t <= 0:
        return x0
    if t >= 1:
        return x1
    out = (1 - t) * x0 + t * x1
    out = np.where(np.isnan(x0) & ~np.isnan(x1), x1, out)
    return np.where(np.isnan(x1) & ~np.isnan(x0), x0, out)


class Superficie:
    """Blocos numa grade dos parâmetros de simulação (1 ou 2 dimensões), para R réplicas.

    Superficie("phi0", grade, desenhos, base)              — uma dimensão (compatível com 16/11)
    Superficie({"phi0": g1, "teto_restituicao": g2}, None, desenhos, base, forma="sobra")
    """

    CAMPOS = ("F", "TX", "Z", "EXA", "SOA")

    def __init__(self, nome, grade, desenhos, base: Parametros, processos: int = 2, log=print,
                 forma: str = "fracao"):
        grades = {nome: grade} if isinstance(nome, str) else dict(nome)
        self.nomes = list(grades)
        self.grades = [np.asarray(g, float) for g in grades.values()]
        self.nome, self.grade = self.nomes[0], self.grades[0]
        self.forma, self.des, self.base = forma, desenhos, base
        self.pesos_gm = [d.obs["gid"].map(d.grupos.set_index("gid")["peso"]).values for d in desenhos]
        shape = tuple(len(g) for g in self.grades)
        self.blocos = []
        for r, d in enumerate(desenhos):
            arr = np.empty(shape, dtype=object)
            for idx in itertools.product(*[range(n) for n in shape]):
                vals = {n: float(self.grades[k][i]) for k, (n, i) in enumerate(zip(self.nomes, idx))}
                arr[idx] = roda_bloco(d, replace(base, **vals), rep=r, processos=processos, forma=forma)
                log(f"  réplica {r}, " + ", ".join(f"{n} = {v:g}" for n, v in vals.items()))
            self.blocos.append(arr)
        self.alvo = desenhos[0].alvo_b

    def __setstate__(self, st):     # superfícies gravadas em 16/11 (uma dimensão, sem forma)
        self.__dict__.update(st)
        if "grades" not in st:
            self.nomes, self.grades, self.forma = [self.nome], [np.asarray(self.grade, float)], "fracao"
            novos = []
            for linha in self.blocos:
                arr = np.empty(len(linha), dtype=object)
                for i, x in enumerate(linha):
                    arr[i] = x
                novos.append(arr)
            self.blocos = novos

    def _cantos(self, v):
        v = np.atleast_1d(np.asarray(v, float))
        L = []
        for g, x in zip(self.grades, v):
            x = float(np.clip(x, g[0], g[-1]))
            if len(g) == 1:
                L.append((0, 0, 0.0)); continue
            i = int(np.clip(np.searchsorted(g, x) - 1, 0, len(g) - 2))
            L.append((i, i + 1, (x - g[i]) / (g[i + 1] - g[i])))
        return L

    def _campo(self, arr, campo, cantos):
        def rec(d, idx):
            if d == len(cantos):
                return getattr(arr[tuple(idx)], campo)
            i0, i1, t = cantos[d]
            if t <= 0:
                return rec(d + 1, idx + [i0])
            if t >= 1:
                return rec(d + 1, idx + [i1])
            return _lin(rec(d + 1, idx + [i0]), rec(d + 1, idx + [i1]), t)
        return rec(0, [])

    def interpola_todos(self, v, reps=None) -> dict:
        reps = range(len(self.des)) if reps is None else reps
        cantos = self._cantos(v)
        tem_alvo = getattr(self.blocos[0].flat[0], "EXA", None) is not None
        out = {c: [] for c in self.CAMPOS}; W = []
        for r in reps:
            for c in self.CAMPOS:
                if c in ("EXA", "SOA") and not tem_alvo:
                    continue
                out[c].append(self._campo(self.blocos[r], c, cantos))
            W.append(self.pesos_gm[r] / len(reps))
        with np.errstate(invalid="ignore"):
            F = np.nanmean(np.stack(out["F"]), axis=0)
        res = dict(F=F, TX=np.concatenate(out["TX"], axis=1), Z=np.concatenate(out["Z"], axis=1),
                   W=np.concatenate(W))
        if tem_alvo:
            res["EXA"] = sum(out["EXA"]); res["SOA"] = sum(out["SOA"])
        return res

    def interpola(self, v, reps=None) -> tuple:
        d = self.interpola_todos(v, reps)
        return d["F"], d["TX"], d["Z"], d["W"]


def _wquantil(x, w, q):
    o = np.argsort(x); x, w = x[o], w[o]
    c = np.cumsum(w) / w.sum()
    return float(np.interp(q, c, x))


def momentos_w(d: dict, w: np.ndarray) -> dict:
    """Momentos de calibração como esperança sobre os níveis contratuais com pesos w."""
    F = d["F"]
    ok = ~np.isnan(F).any(axis=0)
    Fo = F[:, ok]
    m1 = float((w[:, None] * Fo).sum(axis=0).mean()); m2 = float((w[:, None] * Fo**2).sum(axis=0).mean())
    x = d["TX"].ravel(); ww = (w[:, None] * d["W"][None, :]).ravel()
    m = ~np.isnan(x)
    out = dict(frac_lance_media=m1, frac_lance_dp=float(np.sqrt(max(m2 - m1**2, 0.0))),
               taxa_contempl_q50=_wquantil(x[m], ww[m], 0.5))
    if "EXA" in d:
        ex = float((w * d["EXA"].sum(axis=1)).sum()); so = float((w * d["SOA"].sum(axis=1)).sum())
        out["frac_sorteio_excluidos"] = ex / max(ex + so, 1e-12)
    return out


def momentos_mistura(F, TX, W, m_s, sigma_s) -> dict:
    """mu_cal simulado na forma 'fracao' (compatível com 16/11)."""
    return momentos_w(dict(F=F, TX=TX, W=W), painel.pesos_fracao(m_s, sigma_s))


class Objetivo:
    """theta = (parâmetros de simulação da superfície..., parâmetros da mistura...)."""

    def __init__(self, sup: Superficie, mu: dict, W: np.ndarray, cal=None):
        self.sup = sup
        self.cal = cal or CAL_FORMA.get(sup.forma, CAL)
        self.mu, self.W = np.array([mu[k] for k in self.cal]), W
        self.d_sim = len(sup.nomes)
        self.nomes = sup.nomes + MISTURA[sup.forma]
        self._cache = {}

    def _pesos(self, mix):
        return painel.pesos(self.sup.forma, tuple(mix), painel.niveis_de(self.sup.forma))

    def momentos(self, theta, reps=None) -> np.ndarray:
        v, mix = tuple(theta[: self.d_sim]), theta[self.d_sim:]
        chave = (tuple(round(float(x), 10) for x in v), None if reps is None else tuple(reps))
        if chave not in self._cache:
            self._cache = {chave: self.sup.interpola_todos(v, reps)}
        m = momentos_w(self._cache[chave], self._pesos(mix))
        return np.array([m[k] for k in self.cal])

    def Q(self, theta, mu=None, reps=None) -> float:
        if any(not (LIMITES[n][0] <= x <= LIMITES[n][1]) for n, x in zip(self.nomes, theta)):
            return 1e12
        d = self.momentos(theta, reps) - (self.mu if mu is None else mu)
        return float(d @ self.W @ d)

    def _inicios_mistura(self):
        return {"fracao": [(0.4, 0.3), (0.7, 0.3), (1.0, 0.3)], "sobra": [(0.2,), (0.5,), (0.8,)],
                "kappa": [(0.3,), (1.0,)]}[self.sup.forma]

    def minimiza(self, mu=None, reps=None, x0=None):
        """Busca inicial nos nós da grade (mistura otimizada em cada nó) e Nelder-Mead conjunto."""
        mu = self.mu if mu is None else mu
        if x0 is None:
            melhor = (np.inf, None)
            for no in itertools.product(*self.sup.grades):
                for m0 in self._inicios_mistura():
                    r = optimize.minimize(lambda z: self.Q((*no, *z), mu, reps), x0=list(m0), method="Nelder-Mead",
                                          options=dict(xatol=1e-4, fatol=1e-6, maxiter=400))
                    if r.fun < melhor[0]:
                        melhor = (r.fun, (*no, *r.x))
            x0 = melhor[1]
        r = optimize.minimize(lambda z: self.Q(z, mu, reps), x0=x0, method="Nelder-Mead",
                              options=dict(xatol=1e-5, fatol=1e-8, maxiter=3000))
        return r.x, r.fun


# ================================================================ comandos

def _carrega(proc):
    a, b = painel.carrega(proc)
    fixos = pd.read_csv(Path("results") / "parametros_fixos.csv")
    return a, b, fixos


def _pkl(proc, forma):
    return Path(proc) / f"calibracao_superficie_{forma}.pkl"


class _Unpickler(pickle.Unpickler):
    """Superfícies gravadas por `python -m` têm as classes registradas em __main__."""
    def find_class(self, module, name):
        if module == "__main__":
            module = "src.analysis.calibracao"
        return super().find_class(module, name)


def carrega_pkl(proc, forma) -> dict:
    with open(_pkl(proc, forma), "rb") as fh:
        return _Unpickler(fh).load()


def identificacao(args):
    """Jacobiano no ponto de partida (modelo de 16/11, forma 'fracao')."""
    a, b, fixos = _carrega(args.proc)
    dados = Dados(a, b)
    mu = dados.momentos()
    se = dados.bootstrap(args.B, SEMENTE)[CAL].std().values
    des = [painel.monta_desenho(a, b, args.grupos_por_adm, seed=0)]
    base = base_parametros(fixos)
    p0 = PONTO_PARTIDA
    L = []
    for nome in ("phi0", "lam_max"):
        vals = [p0[nome] - PASSOS[nome], p0[nome] + PASSOS[nome]]
        sup = Superficie(nome, vals, des, replace(base, phi0=p0["phi0"], lam_max=p0["lam_max"]),
                         processos=args.processos)
        mm = [momentos_mistura(*[x for i, x in enumerate(sup.interpola(v)) if i in (0, 1, 3)], p0["m_s"], p0["sigma_s"])
              for v in vals]
        d = (np.array([mm[1][k] for k in CAL]) - np.array([mm[0][k] for k in CAL])) / 2
        for k, x, s in zip(CAL, d, se):
            L.append(dict(parametro=nome, passo=PASSOS[nome], momento=k, delta_por_passo=x, delta_em_ep=x / s))
    sup = Superficie("phi0", [p0["phi0"]], des, replace(base, phi0=p0["phi0"], lam_max=p0["lam_max"]),
                     processos=args.processos)
    bl, Wg = sup.blocos[0][0], sup.pesos_gm[0]
    for nome in ("m_s", "sigma_s"):
        mm = []
        for sg in (-1, 1):
            q2 = dict(m_s=p0["m_s"], sigma_s=p0["sigma_s"]); q2[nome] += sg * PASSOS[nome]
            mm.append(momentos_mistura(bl.F, bl.TX, Wg, q2["m_s"], q2["sigma_s"]))
        d = (np.array([mm[1][k] for k in CAL]) - np.array([mm[0][k] for k in CAL])) / 2
        for k, x, s in zip(CAL, d, se):
            L.append(dict(parametro=nome, passo=PASSOS[nome], momento=k, delta_por_passo=x, delta_em_ep=x / s))
    t = pd.DataFrame(L)
    J = t.pivot(index="momento", columns="parametro", values="delta_em_ep").loc[CAL]
    resumo = []
    for comp in ("phi0", "lam_max"):
        sv = np.linalg.svd(J[[comp, "m_s", "sigma_s"]].values, compute_uv=False)
        resumo.append(dict(parametro="conjunto_" + comp, momento="valores_singulares",
                           sv1=sv[0], sv2=sv[1], sv3=sv[2], condicao=sv[0] / sv[-1]))
    t = pd.concat([t, pd.DataFrame(resumo)], ignore_index=True)
    t["mu_dado"] = t["momento"].map(mu); t["ep_dado"] = t["momento"].map(dict(zip(CAL, se)))
    t.round(6).to_csv(Path("results") / "calibracao_identificacao.csv", index=False)
    print(J.round(3).to_string()); print(pd.DataFrame(resumo).round(3).to_string(index=False))


def calibra(args):
    a, b, fixos = _carrega(args.proc)
    forma = args.forma
    cal = CAL_FORMA[forma]
    dados = Dados(a, b)
    mu = dados.momentos()
    boot = dados.bootstrap(args.B, SEMENTE)
    var = boot[cal].var().values
    W = np.diag(1.0 / var)
    base = base_parametros(fixos, forma)
    grades = GRADES_FORMA[forma]
    if args.reusar_superficie:
        sup = carrega_pkl(args.proc, forma)["sup"]
        des = sup.des
        print("[superfície reaproveitada]", flush=True)
    else:
        des = [painel.monta_desenho(a, b, args.grupos_por_adm, seed=r) for r in range(args.replicas)]
        n = int(np.prod([len(g) for g in grades.values()]))
        print(f"[{forma}: {len(des)} réplicas × {n} pontos × {len(painel.niveis_de(forma))} níveis]", flush=True)
        sup = Superficie(grades, None, des, base, processos=args.processos, forma=forma,
                         log=lambda s: print(s, flush=True))
        with open(_pkl(args.proc, forma), "wb") as fh:
            pickle.dump(dict(sup=sup), fh)
    obj = Objetivo(sup, mu, W, cal)
    th, q = obj.minimiza()
    print("theta", dict(zip(obj.nomes, th)), "Q", q, flush=True)
    th_r = [obj.minimiza(reps=[r], x0=th)[0] for r in range(len(des))]
    var_sem = np.var(th_r, axis=0, ddof=1) / len(des)
    mus = boot[cal].values[: args.B_theta]
    th_b = []
    for i, m in enumerate(mus):
        th_b.append(obj.minimiza(mu=m, x0=th)[0])
        if (i + 1) % 25 == 0:
            print(f"  bootstrap {i+1}/{len(mus)}", flush=True)
    th_b = np.array(th_b)
    ep_b = th_b.std(axis=0, ddof=1); ep_t = np.sqrt(ep_b**2 + var_sem)
    # conferência por simulação direta
    par = replace(base, **dict(zip(sup.nomes, map(float, th[: obj.d_sim]))))
    direto = [roda_bloco(d, par, rep=r, processos=args.processos, forma=forma) for r, d in enumerate(des)]
    dd = dict(F=np.nanmean(np.stack([x.F for x in direto]), axis=0),
              TX=np.concatenate([x.TX for x in direto], axis=1),
              W=np.concatenate([p / len(des) for p in sup.pesos_gm]),
              EXA=sum(x.EXA for x in direto), SOA=sum(x.SOA for x in direto))
    m_dir = momentos_w(dd, obj._pesos(th[obj.d_sim:]))
    m_sup = dict(zip(cal, obj.momentos(th)))
    T = pd.DataFrame(dict(parametro=obj.nomes, valor=th, ep_bootstrap=ep_b, ep_semente=np.sqrt(var_sem), ep_total=ep_t,
                          ic95_inf=th - 1.96 * ep_t, ic95_sup=th + 1.96 * ep_t,
                          p2_5_bootstrap=np.percentile(th_b, 2.5, axis=0),
                          p97_5_bootstrap=np.percentile(th_b, 97.5, axis=0)))
    for r, x in enumerate(th_r):
        T[f"replica_{r}"] = x
    T.round(6).to_csv(Path("results") / "calibracao_theta.csv", index=False)
    M = pd.DataFrame(dict(momento=cal, dado=[mu[k] for k in cal], ep_dado=np.sqrt(var), peso_W=np.diag(W),
                          simulado_superficie=[m_sup[k] for k in cal], simulado_direto=[m_dir[k] for k in cal]))
    M["t_residuo"] = (M["simulado_direto"] - M["dado"]) / M["ep_dado"]
    M["Q_parcela"] = M["t_residuo"] ** 2
    M.round(6).to_csv(Path("results") / "calibracao_momentos.csv", index=False)
    cfg = dict(forma=forma, semente_bootstrap=SEMENTE, B=args.B, B_theta=args.B_theta, replicas=len(des),
               grupos_por_adm=args.grupos_por_adm, parametros=obj.nomes,
               grades={k: list(map(float, v)) for k, v in zip(sup.nomes, sup.grades)},
               momentos_calibracao=cal, W="diag(1/Var_boot(momentos de calibração))", Q_min=q,
               graus_sobreidentificacao=len(cal) - len(th), Q_direto=float(M["Q_parcela"].sum()),
               emb_max=base.emb_max, sorteio_excluidos=base.sorteio_excluidos,
               fixos=dict(phi1=base.phi1, phi2=base.phi2, mu_theta=base.mu_theta, sd_theta=base.sd_theta,
                          a_lam=base.a_lam, b_lam=base.b_lam, lam_max=base.lam_max,
                          vagas_sorteio=base.vagas_sorteio, vagas_excluidos=base.vagas_excluidos))
    pd.DataFrame([dict(chave=k, valor=json.dumps(v, ensure_ascii=False)) for k, v in cfg.items()]).to_csv(
        Path("results") / "calibracao_config.csv", index=False)
    pd.DataFrame(th_b, columns=obj.nomes).round(6).to_csv(Path("results") / "calibracao_bootstrap.csv", index=False)
    with open(_pkl(args.proc, forma), "wb") as fh:
        pickle.dump(dict(sup=sup, mu=mu, W=W, theta=th, nomes=obj.nomes, boot=boot, th_b=th_b, th_r=th_r), fh)
    print(T.round(4).to_string(index=False)); print(M.round(5).to_string(index=False))


def momentos_teste(F, Z, Wg, alvo, adms, m_s=None, sigma_s=None, n_sorteios=500, seed=SEMENTE, w=None):
    """mu_tes simulado: frac_sem_contempl pela mistura; spearman_lance_tamanho como média sobre
    realizações do nível contratual por administradora (ESTADO §4, critério de H2).
    w = pesos dos níveis (se None, forma 'fracao' com (m_s, sigma_s))."""
    w = painel.pesos_fracao(m_s, sigma_s) if w is None else np.asarray(w, float)
    sem = 0.0
    for k, wk in enumerate(w):
        m = ~np.isnan(Z[k])
        sem += wk * np.average(Z[k][m], weights=Wg[m])
    idx = {c: j for j, c in enumerate(adms)}
    adm_lin = alvo["cnpj"].map(idx).values
    tam = alvo["tam_med"].values
    rng = np.random.default_rng(seed)
    sp = []
    for _ in range(n_sorteios):
        niv = rng.choice(len(w), size=len(adms), p=w)
        f = F[niv[adm_lin], np.arange(F.shape[1])]
        ok = ~np.isnan(f)
        sp.append(stats.spearmanr(f[ok], tam[ok]).statistic)
    return dict(spearman_lance_tamanho=float(np.mean(sp)), frac_sem_contempl=float(sem))


def h2(args):
    P = carrega_pkl(args.proc, args.forma)
    sup, th, boot, th_b = P["sup"], P["theta"], P["boot"], P["th_b"]
    forma = sup.forma
    d_sim = len(sup.nomes)

    def pesos_mix(t):
        return painel.pesos(forma, tuple(t[d_sim:]), painel.niveis_de(forma))

    a, b, fixos = _carrega(args.proc)
    mu = Dados(a, b).momentos()
    d_dado = np.array([mu[k] for k in TES])
    S_dado = boot[TES].cov().values
    adms = sup.des[0].adms
    par = replace(sup.base, **dict(zip(sup.nomes, map(float, th[:d_sim]))))
    blocos = [roda_bloco(d, par, rep=r, processos=args.processos, forma=forma) for r, d in enumerate(sup.des)]
    w = pesos_mix(th)
    por_rep = [momentos_teste(bl.F, bl.Z, sup.pesos_gm[r], sup.alvo, adms, w=w) for r, bl in enumerate(blocos)]
    F = np.nanmean(np.stack([x.F for x in blocos]), axis=0)
    Z = np.concatenate([x.Z for x in blocos], axis=1)
    Wg = np.concatenate([p / len(blocos) for p in sup.pesos_gm])
    m_sim = momentos_teste(F, Z, Wg, sup.alvo, adms, w=w)
    v_sim = np.array([[x[k] for k in TES] for x in por_rep])
    S_sim = np.cov(v_sim.T, ddof=1) / len(blocos)
    v_th = []
    for t in th_b:
        dd = sup.interpola_todos(tuple(t[:d_sim]))
        x = momentos_teste(dd["F"], dd["Z"], dd["W"], sup.alvo, adms, w=pesos_mix(t), n_sorteios=100)
        v_th.append([x[k] for k in TES])
    S_th = np.cov(np.array(v_th).T, ddof=1)
    S = S_dado + S_sim + S_th
    d = np.array([m_sim[k] for k in TES]) - d_dado
    J = float(d @ np.linalg.solve(S, d)); p = float(stats.chi2.sf(J, 2))
    se = np.sqrt(np.diag(S)); t = d / se
    cal = pd.read_csv(Path("results") / "calibracao_momentos.csv")
    ajuste_ruim = bool((cal["t_residuo"].abs() > 2).any())
    obs = "partição pendente de confirmação" + ("; condicional a ajuste ruim de calibração" if ajuste_ruim else "")
    if forma == "sobra":
        obs += "; modelo revisado após ver o teste de 16/11 (ESTADO §4, 19/11)"
    L = []
    for i, k in enumerate(TES):
        L.append(dict(item=k, dado=d_dado[i], simulado=m_sim[k], diferenca=d[i], ep_dado=np.sqrt(S_dado[i, i]),
                      ep_simulacao=np.sqrt(S_sim[i, i]), ep_theta=np.sqrt(S_th[i, i]), ep_total=se[i], t=t[i],
                      limiar=2.24, rejeita=bool(abs(t[i]) > 2.24), menor_dif_detectavel_80=(1.96 + 0.84) * se[i],
                      observacao=obs + ("; contaminado (ESTADO §5 item 21)" if k == "frac_sem_contempl" else "")))
    L.append(dict(item="wald_conjunto", t=J, limiar=5.99, rejeita=bool(J > 5.99), simulado=p,
                  observacao=obs + "; coluna t = J, coluna simulado = p-valor qui2(2)"))
    L.append(dict(item="regra_secundaria_spearman", t=t[0], limiar=1.96, rejeita=bool(abs(t[0]) > 1.96),
                  observacao=obs + "; só spearman_lance_tamanho"))
    L.append(dict(item="sinal_spearman_simulado_negativo", t=m_sim["spearman_lance_tamanho"], limiar=0.0,
                  rejeita=bool(m_sim["spearman_lance_tamanho"] < 0), observacao=obs))
    pd.DataFrame(L).round(6).to_csv(Path("results") / "h2_teste.csv", index=False)
    print(pd.DataFrame(L).round(4).to_string(index=False))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("comando", choices=["identificacao", "calibra", "h2"])
    ap.add_argument("--proc", default="data/processed", type=Path)
    ap.add_argument("--forma", default="sobra", choices=["sobra", "fracao"])
    ap.add_argument("--B", default=500, type=int, help="reamostragens para Var dos momentos de dados (W)")
    ap.add_argument("--B-theta", default=100, type=int, help="reamostragens re-otimizadas para o ep de Theta")
    ap.add_argument("--grupos-por-adm", default=12, type=int)
    ap.add_argument("--replicas", default=3, type=int)
    ap.add_argument("--processos", default=2, type=int)
    ap.add_argument("--reusar-superficie", action="store_true",
                    help="reaproveita as simulações da grade guardadas em data/processed")
    args = ap.parse_args(argv)
    {"identificacao": identificacao, "calibra": calibra, "h2": h2}[args.comando](args)


if __name__ == "__main__":
    from src.analysis import calibracao as _modulo   # classes gravadas no pickle com o caminho do módulo
    _modulo.main()
