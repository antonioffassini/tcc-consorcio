"""Simulador de um grupo de consórcio (etapa 4).

Unidades: crédito C = 1; sem taxa de administração e fundo de reserva
(CONTEXT §4). Dinâmica mensal (Res. BCB 285/2023, arts. 12 e 13; ESTADO §5):

  1. arrecadação: cada cota não excluída com saldo devedor paga a parcela
     fixa 1/(T - entrada), limitada ao saldo; o lance amortiza as últimas
     parcelas e encurta o prazo da cota, sem mudar a parcela (art. 12,
     parágrafo único: "forma prevista no contrato" — escolha do modelo);
  2. sorteio das kappa vagas previstas no contrato (art. 2º, XII; precedência,
     art. 12, I), entre cotas ativas não contempladas e excluídas não
     restituídas; excluída sorteada recebe a restituição do que pagou;
  3. lance sobre o saldo residual, com a regra de contemplação trocável
     (`regra`); o lance tem parte livre (limitada pela liquidez lambda_i) e
     parte embutida (limitada por emb_max, art. 13); vence quem oferta maior
     percentual do crédito, enquanto houver recurso (R >= 1 - b);
  4. sorteio da sobra (opcional, sensibilidade): se após o lance ainda
     houver recurso para um crédito, novas vagas vão a sorteio;
  5. inadimplência e exclusão: cota ativa não contemplada deixa de pagar com
     risco h(idade); fica inadimplente (conta entre as ativas, como no Bacen,
     mas não paga nem concorre, art. 11, § 1º) e é excluída depois de
     `atraso_exclusao` vencimentos sem pagamento (art. 32, II: três); com
     probabilidade rho a vaga excluída é recolocada para um novo participante,
     que assume saldo devedor 1 (ESTADO §5 item 20). Com atraso 0, a exclusão
     é imediata, como no protótipo.

Os excluídos continuam concorrendo no sorteio (ESTADO §5 item 5). No
encerramento, os excluídos remanescentes são restituídos com o saldo.

Compatibilidade: com os valores padrão (kappa = 1, emb_max = 0, rho = 0,
h constante, sem sorteio da sobra) a dinâmica é a do protótipo de 26/10.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

ATIVA, CONTEMPLADA, EXCLUIDA, RESTITUIDA, INADIMPLENTE = 0, 1, 2, 3, 4
EPS = 1e-9


@dataclass
class Parametros:
    N: int = 600            # cotas na formação do grupo
    T: int = 200            # prazo (assembleias)
    vagas_sorteio: float = 1  # kappa: vagas de sorteio previstas por assembleia (contrato);
                              # valor não inteiro = arredondamento aleatório a cada assembleia
    h: float = 0.0          # risco mensal de exclusão, se h_idade for None
    h_idade: tuple | None = None  # ((cortes em t/T), (taxas por faixa)): risco por idade
    rho: float = 0.0        # probabilidade de recolocação da vaga excluída
    atraso_exclusao: int = 0  # vencimentos sem pagamento até a exclusão (0 = imediata)
    # tipos: urgência theta ~ lognormal; liquidez lambda ~ Beta * lam_max (fração de C)
    mu_theta: float = 0.0
    sd_theta: float = 0.5
    a_lam: float = 2.0
    b_lam: float = 5.0
    lam_max: float = 0.6
    # política de lance: b* = max(0, phi0 + phi1*theta + phi2*restante)
    phi0: float = 0.10
    phi1: float = 0.10
    phi2: float = -0.10
    emb_max: float = 0.0    # teto do lance embutido, fração do crédito (art. 13)
    sorteio_sobra: bool = False
    # sorteio de excluídas (ESTADO §4, 19/11): "comum" = mesmo sorteio das ativas (tipo Sicredi,
    # protótipo); "separado" = depois do sorteio das ativas, com vagas_excluidos restituições
    # garantidas (havendo saldo) e outras enquanto a soma restituída na assembleia <= teto_restituicao
    sorteio_excluidos: str = "comum"
    vagas_excluidos: int = 1
    teto_restituicao: float = 0.0

    def risco(self, t: int) -> float:
        if self.h_idade is None:
            return self.h
        cortes, taxas = self.h_idade
        k = int(np.searchsorted(np.asarray(cortes), (t + 1) / self.T, side="left"))
        return float(taxas[min(k, len(taxas) - 1)])


@dataclass
class Resultado:
    contempl_sorteio: np.ndarray
    contempl_lance: np.ndarray
    restituicoes: np.ndarray
    ativas: np.ndarray
    saldo: np.ndarray
    espera: np.ndarray           # meses entre a entrada e a contemplação (nan se não contemplado)
    entradas: float
    saidas: float
    saldo_final: float
    lances_pagos: float = 0.0    # parte livre dos lances vencedores
    lances_embutidos: float = 0.0
    extra: dict = field(default_factory=dict)


def lance_politica(par: Parametros, theta, lam, restante, devedor=None):
    """Lance desejado b* e sua divisão em parte livre e parte embutida.

    Retorna (livre, embutido). A parte livre vem primeiro, até a liquidez;
    o embutido cobre o restante até emb_max. Nenhuma das partes passa do
    saldo devedor.
    """
    alvo = np.clip(par.phi0 + par.phi1 * theta + par.phi2 * restante, 0.0, None)
    teto = np.inf if devedor is None else devedor
    livre = np.minimum(np.minimum(alvo, lam), teto)
    emb = np.minimum(np.minimum(alvo - livre, par.emb_max), teto - livre)
    return livre, np.clip(emb, 0.0, None)


def regra_M0(R, cand, livre, emb):
    """Lance pay-as-bid sobre o saldo residual (mecanismo vigente).

    Ordena por percentual total ofertado (livre + embutido). O vencedor
    recebe 1 - embutido e paga a parte livre; a contemplação exige
    R + livre >= 1 - embutido, isto é, R >= 1 - b. Como a condição só
    depende de b, o primeiro lance inviável encerra a assembleia.
    Retorna (vencedores, livre_pago, embutido_usado, R).
    """
    b = livre[cand] + emb[cand]
    ordem = np.argsort(-b, kind="stable")
    venc = []
    for k in ordem:
        if b[k] <= 0 or R + b[k] < 1.0 - EPS:
            break
        i = cand[k]
        R += livre[i] - (1.0 - emb[i])
        venc.append(i)
    venc = np.array(venc, dtype=int)
    return venc, livre[venc], emb[venc], R


class _Cotas:
    """Arrays das cotas com capacidade crescente (recolocação cria cotas novas)."""

    def __init__(self, n, cap):
        self.n = n
        self.sit = np.full(cap, ATIVA)
        self.devedor = np.zeros(cap)
        self.devedor[:n] = 1.0
        self.pago = np.zeros(cap)
        self.entrada = np.zeros(cap, int)
        self.espera = np.full(cap, np.nan)
        self.theta = np.zeros(cap)
        self.lam = np.zeros(cap)
        self.parcela = np.zeros(cap)
        self.inad = np.full(cap, -1)
        self.t_excl = np.full(cap, -1)      # assembleia da exclusão
        self.t_rest = np.full(cap, -1)      # assembleia da restituição
        self.livre = np.zeros(cap)          # lance livre pago na contemplação
        self.emb = np.zeros(cap)            # lance embutido usado na contemplação
        self.t_cont = np.full(cap, -1)      # assembleia da contemplação

    def cresce(self, extra):
        if self.n + extra <= len(self.sit):
            return
        cap = max(2 * len(self.sit), self.n + extra)
        for nome, fill in [("sit", ATIVA), ("devedor", 0.0), ("pago", 0.0), ("entrada", 0),
                           ("espera", np.nan), ("theta", 0.0), ("lam", 0.0), ("parcela", 0.0), ("inad", -1), ("t_excl", -1), ("t_rest", -1),
                           ("livre", 0.0), ("emb", 0.0), ("t_cont", -1)]:
            v = getattr(self, nome)
            novo = np.full(cap, fill, dtype=v.dtype)
            novo[: len(v)] = v
            setattr(self, nome, novo)


def simula(par: Parametros, seed: int = 0, regra=regra_M0, sorteio=None,
           horizonte: int | None = None, mecanismo=None) -> Resultado:
    """Simula um grupo do início ao encerramento (ou até `horizonte` assembleias).

    `regra` decide o lance; `sorteio`, se dado, escolhe a cota sorteada entre
    as elegíveis: sorteio(rng, elig, cotas, t) -> índice (ou None). Padrão: uniforme.
    `mecanismo` (src/sim/regras.py), se dado, substitui `regra` e `sorteio`.
    """
    if mecanismo is not None:
        regra, sorteio = mecanismo.lance, mecanismo.sorteio
    rng = np.random.default_rng(seed)
    N, T = par.N, par.T
    c = _Cotas(N, cap=2 * N + 16)
    c.theta[:N] = rng.lognormal(par.mu_theta, par.sd_theta, N)
    c.lam[:N] = rng.beta(par.a_lam, par.b_lam, N) * par.lam_max
    c.parcela[:N] = 1.0 / T
    R = entradas = saidas = lances_pagos = lances_emb = 0.0
    cs, cl, rs, at, sd = (np.zeros(T, int), np.zeros(T, int), np.zeros(T, int),
                          np.zeros(T, int), np.zeros(T))
    falha = np.zeros(T, int)

    def sorteia_um(t, pool="comum", limite=np.inf):
        """Uma extração. pool: 'comum' (ativas e excluídas), 'ativas' ou 'excluidas'.
        A regra de sorteio do mecanismo vale para 'comum' e 'ativas'; excluídas entre si
        são sorteadas de modo uniforme. Retorna False se não houve contemplação/restituição
        (sem elegível, saldo insuficiente ou custo acima de `limite`)."""
        nonlocal R, saidas
        sit = c.sit[: c.n]
        if pool == "ativas":
            elig = np.flatnonzero(sit == ATIVA)
        elif pool == "excluidas":
            elig = np.flatnonzero(sit == EXCLUIDA)
        else:
            elig = np.flatnonzero((sit == ATIVA) | (sit == EXCLUIDA))
        if len(elig) == 0:
            return False
        if pool == "excluidas" or sorteio is None:
            i = rng.choice(elig)
        else:
            i = sorteio(rng, elig, c, t)
        if i is None:
            return False
        i = int(i)
        custo = 1.0 if c.sit[i] == ATIVA else c.pago[i]
        if R + EPS < custo or custo > limite + EPS:
            return False
        R -= custo; saidas += custo
        if c.sit[i] == ATIVA:
            c.sit[i] = CONTEMPLADA; c.espera[i] = t + 1 - c.entrada[i]; cs[t] += 1; c.t_cont[i] = t
        else:
            c.sit[i] = RESTITUIDA; rs[t] += 1; c.t_rest[i] = t
        return True

    H = T if horizonte is None else min(T, int(horizonte))
    for t in range(H):
        n = c.n
        sit, dev = c.sit[:n], c.devedor[:n]
        # 1. arrecadação
        pagam = ((sit == ATIVA) | (sit == CONTEMPLADA)) & (dev > EPS)
        at[t] = int(pagam.sum() + (sit == INADIMPLENTE).sum())
        parc = np.where(pagam, np.minimum(c.parcela[:n], dev), 0.0)
        dev -= parc; c.pago[:n] += parc
        R += parc.sum(); entradas += parc.sum()
        # 2. sorteio (precedência)
        kap = int(par.vagas_sorteio)
        resto = par.vagas_sorteio - kap
        if resto > 1e-12 and rng.random() < resto:
            kap += 1
        separado = par.sorteio_excluidos == "separado"
        if kap and R + EPS < 1.0 and (c.sit[: c.n] == ATIVA).any():
            falha[t] = 1     # sorteio previsto não realizado por falta de saldo
        for _ in range(kap):
            if not sorteia_um(t, "ativas" if separado else "comum"):
                break
        if separado:
            restituido, k = 0.0, 0
            while True:
                lim = np.inf if k < par.vagas_excluidos else par.teto_restituicao - restituido
                r0 = R
                if not sorteia_um(t, "excluidas", lim):
                    break
                restituido += r0 - R; k += 1
        # 3. lance com o saldo residual
        cand = np.flatnonzero((sit == ATIVA) & (dev > EPS))
        if len(cand):
            livre, emb = np.zeros(n), np.zeros(n)
            livre[cand], emb[cand] = lance_politica(par, c.theta[cand], c.lam[cand], (T - t) / T, dev[cand])
            venc, lv, em, R_novo = regra(R, cand, livre, emb)
            if len(venc):
                entradas += lv.sum(); saidas += (1.0 - em).sum()
                lances_pagos += lv.sum(); lances_emb += em.sum()
                dev[venc] -= lv + em; c.pago[venc] += lv
                R = R_novo
                sit[venc] = CONTEMPLADA; c.espera[venc] = t + 1 - c.entrada[venc]; cl[t] += len(venc)
                c.t_cont[venc] = t; c.livre[venc] = lv; c.emb[venc] = em
        # 4. sorteio da sobra (sensibilidade)
        if par.sorteio_sobra:
            while R + EPS >= 1.0 and sorteia_um(t, "ativas" if separado else "comum"):
                pass
        # 5. inadimplência, exclusão e recolocação
        def recoloca(sai):
            if par.rho <= 0 or not len(sai):
                return
            k = int((rng.random(len(sai)) < par.rho).sum())
            if k:
                c.cresce(k)
                j = slice(c.n, c.n + k)
                c.sit[j] = ATIVA; c.devedor[j] = 1.0; c.pago[j] = 0.0
                c.entrada[j] = t + 1; c.espera[j] = np.nan; c.inad[j] = -1
                c.parcela[j] = 1.0 / (T - t - 1)
                c.theta[j] = rng.lognormal(par.mu_theta, par.sd_theta, k)
                c.lam[j] = rng.beta(par.a_lam, par.b_lam, k) * par.lam_max
                c.n += k

        if par.atraso_exclusao > 0:
            vence = np.flatnonzero((sit == INADIMPLENTE) & (t - c.inad[:n] >= par.atraso_exclusao))
            sit[vence] = EXCLUIDA; c.t_excl[vence] = t
            if t < T - 1:
                recoloca(vence)
        h = par.risco(t)
        if h > 0 and t < T - 1:
            nc = np.flatnonzero((sit == ATIVA) & (dev > EPS))
            sai = nc[rng.random(len(nc)) < h]
            if par.atraso_exclusao > 0:
                sit[sai] = INADIMPLENTE; c.inad[sai] = t
            else:
                sit[sai] = EXCLUIDA; c.t_excl[sai] = t
                recoloca(sai)
        sd[t] = R
    # encerramento: restitui excluídos (e inadimplentes) remanescentes com o saldo
    for i in [] if H < T else np.flatnonzero((c.sit[: c.n] == EXCLUIDA) | (c.sit[: c.n] == INADIMPLENTE)):
        v = min(c.pago[i], R); R -= v; saidas += v; c.t_rest[i] = T
    res = Resultado(cs, cl, rs, at, sd, c.espera[: c.n].copy(), entradas, saidas, R,
                    lances_pagos, lances_emb)
    res.extra["cotas_total"] = c.n
    n = c.n
    res.extra.update(falha_sorteio=falha, horizonte=H, theta=c.theta[:n].copy(), entrada=c.entrada[:n].copy(),
                     t_cont=c.t_cont[:n].copy(), livre=c.livre[:n].copy(), emb=c.emb[:n].copy(),
                     t_excl=c.t_excl[:n].copy(), t_rest=c.t_rest[:n].copy(), pago=c.pago[:n].copy(),
                     situacao=c.sit[:n].copy())
    return res


def momentos_simulados(res: Resultado, janela: slice | None = None) -> dict:
    """Mesmas fórmulas de src/analysis/momentos.py, aplicadas ao grupo simulado."""
    cs, cl, at = res.contempl_sorteio, res.contempl_lance, res.ativas
    janela = janela or slice(None)
    tot = cs[janela] + cl[janela]
    taxa = tot / np.maximum(at[janela], 1)
    return dict(frac_lance=cl[janela].sum() / max(tot.sum(), 1),
                taxa_contempl_mediana=float(np.median(taxa)),
                frac_sem_contempl=float((tot == 0).mean()))
