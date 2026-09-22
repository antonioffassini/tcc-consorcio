#!/usr/bin/env python3
"""Gera os arquivos de secao em text/ a partir do manifesto docs/estrutura.tsv.
Nao sobrescreve arquivo existente. Rode quantas vezes quiser."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAN = ROOT / "docs" / "estrutura.tsv"
TEXT = ROOT / "text"

TPL = """---
secao: {num}
titulo: {titulo}
status: esqueleto
responsavel:
insumos:
{insumos}
fontes:
excecoes:
paginas_alvo: {pag}
---

# {titulo}

<!-- ESCOPO: {escopo} -->

<!-- Esta secao esta com status 'esqueleto' e e ignorada pela auditoria.
     Mude para 'rascunho' quando comecar a escrever e para 'fechado'
     quando passar na revisao adversarial. -->
"""

TEXT.mkdir(exist_ok=True)
with MAN.open(encoding="utf-8") as fh:
    for row in csv.DictReader(fh, delimiter="\t"):
        p = TEXT / (row["arquivo"] + ".md")
        if p.exists():
            print("existe, mantido: " + p.name)
            continue
        ins = "\n".join("  - " + i.strip() for i in row["insumos"].split(";") if i.strip())
        p.write_text(TPL.format(num=row["num"], titulo=row["titulo"], pag=row["paginas"],
                                escopo=row["escopo"], insumos=ins or "  -"), encoding="utf-8")
        print("criado: " + p.name)
