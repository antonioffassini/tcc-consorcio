"""Leitura dos arquivos brutos do Bacen (data/raw/bacen), sem alterá-los.

Dois tipos de pacote entram no pipeline:

* ``AAAAMMConsorcios.zip`` (mensal): contém ``AAAAMMBens_Imoveis_Grupos.csv``
  (grão grupo, segmento imóveis) e ``AAAAMMSegmentos_Consolidados.csv``
  (grão administradora × segmento). Os grupos de bens móveis só aparecem
  nos meses de fim de trimestre e não são usados.
* ``AAAAMMConsorcios_UF.zip`` (trimestral): ``AAAAMMConsorcios_UF.csv``,
  grão administradora × segmento × UF, único arquivo que separa as
  contemplações por lance e por sorteio.

Os ``*_ADM.zip`` (contábeis, Docs 4010/4110 consolidados do sistema) não
entram: ver ESTADO.md §5 item 12.

Os arquivos são CSV com ``;``, decimal com vírgula, codificação Latin-1 e
cabeçalho iniciado por ``#``. O leiaute vale desde a data-base 2017-03.
"""
from __future__ import annotations

import io
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

ENCODING = "latin1"

# Cabeçalho oficial -> nome curto usado no pipeline
COLS_GRUPOS = {
    "#Nome_da_Administradora": "nome_adm",
    "CNPJ_da_Administradora": "cnpj",
    "Data_base": "data_base",
    "Código_do_grupo": "grupo",
    "Código_do_segmento": "segmento",
    "Número_da_assembléia_geral_ordinária": "assembleia",
    "Valor_médio_do_bem": "valor_bem",
    "Índice_de_correção": "indice_correcao",
    "Taxa_de_administração": "taxa_adm",
    "Prazo_do_grupo_em_meses": "prazo",
    "Quantidade_de_cotas_ativas_em_dia": "ativas_em_dia",
    "Quantidade_de_cotas_ativas_contempladas_inadimplentes": "ativas_contempl_inad",
    "Quantidade_de_cotas_ativas_não_contempladas_inadimplentes": "ativas_nao_contempl_inad",
    "Quantidade_de_cotas_ativas_contempladas_no_mês": "contempladas_mes",
    "Quantidade_de_cotas_excluídas": "excluidas_estoque",
    "Quantidade_de_cotas_ativas_quitadas": "ativas_quitadas",
    "Quantidade_de_cotas_ativas_com_crédito_pendente_de_utilização": "credito_pendente",
}

COLS_SEGMENTOS = {
    "#Nome_da_Administradora": "nome_adm",
    "CNPJ_da_Administradora": "cnpj",
    "Data_base": "data_base",
    "Código_do_segmento": "segmento",
    "Taxa_de_administração": "taxa_adm",
    "Quantidade_de_grupos_ativos": "grupos_ativos",
    "Quantidade_de_grupos_constituídos_no_mês": "grupos_constituidos_mes",
    "Quantidade_de_grupos_encerrados_no_mês": "grupos_encerrados_mes",
    "Quantidade_de_cotas_comercializadas_no_mês": "cotas_comercializadas_mes",
    "Quantidade_de_cotas_excluídas_a_comercializar": "excluidas_a_comercializar",
    "Quantidade_acumulada_de_cotas_ativas_contempladas": "contempladas_acum",
    "Quantidade_de_cotas_ativas_não_contempladas": "ativas_nao_contempladas",
    "Quantidade_de_cotas_ativas_contempladas_no_mês": "contempladas_mes",
    "Quantidade_de_cotas_ativas_em_dia": "ativas_em_dia",
    "Quantidade_de_cotas_ativas_contempladas_inadimplentes": "ativas_contempl_inad",
    "Quantidade_de_cotas_ativas_não_contempladas_inadimplentes": "ativas_nao_contempl_inad",
    "Quantidade_de_cotas_excluídas": "excluidas_estoque",
    "Quantidade_de_cotas_ativas_quitadas": "ativas_quitadas",
    "Quantidade_de_cotas_ativas_com_crédito_pendente_de_utilização": "credito_pendente",
}

COLS_UF = {
    "#Data_base": "data_base",
    "CNPJ_da_Administradora": "cnpj",
    "Nome_da_Administradora": "nome_adm",
    "Código_do_segmento": "segmento",
    "Unidade_da_Federação_do_consorciado": "uf",
    "Quantidade_de_consorciados_ativos_contemplados_por_lance": "ativos_lance_acum",
    "Quantidade_de_consorciados_ativos_contemplados_por_sorteio": "ativos_sorteio_acum",
    "Quantidade_de_consorciados_ativos_não_contemplados": "ativos_nao_contemplados",
    "Quantidade_de_consorciados_excluídos_contemplados": "excluidos_contempl_acum",
    "Quantidade_de_consorciados_excluídos_não_contemplados": "excluidos_nao_contemplados",
    "Quantidade_de_consorciados_ativos_contemplados_por_lance_no_trimestre": "lance_trim",
    "Quantidade_de_consorciados_ativos_contemplados_por_sorteio_no_trimestre": "sorteio_trim",
    "Quantidade_de_consorciados_excluídos_contemplados_no_trimestre": "excluidos_contempl_trim",
    "Quantidade_de_adesões_no_trimestre": "adesoes_trim",
}

TEXTO = {"nome_adm", "cnpj", "grupo", "uf"}
NUMERO_DECIMAL = {"valor_bem", "taxa_adm"}

ZIP_MENSAL = re.compile(r"^(\d{6})Consorcios\.zip$")
ZIP_UF = re.compile(r"^(\d{6})Consorcios_UF\.zip$")


@dataclass
class Leitura:
    """Resultado bruto da leitura de um CSV dentro de um zip."""

    arquivo: str  # zip/membro
    data_base_arquivo: str  # AAAAMM do nome do arquivo
    df: pd.DataFrame
    linhas_lidas: int
    colunas_ausentes: list[str]
    colunas_extras: list[str]


def _normaliza_header(h: str) -> str:
    # Há variação de espaço no dicionário ("no_ trimestre"); o cabeçalho real
    # não tem, mas a normalização protege contra isso.
    return re.sub(r"\s+", "", h)


def _le_csv(raw: bytes, mapa: dict[str, str]) -> tuple[pd.DataFrame, list[str], list[str]]:
    df = pd.read_csv(
        io.BytesIO(raw), sep=";", encoding=ENCODING, dtype=str, keep_default_na=False
    )
    norm = {_normaliza_header(k): v for k, v in mapa.items()}
    cols = [_normaliza_header(c) for c in df.columns]
    ausentes = [k for k in norm if k not in cols]
    extras = [c for c in cols if c not in norm]
    df.columns = [norm.get(c, c) for c in cols]
    df = df[[v for v in mapa.values() if v in df.columns]].copy()
    for c in df.columns:
        df[c] = df[c].str.strip()
        if c in TEXTO:
            df[c] = df[c].replace("", pd.NA)
            continue
        s = df[c].replace("", pd.NA)
        if c in NUMERO_DECIMAL:
            s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
        df[c] = pd.to_numeric(s, errors="coerce")
    return df, ausentes, extras


def lista_zips(raw_dir: Path) -> tuple[dict[str, Path], dict[str, Path]]:
    bacen = raw_dir / "bacen" if (raw_dir / "bacen").is_dir() else raw_dir
    mensais, uf = {}, {}
    for p in sorted(bacen.glob("*.zip")):
        if m := ZIP_MENSAL.match(p.name):
            mensais[m.group(1)] = p
        elif m := ZIP_UF.match(p.name):
            uf[m.group(1)] = p
    return mensais, uf


def _membro(z: zipfile.ZipFile, sufixo: str) -> str | None:
    for n in z.namelist():
        if n.endswith(sufixo):
            return n
    return None


def le_mensal(path: Path, aaaamm: str, qual: str) -> Leitura | None:
    """qual = 'grupos' (Bens_Imoveis_Grupos) ou 'segmentos' (Segmentos_Consolidados)."""
    sufixo, mapa = {
        "grupos": ("Bens_Imoveis_Grupos.csv", COLS_GRUPOS),
        "segmentos": ("Segmentos_Consolidados.csv", COLS_SEGMENTOS),
    }[qual]
    with zipfile.ZipFile(path) as z:
        nome = _membro(z, sufixo)
        if nome is None:
            return None
        raw = z.read(nome)
    df, aus, ext = _le_csv(raw, mapa)
    return Leitura(f"{path.name}/{nome}", aaaamm, df, len(df), aus, ext)


def le_uf(path: Path, aaaamm: str) -> Leitura | None:
    with zipfile.ZipFile(path) as z:
        nome = _membro(z, "Consorcios_UF.csv")
        if nome is None:
            return None
        raw = z.read(nome)
    df, aus, ext = _le_csv(raw, COLS_UF)
    return Leitura(f"{path.name}/{nome}", aaaamm, df, len(df), aus, ext)
