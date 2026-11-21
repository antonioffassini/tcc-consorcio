"""Simulação no grão dos dados: administradoras, grupos e meses observados.

O simulador de um grupo (`grupo.py`) roda cada grupo amostrado do painel A
até a última assembleia observada, com prazo e tamanho tirados do próprio
grupo. Os momentos simulados são calculados só nos meses e trimestres que
existem nos dados, com as mesmas fórmulas de `src/analysis/momentos.py`.

Heterogeneidade (ESTADO §4, 15/11):
  - estrutural, observada: prazo T e tamanho N de cada grupo (painel A);
    idade de cada grupo em cada mês observado;
  - contratual, latente: as vagas de sorteio previstas por assembleia
    (Res. BCB 285/2023, art. 2º, XII; art. 12, I) são fixadas pela
    administradora j. Forma adotada ("fracao"): kappa_g = max(1, s_j * N_g/T_g),
    em que N_g/T_g é a capacidade ordinária mensal do grupo (cartas por mês
    pagas pelas parcelas) e s_j ~ LogNormal(log m_s, sigma_s) é a fração dessa
    capacidade reservada ao sorteio. Forma alternativa, descartada no passo 1
    ("kappa"): kappa_j - 1 ~ Poisson(nu), independente do tamanho do grupo
    (ver results/sim_forma_heterogeneidade.csv e ESTADO §4, 15/11).
    O efeito dos parâmetros da distribuição é obtido por mistura: cada grupo é
    simulado uma vez para cada nível da grade e os momentos são ponderados
    pela massa da distribuição em cada nível. Isso mantém a função objetivo
    contínua nos parâmetros da distribuição, com números aleatórios comuns;
  - comportamental, comum: phi, distribuições de theta e lambda.
Parâmetros fixados fora do SMM, a partir do painel A: risco de exclusão por
faixa de idade h(t/T) e recolocação rho (`parametros_fixos`).
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from .grupo import Parametros, regra_M0, simula

KAPPAS = (1, 2, 3, 4)
GRADE_S = (0.1, 0.25, 0.4, 0.55, 0.7, 0.85, 1.0, 1.3, 1.7)
NIVEIS_SOBRA = (0, 1)
FORMAS = ("sobra", "fracao", "kappa")
# "sobra" (19/11, ESTADO §4): a heterogeneidade contratual é o destino da sobra sem lance;
# nível 1 = a administradora faz sorteio da sobra (Porto, Itaú, Sicredi), 0 = leva o saldo
# à assembleia seguinte (Santander); P(nível 1) = pi. As vagas de sorteio das ativas ficam
# em kappa_a = 1 (o que vier da base). "fracao" é o modelo de 16/11 (sensibilidade).
CORTES_IDADE = (0.1, 0.2, 1 / 3, 0.5, 2 / 3, 10.0)
MIN_CONTEMPL = 30


# ---------------------------------------------------------------- dados

def carrega(proc: Path):
    a = pd.read_parquet(Path(proc) / "painel_a_grupo_mes.parquet")
    b = pd.read_parquet(Path(proc) / "painel_b_adm_trimestre.parquet")
    return a, b


def parametros_fixos(a: pd.DataFrame) -> pd.DataFrame:
    """h por faixa de idade e rho, calculados no painel A (pós-285).

    h: soma(excluidas_mes, truncada no p99 do grupo×mês) / soma(ativas), por
    faixa de assembleia/prazo. rho: reposição líquida de vagas sobre exclusões
    no primeiro terço do prazo, onde está a maior parte das exclusões, com
    reposição = Δativas + excluidas_mes + Δquitadas; truncado em 1 (o modelo
    não cria vaga nova além da recolocada).
    """
    x = a[a["ativas"] > 0].sort_values(["cnpj", "grupo", "data_base"]).copy()
    g = x.groupby(["cnpj", "grupo"])
    x["d_at"] = g["ativas"].diff(); x["d_q"] = g["ativas_quitadas"].diff()
    x = x[x["excluidas_mes"].notna() & x["d_at"].notna() & ~x["flag_mes_anterior_ausente"]]
    x["idade"] = x["assembleia"] / x["prazo"]
    q99 = x["excluidas_mes"].quantile(0.99)
    L, lo = [], 0.0
    for k, hi in enumerate(CORTES_IDADE):
        s = x[(x["idade"] > lo) & (x["idade"] <= hi)]
        h = s["excluidas_mes"].clip(upper=q99).sum() / s["ativas"].sum()
        L.append(dict(parametro=f"h_faixa{k}", valor=round(float(h), 5), limite_inf=round(lo, 4),
                      limite_sup=round(min(hi, 1.0), 4), n=len(s)))
        lo = hi
    t1 = x[x["idade"] <= 1 / 3]
    rep = t1["d_at"] + t1["excluidas_mes"] + t1["d_q"]
    rho_bruto = rep.sum() / t1["excluidas_mes"].sum()
    L.append(dict(parametro="rho_bruto", valor=round(float(rho_bruto), 4), limite_inf=0, limite_sup=round(1 / 3, 4), n=len(t1)))
    L.append(dict(parametro="rho", valor=round(float(min(1.0, rho_bruto)), 4), limite_inf=0, limite_sup=round(1 / 3, 4), n=len(t1)))
    return pd.DataFrame(L)


def h_idade_de(fixos: pd.DataFrame) -> tuple:
    f = fixos[fixos["parametro"].str.startswith("h_faixa")]
    return (tuple(CORTES_IDADE), tuple(f["valor"].astype(float)))


@dataclass
class Desenho:
    grupos: pd.DataFrame       # um por grupo amostrado: gid, cnpj, adm, N, T, horizonte, peso, seed
    obs: pd.DataFrame          # grupo×mês observado: gid, t (0-based), trimestre, data_base
    alvo_b: pd.DataFrame       # administradora×trimestre do momento de lance (com tam_med do dado)
    adms: np.ndarray           # cnpjs, na ordem do índice adm


def monta_desenho(a: pd.DataFrame, b: pd.DataFrame, grupos_por_adm: int = 4, seed: int = 0) -> Desenho:
    """Amostra até `grupos_por_adm` grupos por administradora (semente fixa).

    Peso de cada grupo = (grupos da administradora no painel) / (amostrados),
    para que os quantis por grupo×mês reproduzam a composição do painel A.
    """
    rng = np.random.default_rng(seed)
    a = a[(a["regime"] == "pos285") & (a["ativas"] > 0)]
    adms = np.sort(a["cnpj"].unique())
    idx = {c: k for k, c in enumerate(adms)}
    G, O = [], []
    gid = 0
    for c in adms:
        gs = np.sort(a.loc[a["cnpj"] == c, "grupo"].unique())
        esc = rng.choice(gs, size=min(grupos_por_adm, len(gs)), replace=False)
        for g in np.sort(esc):
            x = a[(a["cnpj"] == c) & (a["grupo"] == g)]
            T = int(x["prazo"].median())
            t = (x["assembleia"].astype(int) - 1).clip(lower=0)
            ok = t < T
            if not ok.any():
                continue
            G.append(dict(gid=gid, cnpj=c, adm=idx[c], grupo=g, N=max(10, int(round(x["ativas"].median()))),
                          T=T, horizonte=int(t[ok].max()) + 1, peso=len(gs) / len(esc),
                          seed=int(rng.integers(2**31))))
            O.append(pd.DataFrame(dict(gid=gid, t=t[ok].values, trimestre=x.loc[ok, "trimestre"].values,
                                       data_base=x.loc[ok, "data_base"].values)))
            gid += 1
    grupos = pd.DataFrame(G)
    obs = pd.concat(O, ignore_index=True)
    bp = b[(b["regime"] == "pos285") & (b["contempl_trim"] >= MIN_CONTEMPL)]
    car = a.groupby(["cnpj", "trimestre"]).agg(tam_med=("cotas_total", "median")).reset_index()
    alvo = bp[["cnpj", "trimestre", "frac_lance"]].merge(car, on=["cnpj", "trimestre"], how="inner")
    return Desenho(grupos, obs, alvo.reset_index(drop=True), adms)


# ---------------------------------------------------------------- simulação

def _roda(args):
    par, seed, horizonte, ts, regra, sorteio = args
    r = simula(par, seed=seed, regra=regra, sorteio=sorteio, horizonte=horizonte)
    return np.stack([r.contempl_lance[ts], r.contempl_sorteio[ts], r.ativas[ts], r.restituicoes[ts]])


def _roda_mec(args):
    par, seed, horizonte, ts, mec = args
    r = simula(par, seed=seed, mecanismo=mec, horizonte=horizonte)
    return np.stack([r.contempl_lance[ts], r.contempl_sorteio[ts], r.ativas[ts], r.restituicoes[ts]])


def niveis_de(forma: str) -> tuple:
    return {"fracao": GRADE_S, "kappa": KAPPAS, "sobra": NIVEIS_SOBRA}[forma]


def vagas(forma: str, nivel: float, N: int, T: int) -> float:
    return max(1.0, nivel * N / T) if forma == "fracao" else float(nivel)


def ajusta(base: Parametros, forma: str, nivel, N: int, T: int) -> Parametros:
    """Parâmetros do grupo (N, T) no nível contratual `nivel` da forma dada."""
    if forma == "sobra":
        return replace(base, N=N, T=T, sorteio_sobra=bool(nivel))
    return replace(base, N=N, T=T, vagas_sorteio=vagas(forma, nivel, N, T))


def simula_desenho(des: Desenho, base: Parametros, kappas=None, regra=regra_M0, sorteio=None,
                   processos: int = 1, rep: int = 0, forma: str = "fracao", mecanismo=None) -> dict:
    """Roda cada grupo do desenho para cada nível da heterogeneidade contratual.
    Retorna {nível: array (n_obs, 4)} alinhado com des.obs: colunas lance,
    sorteio, ativas, restituições. `kappas` = níveis (padrão: grade da forma)."""
    kappas = niveis_de(forma) if kappas is None else kappas
    ts = {g: v["t"].values for g, v in des.obs.groupby("gid")}
    tarefas, chaves = [], []
    for k in kappas:
        for g in des.grupos.itertuples():
            par = ajusta(base, forma, k, g.N, g.T)
            if mecanismo is None:
                tarefas.append((par, g.seed + 7919 * rep, g.horizonte, ts[g.gid], regra, sorteio))
            else:
                tarefas.append((par, g.seed + 7919 * rep, g.horizonte, ts[g.gid], mecanismo))
            chaves.append((k, g.gid))
    if processos > 1:
        with Pool(processos) as p:
            outs = p.map(_roda if mecanismo is None else _roda_mec, tarefas, chunksize=4)
    else:
        outs = [(_roda if mecanismo is None else _roda_mec)(x) for x in tarefas]
    res = {}
    ordem = des.obs["gid"].values
    for k in kappas:
        blocos = {g: o for (kk, g), o in zip(chaves, outs) if kk == k}
        res[k] = np.concatenate([blocos[g].T for g in des.grupos["gid"]], axis=0)
        assert len(res[k]) == len(ordem)
    return res


def pesos_kappa(nu: float, kappas=KAPPAS) -> np.ndarray:
    w = stats.poisson.pmf(np.asarray(kappas) - 1, max(nu, 1e-8))
    return w / w.sum()


def pesos_fracao(m_s: float, sigma_s: float, grade=GRADE_S) -> np.ndarray:
    """Massa da LogNormal(log m_s, sigma_s) em cada célula da grade (bordas nos pontos médios)."""
    g = np.asarray(grade, float)
    bordas = np.concatenate([[0.0], (g[1:] + g[:-1]) / 2, [np.inf]])
    cdf = stats.lognorm.cdf(bordas, s=max(sigma_s, 1e-6), scale=max(m_s, 1e-8))
    w = np.diff(cdf)
    return w / w.sum()


def pesos_sobra(pi: float) -> np.ndarray:
    p = float(np.clip(pi, 0.0, 1.0))
    return np.array([1.0 - p, p])


def pesos(forma: str, psi: tuple, niveis) -> np.ndarray:
    """psi = (nu,) para 'kappa'; (m_s, sigma_s) para 'fracao'; (pi,) para 'sobra'."""
    if forma == "sobra":
        return pesos_sobra(psi[0])
    return pesos_kappa(psi[0], tuple(niveis)) if forma == "kappa" else pesos_fracao(psi[0], psi[1], tuple(niveis))


# ---------------------------------------------------------------- momentos

def _frac_adm_trim(des: Desenho, sim_k: np.ndarray) -> pd.DataFrame:
    o = des.obs.assign(lance=sim_k[:, 0], sorteio=sim_k[:, 1])
    o = o.merge(des.grupos[["gid", "cnpj"]], on="gid")
    s = o.groupby(["cnpj", "trimestre"])[["lance", "sorteio"]].sum().reset_index()
    s["frac"] = s["lance"] / (s["lance"] + s["sorteio"]).replace(0, np.nan)
    return des.alvo_b.merge(s[["cnpj", "trimestre", "frac"]], on=["cnpj", "trimestre"], how="left")


def _wquantil(x, w, q):
    o = np.argsort(x); x, w = x[o], w[o]
    c = np.cumsum(w) / w.sum()
    return float(np.interp(q, c, x))


def momentos_calibracao(des: Desenho, sims: dict, psi, forma: str = "kappa") -> dict:
    """mu_cal (ESTADO §4, 09/11): frac_lance_media, frac_lance_dp, taxa_contempl_q50,
    como esperança sobre a distribuição da heterogeneidade contratual (mistura).
    psi: nu (forma 'kappa') ou (m_s, sigma_s) (forma 'fracao')."""
    psi = (psi,) if np.isscalar(psi) else tuple(psi)
    w = pesos(forma, psi, tuple(sims))
    F = np.column_stack([_frac_adm_trim(des, sims[k])["frac"].values for k in sims])
    ok = ~np.isnan(F).any(axis=1)
    F = F[ok]
    m1 = float((F * w).sum(axis=1).mean())
    m2 = float((F**2 * w).sum(axis=1).mean())
    peso_g = des.obs["gid"].map(des.grupos.set_index("gid")["peso"]).values
    taxas, ws = [], []
    for k, wk in zip(sims, w):
        s = sims[k]; at = s[:, 2]; m = at > 0
        taxas.append((s[m, 0] + s[m, 1]) / at[m]); ws.append(peso_g[m] * wk)
    q50 = _wquantil(np.concatenate(taxas), np.concatenate(ws), 0.5)
    return dict(frac_lance_media=m1, frac_lance_dp=float(np.sqrt(max(m2 - m1**2, 0.0))),
                taxa_contempl_q50=q50)


def sorteia_niveis(des: Desenho, psi, rng, forma: str = "fracao") -> np.ndarray:
    """Uma realização do nível contratual por administradora."""
    psi = (psi,) if np.isscalar(psi) else tuple(psi)
    niv = niveis_de(forma)
    return rng.choice(np.asarray(niv, float), size=len(des.adms), p=pesos(forma, psi, niv))


def momentos_realizacao(des: Desenho, sims: dict, kappa_adm: np.ndarray) -> dict:
    """Momentos numa realização do nível contratual por administradora
    (kappa_adm[j] = nível da adm. j, um dos níveis de `sims`). Inclui mu_tes:
    só usar depois de escrito o critério de rejeição de H2."""
    adm_obs = des.obs["gid"].map(des.grupos.set_index("gid")["adm"]).values
    k_obs = np.asarray(kappa_adm, float)[adm_obs]
    S = np.zeros_like(sims[next(iter(sims))])
    for k in sims:
        m = np.isclose(k_obs, k)
        S[m] = sims[k][m]
    fr = _frac_adm_trim(des, S)
    ok = fr["frac"].notna()
    peso_g = des.obs["gid"].map(des.grupos.set_index("gid")["peso"]).values
    tot = S[:, 0] + S[:, 1]; m = S[:, 2] > 0
    return dict(frac_lance_media=float(fr.loc[ok, "frac"].mean()),
                frac_lance_dp=float(fr.loc[ok, "frac"].std()),
                taxa_contempl_q50=_wquantil(tot[m] / S[m, 2], peso_g[m], 0.5),
                spearman_lance_tamanho=float(stats.spearmanr(fr.loc[ok, "frac"], fr.loc[ok, "tam_med"]).statistic),
                frac_sem_contempl=float(np.average(tot[m] == 0, weights=peso_g[m])),
                frac_sorteio_excluidos=float(S[:, 3].sum() / max(S[:, 3].sum() + S[:, 1].sum(), 1)))
