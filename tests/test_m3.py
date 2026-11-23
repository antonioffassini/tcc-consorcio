"""Testes do bloco de 22/11: família M3, F_theta alternativas, invariância de escala e η pelos regulamentos."""
from dataclasses import replace

import numpy as np
import pandas as pd

from src.sim import painel
from src.sim.grupo import Parametros, simula, sorteia_theta
from src.sim.regras import LanceUniforme, Mecanismo, M2, familia_m3, regra_M2

BASE = Parametros(N=300, T=120, sorteio_excluidos="separado", emb_max=0.3, atraso_exclusao=3, rho=1.0,
                  h=0.004, phi0=-0.04, teto_restituicao=0.15)


def _lances(seed=0, n=40):
    rng = np.random.default_rng(seed)
    livre = rng.uniform(0, 0.4, n) * (rng.random(n) < 0.6)
    emb = rng.uniform(0, 0.3, n) * (rng.random(n) < 0.5)
    return np.arange(n), livre, emb


def test_reserva_zero_igual_a_M2():
    for s in range(20):
        cand, livre, emb = _lances(s)
        for R in (0.5, 1.7, 3.2, 8.0):
            a = regra_M2(R, cand, livre, emb)
            b = LanceUniforme(0.0)(R, cand, livre, emb)
            assert np.array_equal(a[0], b[0])
            assert np.allclose(a[1], b[1]) and np.allclose(a[2], b[2]) and np.isclose(a[3], b[3])


def test_reserva_respeitada_e_viabilidade():
    for s in range(20):
        cand, livre, emb = _lances(s)
        for p in (0.05, 0.1, 0.2):
            for R in (1.0, 2.5, 6.0):
                venc, lv, em, R1 = LanceUniforme(p)(R, cand, livre, emb)
                if len(venc):
                    preco = lv + em
                    assert np.allclose(preco, preco[0]) and preco[0] >= p - 1e-12
                    assert np.all(livre[venc] + emb[venc] >= p - 1e-12)
                    assert np.all(em <= emb[venc] + 1e-12)
                    assert R1 >= -1e-9


def test_reserva_maior_contempla_ao_menos_tanto_quanto_M2():
    """Preço de reserva sobe o preço pago: com os mesmos lances, mais vencedores cabem no fundo."""
    for s in range(20):
        cand, livre, emb = _lances(s, 200)
        for R in (2.0, 5.0):
            k2 = len(regra_M2(R, cand, livre, emb)[0])
            k3 = len(LanceUniforme(0.05)(R, cand, livre, emb)[0])
            n_eleg = int(((livre + emb) >= 0.05).sum())
            assert k3 >= min(k2, n_eleg)


def test_M3s_forca_sorteio_da_sobra():
    m3s = dict(familia_m3())["M3s"]
    sem = simula(replace(BASE, sorteio_sobra=False, phi0=-0.3), seed=3, mecanismo=M2)
    com = simula(replace(BASE, sorteio_sobra=False, phi0=-0.3), seed=3, mecanismo=m3s)
    ref = simula(replace(BASE, sorteio_sobra=True, phi0=-0.3), seed=3, mecanismo=M2)
    assert com.contempl_sorteio.sum() == ref.contempl_sorteio.sum()
    assert com.contempl_sorteio.sum() >= sem.contempl_sorteio.sum()


def test_familia_m3_tem_11_variantes_registradas():
    nomes = [n for n, _ in familia_m3()]
    assert len(nomes) == 11 and len(set(nomes)) == 11


def test_invariancia_da_escala_da_urgencia():
    """theta*c com phi1/c: mesmos números aleatórios, mesmo comportamento (ESTADO §4, 22/11)."""
    c = 0.2
    a = simula(BASE, seed=7)
    b = simula(replace(BASE, mu_theta=BASE.mu_theta + np.log(c), phi1=BASE.phi1 / c), seed=7)
    assert np.array_equal(a.contempl_lance, b.contempl_lance)
    assert np.array_equal(a.contempl_sorteio, b.contempl_sorteio)
    assert np.allclose(a.extra["livre"], b.extra["livre"])
    assert np.allclose(b.extra["theta"], c * a.extra["theta"])


def test_distribuicoes_de_theta():
    rng = np.random.default_rng(0)
    g = sorteia_theta(rng, replace(BASE, theta_dist="gamma", gamma_forma=2.0, gamma_media=0.2), 200_000)
    assert abs(g.mean() - 0.2) < 0.003
    m = sorteia_theta(rng, replace(BASE, theta_dist="mistura", mist_p=0.4, mist_baixo=0.14, mist_alto=0.6), 200_000)
    assert set(np.unique(m)) == {0.14, 0.6} and abs((m == 0.6).mean() - 0.4) < 0.005


def test_sobra_pelos_regulamentos():
    adms = np.array(["48041735", "00000776", "07808907", "55942312", "11111111", "22222222"])
    grupos = pd.DataFrame(dict(cnpj=adms, gid=range(6)))
    des = painel.Desenho(grupos=grupos, obs=pd.DataFrame(), alvo_b=pd.DataFrame(), adms=adms)
    painel.atribui_sobra(des, eta0=0.0, seed=1)
    assert des.grupos["sobra"].tolist() == [1, 1, 1, 0, 0, 0]
    painel.atribui_sobra(des, eta0=1.0, seed=1)
    assert des.grupos["sobra"].tolist() == [1, 1, 1, 0, 1, 1]


# ---- família M4: lance fixo (ESTADO §4, 23/11)
from src.sim.regras import LanceFixo, m4f, FAMILIA_M4, resolve, regra_M2 as _rM2


def test_m4_fixo_paga_preco_e_respeita_saldo():
    cand = np.arange(6); livre = np.array([0.0, 0.1, 0.25, 0.3, 0.5, 0.2]); emb = np.zeros(6)
    v, lv, em, R = LanceFixo(0.2, None, None)(2.0, cand, livre, emb, rng=np.random.default_rng(1))
    assert len(v) == 2 and set(v) <= {2, 3, 4, 5}
    assert np.allclose(lv + em, 0.2) and np.isclose(R, 2.0 - 2 * 0.8)


def test_m4_fixo_um_e_depois_livre():
    cand = np.arange(5); livre = np.array([0.4, 0.3, 0.22, 0.1, 0.0]); emb = np.zeros(5)
    v, lv, em, R = LanceFixo(0.2, 1, _rM2)(3.0, cand, livre, emb, rng=np.random.default_rng(0))
    assert v[0] in (0, 1, 2) and np.isclose(lv[0] + em[0], 0.2)
    assert len(set(v)) == len(v)


def test_m4_familia_e_sequencia_comum():
    assert len(FAMILIA_M4) == 8 and all(resolve(n).nome == n for n in FAMILIA_M4)
    par = Parametros(N=60, T=60)
    a = simula(par, seed=3, mecanismo=m4f("M4f_p0.2_n1_a1")); b = simula(par, seed=3)
    assert np.allclose(a.extra["theta"][:60], b.extra["theta"][:60]) if "theta" in a.extra else True
