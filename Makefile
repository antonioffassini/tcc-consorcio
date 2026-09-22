# TCC - pipeline reprodutivel ponta a ponta.
# Regra de ouro: nenhum resultado existe se nao for gerado por um alvo daqui.

PY := python3
SECOES := $(sort $(wildcard text/*.md))

.PHONY: all data painel experimentos resultados auditoria docx limpar ajuda

ajuda:
	@echo "make painel        - le data/raw, gera data/processed/painel.parquet"
	@echo "make experimentos  - roda calibracao e simulacoes (seeds fixas)"
	@echo "make resultados    - gera tabelas e figuras em results/"
	@echo "make auditoria     - checa citacoes, numeros e marcadores pendentes"
	@echo "make docx          - monta build/monografia.docx a partir de text/"
	@echo "make all           - painel -> experimentos -> resultados -> auditoria -> docx"
	@echo "make limpar        - apaga derivados (nunca toca data/raw)"

all: painel experimentos resultados auditoria docx

painel:
	$(PY) -m src.pipeline.build_panel --raw data/raw --out data/processed

experimentos: painel
	$(PY) -m src.experiments.run --config src/config/base.yaml --seed 42

resultados: experimentos
	$(PY) -m src.analysis.make_tables --out results
	$(PY) -m src.analysis.make_figures --out results

auditoria:
	$(PY) scripts/audit.py --strict

esqueleto:
	$(PY) scripts/gen_skeleton.py

docx:
	bash scripts/build_docx.sh

limpar:
	rm -rf data/processed/* results/* build/*
	@echo "data/raw preservado."
