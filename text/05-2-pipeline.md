---
secao: 5.2
titulo: Pipeline de extração e consolidação
status: rascunho
responsavel:
insumos:
  - src/pipeline
  - src/pipeline/README.md
  - tests/test_paineis.py, tests/test_unidades.py
  - ESTADO.md §5 itens 6, 14 a 17
fontes:
  - results/qualidade_dados.csv
excecoes:
  - 285
  - 381
  - 525
  - 3.679
paginas_alvo: 4
---

# Pipeline de extração e consolidação

Os arquivos do Bacen chegam como zips mensais e trimestrais, em CSV com separador ponto e vírgula, decimal com vírgula e codificação Latin-1. O pipeline (`src/pipeline/`) lê esses arquivos sem nunca alterá-los, aplica regras de validade explícitas, gera os dois painéis do trabalho e um relatório de qualidade em formato longo (`results/qualidade_dados.csv`). Esta seção descreve as decisões de tratamento, porque cada uma delas muda algum número dos capítulos seguintes.

## Princípios

Três regras orientam o pipeline. A primeira é que o dado bruto é imutável: `data/raw/` só é lido, e tudo o que deriva dele fica em `data/processed/`, que pode ser apagado e regenerado. A segunda é que nenhuma observação é descartada por suspeita: linhas com problema conhecido recebem uma sinalização e permanecem no painel, e a decisão de excluí-las, quando houver, é tomada no cálculo do momento e registrada ali. A terceira é que lacunas não são preenchidas: o mês que falta para um grupo continua faltando, e a diferença de estoque do mês seguinte fica vazia, em vez de ser imputada.

## Leitura e validação

O leiaute dos arquivos mudou em março de 2017, com a adoção do dicionário de campos ainda vigente; as séries anteriores, que seguem a codificação da Carta Circular n. 3.679/2014, não são lidas. A partir daí, o pipeline confere o cabeçalho de cada arquivo contra o dicionário. Nenhum arquivo teve cabeçalho divergente, nem antes nem depois da mudança da remessa promovida pela Instrução Normativa BCB n. 525/2024 (`results/qualidade_dados.csv`, escopo `leiaute`). Também não falta nenhum arquivo mensal nem trimestral no período.

As regras de validade descartam linhas com contagem nula ou negativa, chave nula, segmento diferente de imóveis ou data-base diferente da do arquivo. Nenhuma linha caiu nessas regras em todo o período; o relatório registra, por arquivo, linhas lidas, células nulas, duplicatas por chave e linhas aproveitadas, e não há duplicata em nenhum dos dois painéis.

Como teste de quebra de série que a validação de cabeçalho não pegaria, o pipeline mede a continuidade dos grupos: a fração dos grupos presentes num mês que também estavam presentes no mês anterior. A medida cai quando entram muitos grupos novos ou quando grupos voltam depois de um mês ausente. No regime posterior à Resolução BCB n. 285/2023, ela fica entre 0,97 e 0,99 na maior parte dos meses, sem degrau no fim de 2024, quando a remessa mudou. Há três quedas isoladas: para 0,8521 em maio de 2025 e para cerca de 0,936 em novembro de 2025 e em maio de 2026. A última coincide com a volta, em maio de 2026, de uma administradora que quase desaparecera da remessa de abril; o padrão aponta para remessas incompletas, e não para mudança de leiaute (`results/qualidade_dados.csv`).

## Os dois painéis

**Painel A — grupo e mês.** Chave (administradora, grupo, data-base), segmento de imóveis, a partir de julho de 2024. As cotas ativas são a soma das ativas em dia com as inadimplentes, contempladas ou não, que é a mesma soma que o Bacen usa para ponderar. A taxa de contemplação do grupo no mês é o número de cotas contempladas dividido pelas ativas. O fluxo de exclusões sai da diferença do estoque de excluídas entre meses consecutivos do mesmo grupo. Essa diferença é negativa em parte dos grupos e meses, o que ocorre quando uma cota excluída é recolocada; o painel guarda a diferença bruta e uma versão truncada em zero, e sinaliza os 2.488 casos de diferença negativa. A diferença fica vazia em 1.401 observações cujo mês anterior falta.

**Painel B — administradora e trimestre.** Chave (administradora, data-base), com as UFs somadas. Traz as cotas ativas contempladas no trimestre por lance e por sorteio, a fração de lance e os excluídos contemplados. O regime posterior à Resolução começa em setembro de 2024, primeiro trimestre inteiro sob a nova norma.

## Sinalizações

As observações potencialmente afetadas pelas medidas da Resolução BCB n. 381/2024 para o Rio Grande do Sul são sinalizadas nos dois painéis: no painel A, quando a administradora tem metade ou mais das cotas ativas de imóveis no estado (411 observações); no painel B, por trimestre, com a fração de lance recalculada sem o RS (208 observações). A sensibilidade dos momentos a essas observações é feita no cálculo de cada momento (seção 5.3). Também são sinalizados grupos com assembleias realizadas acima do prazo e com zero cotas ativas.

Há lacunas de remessa. No painel A, 156 chaves de grupo têm meses ausentes entre a primeira e a última aparição, somando 170 períodos faltantes; no painel B, duas administradoras têm trimestres ausentes.

## Conciliação entre fontes

A soma dos grupos de cada administradora bate exatamente com o arquivo consolidado em todos os meses, para cotas contempladas, ativas em dia e estoque de excluídas (fração de coincidência igual a 1). No arquivo por UF, os estoques somados batem com o consolidado em 0,9829 dos casos para as contempladas acumuladas e em 0,9351 para as não contempladas.

O fluxo trimestral é outra história. A soma de lances e sorteios do arquivo por UF no trimestre, comparada à soma de três meses de contempladas nos grupos, dá razão agregada de 1,095 no regime posterior à Resolução, com divergências grandes nos dois sentidos em algumas administradoras (`results/qualidade_dados.csv`). As hipóteses mais prováveis são critérios diferentes de data de contemplação entre as remessas e grupos de imóveis reportados de forma distinta, mas nenhuma foi confirmada. A consequência para o trabalho é uma regra: nenhum momento combina fluxos das duas fontes. Os momentos sobre o canal vêm só do painel B, e os momentos sobre a dinâmica do grupo, só do painel A.

## Reprodutibilidade

O pipeline roda com um comando, `python -m src.pipeline.build_panel --raw data/raw --out data/processed`, em alguns segundos, e é coberto por testes que rodam sobre os painéis gerados: ausência de duplicata por chave, contagens não negativas, ativas iguais à soma das situações, lance mais sorteio igual ao total, painel B igual à reagregação do arquivo bruto e soma dos grupos igual ao consolidado em todos os meses. Testes com dados sintéticos cobrem as funções de diferença de estoque, validação e agregação por UF. O protocolo completo, do dado bruto ao texto, está na seção 6.6.
