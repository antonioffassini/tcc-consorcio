---
secao: 7.1
titulo: Ajuste aos momentos observados
status: rascunho
responsavel:
insumos:
  - results/
  - ESTADO.md §4, 2026-11-15 a 2026-11-22; §5 itens 19 a 28, 31 e 34
fontes:
  - results/calibracao_momentos.csv
  - results/calibracao_theta.csv
  - results/calibracao_config.csv
  - results/versoes_modelo.csv
  - results/sim_heterogeneidade.csv
  - results/sim_forma_heterogeneidade.csv
  - results/arquivo_2026-11-16/calibracao_theta.csv
excecoes:
  - 0,2
  - 14.6
  - 2,5
  - 97,5
  - 35.1
  - 0,5
  - 172
paginas_alvo: 4
---

# Ajuste aos momentos observados

Esta seção apresenta o resultado da calibração do modelo e o caminho que levou até ele. O caminho importa: o modelo calibrado aqui é a quarta versão do simulador, e as anteriores foram abandonadas ou revistas por motivos que os próprios dados, os contratos ou a plausibilidade econômica indicaram. Registrar esses motivos é parte do resultado, porque mostra quais suposições os agregados do Bacen são capazes de rejeitar.

## O modelo calibrado

A Tabela 7.1 compara os quatro momentos de calibração nos dados e no modelo calibrado. A coluna da superfície é o valor que a minimização viu; a da simulação direta é o valor obtido rodando o simulador no ponto calibrado, sem interpolação. A última coluna mede a distância da simulação direta ao dado em erros-padrão do dado.

**Tabela 7.1 — Momentos de calibração no ponto calibrado**

| Momento | Dado | Erro-padrão | Superfície | Simulação direta | Distância (ep) |
|---|---|---|---|---|---|
| Média da fração de lance | 0,7344 | 0,0163 | 0,7327 | 0,7419 | 0,46 |
| Desvio-padrão da fração de lance | 0,1163 | 0,0097 | 0,1254 | 0,1215 | 0,53 |
| Mediana da taxa mensal de contemplação | 0,00506 | 0,00047 | 0,00553 | 0,00556 | 1,06 |
| Fração dos sorteios a excluídos | 0,7342 | 0,0275 | 0,7324 | 0,7404 | 0,22 |

Fonte: elaborado pelos autores (`results/calibracao_momentos.csv`).

Três momentos ficam a menos de um erro-padrão do dado, e a mediana da taxa mensal de contemplação, a pouco mais de um. A função objetivo vale 1,902 na superfície e 1,670 na simulação direta (`results/calibracao_config.csv`); com quatro momentos e três parâmetros, um valor dessa ordem corresponde a um ajuste compatível com o erro amostral dos dados. A diferença entre superfície e simulação direta é pequena perto dos erros-padrão, o que indica que a interpolação não distorce o ponto calibrado. O desvio que resta tem direção: o modelo contempla um pouco mais por mês do que os dados.

**Tabela 7.2 — Parâmetros calibrados**

| Parâmetro | Estimativa | Erro-padrão total | Percentil 2,5 | Percentil 97,5 |
|---|---|---|---|---|
| $\phi_0$ (intercepto da política) | −0,0508 | 0,0429 | −0,0725 | 0,0807 |
| $\phi_1$ (peso da urgência) | 0,5733 | 0,1427 | 0,2522 | 0,8598 |
| $\bar r$ (teto de restituição, em créditos) | 0,1584 | 0,0312 | 0,0999 | 0,2085 |

Fonte: elaborado pelos autores (`results/calibracao_theta.csv`). Percentis do bootstrap de cem reamostragens de administradoras; erro-padrão total combina bootstrap e variação entre réplicas.

$\hat\phi_0$ é negativo e próximo de zero: só os participantes com urgência suficiente, ou perto do fim do grupo, ofertam lance. O valor não tem interpretação isolada, porque depende de $\phi_1$ e $\phi_2$.

$\hat\phi_1$ está identificado, com intervalo afastado de zero. Ele mede quanto a urgência separa quem oferta de quem não oferta, e é informado sobretudo pelo desvio-padrão da fração de lance entre administradoras. O valor fica perto de 0,5, que é o peso que reproduziria, na escala atual da urgência, exatamente o comportamento da versão anterior do modelo: os dados não pedem uma política diferente, só uma escala de urgência com leitura financeira plausível.

$\hat{\bar r}$ indica que, além da restituição garantida, cada assembleia restitui excluídos até cerca de 0,158 crédito. O parâmetro está bem identificado e é ele que permite ao modelo reproduzir o peso dos excluídos no uso do fundo. O valor é da mesma ordem do limite que um dos regulamentos fixa, de 20% do menor crédito do grupo por assembleia [@portoseguro2025regulamento, art. 35.1], sem que esse limite tenha sido imposto à calibração.

## Do protótipo ao modelo revisado

O modelo da Tabela 7.1 é o quarto; as três primeiras versões são as da Tabela 7.3. A Tabela 7.3 mostra os mesmos momentos nas três versões: o protótipo de 26 de outubro, o modelo calibrado de 16 de novembro e o modelo revisado de 19 de novembro. As duas últimas linhas são momentos de teste, discutidos na seção 7.2, e aparecem aqui porque foram eles que motivaram a última revisão.

**Tabela 7.3 — Momentos nas três versões do modelo**

| Momento | Dado | Protótipo (26/10) | Modelo de 16/11 | Modelo revisado (19/11) |
|---|---|---|---|---|
| Média da fração de lance | 0,7344 | 0,7672 | 0,7384 | 0,7420 |
| Dispersão da fração de lance | 0,1163 | 0,0125 | 0,1173 | 0,1247 |
| Mediana da taxa de contemplação | 0,0051 | 0,0049 | 0,00512 | 0,00551 |
| Fração dos sorteios a excluídos | 0,7342 | 0,3567 | não calibrada | 0,7397 |
| Spearman lance × tamanho (teste) | 0,3161 | não calculado | 0,0212 | 0,5320 |
| Meses sem contemplação (teste) | 0,0663 | 0,1795 | 0,0398 | 0,0531 |

Fonte: `results/versoes_modelo.csv`. No protótipo, a dispersão é entre grupos, e não entre administradoras, e a fração dos sorteios a excluídos foi calculada na rodada de 15 de novembro com as regras do protótipo (`results/sim_heterogeneidade.csv`).

Seis suposições caíram entre a primeira e a terceira versão, e três entre a terceira e a quarta. O Quadro 7.1 as reúne, com o sinal que as denunciou e o que mudou.

**Quadro 7.1 — Suposições revistas**

| Suposição | Como o problema apareceu | Correção |
|---|---|---|
| Grupo fechado, simulado da formação ao encerramento | 0,1795 de meses sem contemplação no protótipo, contra 0,0663; o painel mostra exclusão concentrada no início e vagas recolocadas | Grupo aberto, com recolocação; exclusão por faixa de idade; grupos simulados nas idades observadas |
| Dispersão entre administradoras vinda só dos tipos | Dispersão de 0,0125 entre grupos, contra 0,1163 entre administradoras | Camada de heterogeneidade contratual por administradora (seção 4.2) |
| Número fixo de sorteios por administradora | No nível que dá a média, essa forma já gera dispersão acima da observada, sem espaço para heterogeneidade | Forma descartada antes da calibração (`results/sim_forma_heterogeneidade.csv`) |
| Ativas e excluídas no mesmo sorteio | Só 0,3567 dos sorteios iam a excluídos, contra 0,7342 | Sorteio de excluídas separado, com teto $\bar r$, como em três dos quatro regulamentos |
| Sorteios por assembleia proporcionais à capacidade do grupo; sobra sem sorteio | Spearman simulado de 0,0212 no teste de 16/11, contra 0,3161; nenhum regulamento fixa número de sorteios | Um sorteio previsto; heterogeneidade passa ao destino da sobra |
| Teto do embutido de 25% do crédito | Leitura dos regulamentos | 30%, como nos dois que o fixam (Itaú, cl. 14.6; Santander) |
| Mediana da urgência igual a 1 | Equivale a descontar a espera a cerca de 172% ao ano | Mediana 0,2, cerca de 22% ao ano (seção 4.2) |
| Fração de administradoras que sorteiam a sobra calibrada | Bootstrap de 0 a 1: não identificada | Cláusula tirada dos regulamentos; $\eta_0$ para as demais (seção 4.2) |
| Peso da urgência na política fixo | Grau de liberdade liberado pela saída de $\eta$ | $\phi_1$ calibrado (Tabela 7.2) |

Fontes: `results/versoes_modelo.csv`, `results/sim_heterogeneidade.csv`, `results/sim_forma_heterogeneidade.csv`.

A primeira e a segunda correção vieram dos fatos estilizados e da primeira rodada, antes da calibração. A terceira foi decidida só com momentos de calibração. As três últimas vieram de outro lugar: o modelo de 16 de novembro ajustava os momentos de calibração quase exatamente, e foi o teste fora da amostra que mostrou um problema. O Spearman simulado perto de zero indicava que a regra de vagas proporcional à capacidade anulava, por construção, a relação entre tamanho do grupo e lance: se o número de sorteios cresce com o tamanho, o saldo que sobra para o lance não cresce. A suspeita levou à leitura dos regulamentos de cinco administradoras, que mostrou três divergências entre o modelo e a prática contratual. Com o modelo revisado, o Spearman simulado passa a 0,5320: excede o dado, mas tem o sinal e a ordem de grandeza certos.

Dois erros de implementação foram corrigidos no mesmo período, sem efeito sobre os resultados. Uma mudança na regra de parcela, que a recalculava a cada assembleia, quebrou o teste que exige a contemplação de todas as cotas até o encerramento, e foi revertida para a parcela fixa da seção 4.1. A interpolação da superfície propagava valores ausentes de um nó para os vizinhos; corrigida, a recalibração deu o mesmo ponto.

O episódio tem uma consequência metodológica que a seção 7.2 trata com cuidado: a revisão de 19 de novembro foi motivada pelos regulamentos, mas feita depois de conhecido o resultado do teste de 16 de novembro. O teste do modelo revisado não é cego. Os resultados da versão de 16 de novembro ficaram arquivados (`results/arquivo_2026-11-16/`), e essa versão é mantida como análise de sensibilidade da comparação entre mecanismos (seção 7.5).
