---
secao: 6.1
titulo: Arquitetura da simulação
status: rascunho
responsavel:
insumos:
  - src/sim (grupo.py, regras.py, painel.py, docking.py)
  - src/analysis (calibracao.py, comparacao.py)
  - ESTADO.md §4, 2026-11-15 (simulação no grão do painel; mistura) e 2026-11-16 (desenho numérico)
fontes:
  - results/sim_heterogeneidade.csv
  - results/h3_config_sobra.csv
  - results/calibracao_config.csv
excecoes:
  - 7919
  - 285
paginas_alvo: 4
---

# Arquitetura da simulação

O simulador foi escrito em Python, com NumPy para a aritmética vetorizada dentro de cada assembleia, e organizado em camadas que podem ser testadas separadamente. Esta seção descreve as camadas, o laço de simulação, o tratamento dos números aleatórios e o modo como um conjunto de grupos simulados é posto ao lado do painel do Bacen.

## Camadas

**Grupo (`src/sim/grupo.py`).** A função `simula` recebe os parâmetros de um grupo e uma semente e executa a sequência de assembleias da seção 4.1, do início do grupo até o encerramento ou até um horizonte dado. Guarda, por assembleia, as contemplações por sorteio e por lance, as restituições, as cotas pagantes, o saldo e os sorteios que falharam por falta de saldo; por cota, a entrada, a contemplação, o lance pago, a exclusão e a restituição. É a especificação de referência do modelo: o jogo educacional desenvolvido em paralelo, em Java, segue esta implementação e é comparado a ela (seção 6.5).

**Mecanismo (`src/sim/regras.py`).** O mecanismo de contemplação é um objeto com duas partes intercambiáveis, a regra de sorteio das ativas e a regra de lance. $M_0$, $M_1$ e $M_2$ são instâncias desse objeto (seção 4.3). A sequência da assembleia, a restrição de recursos e o sorteio de excluídas ficam fora do mecanismo e não podem ser alterados por ele. Essa separação é o que garante, no código, a condição da seção 4.3 de que os desenhos diferem apenas no que se quer avaliar.

**Desenho e painel (`src/sim/painel.py`).** Monta o conjunto de grupos a simular a partir do painel A e calcula os momentos simulados no mesmo grão dos dados.

**Calibração e comparação (`src/analysis/`).** `calibracao.py` implementa a função objetivo, a superfície de resposta, o bootstrap e o teste de H2 (seções 6.3 e 6.5); `comparacao.py` implementa os critérios da seção 4.4 e a comparação pareada entre mecanismos (seção 7.4).

**Interface de docking (`src/sim/docking.py`).** Recebe um arquivo JSON com parâmetros, mecanismo e sementes, roda o simulador e devolve outro JSON com as métricas por semente e agregadas. É a única ponte entre o simulador do trabalho e a implementação em Java.

## O desenho de grupos

O simulador não gera grupos fictícios. Para cada administradora do painel A no regime posterior à Resolução BCB n. 285/2023, sorteiam-se, com semente fixa, até doze grupos, e cada grupo simulado recebe o prazo, o tamanho e as idades observadas do grupo real correspondente. O grupo é simulado desde a primeira assembleia até a última idade em que aparece no painel, e as saídas são lidas apenas nas assembleias correspondentes aos meses observados. Cada grupo recebe um peso igual ao número de grupos da sua administradora no painel dividido pelo número de grupos sorteados, para que as estatísticas por grupo e mês reproduzam a composição do painel. Uma réplica do desenho tem 543 grupos (`results/sim_heterogeneidade.csv`).

Esse desenho resolve um problema que o protótipo de outubro tinha: simular a vida inteira de grupos-padrão e compará-la com um painel concentrado em grupos jovens. Com as idades copiadas do painel, um grupo de vinte meses é comparado a si mesmo aos vinte meses, e não à média de uma vida de duzentas assembleias.

Os momentos sobre o canal de contemplação são agregados por administradora e trimestre, somando os grupos simulados da administradora nos meses do trimestre e mantendo apenas os pares administradora e trimestre presentes no painel B com ao menos trinta contemplações. Os momentos por grupo e mês usam diretamente as saídas de cada grupo.

## Heterogeneidade contratual por mistura

A cláusula contratual da seção 4.2 é uma variável discreta por administradora: a administradora sorteia ou não a sobra. Sortear essa cláusula a cada avaliação da função objetivo tornaria a função descontínua em $\eta$. O simulador faz outra coisa: roda cada grupo nos dois níveis da cláusula e calcula os momentos como média ponderada dos dois resultados, com pesos $1-\eta$ e $\eta$. A função objetivo fica, assim, contínua e exata em $\eta$, sem simulação adicional para cada valor. No modelo de 16/11, o mesmo artifício era aplicado aos nove níveis de $s_j$, com pesos dados pela massa da lognormal em cada célula da grade. Os momentos de teste e os intervalos, que dependem da realização conjunta das cláusulas entre administradoras, usam realizações sorteadas, e não a mistura (seção 6.5).

## Números aleatórios

Cada grupo do desenho recebe uma semente própria, sorteada uma vez a partir da semente do desenho e guardada com ele. A semente da réplica $r$ é a do grupo somada a 7919 vezes $r$. Com isso, a mesma réplica usa os mesmos números aleatórios em qualquer ponto do espaço de parâmetros e sob qualquer mecanismo, o que tem duas consequências. Na calibração, diferenças na função objetivo entre dois pontos refletem a mudança de parâmetro, e não do sorteio, e a superfície de resposta fica suave. Na comparação entre mecanismos, cada grupo enfrenta a mesma sequência de choques de inadimplência e os mesmos tipos de participantes sob $M_0$, $M_1$ e $M_2$, e a diferença entre mecanismos é medida grupo a grupo, com variância muito menor que a de amostras independentes. O gerador é o PCG64 do NumPy.

A calibração usa três réplicas, cada uma com seu próprio desenho de grupos (sementes de desenho 0, 1 e 2), e a comparação entre mecanismos usa as mesmas três, num total de 1.629 grupos simulados (`results/calibracao_config.csv`; `results/h3_config_sobra.csv`).

## Custo computacional

O laço de simulação é sequencial nas assembleias e vetorizado nas cotas. Os grupos são independentes entre si e rodam em paralelo, distribuídos entre processos. Uma avaliação completa da superfície de calibração exige simular cada grupo do desenho em cada nó da grade e em cada nível da cláusula contratual, para cada réplica. [RESULTADO PENDENTE: tempo de execução da calibração, da comparação e de uma réplica, medido em script e salvo em results/]
