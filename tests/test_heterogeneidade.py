"""Verificação do passo 1 (15/11): kappa contratual, lance embutido, exclusão por
idade com recolocação, sorteio da sobra, horizonte e simulação no grão do painel."""
import numpy as np
import pytest

from src.sim.grupo import Parametros, simula
from src.sim import painel

SEM_LANCE = dict(phi0=0, phi1=0, phi2=0)


def test_kappa_vagas_de_sorteio_por_assembleia():
    # N = 2T, kappa = 2, sem lance e sem exclusão: duas contemplações por mês e todos até T.
    par = Parametros(N=200, T=100, vagas_sorteio=2, **SEM_LANCE)
    r = simula(par, seed=2)
    assert (r.contempl_sorteio == 2).all() and r.contempl_lance.sum() == 0
    assert not np.isnan(r.espera).any()


def test_sorteio_da_sobra_preenche_vagas_sem_lance():
    # kappa = 1 mas há recurso para duas cartas por mês: a sobra vai a sorteio.
    par = Parametros(N=200, T=100, vagas_sorteio=1, sorteio_sobra=True, **SEM_LANCE)
    r = simula(par, seed=2)
    assert (r.contempl_sorteio == 2).all()
    sem = simula(Parametros(N=200, T=100, vagas_sorteio=1, **SEM_LANCE), seed=2)
    assert sem.contempl_sorteio[:50].sum() == 50


def test_lance_embutido_sem_liquidez():
    # Sem liquidez (lam_max = 0), só há lance embutido: contempla por lance sem
    # entrar dinheiro de lance no fundo, e o crédito entregue é 1 - embutido.
    par = Parametros(N=400, T=100, lam_max=0.0, emb_max=0.3, phi0=0.3, phi1=0, phi2=0)
    r = simula(par, seed=5)
    assert r.contempl_lance.sum() > 0
    assert r.lances_pagos == 0 and r.lances_embutidos > 0
    assert abs(r.entradas - r.saidas - r.saldo_final) < 1e-9


def test_embutido_respeita_teto_e_aumenta_contemplacao_por_lance():
    base = dict(N=600, T=200, h=0.005, lam_max=0.05, phi0=0.3)
    f = []
    for e in (0.0, 0.1, 0.3):
        r = simula(Parametros(emb_max=e, **base), seed=8)
        if r.contempl_lance.sum():
            assert r.lances_embutidos / r.contempl_lance.sum() <= e + 1e-12
        f.append(r.contempl_lance.sum())
    assert f[0] <= f[1] <= f[2]


def test_conservacao_com_embutido_e_recolocacao():
    par = Parametros(N=500, T=150, emb_max=0.25, h_idade=((0.2, 0.5, 10), (0.03, 0.01, 0.002)), rho=1.0)
    for s in range(3):
        r = simula(par, seed=s)
        assert abs(r.entradas - r.saidas - r.saldo_final) < 1e-8
        assert (r.saldo >= -1e-9).all()


def test_recolocacao_mantem_cotas_pagantes():
    # Sem lance, com rho = 1, as vagas excluídas voltam a pagar no mês seguinte:
    # o número de cotas pagantes fica em N enquanto ninguém quitou.
    par = Parametros(N=300, T=200, h=0.03, rho=1.0, **SEM_LANCE)
    r = simula(par, seed=9)
    assert (r.ativas[:30] == 300).all()
    sem = simula(Parametros(N=300, T=200, h=0.03, rho=0.0, **SEM_LANCE), seed=9)
    assert sem.ativas[29] < 300
    assert r.extra["cotas_total"] > 300


def test_risco_por_idade():
    par = Parametros(T=100, h_idade=((0.1, 0.5, 10), (0.04, 0.01, 0.001)))
    assert par.risco(0) == 0.04 and par.risco(9) == 0.04
    assert par.risco(10) == 0.01 and par.risco(49) == 0.01
    assert par.risco(50) == 0.001 and par.risco(99) == 0.001


def test_horizonte_e_prefixo_da_simulacao_completa():
    par = Parametros(N=400, T=150, h=0.01, rho=1.0, emb_max=0.2)
    cheio, curto = simula(par, seed=4), simula(par, seed=4, horizonte=60)
    assert np.array_equal(cheio.contempl_lance[:60], curto.contempl_lance[:60])
    assert np.array_equal(cheio.contempl_sorteio[:60], curto.contempl_sorteio[:60])
    assert np.array_equal(cheio.ativas[:60], curto.ativas[:60])


def test_pesos_kappa():
    w = painel.pesos_kappa(0.5)
    assert np.isclose(w.sum(), 1) and (w > 0).all() and w[0] > w[1] > w[2]
    assert np.isclose(painel.pesos_kappa(0.0)[0], 1.0)


def test_mistura_igual_a_kappa_unico_quando_nu_zero(painel_a, painel_b):
    des = painel.monta_desenho(painel_a, painel_b, grupos_por_adm=1, seed=0)
    base = Parametros(h=0.01, rho=1.0)
    sims = painel.simula_desenho(des, base, kappas=(1, 2), forma="kappa")
    m_mix = painel.momentos_calibracao(des, sims, 0.0, forma="kappa")
    m_um = painel.momentos_calibracao(des, {1: sims[1]}, 0.0, forma="kappa")
    for k in m_mix:
        assert np.isclose(m_mix[k], m_um[k], atol=1e-6)


def test_parametros_fixos(painel_a):
    f = painel.parametros_fixos(painel_a).set_index("parametro")["valor"]
    h = f[[c for c in f.index if c.startswith("h_faixa")]].values
    assert len(h) == len(painel.CORTES_IDADE) and (h >= 0).all()
    assert 0 <= f["rho"] <= 1


def test_pesos_fracao_e_vagas():
    w = painel.pesos_fracao(0.7, 0.3)
    assert np.isclose(w.sum(), 1) and (w >= 0).all()
    assert painel.GRADE_S[int(np.argmax(w))] in (0.55, 0.7, 0.85)
    # vagas proporcionais à capacidade ordinária, com piso de uma vaga
    assert painel.vagas("fracao", 0.5, 800, 200) == 2.0
    assert painel.vagas("fracao", 0.1, 200, 200) == 1.0
    assert painel.vagas("kappa", 3, 800, 200) == 3.0


def test_vagas_nao_inteiras_media_por_assembleia():
    # kappa = 1,5 sem lance e com recurso de sobra: média de 1,5 sorteio por mês.
    par = Parametros(N=600, T=200, vagas_sorteio=1.5, **SEM_LANCE)
    r = simula(par, seed=1, horizonte=150)
    assert abs(r.contempl_sorteio[:150].mean() - 1.5) < 0.15


def test_inadimplencia_antes_da_exclusao():
    # Risco só na 1ª assembleia; com atraso de 3 vencimentos, a exclusão (e a
    # recolocação) só aparece no fim da 4ª assembleia. Inadimplentes contam
    # entre as ativas, mas não pagam.
    par = Parametros(N=300, T=100, h_idade=((0.01, 10), (0.5, 0.0)), rho=1.0, atraso_exclusao=3, **SEM_LANCE)
    assert simula(par, seed=3, horizonte=3).extra["cotas_total"] == 300
    r = simula(par, seed=3, horizonte=4)
    assert r.extra["cotas_total"] > 300
    assert (r.ativas[:4] == 300).all()
    pagou = simula(Parametros(N=300, T=100, **SEM_LANCE), seed=3, horizonte=4).entradas
    assert r.entradas < pagou


def test_conservacao_com_inadimplencia():
    par = Parametros(N=500, T=150, emb_max=0.25, h_idade=((0.2, 0.5, 10), (0.03, 0.01, 0.002)),
                     rho=1.0, atraso_exclusao=3, vagas_sorteio=2.4)
    for s in range(3):
        r = simula(par, seed=s)
        assert abs(r.entradas - r.saidas - r.saldo_final) < 1e-8
        assert (r.saldo >= -1e-9).all()
