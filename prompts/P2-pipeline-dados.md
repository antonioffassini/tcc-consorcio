# P2 — Pipeline de dados (usar no Claude Code)

Os CSVs do banco de dados de consórcios do Bacen estão em `data/raw/bacen/`
(Documentos 4010/2080, 4110 e Dados por UF).

Construa `src/pipeline/build_panel.py` que:
1. leia todos os arquivos, tolerando variação de encoding e separador;
2. normalize esquemas entre datas-base — o leiaute mudou pela Carta Circular
   3.679/14, então trate a quebra explicitamente e documente o mapeamento;
3. consolide um painel em nível grupo × administradora × segmento × data-base;
4. emita `results/qualidade_dados.csv` com cobertura temporal, campos faltantes
   e quebras de série detectadas.

ANTES de escrever código: liste as decisões de modelagem de dados que pretende
tomar e peça confirmação. Depois: código com testes em `tests/`, executável por
`make painel`, sem estado escondido.

**Contrato de saída:** decisões listadas primeiro; depois código + testes que passam.
