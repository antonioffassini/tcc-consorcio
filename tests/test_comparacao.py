"""Verificação do passo 4 (19/11): métricas de H3 por grupo e regra de dominância."""
import numpy as np
import pandas as pd

from src.analysis import comparacao as K
from src.sim.grupo import Parametros, simula
from src.sim.regras import M0, M2


def test_metricas_sem_exclusao():
    par = Parametros(N=200, T=100, h=0.0)
    m = K.metricas_grupo(simula(par, seed=1), par.T)
    assert 0 < m["W"] < 1 and m["E"] > 0 and 0 <= m["S"] <= 1
    assert m["n_excl"] == 0 and np.isnan(m["Rst"]) and m["n_cotas"] == 200


def test_metricas_com_exclusao_e_recolocacao():
    par = Parametros(N=300, T=120, h=0.02, rho=1.0, atraso_exclusao=3, sorteio_excluidos="separado",
                     teto_restituicao=0.2, emb_max=0.3)
    m = K.metricas_grupo(simula(par, seed=2), par.T)
    assert m["n_excl"] > 0 and m["Rst"] > 0
    assert m["n_cotas"] > 0


def test_utilidade_cai_com_a_espera():
    # mesma cota, espera maior => utilidade menor (desconto exp(-theta w / 12))
    th, e = 1.0, 0.0
    u = [np.exp(-th * w / 12) * (1 - e) for w in (1, 12, 60)]
    assert u[0] > u[1] > u[2]


def test_resumo_diferenca_nula_contra_si_mesmo():
    linhas = []
    rng = np.random.default_rng(0)
    for mec in ("M0", "Mx"):
        for g in range(20):
            linhas.append(dict(replica=0, mecanismo=mec, gid=g, cnpj=g % 5, adm=g % 5, peso=1.0,
                               W=0.3 + 0.01 * g, E=10.0, S=0.0, Rst=5.0, espera_media=20.0, frac_lance=0.7))
    df = pd.DataFrame(linhas)
    niv, dif = K.resume(df, 50, 1)
    linha = dif.set_index("mecanismo").loc["Mx"]
    for c in K.CRITERIOS:
        assert abs(linha[c]) < 1e-12
    assert not linha["domina_M0"]


def test_resumo_detecta_dominancia():
    linhas = []
    for mec, dw in (("M0", 0.0), ("Mx", 0.05)):
        for g in range(30):
            linhas.append(dict(replica=0, mecanismo=mec, gid=g, cnpj=g % 10, adm=g % 10, peso=1.0,
                               W=0.3 + 0.001 * g + dw, E=10.0, S=0.0, Rst=5.0, espera_media=20.0, frac_lance=0.7))
    niv, dif = K.resume(pd.DataFrame(linhas), 100, 1)
    linha = dif.set_index("mecanismo").loc["Mx"]
    assert linha["domina_M0"] and linha["melhora"] == "W" and linha["piora"] == ""
