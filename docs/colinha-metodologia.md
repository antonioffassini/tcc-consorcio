# Colinha — metodologia (1.7) e cronograma
Uma entrada por slide. **Fala** para ler ou parafrasear; **Ponte** leva ao próximo; **Se perguntarem** são respostas curtas. As falas também estão nas anotações do orador no .pptx.
Tempo-alvo: 15 a 20 minutos.

---

## Slide 1 — A metodologia em uma página

**Fala**

Professor, esta é a metodologia inteira numa frase: construir um consórcio simulado, ajustá-lo até que ele se pareça com os dados do Banco Central e, só então, trocar a regra de contemplação para ver o que muda.

As sete etapas se agrupam em quatro blocos. Medir: dados e fatos, o que o mundo real mostra. Construir: modelo e simulador, o consórcio de mentira. Confiar: verificar e calibrar, ou seja, garantir que o simulador está certo e se parece com a realidade. Responder: comparar regras e, por fim, o experimento de aprendizado.

Cada hipótese tem seu lugar: H2 é testada na etapa 5, H3 na 6 e H1 na 7.

E já adianto onde entra a IA, porque é a dúvida mais comum: só na etapa 7, com agentes que aprendem por reforço. Eles servem para testar se a fórmula clássica de leilão basta, a H1, e para mostrar como as pessoas reagiriam a cada regra nova. Nas outras etapas, os agentes seguem uma fórmula calibrada.

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

## Slide 4 — Fatos e momentos: o que o modelo é obrigado a reproduzir

**Fala**

Dois termos que andam juntos. O fato estilizado é a frase: um padrão que se repete nos dados. O momento é o número que mede essa frase, com uma fórmula fixa, calculado exatamente do mesmo jeito no dado real e no simulado. O fato orienta; o momento é o que entra na conta.

À esquerda, três fatos; à direita, os momentos de cada um, ainda da leitura exploratória, que vamos refazer no pipeline. Primeiro fato: o lance domina, mas varia muito entre administradoras. Ele vira três números: a fração média por lance, cerca de 0,73; o desvio-padrão entre administradoras, cerca de 0,12; e o intervalo, de 0,12 a 0,97. Segundo fato: contemplar é raro e irregular, cerca de meio por cento das cotas por mês, com uns 7 por cento dos meses sem nenhuma. Terceiro: grupos maiores têm mais lance, correlação de cerca de 0,56, enquanto o prazo não tem relação.

Embaixo, o passo crítico: antes de qualquer ajuste, os momentos são divididos. Os de calibração o modelo vê e usa para ajustar o theta. Os de teste ficam na gaveta e só são abertos depois, para testar H2. É treino e teste, como em aprendizado de máquina.

**Ponte:** Sabendo o que reproduzir, escrevemos o modelo.

**Se perguntarem**

- *Esses números já valem?* — Não; foram calculados fora do pipeline. Só entram no texto depois de regenerados pelo código, com arquivo em results/.
- *Por que não usar só o fato, sem o número?* — Porque a calibração compara números: o simulado e o real precisam ser medidos pela mesma fórmula.

---

## Slide 5 — Modelo: as regras do jogo, escritas no papel

**Fala**

Esta etapa é no papel, sem software. É a especificação que o código vai implementar, e vira o Capítulo 4.

Cada cota é um agente com duas características sorteadas no início: urgência, quanto vale por mês ter o bem já, e liquidez, quanto caixa tem para lance, em percentual do crédito. E uma situação: ativa, contemplada ou excluída.

No meio, a política de lance, que é a regra de decisão do agente. Uma forma ilustrativa: o lance é o mínimo entre o caixa disponível e uma combinação da urgência e dos meses restantes. O mínimo garante que ninguém oferece mais do que tem; o peso da urgência diz que quem tem mais pressa oferece mais; o peso do tempo captura que o incentivo muda ao longo do grupo.

À direita, o estado do grupo: saldo do fundo, mês, quem está ativo. E a regra de contemplação, que é uma peça separada.

O que será calibrado são esses pesos, os thetas, mais a média e a dispersão de urgência e liquidez entre as cotas: de 5 a 8 números. Esse conjunto é o que chamamos de theta, e vale um slide próprio.

**Ponte:** O que exatamente é esse theta.

**Se perguntarem**

- *Por que uma política tão simples?* — Porque cada parâmetro a mais precisa ser identificado só com dado agregado; poucos parâmetros mantêm a calibração possível. A etapa 7 testa se essa simplicidade esconde algo.
- *De onde vêm urgência e liquidez?* — Não são observadas: são distribuições cujos parâmetros a calibração estima.

---

## Slide 6 — O θ: os números que a calibração vai procurar

**Fala**

Theta é tudo o que descreve o comportamento e não aparece nos dados. Ele tem duas partes, e a distinção importa.

A primeira é quem as pessoas são: as distribuições de urgência e de liquidez entre as cotas. Isso não muda quando a regra muda; quem tem pouco caixa continua tendo pouco caixa.

A segunda é como elas jogam: os pesos da política de lance. Isso muda quando a regra muda, e é aí que entra a etapa 7.

A tabela mostra cada parâmetro e o momento que o puxa. A liquidez média é puxada pela fração média de contemplações por lance: mais caixa, mais lance. A dispersão da liquidez é puxada pela dispersão entre administradoras. A urgência e os pesos da política dependem de como o lance varia ao longo do prazo, e isso ainda vamos verificar.

Um exemplo do que o otimizador faz: se o simulado dá 50 por cento de contemplações por lance e o real dá 73, ele sobe a liquidez média ou o lance de base. A associação é intuitiva; quais parâmetros os dados públicos conseguem identificar é testado no capítulo 6. O que não for identificável é fixado e tratado como análise de sensibilidade.

**Ponte:** O modelo vira código no simulador.

**Se perguntarem**

- *E se um parâmetro não for identificável?* — Fixa-se num valor plausível e varia-se esse valor na análise de sensibilidade; a conclusão só vale se a ordenação das regras não depender dele.

---

## Slide 7 — Simulador: o modelo virando código

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

## Slide 8 — Verificar: o código faz o que o modelo diz?

**Fala**

Verificar é conferir se o código faz o que o modelo diz, rodando-o em casos simples cuja resposta já se conhece.

Primeiro caso: só sorteio, uma vaga por mês, N cotas, ninguém atrasa. A espera média tem de dar N mais um sobre dois meses, e todas as cotas em dia têm a mesma chance. Segundo: um único leilão, com n agentes e valores uniformes; o lance de equilíbrio da teoria é n menos um sobre n vezes o valor. Terceiro: em qualquer configuração, a contabilidade do fundo tem de fechar. Quarto: sem inadimplência, ninguém é excluído e todos são contemplados até o fim.

Cada caso vira um teste automático. Se falhar, é bug: corrige-se o código, nunca o teste.

**Ponte:** Com o código certo, a pergunta seguinte é se ele se parece com a realidade.

**Se perguntarem**

- *Verificação e validação não são a mesma coisa?* — Não. Verificação: o código implementa o modelo. Validação: o modelo representa a realidade (H2).

---

## Slide 9 — Calibrar: girar os botões até bater com o Bacen

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

## Slide 10 — Comparar: trocar a regra e medir o efeito

**Fala**

Com os parâmetros calibrados, trocamos a peça da regra e simulamos milhares de grupos em cada uma.

M zero é a vigente: sorteio, depois lance em que cada vencedor paga o que ofereceu. M um é o sorteio ponderado pela espera: quem espera há mais tempo tem mais chance. M dois é o lance de preço uniforme: todos os vencedores pagam o mesmo percentual.

Em cada regra medimos três coisas: bem-estar, o valor de receber cedo menos o custo dos lances; espera, quão desigual é o tempo até a contemplação; e estabilidade, o saldo do fundo e os meses sem contemplação.

À direita, a robustez. Os parâmetros calibrados têm incerteza, então repetimos a comparação em cada combinação plausível. H3 exige que a ordem entre as regras não se inverta. O trabalho afirma qual regra é melhor, não quanto. E há uma proposta, que explico a seguir: repetir essa comparação com agentes que aprendem.

**Ponte:** Por fim, a etapa 7, onde entra a IA.

**Se perguntarem**

- *Essas alternativas são permitidas pela lei?* — São desenhos que mantêm sorteio e lance como formas de contemplação; a admissibilidade de cada uma é discutida no Capítulo 4.

---

## Slide 11 — Onde entra a IA, e para que serve

**Fala**

Os agentes das etapas 4 a 6 seguem uma fórmula; os da etapa 7 aprendem sozinhos. E há uma razão concreta para precisar dos segundos.

O agente de regra fixa tem um limite. O theta dele foi calibrado sob a regra atual. Sob outra regra, as pessoas mudariam de estratégia: num leilão de preço uniforme, por exemplo, compensa ofertar diferente do que num de primeiro preço. Usar o theta da regra atual para avaliar uma regra nova é supor que ninguém reage a ela.

O agente que aprende resolve isso. Ele mantém quem as pessoas são, a urgência e a liquidez calibradas, e reaprende como jogar cada regra, por tentativa e erro, com Q-learning. Ninguém lhe dá a fórmula.

Por isso ele tem dois papéis. O primeiro é a H1: a fórmula clássica de leilão descreve como se joga o consórcio? O segundo, que estamos propondo agora e ainda vamos decidir entre nós, é a robustez de H3: a regra vencedora continua vencendo quando as pessoas se adaptam a ela?

Não há ChatGPT nem modelo de linguagem. E treinar os agentes uma vez por regra é viável; o que seria inviável é treiná-los a cada passo da calibração.

**Ponte:** Como esse agente aprende, passo a passo.

**Se perguntarem**

- *Isso não é a crítica de Lucas?* — É exatamente: comportamento estimado sob uma política não vale sob outra. Separar o que é estrutural (urgência, liquidez) do que é estratégia (política) é a resposta padrão.
- *Os agentes que aprendem usam dados reais?* — Não diretamente: aprendem dentro do simulador, com as pessoas calibradas nos dados.

---

## Slide 12 — Como o agente aprende, passo a passo

**Fala**

O ciclo de aprendizado tem cinco passos. Um: o agente observa sua situação, por exemplo meses restantes, urgência e caixa. Dois: escolhe um lance, normalmente o melhor segundo sua tabela, mas às vezes um aleatório, para explorar. Três: o simulador roda a assembleia. Quatro: ele recebe a recompensa: se foi contemplado, o valor de receber menos o custo do lance; se não, zero. Cinco: atualiza a tabela, e o lance que deu certo ganha valor. Isso se repete por milhares de grupos.

À direita, a tabela, com valores ilustrativos. Cada linha é uma situação, cada coluna um lance em percentual do crédito, e cada célula é quanto o agente espera ganhar. Em destaque, o melhor lance de cada situação. Repare que quem tem urgência mas pouco caixa não consegue dar lances altos.

O teste de H1 é comparar o lance aprendido com a fórmula da teoria. Se forem diferentes, a teoria clássica não basta. E, se aprovarmos o segundo papel, os mesmos agentes jogam cada uma das três regras.

**Ponte:** Resumindo as ferramentas.

**Se perguntarem**

- *Por que Q-learning?* — É o algoritmo do trabalho de referência em leilões com agentes que aprendem (Banchio e Skrzypacz, 2022), simples de implementar e auditar.
- *E se não convergir?* — Reduz-se o espaço de situações e de lances (discretização mais grossa) e aumenta-se o número de episódios; o resultado é reportado com a convergência observada.

---

## Slide 13 — As ferramentas, e onde cada uma entra

**Fala**

Tudo é em Python. O pandas lê e limpa os dados e calcula os momentos. O NumPy faz as contas e os sorteios do simulador. O SciPy fornece o otimizador da calibração. O pytest roda os testes automáticos dos dados e da verificação. O multiprocessing roda os grupos em paralelo. O Q-learning é código próprio. O Git e o GitHub guardam o histórico e permitem trabalhar a três. E o Makefile, o script de auditoria e o pandoc rodam tudo com um comando, garantem que todo número do texto venha de um arquivo de resultado e geram a monografia.

O multiprocessing e o Q-learning ainda são propostas, a confirmar entre nós.

**Ponte:** Onde estamos nisso tudo.

**Se perguntarem**

- *Por que não Java?* — O ecossistema científico do Python (pandas, NumPy, SciPy) e a velocidade de desenvolvimento pesam mais que o desempenho bruto; os trechos pesados são vetorizados.

---

## Slide 14 — Onde estamos

**Fala**

Com franqueza: estamos no começo da parte técnica. Os dados estão baixados, todos os 236 arquivos. A leitura exploratória dos fatos foi feita, mas precisa ser refeita no pipeline, e falta decidir a divisão entre calibração e teste. O modelo está definido em ideia, no Capítulo 1, mas a especificação formal ainda vai ser escrita. Da etapa 4 em diante, nada começou.

No texto, o Capítulo 1 foi reescrito e apresentado, o 2 está em rascunho e os demais por escrever.

A boa notícia é que o maior risco, se o dado público permite calibrar alguma coisa, já teve resposta exploratória positiva.

**Ponte:** Por isso refizemos o cronograma.

---

## Slide 15 — Cronograma até a entrega

**Fala**

A meta inicial de 12 de outubro não foi cumprida, e este cronograma a substitui. É uma meta por semana; cada linha é uma frente de trabalho e cada barra mostra em que semana ela acontece. A linha vermelha mostra onde estamos: no fim da semana zero.

Linha por linha:

Cap. 1 e apresentação, semana 0: reescrever a introdução depois do retorno do senhor e apresentá-la. Feito.

Dados e fatos, semana 1: as etapas 1 e 2. Escrever o código que lê os arquivos do Banco Central e monta os dois painéis, por grupo e por administradora; calcular os momentos, que são os números que o simulador terá de reproduzir; e decidir quais momentos calibram e quais ficam guardados para o teste.

Modelo, semanas 1 e 2: a etapa 3. Escrever no papel as regras do jogo: quem são os agentes, como decidem o lance, como o fundo evolui mês a mês e como funcionam as três regras comparadas. Vira o Capítulo 4.

Simulador e verificação, semana 2: a etapa 4 e a primeira metade da 5. Transformar o modelo em código e testá-lo em casos simples cuja resposta já se conhece; se não bater, é erro de programação.

Calibração e H2, semana 3: a segunda metade da etapa 5. Ajustar os parâmetros até o simulador reproduzir os momentos de calibração e, depois, conferir se ele acerta os momentos guardados. É o teste da H2: se passar, o simulador é confiável.

Comparação e H3, semana 4: a etapa 6. Trocar a regra de contemplação, simular milhares de grupos em cada uma e medir bem-estar, espera e estabilidade, repetindo para toda a faixa plausível de parâmetros. É o teste da H3.

Aprendizado e H1, semana 5: a etapa 7. Treinar os agentes que aprendem por reforço, comparar o lance aprendido com a fórmula da teoria, que é a H1, e, se aprovarmos, usá-los para refazer a comparação com pessoas que se adaptam a cada regra. Ao fim dessa semana os experimentos são congelados: nenhum experimento novo depois disso.

Capítulos 5 a 7, semanas 2 a 5: escrever dados, simulação e resultados em paralelo, à medida que cada etapa termina, para não deixar o texto todo para o fim.

Capítulos 3, 8 e 9 e revisão, semana 6: revisão da literatura, discussão e conclusão, e uma revisão completa, com a auditoria de números e citações.

Entrega final, semana 7: gerar a monografia formatada e entregar. A data exata ainda será confirmada no calendário da Escola.

**Ponte:** E o que fazemos já na próxima semana.

**Se perguntarem**

- *E se atrasar?* — O corte é na etapa 7: sem ela, H1 fica como trabalho futuro e a tese principal (H2 e H3) se mantém.
- *O que significa congelar os experimentos?* — A partir do fim da semana 5 nenhum experimento novo é rodado; só se escreve sobre o que já existe. Evita mexer no modelo depois de ver os resultados.
- *Por que o modelo ocupa duas semanas?* — Porque começa em paralelo com os dados na semana 1 e só fecha quando os fatos mostram o que ele precisa reproduzir.

---

## Slide 16 — Meta da semana 1 (19–23/10)

**Fala**

Três entregas para a semana que vem. Um: o pipeline, com os dois painéis e o relatório de qualidade. Dois: os fatos calculados pelo código, com a divisão entre calibração e teste registrada antes de qualquer ajuste. Três: o modelo escrito, que é o rascunho do Capítulo 4.

Com isso, a semana 2 começa direto no simulador, e o capítulo de dados pode ser escrito em paralelo.

**Ponte:** (Abrir para comentários.)
