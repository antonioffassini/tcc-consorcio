# P4 — Rascunho de seção (só após P0 dar PRONTA)

Escreva `text/<arquivo>.md`, respeitando o escopo do frontmatter.

Regras:
- Notação exclusivamente do CONTEXT §5.
- Toda citação como `[@chave]` com entrada existente em `refs/refs.bib`.
  Faltou referência? escreva `[CITAR: o que falta]`.
- Todo número vem de um CSV em `results/`. Não existe ainda? escreva
  `[RESULTADO PENDENTE: qual]`. Nunca estime, nunca ilustre com número inventado.
- Voz impessoal, português brasileiro, ABNT.
- Ao terminar, atualize `status:` para `rascunho` e preencha `fontes:` com os
  CSVs efetivamente usados.

**Contrato de saída:** arquivo escrito que passa em `python scripts/audit.py`.
