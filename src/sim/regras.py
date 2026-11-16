"""Mecanismos de contemplação como estratégias trocáveis (passo 2, 16/11).

Um mecanismo = regra de sorteio + regra de lance; a ordem sorteio → lance e a
restrição de recursos ficam no simulador (`grupo.simula`), iguais para todos.

  M0 — vigente: sorteio uniforme entre ativas não contempladas e excluídas
       não restituídas; lance pay-as-bid (cada vencedor paga o próprio lance).
  M1 — sorteio ponderado pela situação da cota: peso 1 para a cota ativa e
       omega para a excluída; lance pay-as-bid. Com omega = 1, é M0.
  M2 — sorteio uniforme; lance de preço uniforme: os k maiores lances vencem
       e todos pagam o (k+1)-ésimo maior lance (primeiro lance recusado).

Assinaturas (as mesmas de `grupo.regra_M0`):
  lance(R, cand, livre, emb, max_venc=None) -> (vencedores, livre_pago, embutido_usado, R)
  sorteio(rng, elig, cotas, t) -> índice da cota sorteada, ou None
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .grupo import EPS, EXCLUIDA, regra_M0


# ---------------------------------------------------------------- lance

def regra_M2(R, cand, livre, emb, max_venc=None):
    """Lance de preço uniforme sobre o saldo residual R.

    Ordena os lances totais b = livre + embutido. Com k vencedores, o preço é
    p_k = b_(k+1) (zero se não houver (k+1)-ésimo lance). Cada vencedor
    amortiza p_k: paga a parte livre até min(livre_i, p_k) e completa com
    embutido; recebe 1 - embutido. A saída líquida do fundo por vencedor é
    1 - p_k, então k vencedores são viáveis se R >= k (1 - p_k). Como p_k
    não cresce com k, a condição é monótona e basta aumentar k até falhar.
    """
    b = livre[cand] + emb[cand]
    ordem = np.argsort(-b, kind="stable")
    bs = b[ordem]
    n_pos = int((bs > 0).sum())
    teto = n_pos if max_venc is None else min(n_pos, int(max_venc))
    k = 0
    while k < teto:
        k1 = k + 1
        p = bs[k1] if k1 < len(bs) else 0.0
        if R + EPS < k1 * (1.0 - p):
            break
        k = k1
    if k == 0:
        return np.array([], int), np.array([]), np.array([]), R
    p = bs[k] if k < len(bs) else 0.0
    venc = cand[ordem[:k]]
    lv = np.minimum(livre[venc], p)
    em = p - lv
    R = R + lv.sum() - (1.0 - em).sum()
    return venc, lv, em, R


def regra_M0_limitada(R, cand, livre, emb, max_venc=None):
    """Pay-as-bid com teto opcional de vencedores (usado nos testes de leilão)."""
    if max_venc is None:
        return regra_M0(R, cand, livre, emb)
    b = livre[cand] + emb[cand]
    top = cand[np.argsort(-b, kind="stable")[: int(max_venc)]]
    return regra_M0(R, top, livre, emb)


# ---------------------------------------------------------------- sorteio

@dataclass(frozen=True)
class SorteioPonderado:
    """Sorteio com peso omega para a cota excluída e 1 para a ativa.

    Diferente do peso pela espera — que num grupo fechado é igual para todas
    as não contempladas e reproduz o sorteio uniforme (ESTADO §3, 15/11) —, a
    situação da cota separa as elegíveis mesmo no grupo fechado sempre que há
    exclusão. Não é manipulável (ser excluído custa a carta) e atua na margem
    que pesa nos dados: a maior parte dos sorteios vai a excluídos (§5 item 22).
    beta_espera > 0 acrescenta peso (1 + meses desde a entrada)^beta, que só
    distingue cotas em grupo aberto (recolocação); padrão 0.
    """
    omega: float = 0.5
    beta_espera: float = 0.0

    def pesos(self, elig, cotas, t):
        w = np.where(cotas.sit[elig] == EXCLUIDA, self.omega, 1.0)
        if self.beta_espera:
            w = w * (1.0 + t - cotas.entrada[elig]) ** self.beta_espera
        return w

    def __call__(self, rng, elig, cotas, t):
        w = self.pesos(elig, cotas, t)
        s = w.sum()
        if s <= 0:
            return None
        k = int(np.searchsorted(np.cumsum(w), rng.random() * s, side="right"))
        return elig[min(k, len(elig) - 1)]


# ---------------------------------------------------------------- mecanismos

@dataclass(frozen=True)
class Mecanismo:
    nome: str
    lance: Callable = regra_M0
    sorteio: Callable | None = None   # None = uniforme (rng.choice), como no protótipo


OMEGA_M1 = 0.5   # valor de referência; a comparação varre omega (passo 4)

M0 = Mecanismo("M0")
M1 = Mecanismo("M1", regra_M0, SorteioPonderado(OMEGA_M1))
M2 = Mecanismo("M2", regra_M2)
MECANISMOS = {"M0": M0, "M1": M1, "M2": M2}


def m1(omega: float, beta_espera: float = 0.0) -> Mecanismo:
    return Mecanismo(f"M1(omega={omega:g})", regra_M0, SorteioPonderado(omega, beta_espera))
