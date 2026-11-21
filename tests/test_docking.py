"""Verificação do passo 5 (19/11): interface de docking (lado Python)."""
import json

import numpy as np
import pytest

from src.sim import docking
from src.sim.grupo import Parametros, simula
from src.sim.regras import M2

ENTRADA = {"versao": "docking-1", "parametros": {"N": 200, "T": 100, "h": 0.01, "rho": 1.0, "emb_max": 0.3,
                                                 "sorteio_excluidos": "separado", "teto_restituicao": 0.2},
           "mecanismo": "M2", "sementes": [0, 1, 2], "horizonte": None}


def test_ida_e_volta_por_arquivo(tmp_path):
    e, s = tmp_path / "e.json", tmp_path / "s.json"
    e.write_text(json.dumps(ENTRADA), encoding="utf-8")
    docking.main([str(e), str(s), "--series"])
    out = json.loads(s.read_text(encoding="utf-8"))
    assert out["versao"] == "docking-1" and out["implementacao"] == "python"
    assert [x["semente"] for x in out["por_semente"]] == [0, 1, 2]
    assert len(out["por_semente"][0]["series"]["saldo"]) == 100
    assert out["agregado"]["frac_lance"]["n"] == 3


def test_saida_igual_a_simulacao_direta():
    out = docking.roda(ENTRADA)
    par = Parametros(**ENTRADA["parametros"])
    r = simula(par, seed=1, mecanismo=M2)
    x = out["por_semente"][1]
    assert x["contempl_lance"] == int(r.contempl_lance.sum())
    assert x["contempl_sorteio"] == int(r.contempl_sorteio.sum())
    assert np.isclose(x["saldo_final"], r.saldo_final)
    assert abs(x["entradas"] - x["saidas"] - x["saldo_final"]) < 1e-8


def test_parametro_desconhecido_e_mecanismo_invalido():
    with pytest.raises(ValueError):
        docking.roda({"parametros": {"N": 10, "xyz": 1}})
    with pytest.raises(ValueError):
        docking.roda({"parametros": {"N": 50, "T": 50}, "mecanismo": "M9"})


def test_h_idade_em_lista_json():
    e = dict(ENTRADA, parametros=dict(ENTRADA["parametros"], h=0.0, h_idade=[[0.2, 10], [0.03, 0.005]]),
             sementes=[0])
    out = docking.roda(e)
    assert out["entrada"]["parametros"]["h_idade"] == ((0.2, 10), (0.03, 0.005))
