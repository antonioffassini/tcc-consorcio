---
secao: 3.3
titulo: Teoria de leilões e desenho de mecanismo
status: rascunho
responsavel:
insumos:
  - refs/pdfs/
fontes:
excecoes:
paginas_alvo: 5
---

# Teoria de leilões e desenho de mecanismo

O lance do consórcio é um leilão de lance fechado em que vários itens idênticos, as cartas de crédito do mês, são disputados ao mesmo tempo, e em que cada vencedor paga o que ofereceu. Esta seção reúne o que a teoria de leilões diz sobre esse formato e sobre a alternativa que o Capítulo 4 examina, o leilão de preço uniforme. Não se pretende uma revisão exaustiva da área, apenas os fundamentos que o modelo usa.

## Primeiro preço e segundo preço

A comparação entre os formatos de leilão começa com Vickrey [-@vickrey1961counterspeculation]. Para um único item indivisível, o autor mostra que o leilão progressivo, em que os lances sobem até restar um interessado, oferece melhores chances de alocação ótima do que o leilão holandês, e sugere que fixar o preço das propostas fechadas no segundo maior lance, e não no maior, poderia melhorar a alocação sem prejudicar o vendedor. A intuição é que, quando o preço não depende do próprio lance, o participante não tem razão para ofertar abaixo do valor que atribui ao item; quando depende, ele sombreia o lance, e a ordem dos lances pode deixar de refletir a ordem dos valores.

No consórcio vigente, o vencedor paga o próprio lance, como num leilão de primeiro preço. O leilão de preço uniforme examinado neste trabalho, em que todos os vencedores do mês pagam o primeiro lance recusado, é a extensão do leilão de segundo preço a vários itens. A analogia com o resultado de Vickrey, porém, é limitada por duas diferenças. Os participantes do consórcio disputam a mesma carta em várias assembleias, e quem perde hoje volta a ofertar no mês seguinte, de modo que o lance de cada mês é parte de uma estratégia dinâmica. E o número de itens leiloados em cada mês depende do próprio leilão, porque o lance pago entra no fundo e financia novas contemplações. Por isso, as propriedades do leilão estático não se transferem diretamente, e a comparação exige simulação (seção 4.3).

## Aprendizado e desenho de leilões

Uma linha recente usa algoritmos de aprendizado para estudar e desenhar leilões. Banchio e Skrzypacz [-@banchio2022artificial] simulam leilões repetidos disputados por algoritmos de Q-learning e mostram que, no leilão de primeiro preço, os algoritmos convergem para lances abaixo dos valores, um resultado colusivo tácito, enquanto no de segundo preço isso não ocorre; a diferença vem do incentivo, no primeiro preço, a cobrir o rival por um único incremento. Mostram também que informar o menor lance vencedor torna o leilão mais competitivo. Esse resultado motiva duas escolhas deste trabalho: o estado observado pelos agentes inclui o lance de corte da assembleia anterior (seção 6.2), e a comparação entre os formatos é refeita com agentes que aprendem (seção 7.6).

Em outra direção, Dütting e coautores [-@dutting2019optimal] modelam o próprio leilão como uma rede neural e tratam o desenho ótimo como um problema de aprendizado com restrições, recuperando as soluções analíticas conhecidas e obtendo mecanismos novos onde a solução ótima é desconhecida. Zheng e coautores [-@zheng2022ai] propõem um arcabouço de dois níveis em que agentes e planejador se adaptam um ao outro, aplicado ao desenho de tributação. Este trabalho não chega a esse ponto: os desenhos comparados são escolhidos numa família finita e admissível pela regulação, e o aprendizado é usado apenas do lado dos participantes. A busca automática de desenhos fica como extensão.
