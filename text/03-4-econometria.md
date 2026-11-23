---
secao: 3.4
titulo: Econometria estrutural com dados incompletos
status: rascunho
responsavel:
insumos:
  - refs/pdfs/
fontes:
excecoes:
paginas_alvo: 4
---

# Econometria estrutural com dados incompletos

Avaliar uma regra de alocação que nunca foi aplicada exige um modelo do comportamento dos participantes, e o modelo precisa ser ajustado aos dados disponíveis. Esta seção trata de duas tradições que lidam com esse problema: a econometria estrutural de leilões, que recupera as preferências a partir dos lances observados, e a estimação por momentos simulados, que ajusta um modelo de simulação a estatísticas agregadas.

## Identificação a partir dos lances

A econometria estrutural de leilões parte da hipótese de que os lances observados são estratégias de equilíbrio e inverte a função de lance para recuperar a distribuição dos valores. Guerre, Perrigne e Vuong [-@guerre2000optimal] mostram que, no leilão de primeiro preço com valores privados independentes, a distribuição dos valores é identificada sem hipótese paramétrica a partir dos lances e do número de participantes, e propõem um estimador em dois passos com a taxa ótima de convergência. Athey e Haile [-@athey2002identification] estendem a análise a vários formatos de leilão e estruturas de informação e mostram que a identificação depende do que se observa: o modelo mais simples é identificado mesmo quando só o preço de cada leilão é observado, mas modelos mais ricos exigem a identidade dos vencedores, mais de um lance por leilão ou variação exógena no número de participantes. Campo e coautores [-@campo2011semiparametric] tratam o caso de ofertantes avessos ao risco, em que o modelo geral não é identificado, e propõem uma identificação semiparamétrica. Aradillas-López, Gandhi e Quint [-@aradillas2013identification] usam a variação no número de participantes para obter limites identificados quando os valores são correlacionados.

O que essa literatura tem em comum é observar lances, ao menos o lance vencedor de cada leilão. Os dados públicos do consórcio não trazem nenhum lance: informam quantas cotas foram contempladas por sorteio e por lance em cada grupo e administradora, mas não quanto se ofertou. A inversão da função de lance não é, portanto, aplicável, e é preciso outra forma de ligar o modelo aos dados.

## Momentos simulados

A estimação por momentos simulados resolve esse problema quando o modelo pode ser simulado, mas não tem expressão analítica para as estatísticas que se observam. McFadden [-@mcfadden1989method] propõe substituir, num estimador de momentos, as probabilidades que exigiriam integração numérica por estimativas obtidas por simulação de Monte Carlo, e mostra que o estimador continua consistente e assintoticamente normal sem que cada probabilidade seja estimada com precisão, porque o erro de simulação é controlado pela lei dos grandes números entre observações. Duffie e Singleton [-@duffie1993simulated] estendem o método a modelos dinâmicos de Markov, em que os momentos simulados vêm de trajetórias geradas pelo modelo, e dão as condições de consistência e a distribuição assintótica do estimador. Gouriéroux, Monfort e Renault [-@gourieroux1993indirect] generalizam a ideia na inferência indireta: em vez de momentos escolhidos diretamente, ajusta-se o modelo para que um modelo auxiliar estimado nos dados reais e nos simulados dê resultados próximos, com testes de especificação baseados na mesma construção.

Este trabalho usa a versão mais direta do método. O modelo de simulação do grupo de consórcio gera, para cada vetor de parâmetros, as mesmas estatísticas que o Banco Central publica, e os parâmetros são escolhidos para aproximar as estatísticas simuladas das observadas (seção 6.3). As estatísticas que não entram no ajuste ficam reservadas para um teste de sobreidentificação (seção 7.2), na mesma lógica dos testes de especificação propostos por Gouriéroux, Monfort e Renault.

## A crítica de Lucas

Um modelo ajustado sob a regra vigente pode não servir para prever o que aconteceria sob outra regra, se o comportamento estimado depender da própria regra. É a crítica de Lucas [-@lucas1976econometric] à avaliação de políticas com modelos econométricos cujos parâmetros não são invariantes à política avaliada. No caso deste trabalho, a política de lance é calibrada sob o mecanismo vigente e aplicada sem mudança aos desenhos alternativos na comparação principal (seção 7.4). A crítica é enfrentada de duas formas: com agentes que aprendem a ofertar sob cada desenho (seção 7.6) e com a declaração explícita dessa limitação entre as ameaças à validade (seção 8.3).
