---
secao: 5.3
titulo: Fatos estilizados
status: rascunho
responsavel:
insumos:
  - results/fatos_momentos.csv
  - results/parametros_fixos.csv
  - results/g1_identificacao.csv
  - ESTADO.md §5 itens 8, 9, 15, 18, 20 e 22
fontes:
  - results/fatos_momentos.csv
  - results/parametros_fixos.csv
  - results/g1_identificacao.csv
  - results/calibracao_momentos.csv
excecoes:
  - 285
paginas_alvo: 5
---

# Fatos estilizados

Antes de construir o modelo, convém saber o que ele precisa reproduzir. Esta seção reúne seis regularidades dos dados do Bacen no regime posterior à Resolução BCB n. 285/2023, segmento de imóveis. Todas foram calculadas por código sobre os painéis da seção 5.2 (`src/analysis/momentos.py`), e cada número citado está em `results/fatos_momentos.csv`, salvo indicação contrária. Parte delas vira momento de calibração ou de teste (seção 5.4); as demais orientam a especificação do Capítulo 4.

## 1. O lance domina a contemplação, mas com intensidade muito diferente entre administradoras

Entre as 305 observações de administradora e trimestre com ao menos 30 contemplações de ativas, a fração das contemplações que ocorre por lance tem média de 0,7344 e desvio-padrão de 0,1163, e vai de 0,125 a 0,9663. Ponderada pelo número de contemplações, a fração agregada é 0,7991: as administradoras maiores contemplam mais por lance. Sem o Rio Grande do Sul, a média passa a 0,7442, diferença pequena perto da dispersão.

O dado mais importante é onde está essa dispersão. A variância total da fração de lance é 0,0135, e a variância das médias por administradora é 0,0127; dentro de cada administradora, de um trimestre para outro, resta 0,0008. Cerca de 94% da variação está, portanto, entre administradoras. O teste de Kruskal-Wallis da fração de lance por administradora dá estatística 282,4 entre as 49 administradoras com dois ou mais trimestres (`results/g1_identificacao.csv`). Esse fato motivou o teste de identificação do projeto (G1) e a camada de heterogeneidade contratual da seção 4.2: se cada administradora tem um nível próprio e estável, alguma coisa estável distingue as administradoras, e a candidata natural é a cláusula do contrato.

[RESULTADO PENDENTE: figura com a distribuição da fração de lance por administradora, ordenada pela média]

## 2. Administradoras de grupos maiores contemplam mais por lance; o prazo não importa

A correlação de Spearman entre a fração de lance da administradora no trimestre e o tamanho mediano dos seus grupos é 0,3161. Com o prazo mediano, é −0,0085, isto é, nenhuma. A relação com o tamanho tem uma leitura mecânica simples: num grupo maior, a arrecadação mensal cobre mais créditos, mas o sorteio previsto continua sendo um só por assembleia, de modo que o saldo que sobra para o lance cresce com o tamanho do grupo. Que essa leitura seja suficiente para reproduzir a correlação é justamente o que o teste de H2 verifica, e por isso o número fica fora da calibração (seção 5.4).

Uma leitura exploratória anterior ao pipeline havia dado correlação maior, com outra medida de tamanho. Vale o número do pipeline; o registro da diferença fica no log do projeto.

## 3. Contemplar é raro e irregular no nível do grupo

No painel por grupo, com 57.084 observações de grupo e mês com cotas ativas, a taxa mensal de contemplação — cotas contempladas no mês sobre cotas ativas — tem mediana de 0,0051, quartis de 0,003 e 0,0078 e percentil 90 de 0,0101; a média é 0,0057. Em 0,0663 dos grupos e meses não há contemplação nenhuma.

A ordem de grandeza é a esperada. Se todas as cotas fossem contempladas de modo uniforme até o encerramento, a taxa mensal seria da ordem do inverso do prazo, e os prazos longos típicos de imóveis levam a uma taxa dessa ordem. O que a média esconde é que a contemplação se distribui de forma desigual ao longo da vida do grupo, como mostra o fato 5.

## 4. Os excluídos pesam no fundo

A maior parte dos sorteios não vai a cotas ativas. No painel por trimestre, os excluídos contemplados representam 0,734 da soma entre eles e as ativas contempladas por sorteio (`results/calibracao_momentos.csv`). O arquivo não informa o canal da contemplação do excluído, mas o excluído não oferta lance, de modo que essa razão é a fração dos sorteios que vai a excluídos, para restituição. A coincidência numérica com a fração de lance do fato 1 é só coincidência: são razões entre contagens diferentes. A taxa de exclusão no painel por grupo tem mediana de 0,0086 e média de 0,025 ao mês, maior que a de contemplação; a distância entre mediana e média indica meses concentrados de exclusão em alguns grupos.

O fato tem duas consequências. A primeira é que o estoque de excluídos é grande o bastante para disputar o fundo com as ativas, e a ordem entre o sorteio de ativas e o de excluídas importa. A segunda é que um modelo em que excluídos e ativas disputassem o mesmo sorteio uniforme, como no protótipo do trabalho, só reproduziria esse número se os excluídos fossem muito mais numerosos que as ativas. A seção 7.1 mostra como esse fato, inicialmente usado só como diagnóstico, levou à revisão da regra de sorteio das excluídas.

## 5. A exclusão se concentra no início, e o grupo é aberto

O risco mensal de uma cota ativa ser excluída cai de forma acentuada com a idade do grupo (`results/parametros_fixos.csv`):

| Faixa de idade (assembleia sobre prazo) | Risco mensal de exclusão |
|---|---|
| até 0,1 | 0,03797 |
| 0,1 a 0,2 | 0,02408 |
| 0,2 a 0,3333 | 0,01542 |
| 0,3333 a 0,5 | 0,00769 |
| 0,5 a 0,6667 | 0,0037 |
| 0,6667 a 1,0 | 0,00137 |

A exclusão é um fenômeno dos primeiros anos do grupo: quem permanece passa a pagar com regularidade. Ao mesmo tempo, o número de cotas ativas dentro de cada grupo fica estável de um mês para o outro, porque as vagas excluídas são recolocadas para novos participantes. No primeiro terço do prazo, a reposição líquida de vagas equivale a 1,2388 vez as exclusões (`results/parametros_fixos.csv`). O grupo de consórcio real é, portanto, aberto: convivem nele participantes que entraram em momentos diferentes. É esse fato que dá sentido ao desenho $M_1$ da seção 4.3.

## 6. A taxa de contemplação depende da idade do grupo

A mediana da taxa mensal de contemplação é 0,0046 no primeiro terço do prazo, 0,0067 no terço do meio e 0,0033 no último. A queda no fim tem explicação direta: perto do encerramento, boa parte dos grupos já contemplou todas as cotas ativas, e os meses sem contemplação se acumulam. O painel, porém, é concentrado em grupos jovens, e a maior parte das observações está no primeiro terço. Um modelo que simulasse a vida inteira de cada grupo e comparasse o resultado com o painel atribuiria peso excessivo ao fim do prazo; por isso os momentos simulados são calculados nos meses e idades em que cada grupo aparece nos dados (seção 6.1).

## O que os fatos pedem do modelo

Lidos em conjunto, os fatos fixam quatro exigências. O modelo precisa de uma fonte de diferença estável entre administradoras (fato 1); precisa gerar mais lance onde o grupo é maior, sem que isso seja imposto (fato 2); precisa reproduzir o peso dos excluídos no uso do fundo (fato 4); e precisa representar o grupo aberto, com exclusão concentrada no início e recolocação das vagas (fato 5). As três primeiras orientam a escolha dos momentos; a última é atendida diretamente pelos parâmetros estimados no painel, sem passar pela calibração.
