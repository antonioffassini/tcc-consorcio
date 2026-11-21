"""Interface de docking (passo 5, 19/11): lado Python.

Lê um JSON com parâmetros, mecanismo e sementes; roda o motor (`grupo.simula`) uma vez
por semente; grava os momentos em JSON. O jogo Java (projetos/poo-jogo) deve ler o mesmo
JSON de entrada pela sua CLI e gravar a saída no mesmo formato; a comparação (seção 6.5)
é de distribuições entre sementes, não bit a bit, porque os geradores aleatórios diferem.

Uso:
  python -m src.sim.docking entrada.json saida.json [--series]

Entrada (chaves ausentes ficam com o padrão de `grupo.Parametros`):
  {
    "versao": "docking-1",
    "parametros": {"N": 600, "T": 200, "h": 0.005, "phi0": 0.1, ...},
    "mecanismo": "M0" | "M1" | "M2",
    "beta": 1.0,                    # só para M1 (peso pela espera)
    "sementes": [0, 1, 2],
    "horizonte": null               # null = vida inteira do grupo
  }

Saída:
  {
    "versao": "docking-1",
    "implementacao": "python",
    "entrada": {...},               # eco da entrada, com os parâmetros completos
    "por_semente": [{"semente": 0, "contempl_sorteio": ..., "contempl_lance": ...,
                     "restituicoes": ..., "frac_lance": ..., "taxa_contempl_mediana": ...,
                     "frac_sem_contempl": ..., "espera_media": ..., "espera_dp": ...,
                     "lances_livres": ..., "lances_embutidos": ...,
                     "entradas": ..., "saidas": ..., "saldo_final": ..., "cotas_total": ...,
                     "series": {...}}, ...],   # "series" só com --series
    "agregado": {"<momento>": {"media": ..., "dp": ..., "n": ...}, ...}
  }
Unidades: valores monetários em fração do crédito C; tempos em assembleias.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, fields
from pathlib import Path

import numpy as np

from .grupo import Parametros, momentos_simulados, simula
from .regras import M0, M2, m1_espera

VERSAO = "docking-1"
CAMPOS = {f.name for f in fields(Parametros)}
MOMENTOS = ["contempl_sorteio", "contempl_lance", "restituicoes", "frac_lance", "taxa_contempl_mediana",
            "frac_sem_contempl", "espera_media", "espera_dp", "lances_livres", "lances_embutidos",
            "entradas", "saidas", "saldo_final", "cotas_total"]


def parametros_de(d: dict) -> Parametros:
    desconhecidos = set(d) - CAMPOS
    if desconhecidos:
        raise ValueError(f"parâmetros desconhecidos: {sorted(desconhecidos)}")
    d = dict(d)
    if isinstance(d.get("h_idade"), list):
        d["h_idade"] = tuple(tuple(x) for x in d["h_idade"])
    return Parametros(**d)


def mecanismo_de(nome: str, beta: float):
    if nome == "M0":
        return M0
    if nome == "M1":
        return m1_espera(beta)
    if nome == "M2":
        return M2
    raise ValueError(f"mecanismo desconhecido: {nome}")


def roda(entrada: dict, series: bool = False) -> dict:
    par = parametros_de(entrada.get("parametros", {}))
    mec = mecanismo_de(entrada.get("mecanismo", "M0"), float(entrada.get("beta", 1.0)))
    sementes = [int(s) for s in entrada.get("sementes", [0])]
    horizonte = entrada.get("horizonte")
    por = []
    for s in sementes:
        r = simula(par, seed=s, mecanismo=mec, horizonte=horizonte)
        H = r.extra["horizonte"]
        m = momentos_simulados(r, slice(0, H))
        esp = r.espera[~np.isnan(r.espera)]
        linha = dict(semente=s, contempl_sorteio=int(r.contempl_sorteio[:H].sum()),
                     contempl_lance=int(r.contempl_lance[:H].sum()), restituicoes=int(r.restituicoes[:H].sum()),
                     frac_lance=float(m["frac_lance"]), taxa_contempl_mediana=float(m["taxa_contempl_mediana"]),
                     frac_sem_contempl=float(m["frac_sem_contempl"]),
                     espera_media=float(esp.mean()) if len(esp) else None,
                     espera_dp=float(esp.std()) if len(esp) else None,
                     lances_livres=float(r.lances_pagos), lances_embutidos=float(r.lances_embutidos),
                     entradas=float(r.entradas), saidas=float(r.saidas), saldo_final=float(r.saldo_final),
                     cotas_total=int(r.extra["cotas_total"]))
        if series:
            linha["series"] = dict(contempl_sorteio=r.contempl_sorteio[:H].tolist(),
                                   contempl_lance=r.contempl_lance[:H].tolist(),
                                   restituicoes=r.restituicoes[:H].tolist(), ativas=r.ativas[:H].tolist(),
                                   saldo=r.saldo[:H].tolist())
        por.append(linha)
    agg = {}
    for k in MOMENTOS:
        v = np.array([x[k] for x in por if x[k] is not None], float)
        agg[k] = dict(media=float(v.mean()) if len(v) else None,
                      dp=float(v.std(ddof=1)) if len(v) > 1 else None, n=int(len(v)))
    eco = dict(entrada); eco["parametros"] = asdict(par); eco["versao"] = VERSAO
    return dict(versao=VERSAO, implementacao="python", entrada=eco, por_semente=por, agregado=agg)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Docking: roda o motor Python a partir de um JSON")
    ap.add_argument("entrada", type=Path)
    ap.add_argument("saida", type=Path)
    ap.add_argument("--series", action="store_true", help="inclui as séries mensais por semente")
    a = ap.parse_args(argv)
    entrada = json.loads(a.entrada.read_text(encoding="utf-8"))
    saida = roda(entrada, series=a.series)
    a.saida.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
