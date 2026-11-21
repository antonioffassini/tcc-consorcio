"""Verificação do passo 3 (16/11): momentos de dados e bootstrap, momentos simulados
por mistura, superfície interpolada e função objetivo do SMM."""
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from src.analysis import calibracao as cal
from src.sim import painel
from src.sim.grupo import Parametros


@pytest.fixture(scope="module")
def dados(painel_a, painel_b):
    return cal.Dados(painel_a, painel_b)


def test_momentos_de_dados_iguais_aos_de_fatos_momentos(dados):
    ref = pd.read_csv(Path(__file__).resolve().parent.parent / "results" / "fatos_momentos.csv").set_index("nome")["valor"]
    m = dados.momentos()
    for k in cal.CAL + cal.TES:
        assert abs(m[k] - ref[k]) < 1e-4, k


def test_bootstrap_com_todas_as_administradoras_uma_vez_reproduz_a_amostra(dados):
    m0, m1 = dados.momentos(), dados.momentos(np.ones(len(dados.adms), int))
    for k in m0:
        assert np.isclose(m0[k], m1[k], atol=1e-9), k


def test_bootstrap_reproduzivel_e_com_variancia(dados):
    b1, b2 = dados.bootstrap(20, 7), dados.bootstrap(20, 7)
    assert b1.equals(b2)
    assert (b1[cal.CAL].std() > 0).all()


@pytest.fixture(scope="module")
def pequeno(painel_a, painel_b):
    des = painel.monta_desenho(painel_a, painel_b, grupos_por_adm=1, seed=0)
    base = Parametros(h=0.01, rho=1.0, atraso_exclusao=3, emb_max=0.25)
    sup = cal.Superficie("phi0", [0.0, 0.2], [des], base, processos=1, log=lambda s: None)
    return des, base, sup


def test_mistura_igual_a_painel_momentos_calibracao(pequeno):
    des, base, sup = pequeno
    sims = painel.simula_desenho(des, replace(base, phi0=0.0), forma="fracao")
    ref = painel.momentos_calibracao(des, sims, (0.7, 0.3), forma="fracao")
    bl = sup.blocos[0][0]
    m = cal.momentos_mistura(bl.F, bl.TX, sup.pesos_gm[0], 0.7, 0.3)
    for k in cal.CAL:
        assert np.isclose(m[k], ref[k], atol=1e-9), k


def test_interpolacao_exata_nos_pontos_e_linear_no_meio(pequeno):
    _, _, sup = pequeno
    F0, TX0, _, _ = sup.interpola(0.0)
    F1, TX1, _, _ = sup.interpola(0.2)
    Fm, TXm, _, _ = sup.interpola(0.1)
    assert np.allclose(F0, sup.blocos[0][0].F, equal_nan=True)
    assert np.allclose(F1, sup.blocos[0][1].F, equal_nan=True)
    def meio(a, b):   # média; se um extremo é NaN, vale o outro (NaN não se propaga)
        return np.where(np.isnan(a), b, np.where(np.isnan(b), a, (a + b) / 2))
    assert np.allclose(Fm, meio(F0, F1), equal_nan=True)
    assert np.allclose(TXm, meio(TX0, TX1), equal_nan=True)


def test_objetivo_nulo_no_proprio_momento_simulado(pequeno):
    _, _, sup = pequeno
    obj = cal.Objetivo(sup, dict(zip(cal.CAL, [0.7, 0.1, 0.005])), np.eye(3))
    th = (0.1, 0.6, 0.3)
    m = obj.momentos(th)
    assert obj.Q(th, mu=m) < 1e-20
    assert obj.Q((0.9, 0.6, 0.3)) == 1e12   # fora dos limites


def test_momentos_teste_com_um_unico_nivel(pequeno):
    des, _, sup = pequeno
    bl = sup.blocos[0][0]
    k = painel.GRADE_S.index(0.7)
    r = cal.momentos_teste(bl.F, bl.Z, sup.pesos_gm[0], sup.alvo, des.adms, 0.7, 1e-6, n_sorteios=5)
    f = bl.F[k]; ok = ~np.isnan(f)
    assert np.isclose(r["spearman_lance_tamanho"], stats.spearmanr(f[ok], sup.alvo["tam_med"].values[ok]).statistic)
    z = bl.Z[k]; m = ~np.isnan(z)
    assert np.isclose(r["frac_sem_contempl"], np.average(z[m], weights=sup.pesos_gm[0][m]))
