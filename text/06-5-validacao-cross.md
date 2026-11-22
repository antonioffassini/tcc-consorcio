---
secao: 6.5
titulo: Validação II: sobre-identificação
status: rascunho
responsavel:
insumos:
  - results/overid
  - ESTADO.md §4, 2026-11-16 (critério de rejeição de H2) e 2026-11-09 (projeto do jogo como segunda implementação)
  - src/analysis/calibracao.py (momentos_teste, h2)
  - src/sim/docking.py
fontes:
  - results/h2_teste.csv
excecoes:
  - 5,99
  - 2,24
  - 1,96
paginas_alvo: 3
---

# Validação II: sobre-identificação

A validação da seção 6.4 pergunta se o simulador faz o que diz fazer. Esta seção trata de duas perguntas diferentes. A primeira é se o modelo calibrado descreve os dados além daquilo que foi usado para ajustá-lo — a hipótese H2. A segunda é se o resultado depende da implementação, isto é, se outra equipe, escrevendo outro código a partir da mesma especificação, chegaria aos mesmos números. A primeira é respondida pelo teste de sobre-identificação; a segunda, pela comparação com uma implementação independente (*docking*). O protocolo das duas foi fixado antes dos resultados, e os resultados estão na seção 7.2.

## O teste de H2

Os momentos de teste $\mu^{\text{tes}}$ são a correlação de Spearman entre fração de lance e tamanho dos grupos e a fração de grupos e meses sem contemplação (seção 5.4). A diferença entre simulado e dado é

$$
\Delta = \tilde\mu^{\text{tes}}(\hat\Theta) - \hat\mu^{\text{tes}}.
$$

Os dois momentos são simulados de forma diferente, porque dependem de coisas diferentes. A fração sem contemplação é uma média sobre grupos e meses e é calculada como esperança sobre a cláusula contratual, pela mesma mistura da calibração. O Spearman, ao contrário, depende de quais administradoras têm qual cláusula: uma correlação entre administradoras não é a média das correlações de cada nível. Por isso ele é calculado em quinhentas realizações da cláusula por administradora, sorteadas com a probabilidade calibrada, cada uma correlacionando as frações simuladas por administradora e trimestre com o tamanho observado dos grupos, e o valor simulado é a média das realizações.

A incerteza de $\Delta$ tem três fontes, somadas na covariância $\Sigma$: a do dado, estimada pelo mesmo bootstrap de administradoras da calibração; a de simulação, pela variação entre as três réplicas; e a de $\hat\Theta$, pela variação de $\tilde\mu^{\text{tes}}$ ao longo das estimativas do bootstrap de calibração. A última é a que costuma ser esquecida: um teste que ignore a incerteza dos parâmetros rejeita mais do que deveria.

## A regra de decisão

A regra foi registrada no log do projeto em 16 de novembro, antes de qualquer momento de teste ser calculado no modelo calibrado. A estatística é a de Wald,

$$
J = \Delta^\top \Sigma^{-1} \Delta,
$$

comparada à distribuição qui-quadrado com dois graus de liberdade: **H2 é rejeitada se $J$ > 5,99**, nível de 5%. Para cada momento, relata-se também a razão entre a diferença e seu erro-padrão, com limiar de Bonferroni de 2,24.

Três cláusulas adicionais foram fixadas junto com a regra. Como a fração sem contemplação está parcialmente contaminada (seção 5.4), registrou-se uma regra secundária só com o Spearman, com rejeição se a razão passar de 1,96 em módulo; se as duas regras divergirem, o texto relata as duas e não escolhe a mais favorável. Se o Spearman simulado tiver sinal oposto ao do dado, isso conta como rejeição qualitativa, mesmo com $J$ abaixo do limiar. E não rejeitar não equivale a confirmar: junto com o teste, relata-se a menor diferença que ele detectaria com poder de 80%, para que se saiba o que o teste é capaz de ver.

Na versão do modelo revisada em 19 de novembro, a mesma regra foi aplicada sem alteração. Como a revisão foi feita depois de conhecido o resultado da versão anterior, o segundo teste não é cego, e isso é declarado ao lado do resultado (`results/h2_teste.csv`, coluna de observação).

## Docking com o jogo em Java

A segunda implementação é o motor do jogo educacional desenvolvido pelos autores na disciplina de Laboratório de Programação Orientada a Objetos, escrito em Java, com outra arquitetura e outro gerador de números aleatórios, a partir da mesma especificação do modelo. A única ponte entre as duas é um formato de troca em JSON, chamado `docking-1`: o arquivo de entrada traz os parâmetros do grupo, o mecanismo e uma lista de sementes; cada implementação roda o grupo uma vez por semente e grava, para cada uma, as contemplações por canal, as restituições, a fração de lance, a taxa mediana de contemplação, a fração de meses sem contemplação, a média e o desvio-padrão da espera, os lances pagos e o balanço do fundo, além das médias e desvios entre sementes.

Como os geradores aleatórios diferem, a comparação não pode ser número a número. O critério é de distribuição: para cada métrica e cada configuração de teste, as médias entre sementes das duas implementações não podem diferir mais do que o erro de simulação permite. [RESULTADO PENDENTE: critério numérico do docking, fixado antes de rodar o lado Java, e configurações de teste] O lado Python da interface está implementado e testado: a saída pelo arquivo é igual à simulação direta, e parâmetros desconhecidos ou mecanismos inválidos são recusados. [RESULTADO PENDENTE: resultados do docking, depende do motor Java]

O docking não valida o modelo contra a realidade; valida o código contra a especificação. Um erro de modelagem compartilhado pelas duas implementações passa por ele. O que ele pega é o erro de implementação, como os dois que a bateria de testes encontrou durante o desenvolvimento e que a seção 7.1 registra.
