#!/usr/bin/env bash
# Monta a monografia final. Ordem = ordem alfabetica dos arquivos em text/,
# por isso o prefixo numerico NN- nos nomes.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build
pandoc text/*.md \
  --from markdown \
  --citeproc \
  --bibliography refs/refs.bib \
  --csl refs/abnt.csl \
  --reference-doc build/template-abnt.docx \
  --toc --toc-depth=3 \
  --number-sections \
  -o build/monografia.docx
echo "gerado: build/monografia.docx"
