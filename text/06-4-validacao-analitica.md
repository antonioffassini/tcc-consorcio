---
secao: 6.4
titulo: Validação I: casos-limite com solução fechada
status: rascunho
responsavel:
insumos:
  - apêndice A
  - results/validacao
  - tests/test_mecanismos.py, tests/test_simulador.py, tests/test_heterogeneidade.py
fontes:
excecoes:
paginas_alvo: 4
---

# Validação I: casos-limite com solução fechada

A seção 2.5 assumiu um compromisso: antes de usar o simulador onde a literatura não tem solução analítica, mostrar que ele recupera a solução nos casos em que ela existe. Esta seção cumpre o compromisso em parte. Os casos-limite escolhidos verificam a contabilidade do fundo, as regras de alocação e as propriedades conhecidas dos leilões que $M_0$ e $M_2$ generalizam. Todos estão implementados como testes automatizados no repositório e rodam a cada alteração do código; nenhum resultado do Capítulo 7 foi gerado com uma versão do simulador que não passasse em todos eles.

O que a seção não cobre é a comparação entre o comportamento de agentes que aprendem e o equilíbrio de um modelo de leilão repetido com solução fechada. Essa validação não foi feita. Em seu lugar, a hipótese H1 compara o lance aprendido pelos agentes da seção 6.2 com a previsão da teoria estática, no próprio grupo de consórcio (seção 7.3), e a convergência dos agentes é verificada pelo critério registrado na seção 6.2. A comparação com um equilíbrio de leilão repetido em forma fechada fica como extensão.

## Contabilidade e alocação

**Conservação do dinheiro.** Em qualquer configuração — com ou sem lance embutido, inadimplência, exclusão, recolocação, sorteio separado de excluídas e sorteio da sobra, sob qualquer dos três mecanismos —, o total que entrou no fundo por parcelas e lances livres é igual ao total que saiu em créditos e restituições, mais o saldo final. O saldo nunca fica negativo.

**Ritmo sem lance.** Com o número de cotas igual ao prazo, sem lance e sem exclusão, o grupo contempla exatamente uma cota por assembleia, todas as cotas são contempladas até o encerramento, e a espera média é $(T+1)/2$, valor que se obtém diretamente do sorteio sem reposição.

**Sorteio uniforme.** Em $M_0$, a frequência com que cada cota é sorteada em muitas repetições não difere da uniforme.

**Sequência da assembleia.** No regime de sorteio separado, o sorteio de ativas precede sempre o de excluídas; a soma restituída na assembleia, além da primeira restituição, não ultrapassa o teto $\bar r$; a sobra só é sorteada quando o contrato o prevê.

**Grupo aberto.** A recolocação mantém o número de cotas pagantes; o risco de exclusão segue a faixa de idade do grupo; a cota inadimplente só é excluída depois de três vencimentos.

## Leilão único

A verificação mais informativa é a do leilão de uma vaga. Restringindo o lance a um vencedor, com participantes de valores independentes e uniformes em $[0, 1]$, $M_0$ é um leilão de primeiro preço e $M_2$ é um leilão de segundo preço, para os quais a teoria dá solução fechada [@vickrey1961counterspeculation]. Com $n$ participantes:

- no leilão de primeiro preço, a estratégia de equilíbrio simétrico é ofertar $(n-1)/n$ do valor;
- no de segundo preço, ofertar o próprio valor é estratégia dominante;
- as duas regras dão a mesma receita esperada, $(n-1)/(n+1)$ (equivalência de receita).

Os testes verificam as três propriedades com as regras de lance do simulador. Contra rivais que ofertam $(n-1)/n$ do valor, o lance que maximiza o ganho esperado sob $M_0$, numa grade de lances, fica a no máximo um passo da grade do valor teórico. Sob $M_2$, nenhum desvio do lance igual ao valor aumenta o ganho do participante, em todos os casos sorteados. E as receitas médias de $M_0$ com lances de equilíbrio e de $M_2$ com lances verdadeiros ficam a menos de um centésimo do valor teórico, para dois e cinco participantes.

O teste tem um alcance preciso. Ele mostra que as regras de lance do simulador implementam corretamente os leilões que generalizam, e que a regra de preço de $M_2$ preserva a propriedade de que ofertar o valor é dominante quando há uma vaga. Não mostra que o comportamento simulado no grupo, com a política fixa $\pi_\phi$, seja de equilíbrio. Pelo contrário: a equivalência de receita mostra que, se os participantes respondessem otimamente a cada regra, a troca de $M_0$ por $M_2$ não alteraria a receita esperada no leilão único. Na comparação do Capítulo 7, a política é a mesma sob as duas regras, e a diferença de resultado entre elas inclui, por isso, o efeito de não reotimizar o comportamento. Essa é a limitação discutida nas seções 7.4 e 8.3.

## Propriedades de $M_1$ e $M_2$ no grupo

Dois testes verificam propriedades dos desenhos alternativos fora do leilão único. Para $M_2$ com várias vagas, os vencedores pagam a primeira oferta recusada, e o número de vencedores é o maior inteiro compatível com o saldo a esse preço; com as mesmas ofertas, $M_2$ contempla no máximo tantas cotas quanto $M_0$, e as mesmas primeiras. Para $M_1$, com $\beta = 0$ o mecanismo reproduz $M_0$; num grupo fechado, em que todas as cotas entraram juntas, o peso pela espera também reproduz o sorteio uniforme; e num grupo aberto, o peso reduz a dispersão do tempo de espera, como pretendido.

## Propriedades das famílias $M_3$ e $M_4$

As famílias de desenhos acrescentadas depois da primeira comparação têm testes próprios. Para $M_3$: com lance mínimo zero, o lance de preço uniforme com reserva coincide com $M_2$; nenhum vencedor paga menos que o lance mínimo; o sorteio da sobra é sempre acionado quando o desenho o impõe; e as onze variantes registradas são construídas pelo nome. Para $M_4$: cada vencedor do lance fixo paga exatamente o percentual postado, o número de vencedores respeita o saldo, um mesmo participante não vence duas vezes na assembleia, e o sorteio entre os que aceitam o lance fixo usa um gerador próprio, sem alterar a sequência aleatória comum aos desenhos comparados.

## Onde fica a documentação

A lista completa dos testes, com o que cada um verifica, fica no Apêndice A [RESULTADO PENDENTE: Apêndice A gerado a partir de tests/], e a saída da execução completa da bateria, no repositório. A versão do código usada no Capítulo 7 passou em todos os testes que não dependem dos dados brutos.
