"""Verificação (etapa 5a): o código faz o que o modelo diz em casos de resposta conhecida."""
import numpy as np
from scipy import stats

from src.sim.grupo import Parametros, simula


def test_conservacao_do_dinheiro():
    r = simula(Parametros(N=300, T=100, h=0.01), seed=1)
    assert abs(r.entradas - r.saidas - r.saldo_final) < 1e-9


def test_saldo_nunca_negativo():
    for s in range(5):
        r = simula(Parametros(N=300, T=100, h=0.01, phi0=0.3), seed=s)
        assert (r.saldo >= -1e-9).all()


def test_sem_lance_um_por_mes_e_espera_media_conhecida():
    # N = T, sem lance e sem exclusão: exatamente 1 contemplação por mês, todos até T,
    # e espera média (T+1)/2.
    par = Parametros(N=120, T=120, phi0=0, phi1=0, phi2=0, h=0)
    r = simula(par, seed=3)
    assert (r.contempl_sorteio == 1).all() and r.contempl_lance.sum() == 0
    assert np.isclose(np.nanmean(r.espera), (par.T + 1) / 2)


def test_todos_contemplados_sem_exclusao():
    r = simula(Parametros(N=400, T=100, h=0), seed=4)
    assert not np.isnan(r.espera).any()


def test_sorteio_uniforme():
    # Sem lance, a primeira contemplada tem de ser uniforme entre as cotas.
    par = Parametros(N=10, T=10, phi0=0, phi1=0, phi2=0)
    primeira = [int(np.nanargmin(simula(par, seed=s).espera)) for s in range(3000)]
    obs = np.bincount(primeira, minlength=10)
    assert stats.chisquare(obs).pvalue > 0.001


def test_mais_lance_mais_contemplacao_por_lance():
    base = dict(N=600, T=200, h=0.005)
    f = [simula(Parametros(phi0=x, **base), seed=7) for x in (0.0, 0.1, 0.3)]
    frac = [r.contempl_lance.sum() / (r.contempl_lance.sum() + r.contempl_sorteio.sum()) for r in f]
    assert frac[0] <= frac[1] <= frac[2]


def test_semente_fixa_reproduz():
    a, b = simula(Parametros(h=0.01), seed=11), simula(Parametros(h=0.01), seed=11)
    assert np.array_equal(a.espera, b.espera, equal_nan=True)
