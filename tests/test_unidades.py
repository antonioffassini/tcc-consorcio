"""Testes das funções do pipeline com dados sintéticos (não dependem do Bacen)."""
import numpy as np
import pandas as pd

from src.pipeline import build_panel as bp


def _grupo(db, excl, em_dia=10, cm=1, grupo="001"):
    return dict(cnpj="00000001", nome_adm="X", grupo=grupo, segmento=1, data_base=db,
                assembleia=5, prazo=100, valor_bem=1.0, taxa_adm=15.0, indice_correcao=3,
                ativas_em_dia=em_dia, ativas_contempl_inad=2, ativas_nao_contempl_inad=3,
                contempladas_mes=cm, excluidas_estoque=excl, ativas_quitadas=0, credito_pendente=0)


def test_diferenca_de_excluidas_respeita_lacuna():
    g = pd.DataFrame([_grupo(202407, 10), _grupo(202408, 12), _grupo(202410, 15), _grupo(202411, 14)])
    a = bp.deriva_a(g).set_index("data_base")
    assert np.isnan(a.loc[202407, "excluidas_var"])
    assert a.loc[202408, "excluidas_var"] == 2
    assert np.isnan(a.loc[202410, "excluidas_var"])  # 202409 ausente: não diferencia
    assert bool(a.loc[202410, "flag_mes_anterior_ausente"])
    assert a.loc[202411, "excluidas_var"] == -1 and a.loc[202411, "excluidas_mes"] == 0
    assert bool(a.loc[202411, "flag_excluidas_var_negativa"])
    assert (a["ativas"] == 15).all()
    assert a.loc[202408, "taxa_contemplacao"] == 1 / 15


def test_valida_descarta_negativo_e_duplicata():
    g = pd.DataFrame([_grupo(202407, 10), _grupo(202407, 10), _grupo(202407, -1, grupo="002")])
    q = bp.Qualidade()
    out = bp.valida(g, ["cnpj", "grupo", "data_base"], bp.CONTAGENS_GRUPO, "202407", q, "t", "f")
    assert len(out) == 1
    rel = q.df()
    motivos = set(rel.loc[rel.metrica == "linhas_descartadas", "detalhe"])
    assert motivos == {"contagem_negativa", "duplicata"}


def test_agregacao_uf_soma_e_separa_rs():
    base = dict(data_base=202409, cnpj="00000001", nome_adm="X", segmento=1,
                ativos_lance_acum=5, ativos_sorteio_acum=5, ativos_nao_contemplados=10,
                excluidos_contempl_acum=0, excluidos_nao_contemplados=0, sorteio_trim=1,
                excluidos_contempl_trim=0, adesoes_trim=0)
    uf = pd.DataFrame([dict(base, uf="SP", lance_trim=3), dict(base, uf="RS", lance_trim=1)])
    b = bp.deriva_b(bp.agrega_uf(uf)).iloc[0]
    assert b["lance_trim"] == 4 and b["sorteio_trim"] == 2 and b["contempl_trim"] == 6
    assert b["lance_trim_rs"] == 1 and b["sorteio_trim_rs"] == 1
    assert b["frac_lance"] == 4 / 6 and b["frac_lance_ex_rs"] == 3 / 4
    assert b["rs_exposicao"] == 0.5 and b["regime"] == "pos285"
    assert bool(b["flag_rs_2024"]) and bool(b["flag_rs_2024_exposta"])
