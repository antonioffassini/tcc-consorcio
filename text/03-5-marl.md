---
secao: 3.5
titulo: Aprendizado por reforço multiagente em mercados
status: rascunho
responsavel:
insumos:
  - refs/pdfs/
fontes:
excecoes:
paginas_alvo: 4
---

# Aprendizado por reforço multiagente em mercados

O aprendizado por reforço estuda agentes que aprendem a agir por tentativa e erro, a partir da recompensa que cada ação produz. Esta seção apresenta o método usado neste trabalho, os problemas que surgem quando vários agentes aprendem ao mesmo tempo e os precedentes de seu uso em mercados e leilões.

## Q-learning

O Q-learning, formalizado por Watkins e Dayan [-@watkins1992qlearning], é um método incremental de programação dinâmica em que o agente melhora, a cada experiência, sua estimativa do valor de cada ação em cada estado. Os autores provam que, num ambiente markoviano, as estimativas convergem para os valores ótimos com probabilidade um, desde que todas as ações sejam repetidamente experimentadas em todos os estados e os valores sejam representados de forma discreta. É essa forma tabular, com estados e ações discretos, que este trabalho usa (seção 6.2).

## Vários agentes aprendendo juntos

Quando vários agentes aprendem no mesmo ambiente, a garantia de convergência do caso de um agente deixa de valer, porque o ambiente que cada agente enfrenta muda à medida que os outros aprendem. Busoniu, Babuska e De Schutter [-@busoniu2008comprehensive], numa revisão do aprendizado por reforço multiagente, mostram que a própria definição do objetivo do aprendizado é controversa e identificam dois focos: a estabilidade da dinâmica de aprendizado e a adaptação ao comportamento cambiante dos demais. Hernandez-Leal, Kartal e Taylor [-@hernandezleal2019survey] revisam a extensão desses métodos ao aprendizado profundo, e Canese e coautores [-@canese2021multiagent] comparam os algoritmos multiagente segundo a não estacionariedade, a escalabilidade e a observabilidade. Os três trabalhos sustentam as escolhas da seção 6.2: tabela compartilhada pela população de cotas, critério de convergência que só se aplica depois que a exploração chega ao piso, e verificação da estabilidade da política aprendida em mais de uma semente.

## Aprendizado como modelo de comportamento

O aprendizado por reforço também é usado para descrever como pessoas jogam. Erev e Roth [-@erev1998predicting] examinam experimentos de longa duração com jogos de equilíbrio único em estratégias mistas e mostram que mesmo um modelo de aprendizado por reforço de um parâmetro prevê o comportamento melhor do que o equilíbrio, tanto no ajuste quanto na previsão de experimentos não usados na estimação. O resultado justifica tratar o lance aprendido como hipótese de comportamento, a ser comparada com a previsão da teoria estática (hipótese H1).

## Precedentes em mercados

Calvano e coautores [-@calvano2020artificial] estudam algoritmos de Q-learning que fixam preços num oligopólio com competição repetida e mostram que eles aprendem a cobrar preços acima dos competitivos sem se comunicar, sustentados por estratégias de punição finita seguida de retorno gradual à cooperação; o resultado é robusto a assimetrias, ao número de participantes e a várias formas de incerteza. Os mesmos autores estendem a análise a um ambiente de monitoramento imperfeito, em que as empresas não observam perfeitamente as quantidades das rivais [@calvano2021imperfect]. No caso de leilões, o trabalho de Banchio e Skrzypacz [-@banchio2022artificial], discutido na seção 3.3, é o precedente mais próximo, porque compara formatos de leilão com agentes que aprendem.

Este trabalho difere desses precedentes em dois pontos. Os agentes não são empresas que disputam um mercado, mas cotas de um grupo de consórcio que disputam a ordem de recebimento de um crédito que todas recebem ao final. E o objetivo não é investigar se os agentes coludem, mas verificar se a ordenação dos desenhos obtida com comportamento fixo sobrevive quando o comportamento se adapta à regra, que é a forma computacional de enfrentar a crítica de Lucas (seção 3.4).

## Alinhamento de modelos

Uma última referência metodológica vem da simulação baseada em agentes. Axtell e coautores [-@axtell1996aligning] propõem o alinhamento, ou *docking*, de modelos computacionais: verificar se duas implementações independentes produzem os mesmos resultados, como base para experimentos críticos. A verificação e a validação de modelos de simulação, em geral, seguem a sistematização de Sargent [-@sargent2015introductory]. Este trabalho aplica as duas ideias nas seções 6.4 e 6.5.
