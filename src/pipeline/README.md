# Pipeline de dados (etapa 1)

Lê os zips do Bacen em `data/raw/bacen/` (nunca escreve lá) e gera os dois painéis do trabalho e o relatório de qualidade.

## Como rodar

Na raiz do repositório, com o ambiente do `requirements.txt` ativo:

```bash
make painel        # ou: python -m src.pipeline.build_panel --raw data/raw --out data/processed
make testes        # ou: python -m pytest -q tests
```

No Windows sem `make`, use os comandos da direita (com `python` no lugar de `python3`). Tempo de execução: cerca de 15 s.

## Entradas

| Arquivo | Grão | Uso |
|---|---|---|
| `AAAAMMConsorcios.zip` → `AAAAMMBens_Imoveis_Grupos.csv` | grupo × mês (imóveis) | Painel A |
| `AAAAMMConsorcios.zip` → `AAAAMMSegmentos_Consolidados.csv` | administradora × segmento × mês | só conciliação |
| `AAAAMMConsorcios_UF.zip` → `AAAAMMConsorcios_UF.csv` | administradora × segmento × UF × trimestre | Painel B |
| `AAAAMMConsorcios_ADM.zip` | sistema consolidado | não usado (ESTADO §5 item 12) |

CSV com `;`, decimal com vírgula, Latin-1. Leiaute único desde 2017-03 (o pipeline confere o cabeçalho de cada arquivo contra o dicionário e registra divergência em `results/qualidade_dados.csv`).

## Saídas

**`data/processed/painel_a_grupo_mes.parquet`** — grupo × mês, imóveis, data-base ≥ 2024-07. Chave `(cnpj, grupo, data_base)`.

| Coluna | Definição |
|---|---|
| `ativas` | `ativas_em_dia + ativas_contempl_inad + ativas_nao_contempl_inad` (mesma soma que o Bacen usa para ponderar) |
| `contempladas_mes` | cotas ativas contempladas no mês (lance + sorteio; o canal não é observável neste arquivo) |
| `taxa_contemplacao` | `contempladas_mes / ativas` |
| `excluidas_estoque` | estoque de cotas excluídas na data-base (é estoque, não fluxo) |
| `excluidas_var` | variação do estoque contra o mês anterior do mesmo grupo; vazio se o mês anterior falta |
| `excluidas_mes` | `excluidas_var` truncada em zero (a variação negativa ocorre quando cota excluída é recolocada) |
| `prazo`, `assembleia`, `meses_restantes` | prazo do grupo, nº de AGOs realizadas, diferença |
| `valor_bem` | valor médio do bem de referência do crédito (R$) |
| `rs_exposicao` | fração das cotas ativas de imóveis da administradora domiciliadas no RS, no trimestre (do arquivo por UF; vazio em 2026-04/05, sem arquivo por UF) |
| `flag_rs_2024` | data-base entre 2024-05 e 2024-12 **e** `rs_exposicao ≥ 0,5` |
| `flag_*` | sinalizações; nenhuma linha é descartada por elas |

**`data/processed/painel_b_adm_trimestre.parquet`** — administradora × trimestre, imóveis, 2017-03 a 2026-03, UFs somadas. Chave `(cnpj, data_base)`.

| Coluna | Definição |
|---|---|
| `lance_trim`, `sorteio_trim` | cotas **ativas** contempladas no trimestre por lance / sorteio |
| `contempl_trim`, `frac_lance` | soma e `lance_trim / contempl_trim` |
| `excluidos_contempl_trim` | excluídos contemplados no trimestre (sem separação de canal) |
| `*_rs`, `frac_lance_ex_rs` | parcela do RS e fração de lance sem o RS |
| `regime` | `pos285` a partir de 2024-09 (primeiro trimestre inteiro sob a Res. BCB 285) |
| `flag_rs_2024` | data-base 2024-06 a 2024-12 (Res. BCB 381/2024); `flag_rs_2024_exposta` exige também `rs_exposicao ≥ 0,5` |

**`data/processed/conciliacao.parquet`** — somas dos grupos contra o consolidado por administradora (mensal) e somas das UFs contra o consolidado (trimestral). Usado pelos testes.

**`results/qualidade_dados.csv`** — formato longo (`escopo, arquivo, data_base, metrica, valor, detalhe`): linhas lidas, descartadas e motivo, duplicatas, células nulas, períodos faltantes, administradoras com mês ausente, continuidade dos grupos mês a mês (checagem da IN BCB 525/2024), contagem de cada flag e taxas de conciliação.

## Decisões de tratamento

- RS em 2024: sinalizado, nunca excluído. A sensibilidade é feita no cálculo dos momentos.
- Linhas com contagem nula ou negativa, chave nula, segmento ≠ imóveis ou data-base diferente da do arquivo são descartadas, com motivo registrado. Nos dados de 2017-03 a 2026-05, nenhuma linha caiu nessas regras.
- Lacunas não são preenchidas: o mês ausente fica ausente, e a diferença de estoque do mês seguinte fica vazia.

## Testes (`tests/`)

`test_unidades.py` usa dados sintéticos; `test_paineis.py` roda sobre os painéis gerados: ausência de duplicata por chave, contagens não negativas, `ativas` igual à soma das situações, lance + sorteio = total, painel B igual à reagregação do bruto em três trimestres, soma dos grupos igual ao consolidado em todos os administradora × mês.
