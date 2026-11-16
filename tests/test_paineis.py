"""Testes de integridade sobre os painéis gerados por `make painel`."""
import pandas as pd

from src.pipeline import build_panel as bp
from src.pipeline import leitura as lt

CONT_A = ["ativas", "ativas_em_dia", "ativas_contempl_inad", "ativas_nao_contempl_inad",
          "ativas_quitadas", "credito_pendente", "contempladas_mes", "excluidas_estoque",
          "cotas_total", "prazo", "assembleia"]
CONT_B = bp.CONTAGENS_UF + ["contempl_trim", "lance_trim_rs", "sorteio_trim_rs", "ativos_total",
                            "ativos_total_rs"]


def test_a_sem_duplicatas(painel_a):
    assert not painel_a.duplicated(["cnpj", "grupo", "data_base"]).any()


def test_b_sem_duplicatas(painel_b):
    assert not painel_b.duplicated(["cnpj", "data_base"]).any()


def test_a_recorte_regime(painel_a):
    assert painel_a["data_base"].min() == bp.INICIO_REGIME
    assert (painel_a["regime"] == "pos285").all()


def test_a_contagens_nao_negativas(painel_a):
    assert (painel_a[CONT_A] >= 0).all().all()
    assert (painel_a["excluidas_mes"].dropna() >= 0).all()


def test_b_contagens_nao_negativas(painel_b):
    assert (painel_b[CONT_B] >= 0).all().all()


def test_a_ativas_e_soma_das_situacoes(painel_a):
    s = painel_a["ativas_em_dia"] + painel_a["ativas_contempl_inad"] + painel_a["ativas_nao_contempl_inad"]
    assert (s == painel_a["ativas"]).all()
    assert (painel_a["contempladas_mes"] <= painel_a["ativas"]).all()


def test_b_somas_internas(painel_b):
    assert (painel_b["lance_trim"] + painel_b["sorteio_trim"] == painel_b["contempl_trim"]).all()
    assert (painel_b["lance_trim_rs"] <= painel_b["lance_trim"]).all()
    assert (painel_b["sorteio_trim_rs"] <= painel_b["sorteio_trim"]).all()
    f = painel_b["frac_lance"].dropna()
    assert ((f >= 0) & (f <= 1)).all()


def test_b_bate_com_soma_das_ufs_no_bruto(painel_b, raw_dir):
    """Reagrega do zero três trimestres do bruto e compara com o painel B."""
    _, ufs = lt.lista_zips(raw_dir)
    for db in ["201703", "202412", max(ufs)]:
        uf = lt.le_uf(ufs[db], db).df
        uf = uf[uf["segmento"] == bp.SEGMENTO_IMOVEIS]
        bruto = uf.groupby("cnpj")[["lance_trim", "sorteio_trim", "ativos_nao_contemplados"]].sum()
        p = painel_b[painel_b["data_base"] == int(db)].set_index("cnpj")[bruto.columns]
        pd.testing.assert_frame_equal(bruto.sort_index(), p.sort_index(), check_dtype=False,
                                      check_names=False)


def test_soma_dos_grupos_bate_com_consolidado(conciliacao):
    c = conciliacao[conciliacao["tipo"] == "grupos_vs_consolidado_mensal"]
    assert len(c) > 0
    for col in ["contempladas_mes", "ativas_em_dia", "excluidas_estoque"]:
        assert (c[col] == c[col + "_consolidado"]).all(), col


def test_uf_bate_com_consolidado_na_maioria(conciliacao):
    c = conciliacao[conciliacao["tipo"] == "uf_vs_consolidado_trimestral"]
    acum = c["ativos_lance_acum"] + c["ativos_sorteio_acum"]
    # O arquivo por UF e o consolidado vêm de remessas distintas; divergências
    # pontuais existem e ficam registradas em results/qualidade_dados.csv.
    assert (acum == c["contempladas_acum"]).mean() > 0.95


def test_relatorio_de_qualidade_completo():
    q = pd.read_csv(bp.Path(__file__).resolve().parent.parent / "results" / "qualidade_dados.csv")
    exigidas = {"linhas_lidas", "linhas_descartadas_total", "duplicatas_por_chave", "celulas_nulas",
                "periodos_faltantes_internos", "meses_mensais_faltantes"}
    assert exigidas <= set(q["metrica"])
