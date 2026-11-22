---
secao: 5.4
titulo: Momentos-alvo para calibração
status: rascunho
responsavel:
insumos:
  - results/fatos_momentos.csv
  - results/calibracao_momentos.csv
  - ESTADO.md §4, 2026-11-09 (partição), 2026-11-16 (SMM) e 2026-11-19 (quarto momento)
  - ESTADO.md §5 item 21 (contaminação)
fontes:
  - results/fatos_momentos.csv
  - results/calibracao_momentos.csv
  - results/h2_teste.csv
excecoes:
paginas_alvo: 3
---

# Momentos-alvo para calibração

O método de momentos simulados escolhe os parâmetros do modelo de modo que certas estatísticas da simulação fiquem próximas das mesmas estatísticas nos dados. A escolha dessas estatísticas é a decisão mais importante da calibração, por duas razões. A primeira é de identificação: um momento só serve se responde aos parâmetros que se quer estimar. A segunda é de validação: a hipótese H2 pede que o modelo reproduza momentos que não usou, e isso só tem valor se a separação entre os dois conjuntos foi feita antes de o modelo ser ajustado. Esta seção apresenta a partição, o motivo de cada momento e as ressalvas sobre a independência entre os dois conjuntos.

## A partição

A partição foi registrada no log do projeto em 9 de novembro de 2026, antes do início da calibração e de qualquer cálculo dos momentos de teste no modelo calibrado.

| Momento | Grão | Valor no dado | Papel |
|---|---|---|---|
| Média da fração de lance | administradora × trimestre | 0,7344 | calibração |
| Desvio-padrão da fração de lance | administradora × trimestre | 0,1163 | calibração |
| Mediana da taxa mensal de contemplação | grupo × mês | 0,0051 | calibração |
| Fração dos sorteios que vai a excluídos | administradora × trimestre | 0,734 | calibração (desde 19/11) |
| Spearman entre fração de lance e tamanho dos grupos | administradora × trimestre | 0,3161 | teste de H2 |
| Fração de grupos e meses sem contemplação | grupo × mês | 0,0663 | teste de H2 |

Fontes: `results/fatos_momentos.csv` e `results/calibracao_momentos.csv`.

O vetor de calibração $\mu^{\text{cal}}$ reúne os quatro primeiros; o de teste $\mu^{\text{tes}}$, os dois últimos. Os momentos de calibração descrevem o nível e a dispersão do canal de contemplação e o ritmo total de contemplação. Os de teste descrevem uma relação estrutural entre variáveis, que o modelo não vê diretamente, e uma propriedade da cauda da distribuição da taxa de contemplação.

## Por que estes momentos

**Média da fração de lance.** É o momento que mais responde ao comportamento de lance. Com mais intensidade de lance (maior $\phi_0$), mais participantes ofertam, mais vagas são preenchidas pelo lance, e a fração sobe.

**Desvio-padrão entre administradoras.** É a contrapartida do fato 1 da seção 5.3: o modelo deve gerar a diferença entre administradoras, e não só o nível médio. No modelo revisado, ele responde à fração $\eta$ de administradoras que sorteiam a sobra, porque é essa cláusula que separa administradoras de fração de lance alta e baixa.

**Mediana da taxa de contemplação.** Ancora o ritmo total, que depende do saldo do fundo e, portanto, de quanto as restituições a excluídos consomem. A mediana, e não a média, foi escolhida porque a média é sensível aos meses de contemplação concentrada perto do encerramento.

**Fração dos sorteios que vai a excluídos.** Entrou na calibração em 19 de novembro, junto com a revisão do modelo pelos regulamentos (seção 7.1). Até então, era usada apenas como diagnóstico, fora da partição. É o momento que identifica o teto de restituição $\bar r$, porque esse parâmetro governa quantas excluídas podem ser restituídas por assembleia. A inclusão não tocou os momentos de teste.

**Spearman com o tamanho (teste).** Se o modelo explica a fração de lance pela mecânica do fundo, deve reproduzir sem ajuste a relação entre tamanho do grupo e lance (fato 2 da seção 5.3). É o teste mais exigente disponível, porque nenhum parâmetro do modelo foi desenhado para gerá-la.

**Meses sem contemplação (teste).** Depende da distribuição inteira da taxa mensal, e não da mediana, e reflete ao mesmo tempo a idade dos grupos, o saldo e as regras de sorteio.

## Cálculo nos dois lados

Cada momento é calculado da mesma forma no dado e na simulação, no mesmo grão. A fração de lance simulada é agregada por administradora e trimestre a partir dos grupos simulados de cada administradora, nos mesmos trimestres em que a administradora aparece no painel B; a taxa de contemplação simulada é calculada por grupo e mês, nos mesmos meses em que o grupo aparece no painel A (seção 6.1). Nos dois lados, a média e o desvio-padrão da fração de lance são ponderados pelo número de observações de cada administradora, e a mediana da taxa, pelo peso de cada grupo no painel.

A incerteza amostral de cada momento é estimada por bootstrap de administradoras: as administradoras são reamostradas com reposição, e todas as suas observações, nos dois painéis, entram juntas. A unidade de reamostragem é a administradora porque é nela que está a dependência dos dados. O erro-padrão resultante é de 0,016339 na média da fração de lance, 0,009667 no desvio-padrão, 0,000469 na mediana da taxa e 0,027503 na fração dos sorteios a excluídos (`results/calibracao_momentos.csv`). Os mesmos erros-padrão definem os pesos da função objetivo (seção 6.3) e entram no teste de H2.

## Ressalvas sobre a independência da partição

A partição foi fixada antes do ajuste, mas não antes de qualquer contato do modelo com os dados. Duas ressalvas são declaradas desde já e retomadas nas seções 7.2 e 8.3.

A primeira diz respeito à fração de meses sem contemplação. A primeira rodada do protótipo, em 26 de outubro, já havia mostrado uma distância grande nesse número, e essa distância motivou em parte a revisão das regras de vagas e de exclusão no passo seguinte. O momento está, portanto, parcialmente contaminado: a estrutura do modelo foi ajustada, ainda que indiretamente, para aproximá-lo. O teste de H2 nesse momento é mais fraco que o do Spearman, e a regra de rejeição registra uma versão só com o Spearman (seção 6.5).

A segunda diz respeito à revisão do modelo de 19 de novembro. Ela foi motivada pela leitura dos regulamentos, mas feita depois de conhecido o resultado do teste de H2 da versão anterior, em que o Spearman simulado ficou perto de zero. O teste da versão revisada não é cego, e o valor de $J$ relatado na seção 7.2 deve ser lido com esse desconto.
