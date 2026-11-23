"""Agentes de aprendizado por reforço para H1 e H4 (ESTADO §4, 22/11).

Q-learning tabular por Monte Carlo (toda visita) com uma tabela única compartilhada por
todas as cotas (parâmetros compartilhados). Cada cota é um agente que, a cada assembleia em
que pode ofertar, escolhe o lance total entre ACOES. A recompensa é a utilidade realizada
U_i (a mesma de src/analysis/comparacao.py), recebida na contemplação; cota excluída não
gera atualização.

Estado (240): quintil de theta_i × faixa de lambda_i (3) × faixa do prazo restante (4) ×
faixa do menor lance vencedor da assembleia anterior (4).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .grupo import CONTEMPLADA, EXCLUIDA, INADIMPLENTE, RESTITUIDA, Parametros, sorteia_theta

ACOES = np.round(np.arange(0.0, 0.5001, 0.05), 2)
CORTES_REST = np.array([0.25, 0.5, 0.75])
CORTES_CORTE = np.array([0.02, 0.15, 0.30])
N_EST = 5 * 3 * 4 * 4


def cortes_tipos(par: Parametros, n: int = 200_000, seed: int = 123):
    """Quintis de theta e tercis de lambda da distribuição da base (fixos durante o treino)."""
    rng = np.random.default_rng(seed)
    th = sorteia_theta(rng, par, n)
    lam = rng.beta(par.a_lam, par.b_lam, n) * par.lam_max
    return np.quantile(th, [0.2, 0.4, 0.6, 0.8]), np.quantile(lam, [1 / 3, 2 / 3])


@dataclass
class Agente:
    par: Parametros
    seed: int = 0
    eps: float = 0.3
    alfa: float = 0.1          # passo constante (tentativa 1); alfa <= 0 = média amostral por (s, a) (tentativa 2)
    treino: bool = True
    Q: np.ndarray = None
    visitas: np.ndarray = None
    _buf: list = field(default_factory=list)

    def __post_init__(self):
        self.rng = np.random.default_rng(self.seed)
        self.c_th, self.c_lam = cortes_tipos(self.par)
        if self.Q is None:
            self.Q = np.zeros((N_EST, len(ACOES)))
        if self.visitas is None:
            self.visitas = np.zeros(N_EST)

    # ------------------------------------------------------------ estado e ação
    def estado(self, theta, lam, restante, corte):
        tq = np.searchsorted(self.c_th, theta)
        lb = np.searchsorted(self.c_lam, lam)
        rb = np.searchsorted(CORTES_REST, restante)
        cb = np.searchsorted(CORTES_CORTE, np.full(len(theta), corte))
        return ((tq * 3 + lb) * 4 + rb) * 4 + cb

    def __call__(self, cand, cotas, t, T, par, ctx):
        th, lam, dev = cotas.theta[cand], cotas.lam[cand], cotas.devedor[cand]
        s = self.estado(th, lam, (T - t) / T, ctx["corte"])
        viavel = ACOES[None, :] <= (lam + par.emb_max)[:, None] + 1e-12
        q = np.where(viavel, self.Q[s], -np.inf)
        a = q.argmax(axis=1)
        if self.treino and self.eps > 0:
            explora = self.rng.random(len(cand)) < self.eps
            if explora.any():
                n_v = viavel[explora].sum(axis=1)
                k = (self.rng.random(explora.sum()) * n_v).astype(int)
                a[explora] = np.minimum(k, n_v - 1)   # ações viáveis são um prefixo de ACOES
            self._buf.append((cand.copy(), s, a))
        b = ACOES[a]
        livre = np.minimum(np.minimum(b, lam), dev)
        emb = np.clip(np.minimum(np.minimum(b - livre, par.emb_max), dev - livre), 0.0, None)
        return livre, emb

    # ------------------------------------------------------------ atualização
    @staticmethod
    def utilidade(res, T):
        """U_i por cota; nan para cota excluída (mesma fórmula de comparacao.metricas_grupo)."""
        x = res.extra
        sit, ent, tc = x["situacao"], x["entrada"], x["t_cont"]
        excl = (sit == EXCLUIDA) | (sit == RESTITUIDA) | (sit == INADIMPLENTE) | (x["t_excl"] >= 0)
        tcont = np.where(tc >= 0, tc, T - 1)
        w = (tcont + 1 - ent).astype(float)
        rr = (T - 1 - tcont).astype(float)
        th = x["theta"]
        U = np.exp(-th * w / 12.0) * (1.0 - x["emb"]) - x["livre"] * (1.0 - np.exp(-th * rr / 12.0))
        return np.where(excl, np.nan, U)

    def atualiza(self, res, T):
        if not self._buf:
            return
        U = self.utilidade(res, T)
        idx = np.concatenate([b[0] for b in self._buf])
        s = np.concatenate([b[1] for b in self._buf])
        a = np.concatenate([b[2] for b in self._buf])
        self._buf = []
        G = U[idx]
        ok = ~np.isnan(G)
        s, a, G = s[ok], a[ok], G[ok]
        soma = np.zeros_like(self.Q); n = np.zeros_like(self.Q)
        np.add.at(soma, (s, a), G); np.add.at(n, (s, a), 1.0)
        m = n > 0
        if self.alfa > 0:
            self.Q[m] = (1 - self.alfa) * self.Q[m] + self.alfa * (soma[m] / n[m])
        else:
            if not hasattr(self, "n_sa"):
                self.n_sa = np.zeros_like(self.Q)
            tot = self.n_sa[m] + n[m]
            self.Q[m] = (self.n_sa[m] * self.Q[m] + soma[m]) / tot
            self.n_sa[m] = tot
        np.add.at(self.visitas, s, 1.0)

    def gulosa(self):
        return self.Q.argmax(axis=1)

    def congelada(self) -> "Agente":
        """Cópia sem exploração nem registro, para avaliação."""
        return Agente(self.par, seed=self.seed, eps=0.0, treino=False, Q=self.Q.copy(), visitas=self.visitas.copy())
