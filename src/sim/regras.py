"""Mecanismos de contemplação como estratégias trocáveis (passo 2, 16/11).

Um mecanismo = regra de sorteio + regra de lance; a ordem sorteio → lance e a
restrição de recursos ficam no simulador (`grupo.simula`), iguais para todos.

  M0 — vigente: sorteio uniforme entre ativas não contempladas e excluídas
       não restituídas; lance pay-as-bid (cada vencedor paga o próprio lance).
  M1 — (19/11) sorteio das ativas ponderado pela espera: peso
       (1 + meses desde a entrada)^beta, beta = 1 de referência; lance
       pay-as-bid. Só distingue cotas em grupo aberto (recolocação), que é o
       caso dos dados. Com beta = 0, é M0. A versão de 16/11 (peso omega da
       excluída num sorteio comum) continua disponível em m1(omega, 0), mas
       saiu da comparação: nos contratos, o sorteio de excluídas é separado
       e posterior (ESTADO §5 item 26).
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


@dataclass(frozen=True)
class LanceUniforme:
    """Preço uniforme com preço de reserva p (M3^r, ESTADO §4, 22/11).

    Só concorrem lances b >= p (e b > 0). Com k vencedores, o preço é
    max(b_(k+1), p), em que b_(k+1) é o maior lance elegível recusado (zero se
    não houver). Com p = 0 é exatamente `regra_M2`. O preço não cresce com k,
    então a condição R >= k (1 - preço) é monótona.
    """
    reserva: float = 0.0

    def __call__(self, R, cand, livre, emb, max_venc=None):
        b = livre[cand] + emb[cand]
        ok = (b > 0) & (b >= self.reserva - EPS)
        cand, b = cand[ok], b[ok]
        ordem = np.argsort(-b, kind="stable")
        bs = b[ordem]
        teto = len(bs) if max_venc is None else min(len(bs), int(max_venc))
        preco = lambda k: max(bs[k] if k < len(bs) else 0.0, self.reserva)
        k = 0
        while k < teto:
            if R + EPS < (k + 1) * (1.0 - preco(k + 1)):
                break
            k += 1
        if k == 0:
            return np.array([], int), np.array([]), np.array([]), R
        p = preco(k)
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
    sobra: bool | None = None         # None = cláusula da administradora; True = sorteio da sobra obrigatório (M3^s)


BETA_M1 = 1.0   # valor de referência; o passo 4 varre beta

M0 = Mecanismo("M0")
M1 = Mecanismo("M1", regra_M0, SorteioPonderado(omega=1.0, beta_espera=BETA_M1))
M2 = Mecanismo("M2", regra_M2)
MECANISMOS = {"M0": M0, "M1": M1, "M2": M2}


def m1(omega: float, beta_espera: float = 0.0) -> Mecanismo:
    return Mecanismo(f"M1(omega={omega:g},beta={beta_espera:g})", regra_M0, SorteioPonderado(omega, beta_espera))


def m1_espera(beta: float) -> Mecanismo:
    return Mecanismo(f"M1(beta={beta:g})", regra_M0, SorteioPonderado(1.0, beta))


# ---------------------------------------------------------------- família M3 (ESTADO §4, 22/11)

RESERVAS_M3 = (0.05, 0.10, 0.15, 0.20)
BETAS_M3 = (0.1, 0.25)


@dataclass(frozen=True)
class LancePayAsBidReserva:
    """Pay-as-bid (M0) só com lances >= p: diagnóstico de decomposição do M3 (ESTADO §4, 22/11)."""
    reserva: float = 0.0

    def __call__(self, R, cand, livre, emb, max_venc=None):
        b = livre[cand] + emb[cand]
        return regra_M0(R, cand[b >= self.reserva - EPS], livre, emb)


def m3x(nome: str) -> Mecanismo:
    """Variante pelo nome: M3x_p<reserva>_b<beta>_s<0|1>[_a1] (ESTADO §4, 22/11).
    a1 = lance pay-as-bid (diagnóstico de decomposição); padrão = preço uniforme."""
    partes = dict((x[0], x[1:]) for x in nome.split("_")[1:])
    p, b, s = float(partes.get("p", 0)), float(partes.get("b", 0)), int(partes.get("s", 0))
    lance = LancePayAsBidReserva(p) if partes.get("a") == "1" else LanceUniforme(p)
    return Mecanismo(nome, lance, SorteioPonderado(1.0, b) if b else None, True if s else None)


def familia_m3() -> list[tuple[str, Mecanismo]]:
    """As 11 variantes registradas antes da rodada, todas sobre o lance de preço uniforme."""
    L = [(f"M3r_p{p:g}", Mecanismo(f"M3r(p={p:g})", LanceUniforme(p))) for p in RESERVAS_M3]
    L.append(("M3s", Mecanismo("M3s", regra_M2, None, True)))
    L += [(f"M3rs_p{p:g}", Mecanismo(f"M3rs(p={p:g})", LanceUniforme(p), None, True)) for p in RESERVAS_M3]
    L += [(f"M3e_beta{b:g}", Mecanismo(f"M3e(beta={b:g})", regra_M2, SorteioPonderado(1.0, b))) for b in BETAS_M3]
    return L


# ---------------------------------------------------------------- família M4: lance fixo (ESTADO §4, 23/11)

@dataclass(frozen=True)
class LanceFixo:
    """Lance fixo (preço postado) seguido de lance livre (M4, ESTADO §4, 23/11).

    Prática contratual: Porto Seguro cl. 36.12, Santander 2026 Anexo V, Sicredi cl. 94.3.
    Concorre ao lance fixo quem oferta b >= preco; os vencedores são sorteados
    uniformemente entre eles (o desempate pela Loteria Federal é, para o modelo,
    um sorteio) e cada um paga exatamente `preco`. Até `n` vencedores (None = até
    esgotar o saldo). Quem não vence segue no lance livre `livre` com o mesmo b
    (None = sem lance livre: só preço postado). Saída líquida por vencedor do fixo: 1 - preco.
    """
    preco: float = 0.2
    n: int | None = 1
    livre: Callable | None = None
    usa_rng: bool = True

    def __call__(self, R, cand, livre, emb, max_venc=None, rng=None):
        rng = np.random.default_rng(0) if rng is None else rng
        b = livre[cand] + emb[cand]
        aceita = cand[b >= self.preco - EPS]
        ordem = aceita[rng.permutation(len(aceita))] if len(aceita) else aceita
        teto = len(ordem) if self.n is None else min(len(ordem), self.n)
        k = 0
        while k < teto and R + EPS >= (k + 1) * (1.0 - self.preco):
            k += 1
        vf = ordem[:k]
        lv_f = np.minimum(livre[vf], self.preco)
        em_f = self.preco - lv_f
        R = R + lv_f.sum() - (1.0 - em_f).sum()
        if self.livre is None:
            return vf, lv_f, em_f, R
        resto = np.setdiff1d(cand, vf, assume_unique=True)
        if not len(resto):
            return vf, lv_f, em_f, R
        vl, lv_l, em_l, R = (self.livre(R, resto, livre, emb) if max_venc is None
                             else self.livre(R, resto, livre, emb, max_venc))
        return (np.concatenate([vf, vl]).astype(int), np.concatenate([lv_f, lv_l]),
                np.concatenate([em_f, em_l]), R)


def m4f(nome: str) -> Mecanismo:
    """Variante pelo nome: M4f_p<preço>_n<1|2|all>[_a1] (ESTADO §4, 23/11).

    Padrão: lance livre de preço uniforme com lance mínimo 0,05 e sorteio da sobra
    obrigatório (o M3^rs(0,05) com lance fixo à frente). a1 = lance livre pay-as-bid
    e cláusula da sobra da administradora (a prática de mercado). n = all: só preço
    postado, com sorteio da sobra obrigatório.
    """
    partes = dict((x[0], x[1:]) for x in nome.split("_")[1:])
    p = float(partes["p"]); n = None if partes["n"] == "all" else int(partes["n"])
    if n is None:
        return Mecanismo(nome, LanceFixo(p, None, None), None, True)
    if partes.get("a") == "1":
        return Mecanismo(nome, LanceFixo(p, n, regra_M0), None, None)
    return Mecanismo(nome, LanceFixo(p, n, LanceUniforme(0.05)), None, True)


FAMILIA_M4 = ("M4f_p0.2_n1_a1", "M4f_p0.2_n1", "M4f_p0.2_n2", "M4f_p0.3_n1", "M4f_p0.2_nall", "M4f_p0.3_nall",
              "M3x_p0.05_b0.25_s1", "M3x_p0.05_b1_s1")   # emenda de 23/11 (ESTADO §4): sorteio ponderado pela espera


def resolve(nome: str) -> Mecanismo:
    """Nome -> mecanismo, para M0, M2, variantes M3x e M4f."""
    if nome == "M0":
        return M0
    if nome == "M2":
        return M2
    if nome.startswith("M4f"):
        return m4f(nome)
    return m3x(nome)
