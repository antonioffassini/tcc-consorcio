# TCC — repositório de trabalho

Monografia com pipeline reprodutível e auditoria de ancoragem.
Plano de execução completo em `docs/PLANO.md`.

## Começar

```bash
git init && git add -A && git commit -m "estrutura inicial"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make ajuda
```

## Regras invioláveis

1. Nenhum número no texto sem célula correspondente em `results/`.
2. Nenhuma citação sem PDF em `refs/pdfs/`.
3. Nenhuma seção escrita antes de o prompt P0 dar `PRONTA`.
4. Nenhuma decisão de modelagem fora do log do `CONTEXT.md` §6.
5. Nenhum experimento novo depois do congelamento.

## Fluxo por seção

P0 (insumos) → P4 (rascunho) → `scripts/audit.py` → P5 (adversarial) → `status: fechado`.
Prompts em `prompts/`.

## Antes de toda entrega ao orientador

```bash
make auditoria
```
