"""Verificação do passo 2 (16/11): M1 (sorteio ponderado pela situação da cota)
e M2 (lance de preço uniforme), como estratégias trocáveis.

Leilão único com valores i.i.d. U[0,1] e n participantes: no equilíbrio do
leilão de primeiro preço cada um oferta (n-1)/n do valor; no de segundo preço,
ofertar o valor é estratégia dominante; as duas receitas esperadas valem
(n-1)/(n+1) (equivalência de receita). M0 com teto de um vencedor é o leilão
de primeiro preço; M2 com teto de um vencedor, o de segundo preço.
"""
from types import SimpleNamespace

import numpy as np
import pytest

from src.sim.grupo import ATIVA, EXCLUIDA, Parametros, simula
from src.sim.regras import (M0, M1, M2, MECANISMOS, SorteioPonderado, m1, regra_M0_limitada, regra_M2)

R_FOLGA = 50.0


def _leilao(regra, b, R=R_FOLGA, max_venc=None, emb=None):
    n = len(b)
    cand = np.arange(n)
    livre = np.asarray(b, float).copy()
    e = np.zeros(n) if emb is None else np.asarray(emb, float)
    return regra(R, cand, livre, e, max_venc=max_venc)


def test_leilao_unico_M0_paga_o_proprio_lance_e_M2_o_segundo():
    b = [0.30, 0.55, 0.10, 0.42]
    v0, lv0, _, _ = _leilao(regra_M0_limitada, b, max_venc=1)
    v2, lv2, _, _ = _leilao(regra_M2, b, max_venc=1)
    assert list(v0) == [1] and list(v2) == [1]
    assert np.isclose(lv0[0], 0.55) and np.isclose(lv2[0], 0.42)


@pytest.mark.parametrize("n", [2, 5])
def test_equivalencia_de_receita_no_leilao_unico(n):
    rng = np.random.default_rng(11)
    M = 20000
    r0 = r2 = 0.0
    for _ in range(M):
        v = rng.random(n)
        r0 += _leilao(regra_M0_limitada, (n - 1) / n * v, max_venc=1)[1].sum()   # equilíbrio de 1º preço
        r2 += _leilao(regra_M2, v, max_venc=1)[1].sum()                          # verdade no de 2º preço
    alvo = (n - 1) / (n + 1)
    assert abs(r0 / M - alvo) < 0.01
    assert abs(r2 / M - alvo) < 0.01


def test_lance_de_equilibrio_do_primeiro_preco_e_melhor_resposta():
    # Contra rivais que ofertam (n-1)/n do valor, o lance (n-1)/n * v maximiza
    # o ganho esperado (v - b) P(vencer) na grade, com os vencedores apurados por M0.
    n, v = 4, 0.8
    rng = np.random.default_rng(3)
    rivais = (n - 1) / n * rng.random((6000, n - 1))
    grade = np.round(np.arange(0.40, 0.801, 0.05), 2)
    ganho = []
    for b in grade:
        vence = 0
        for r in rivais[:1500]:
            venc = _leilao(regra_M0_limitada, np.concatenate([[b], r]), max_venc=1)[0]
            vence += int(len(venc) and venc[0] == 0)
        ganho.append((v - b) * vence / 1500)
    # o ganho analítico (v-b)(bn/(n-1))^(n-1) tem máximo em 0,6; a curva simulada
    # deve ter o máximo a no máximo um passo da grade
    assert abs(grade[int(np.argmax(ganho))] - (n - 1) / n * v) <= 0.05 + 1e-9


def test_M2_ofertar_o_valor_e_dominante_no_leilao_unico():
    rng = np.random.default_rng(5)
    for _ in range(300):
        v = rng.random(4)
        outros = rng.random(3)
        for i_v in v:
            def util(b):
                venc, lv, _, _ = _leilao(regra_M2, np.concatenate([[b], outros]), max_venc=1)
                return (i_v - lv[0]) if len(venc) and venc[0] == 0 else 0.0
            u_verdade = util(i_v)
            for d in np.linspace(0, 1, 11):
                assert u_verdade >= util(d) - 1e-12


def test_M2_multiunidade_paga_o_primeiro_lance_recusado():
    b = np.array([0.9, 0.2, 0.7, 0.5, 0.3])
    venc, lv, em, R = _leilao(regra_M2, b, R=3.0)
    # k=1: 1*(1-0.7)=0.3; k=2: 2*(1-0.5)=1.0; k=3: 3*(1-0.3)=2.1; k=4: 4*(1-0.2)=3.2 > 3
    assert sorted(venc) == [0, 2, 3]
    assert np.allclose(lv + em, 0.3)
    assert np.isclose(R, 3.0 - 3 * (1 - 0.3))


def test_M2_contempla_no_maximo_quanto_M0_e_os_mesmos_primeiros():
    rng = np.random.default_rng(8)
    for _ in range(500):
        n = rng.integers(2, 30)
        b = rng.random(n) * 0.6
        R = rng.random() * 6
        v0, _, _, R0 = _leilao(regra_M0_limitada, b, R=R)
        v2, _, _, R2 = _leilao(regra_M2, b, R=R)
        assert len(v2) <= len(v0)
        assert list(v2) == list(v0[: len(v2)])
        assert R2 >= -1e-9 and R0 >= -1e-9


def test_M2_divide_o_preco_entre_livre_e_embutido():
    livre = np.array([0.05, 0.40, 0.10])
    emb = np.array([0.25, 0.00, 0.25])          # lances totais 0,30; 0,40; 0,35
    venc, lv, em, _ = regra_M2(R_FOLGA, np.arange(3), livre, emb, max_venc=2)
    # vencem 1 e 2; preço = 0,30. A cota 2 paga 0,10 livre e 0,20 embutido.
    assert sorted(venc) == [1, 2]
    d = dict(zip(venc, zip(lv, em)))
    assert np.allclose(d[1], (0.30, 0.0)) and np.allclose(d[2], (0.10, 0.20))
    assert (lv <= livre[venc] + 1e-12).all() and (em <= emb[venc] + 1e-12).all()


def _cotas(n_ativas, n_excl):
    sit = np.array([ATIVA] * n_ativas + [EXCLUIDA] * n_excl)
    return SimpleNamespace(sit=sit, entrada=np.zeros(len(sit), int))


def test_M1_frequencia_dos_excluidos_segue_omega():
    c = _cotas(30, 70)
    elig = np.arange(100)
    rng = np.random.default_rng(1)
    s = SorteioPonderado(0.5)
    sai = np.array([s(rng, elig, c, 0) for _ in range(20000)])
    p_excl = (c.sit[sai] == EXCLUIDA).mean()
    assert abs(p_excl - 35 / 65) < 0.015


def test_M1_casos_limite():
    c = _cotas(5, 5)
    elig = np.arange(10)
    assert np.allclose(SorteioPonderado(1.0).pesos(elig, c, 0), 1.0)
    rng = np.random.default_rng(2)
    assert all(c.sit[SorteioPonderado(0.0)(rng, elig, c, 0)] == ATIVA for _ in range(500))
    assert SorteioPonderado(0.0)(rng, np.arange(5, 10), c, 0) is None


def test_M1_nao_e_trivial_no_grupo_fechado():
    # Grupo fechado (rho = 0), com exclusão: com omega = 0 nenhum excluído é
    # restituído antes do encerramento, e a espera das ativas cai em relação a M0.
    par = Parametros(N=400, T=150, h=0.01, rho=0.0)
    e0, e1 = [], []
    for s in range(6):
        r0, r1 = simula(par, seed=s, mecanismo=M0), simula(par, seed=s, mecanismo=m1(0.0))
        assert r1.restituicoes.sum() == 0 and r0.restituicoes.sum() > 0
        e0.append(np.nanmean(r0.espera)); e1.append(np.nanmean(r1.espera))
    assert np.mean(e1) < np.mean(e0)


@pytest.mark.parametrize("mec", [M0, M1, M2])
def test_conservacao_por_mecanismo(mec):
    par = Parametros(N=500, T=150, emb_max=0.25, h_idade=((0.2, 0.5, 10), (0.03, 0.01, 0.002)),
                     rho=1.0, atraso_exclusao=3, vagas_sorteio=1.7)
    for s in range(3):
        r = simula(par, seed=s, mecanismo=mec)
        assert abs(r.entradas - r.saidas - r.saldo_final) < 1e-8
        assert (r.saldo >= -1e-9).all()


def test_M0_por_mecanismo_igual_ao_padrao():
    par = Parametros(N=300, T=120, h=0.01, rho=1.0, emb_max=0.2)
    a, b = simula(par, seed=4), simula(par, seed=4, mecanismo=M0)
    assert np.array_equal(a.contempl_lance, b.contempl_lance)
    assert np.array_equal(a.contempl_sorteio, b.contempl_sorteio)


def test_registro():
    assert set(MECANISMOS) == {"M0", "M1", "M2"}
    assert MECANISMOS["M2"].lance is regra_M2
