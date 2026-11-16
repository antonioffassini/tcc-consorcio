from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"


def _carrega(nome):
    p = PROC / nome
    if not p.exists():
        pytest.skip(f"{p} não existe: rode `make painel` antes")
    return pd.read_parquet(p)


@pytest.fixture(scope="session")
def painel_a():
    return _carrega("painel_a_grupo_mes.parquet")


@pytest.fixture(scope="session")
def painel_b():
    return _carrega("painel_b_adm_trimestre.parquet")


@pytest.fixture(scope="session")
def conciliacao():
    return _carrega("conciliacao.parquet")


@pytest.fixture(scope="session")
def raw_dir():
    if not any((RAW / "bacen").glob("*Consorcios_UF.zip")):
        pytest.skip("data/raw/bacen sem arquivos")
    return RAW
