# Roteiro: andamento do TCC (reunião geral)

*Uns 12 a 14 minutos. Onde está **[passa]**, você troca de slide. O que está entre colchetes não é para ler.*

---

### Slide 1 · O trabalho em uma página

Bom, pessoal, bom dia. Vou passar rapidinho pelo andamento do nosso TCC, que é sobre consórcio.

Em uma frase: a gente quer avaliar a regra que decide **quem recebe o crédito** no consórcio, e comparar essa regra com alternativas que a lei também permitiria. E a gente faz isso num simulador ajustado aos dados públicos do Banco Central.

O motivo é simples: essa regra foi fixada por lei, mexe com milhões de pessoas e ninguém nunca comparou ela com outra coisa. Então a pergunta é: a regra atual é boa? Existe uma melhor?

Vou explicar rapidinho como o consórcio funciona e depois mostro onde a gente está.

**[passa]**

### Slide 2 · O caminho do dinheiro

Então, o consórcio é basicamente um autofinanciamento coletivo. Um grupo de pessoas paga uma parcela todo mês, esse dinheiro vai para um fundo comum, e todo mês tem uma assembleia que entrega crédito para alguns membros.

A ordem é sempre a mesma: primeiro tem o **sorteio**; depois, com o que sobrou no fundo, tem o **lance**, que é quem oferece mais; e o que não dá para fechar um crédito inteiro fica para o mês seguinte. Quem atrasa é excluído, e recebe de volta o que pagou mais pra frente.

E o ponto principal está aqui embaixo: no fim, todo mundo que está em dia recebe o crédito. Então o que se disputa não é *se* a pessoa recebe, é *quando*.

**[passa]**

### Slide 3 · Dois caminhos

São dois caminhos para ser contemplado. O sorteio é automático: toda cota em dia participa, não custa nada a mais, é pura sorte.

O lance é opcional: só entra quem quer, ganha quem oferece o maior percentual do crédito, e o custo é antecipar parcelas que a pessoa ainda deve. Ou seja, quem tem pressa **e** tem dinheiro consegue passar na frente.

**[passa]**

### Slide 4 · O Banco Central só vê o total

E aqui está a dificuldade do trabalho. Todo mês cada pessoa decide se dá lance e de quanto, e isso depende de três coisas: da pressa dela, de quanto dinheiro ela tem e do que ela acha que os outros vão fazer.

Só que o Banco Central só publica o **total**: quantos foram contemplados, quantos por lance e quantos por sorteio. Quem deu lance, de quanto, e quem perdeu, isso a gente não vê. Então o comportamento tem que ser **inferido**, não dá para medir direto.

**[passa]**

### Slide 5 · A pergunta

A pergunta de pesquisa, então: a regra atual é eficiente, em bem-estar dos participantes e estabilidade do grupo, comparada com as alternativas que a regulação permite?

E ela quebra em três: primeiro, **como** as pessoas dão lance. Segundo, se dá para montar um modelo disso só com os dados agregados. E terceiro, se existe uma regra melhor.

**[passa]**

### Slide 6 · Hipóteses

Cada uma dessas perguntas virou uma hipótese, com um teste e um critério para ser rejeitada.

A mais importante para hoje é a **H2**, que é a do meio: o modelo, depois de ajustado, tem que acertar estatísticas que ele **não viu** no ajuste. Se ele não passar nisso, a gente não confia nele para comparar regras, que é a H3. A H1 é um experimento à parte, com inteligência artificial, no final.

**[passa]**

### Slide 7 · Metodologia em uma página

A metodologia, resumindo: a gente constrói um consórcio simulado, ajusta até ele ficar parecido com os dados do Banco Central, e só aí troca a regra para ver o que muda.

São sete etapas, em quatro blocos: **medir** o mundo real, que são os dados e os fatos; **construir** o simulador, que é o modelo e o código; **confiar**, que é verificar e calibrar; e **responder**, que é comparar as regras e, no fim, o aprendizado.

**[passa]**

### Slide 8 · A ideia

A ideia é parecida com um simulador de voo. Antes de testar uma asa nova, você confere se o simulador acerta os voos reais.

Aqui é igual: de um lado, o mundo real, onde a gente só vê os totais e só existe a regra atual. Do outro, o consórcio simulado, onde a gente vê cada lance e pode colocar a regra que quiser. A gente ajusta os "botões" até as estatísticas baterem, confere em estatísticas guardadas e, aí sim, troca a regra.

**[passa]**

### Slide 9 · Onde estamos

Bom, e onde a gente está. As etapas de 1 a 4 estão feitas, e a gente está um pouco à frente do cronograma.

Os dados estão prontos, com pipeline e testes. Os fatos foram calculados e o teste de identificação passou. O modelo está especificado e já implementado. E o simulador já está rodando, em protótipo: ele roda 300 grupos em uns seis segundos. A verificação também foi feita; o que começa agora é a calibração.

Vou mostrar cada uma rapidinho.

**[passa]**

### Slide 10 · Dados

Na parte de dados, a gente pegou os 236 arquivos do Banco Central e transformou em dois painéis limpos: um por grupo e por mês, e outro por administradora e por trimestre, que é onde aparece a divisão entre lance e sorteio.

No recorte que a gente usa, que é imóveis a partir de julho de 2024, são mais de 57 mil observações, uns 3.500 grupos e 76 administradoras. Nenhuma linha precisou ser descartada.

E apareceram três coisas importantes. Uma: a mudança de formato que o Banco Central fez em 2024 não quebrou os arquivos. Duas: o número de excluídos vem como estoque, então a saída do mês a gente calcula por diferença. E três: em algumas administradoras, as duas fontes contam as contemplações de um jeito diferente, então a gente não mistura as duas no mesmo número.

Ah, e a soma dos grupos bate com o total oficial do Banco Central em cem por cento dos casos, o que dá bastante segurança no pipeline.

**[passa]**

### Slide 11 · Fatos e momentos

Aqui são os fatos, ou seja, o que o simulador vai ser obrigado a reproduzir.

O primeiro: o lance domina. Em média, 73% das contemplações saem por lance. Mas isso varia muito entre administradoras: vai de 13% a 97%.

O segundo: contemplar é raro. Por mês, sai mais ou menos meio por cento das cotas de um grupo, e em uns 7% dos meses não sai ninguém.

E o terceiro: administradoras com grupos maiores tendem a ter mais lance; o prazo, por outro lado, não faz diferença nenhuma.

O dado mais importante está aqui embaixo: 94% dessa variação está **entre** administradoras, não dentro delas. Isso é bom, porque significa que tem variação suficiente para ajustar o modelo. E a gente já propôs quais números servem para calibrar e quais ficam guardados para o teste; a divisão final a gente fecha entre nós antes de rodar qualquer ajuste.

**[passa]**

### Slide 12 · Modelo

O modelo, de forma bem resumida: cada cota é um agente, com uma **urgência**, que é quanto vale para ela receber logo, e uma **liquidez**, que é quanto dinheiro ela tem para dar lance.

O lance segue uma regra simples: a pessoa oferece de acordo com a pressa e com o tempo que falta, mas nunca mais do que ela tem. E a regra de contemplação é uma peça separada, que dá para trocar, porque é isso que a gente quer comparar depois.

**[passa]**

### Slide 13 · Simulador

E isso virou código. O simulador roda o grupo mês a mês, na mesma ordem da regra: arrecada, sorteia, recebe os lances com o que sobrou, exclui quem atrasou e registra tudo.

Ele é em Python, e sempre com semente fixa, para dar o mesmo resultado toda vez que roda.

**[passa]**

### Slide 14 · Primeira rodada

Essa aqui é a primeira rodada. É importante dizer: ainda **sem calibração**, com parâmetros de chute. É mais um teste de fumaça do que um resultado.

Mesmo assim, já dá para tirar alguma coisa. Os níveis já ficam perto: a fração de lance deu 77% contra 73% no dado real, e a taxa de contemplação deu praticamente a mesma. Isso mostra que só a estrutura da regra, uma vaga de sorteio e o resto indo para lance, já explica boa parte do padrão.

O que está longe é a variação. No dado real, as administradoras são muito diferentes entre si; no simulador, todos os grupos são iguais. Então já sabemos exatamente o que falta: dar parâmetros que variem por administradora. Isso é o trabalho da calibração.

**[passa]**

### Slide 15 · Verificação

Antes de confiar no simulador, a gente testou ele em casos em que a resposta já é conhecida. Por exemplo: se só tem sorteio e ninguém atrasa, tem que sair exatamente uma pessoa por mês, e a espera média tem que ser a fórmula de sempre. Passou.

Também testamos se o sorteio é justo, se a conta do dinheiro fecha e se, sem inadimplência, todo mundo é contemplado. Tudo passou. Hoje são 21 testes automáticos rodando. O que falta é o caso do leilão clássico, que entra junto com a próxima etapa.

**[passa]**

### Slide 16 · Cronograma

No cronograma, a gente está na semana 2, e o que era das semanas 1 a 3 já está entregue em protótipo, que é o que está em verde.

O congelamento dos experimentos continua no fim da semana 5, e a entrega final na primeira semana de dezembro; a data exata ainda falta confirmar com a Poli.

**[passa]**

### Slide 17 · Próximos passos

Para as próximas duas semanas, são três coisas.

Primeiro, colocar a diferença entre administradoras no modelo, porque é o que a primeira rodada mostrou que falta. Segundo, a calibração propriamente dita, e logo depois o teste da H2, abrindo aqueles números que ficaram guardados. E terceiro, umas decisões nossas, dos autores: fechar a divisão entre calibração e teste e o cronograma, antes de rodar qualquer ajuste.

Com isso, a comparação entre as regras começa na semana 5, ainda com folga para a parte de aprendizado por reforço.

É isso, pessoal. Obrigado! Se tiverem alguma dúvida, fico à disposição.

---

## Se alguém perguntar

- **"Esses números do simulador já valem?"** Ainda não. É uma rodada sem calibração, serve para mostrar que o código roda certo e que os níveis já ficam na ordem certa. Resultado de verdade só depois da calibração e do teste da H2.
- **"Por que só imóveis e só depois de julho de 2024?"** Porque é quando entra a regra atual do Banco Central, a Resolução 285. Se misturasse os períodos, a gente teria que modelar a mudança de regra no meio.
- **"Por que a correlação com o tamanho caiu de 0,56 para 0,32?"** O 0,56 veio de uma leitura exploratória, feita fora do pipeline e com outra medida de tamanho. O número que vale é o do pipeline.
- **"E as enchentes do Rio Grande do Sul?"** A gente não tirou o RS dos dados, só marcou. Sem o RS, a fração média de lance quase não muda: vai de 0,73 para 0,74.
