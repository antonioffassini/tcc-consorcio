# Colinha — metodologia (1.7) e cronograma
Uma entrada por slide. **Fala** para ler ou parafrasear; **Ponte** leva ao próximo; **Se perguntarem** são respostas curtas. As falas também estão nas anotações do orador no .pptx.
Tempo-alvo: 15 a 20 minutos.

---

## Slide 1 — A metodologia em uma página

**Fala**

Professor, esta é a metodologia inteira numa frase: construir um consórcio simulado, ajustá-lo até que ele se pareça com os dados do Banco Central e, só então, trocar a regra de contemplação para ver o que muda.

As sete etapas se agrupam em quatro blocos. Medir: dados e fatos, o que o mundo real mostra. Construir: modelo e simulador, o consórcio de mentira. Confiar: verificar e calibrar, ou seja, garantir que o simulador está certo e se parece com a realidade. Responder: comparar regras e, por fim, o experimento de aprendizado.

Cada hipótese tem seu lugar: H2 é testada na etapa 5, H3 na 6 e H1 na 7.

E já adianto onde entra a IA, porque é a dúvida mais comum: só na etapa 7. Nas outras, os agentes seguem uma regra cujos parâmetros são ajustados aos dados.

**Ponte:** Antes das etapas, a ideia por trás delas.

**Se perguntarem**

- *Por que não estimar direto dos dados?* — Porque as regras alternativas nunca foram usadas: não há dado delas. Só um modelo validado consegue prever o que aconteceria.

---

## Slide 2 — A ideia: um consórcio de mentira, ajustado ao de verdade

**Fala**

A lógica é a de um simulador de voo. Ninguém testa uma asa nova num voo real; testa num simulador que antes foi validado contra voos reais.

À esquerda, o mundo real: grupos de imóveis, dos quais só vemos totais publicados pelo Banco Central, e só sob a regra atual. À direita, o consórcio simulado: as cotas são agentes que decidem, vemos tudo, cada lance, e podemos usar qualquer regra.

As setas mostram o ciclo: calculamos as mesmas estatísticas nos dois lados e giramos os botões do comportamento simulado até elas baterem.

Embaixo, os três movimentos. Ajustar: girar os botões. Conferir: testar em estatísticas guardadas, que o ajuste não viu. Trocar a regra: só com o simulador validado mudamos a regra e medimos o efeito.

**Ponte:** Começando pela etapa 1, os dados.

**Se perguntarem**

- *Quais são os botões?* — Os parâmetros do comportamento: como urgência e liquidez se distribuem entre as cotas e como se traduzem em lance. São de 5 a 8 números, detalhados na etapa 3.

---

## Slide 3 — Dados: dos arquivos do Bacen a duas tabelas limpas

**Fala**

O Banco Central publica três famílias de arquivos sobre consórcio. O mensal traz, por grupo de imóveis, cotas ativas, contempladas e excluídas, prazo e valor do crédito. O trimestral por UF traz, por administradora, quantas contemplações saíram por lance e quantas por sorteio. O contábil cobre o sistema inteiro e só vai até 2024; usamos apenas como contexto.

No meio está o pipeline: scripts em Python com a biblioteca pandas, que abrem os 236 arquivos, padronizam os nomes das colunas, filtram imóveis a partir de julho de 2024, quando passou a valer a Resolução 285, e conferem somas e duplicatas com testes automáticos.

A saída são dois painéis: o A, por grupo e mês, e o B, por administradora e trimestre. Mais um relatório de qualidade dizendo o que foi descartado e por quê.

Situação: os arquivos estão todos baixados; o pipeline ainda vai ser escrito, e é a primeira meta desta semana.

**Ponte:** Com as tabelas prontas, extraímos delas o que o modelo terá de reproduzir.

**Se perguntarem**

- *Por que só desde julho de 2024?* — É quando passou a valer a Resolução BCB 285; um regime só evita modelar a mudança de norma dentro dos dados.
- *Por que dois painéis?* — Porque a separação lance/sorteio só existe no arquivo por administradora e trimestre; por grupo e mês só há o total de contemplados.

---

## Slide 4 — Fatos: o que o modelo é obrigado a reproduzir

**Fala**

Dois termos. Fato estilizado é um padrão robusto nos dados, que qualquer modelo decente precisa reproduzir. Momento é o número que resume esse padrão: uma média, uma dispersão, uma correlação.

Alguns exemplos, ainda da leitura exploratória, que vamos refazer no pipeline: cerca de 73 por cento das contemplações saem por lance, na média entre administradoras. Essa fração muda muito de uma administradora para outra, de 12 a 97 por cento. Administradoras com grupos maiores têm mais lance. E a contemplação é rara: cerca de meio por cento das cotas por mês, com uns 7 por cento dos meses sem nenhuma.

O passo crítico está embaixo: antes de qualquer ajuste, dividimos os momentos em dois grupos. Os de calibração, que o modelo vê e usa para ajustar os botões. E os de teste, que ficam na gaveta e só são abertos depois, para testar H2. É a mesma lógica de treino e teste em aprendizado de máquina: se escolhermos depois de ver o resultado, o teste não vale nada.

**Ponte:** Sabendo o que reproduzir, escrevemos o modelo.

**Se perguntarem**

- *Esses números já valem?* — Não; foram calculados fora do pipeline. Só entram no texto depois de regenerados pelo código, com arquivo em results/.
- *Quantos momentos?* — Algo entre 6 e 10, metade para calibrar e metade para testar. A divisão é a primeira decisão da semana.

---

## Slide 5 — Modelo: as regras do jogo, escritas no papel

**Fala**

Esta etapa é no papel, sem software. É a especificação que o código vai implementar, e vira o Capítulo 4.

Cada cota é um agente com duas características sorteadas no início: urgência, quanto vale por mês ter o bem já, e liquidez, quanto caixa tem para lance, em percentual do crédito. E uma situação: ativa, contemplada ou excluída.

No meio, a política de lance, que é a regra de decisão do agente. Uma forma ilustrativa: o lance é o mínimo entre o caixa disponível e uma combinação da urgência e dos meses restantes. O mínimo garante que ninguém oferece mais do que tem; o peso da urgência diz que quem tem mais pressa oferece mais; o peso do tempo captura que o incentivo muda ao longo do grupo.

À direita, o estado do grupo: saldo do fundo, mês, quem está ativo. E a regra de contemplação, que é uma peça separada.

O que será calibrado são esses pesos, os thetas, mais a média e a dispersão de urgência e liquidez entre as cotas: de 5 a 8 números.

**Ponte:** O modelo vira código no simulador.

**Se perguntarem**

- *Por que uma política tão simples?* — Porque cada parâmetro a mais precisa ser identificado só com dado agregado; poucos parâmetros mantêm a calibração possível. A etapa 7 testa se essa simplicidade esconde algo.
- *De onde vêm urgência e liquidez?* — Não são observadas: são distribuições cujos parâmetros a calibração estima.

---

## Slide 6 — Simulador: o modelo virando código

**Fala**

O simulador é o modelo em Python, organizado em objetos: o grupo, os agentes e a regra. A biblioteca NumPy faz as contas e os sorteios, e as sementes aleatórias são fixas, então a mesma execução dá sempre o mesmo resultado.

À esquerda, o que acontece em cada mês: arrecada as parcelas, sorteia as vagas previstas, cada agente decide seu lance pela política, apura os lances com o saldo que sobrou, exclui quem atrasou três parcelas e restitui, registra as estatísticas.

À direita, o mesmo laço em código. As duas linhas em amarelo são a regra: sortear e apurar. Para testar outra regra, troca-se só esse objeto, sem mexer no resto.

Um grupo dura uns 200 meses, e uma avaliação usa centenas de grupos.

**Ponte:** Antes de usar o simulador, ele passa por dois testes. O primeiro é a verificação.

**Se perguntarem**

- *Quantos agentes por grupo?* — O número de cotas do grupo, tirado do painel; centenas a milhares.
- *E se ficar lento?* — Vetoriza-se em NumPy e roda-se em paralelo; se ainda faltar, reduz-se o número de grupos por avaliação.

---

## Slide 7 — Verificar: o código faz o que o modelo diz?

**Fala**

Verificar é conferir se o código faz o que o modelo diz, rodando-o em casos simples cuja resposta já se conhece.

Primeiro caso: só sorteio, uma vaga por mês, N cotas, ninguém atrasa. A espera média tem de dar N mais um sobre dois meses, e todas as cotas em dia têm a mesma chance. Segundo: um único leilão, com n agentes e valores uniformes; o lance de equilíbrio da teoria é n menos um sobre n vezes o valor. Terceiro: em qualquer configuração, a contabilidade do fundo tem de fechar. Quarto: sem inadimplência, ninguém é excluído e todos são contemplados até o fim.

Cada caso vira um teste automático. Se falhar, é bug: corrige-se o código, nunca o teste.

**Ponte:** Com o código certo, a pergunta seguinte é se ele se parece com a realidade.

**Se perguntarem**

- *Verificação e validação não são a mesma coisa?* — Não. Verificação: o código implementa o modelo. Validação: o modelo representa a realidade (H2).

---

## Slide 8 — Calibrar: girar os botões até bater com o Bacen

**Fala**

A calibração usa o método de momentos simulados. É um ciclo de quatro passos. Um: chuta-se um conjunto de parâmetros. Dois: simulam-se uns 500 grupos com eles. Três: calculam-se, na simulação, os mesmos momentos que calculamos nos dados. Quatro: mede-se a distância entre simulado e real. O otimizador do SciPy propõe parâmetros melhores e o ciclo se repete até a distância não diminuir mais.

A distância é uma soma ponderada dos quadrados das diferenças. O resultado é o comportamento que melhor explica os dados.

Depois, abre-se a gaveta: com os parâmetros finais, o modelo acerta os momentos de teste que nunca viu? Se acertar, H2 passa e o simulador é confiável. Se não, isso é o resultado, e não seguimos para a comparação.

É o mesmo princípio de calibrar um modelo de precificação ao mercado e depois usá-lo para precificar o que o mercado não cota.

**Ponte:** Com o simulador validado, finalmente comparamos regras.

**Se perguntarem**

- *Por que não máxima verossimilhança?* — O modelo não tem verossimilhança tratável, e o dado é só agregado; o método de momentos simulados é o padrão nesses casos.
- *E se houver vários θ que ajustam igualmente bem?* — É identificação parcial; por isso a comparação é repetida em toda a faixa de θ compatível com os dados (robustez, H3).

---

## Slide 9 — Comparar: trocar a regra e medir o efeito

**Fala**

Com os parâmetros calibrados, trocamos a peça da regra e simulamos milhares de grupos em cada uma.

M zero é a vigente: sorteio, depois lance em que cada vencedor paga o que ofereceu. M um é o sorteio ponderado pela espera: quem espera há mais tempo tem mais chance. M dois é o lance de preço uniforme: todos os vencedores pagam o mesmo percentual.

Em cada regra medimos três coisas: bem-estar, o valor de receber cedo menos o custo dos lances; espera, quão desigual é o tempo até a contemplação; e estabilidade, o saldo do fundo e os meses sem contemplação.

À direita, a robustez. Os parâmetros calibrados têm incerteza, então repetimos a comparação em cada combinação plausível. H3 exige que a ordem entre as regras não se inverta. O trabalho afirma qual regra é melhor, não quanto.

**Ponte:** Por fim, a etapa 7, onde entra a IA.

**Se perguntarem**

- *Essas alternativas são permitidas pela lei?* — São desenhos que mantêm sorteio e lance como formas de contemplação; a admissibilidade de cada uma é discutida no Capítulo 4.

---

## Slide 10 — Onde entra a IA

**Fala**

Há dois tipos de agente no trabalho.

O agente de regra fixa, das etapas 4 a 6, segue a fórmula da política. Os parâmetros vêm da calibração. Ele não aprende nada: é como uma regressão. E é rápido, o que permite milhares de simulações.

O agente que aprende, da etapa 7, usa aprendizado por reforço, com o algoritmo Q-learning. Ele começa sem saber nada, tenta lances, recebe uma recompensa e se ajusta. Ninguém lhe dá a fórmula; a estratégia emerge. Mas é lento: precisa de milhares de grupos para aprender.

Não há ChatGPT nem modelo de linguagem. A IA do trabalho é o sistema multiagente e o aprendizado por reforço. E o aprendizado fica fora da calibração porque exigiria treinar os agentes de novo a cada passo do otimizador.

**Ponte:** Como esse agente aprende, passo a passo.

**Se perguntarem**

- *Os agentes que aprendem usam dados reais?* — Não diretamente: aprendem dentro do simulador calibrado, que por sua vez foi ajustado aos dados.

---

## Slide 11 — Como o agente aprende, passo a passo

**Fala**

O ciclo de aprendizado tem cinco passos. Um: o agente observa sua situação, por exemplo meses restantes, urgência e caixa. Dois: escolhe um lance, normalmente o melhor segundo sua tabela, mas às vezes um aleatório, para explorar. Três: o simulador roda a assembleia. Quatro: ele recebe a recompensa: se foi contemplado, o valor de receber menos o custo do lance; se não, zero. Cinco: atualiza a tabela, e o lance que deu certo ganha valor. Isso se repete por milhares de grupos.

À direita, a tabela, com valores ilustrativos. Cada linha é uma situação, cada coluna um lance em percentual do crédito, e cada célula é quanto o agente espera ganhar. Em destaque, o melhor lance de cada situação. Repare que quem tem urgência mas pouco caixa não consegue dar lances altos.

O teste de H1 é comparar o lance aprendido com a fórmula da teoria. Se forem diferentes, a teoria clássica não basta para descrever o consórcio.

**Ponte:** Resumindo as ferramentas.

**Se perguntarem**

- *Por que Q-learning?* — É o algoritmo do trabalho de referência em leilões com agentes que aprendem (Banchio e Skrzypacz, 2022), simples de implementar e auditar.
- *E se não convergir?* — Reduz-se o espaço de situações e de lances (discretização mais grossa) e aumenta-se o número de episódios; o resultado é reportado com a convergência observada.

---

## Slide 12 — As ferramentas, e onde cada uma entra

**Fala**

Tudo é em Python. O pandas lê e limpa os dados e calcula os momentos. O NumPy faz as contas e os sorteios do simulador. O SciPy fornece o otimizador da calibração. O pytest roda os testes automáticos dos dados e da verificação. O multiprocessing roda os grupos em paralelo. O Q-learning é código próprio. O Git e o GitHub guardam o histórico e permitem trabalhar a três. E o Makefile, o script de auditoria e o pandoc rodam tudo com um comando, garantem que todo número do texto venha de um arquivo de resultado e geram a monografia.

O multiprocessing e o Q-learning ainda são propostas, a confirmar entre nós.

**Ponte:** Onde estamos nisso tudo.

**Se perguntarem**

- *Por que não Java?* — O ecossistema científico do Python (pandas, NumPy, SciPy) e a velocidade de desenvolvimento pesam mais que o desempenho bruto; os trechos pesados são vetorizados.

---

## Slide 13 — Onde estamos

**Fala**

Com franqueza: estamos no começo da parte técnica. Os dados estão baixados, todos os 236 arquivos. A leitura exploratória dos fatos foi feita, mas precisa ser refeita no pipeline, e falta decidir a divisão entre calibração e teste. O modelo está definido em ideia, no Capítulo 1, mas a especificação formal ainda vai ser escrita. Da etapa 4 em diante, nada começou.

No texto, o Capítulo 1 foi reescrito e apresentado, o 2 está em rascunho e os demais por escrever.

A boa notícia é que o maior risco, se o dado público permite calibrar alguma coisa, já teve resposta exploratória positiva.

**Ponte:** Por isso refizemos o cronograma.

---

## Slide 14 — Cronograma até a entrega

**Fala**

A meta inicial de 12 de outubro não foi cumprida, e este cronograma a substitui. É uma meta por semana.

Semana 1, de 19 a 23 de outubro: dados e fatos, e começar o modelo. Semana 2: terminar o modelo, que vira o Capítulo 4, e construir o simulador com a verificação. Semana 3: calibração e teste de H2. Semana 4: comparação de regras e H3. Semana 5: aprendizado por reforço e H1, e ao fim dela os experimentos são congelados. Os capítulos de dados, simulação e resultados são escritos em paralelo, das semanas 2 a 5. Semana 6: capítulos de literatura, discussão e conclusão, e revisão. Semana 7: entrega final, com a data exata a confirmar no calendário da Escola.

A linha vermelha mostra onde estamos: no fim da semana zero.

**Ponte:** E o que fazemos já na próxima semana.

**Se perguntarem**

- *E se atrasar?* — O corte é na etapa 7: sem ela, H1 fica como trabalho futuro e a tese principal (H2 e H3) se mantém.

---

## Slide 15 — Meta da semana 1 (19–23/10)

**Fala**

Três entregas para a semana que vem. Um: o pipeline, com os dois painéis e o relatório de qualidade. Dois: os fatos calculados pelo código, com a divisão entre calibração e teste registrada antes de qualquer ajuste. Três: o modelo escrito, que é o rascunho do Capítulo 4.

Com isso, a semana 2 começa direto no simulador, e o capítulo de dados pode ser escrito em paralelo.

**Ponte:** (Abrir para comentários.)
