# Colinha — apresentação do Capítulo 1
Uma entrada por slide, na ordem. **Fala** é o texto para ler ou parafrasear. **Ponte** é a frase que leva ao slide seguinte. **Se perguntarem** são respostas curtas para as perguntas mais prováveis. As mesmas falas estão nas anotações do orador no .pptx.
Tempo-alvo: 25 a 30 minutos.

---

## Slide 1 — O trabalho em uma página

**Fala**

Professor, antes de entrar no capítulo, queria deixar o trabalho inteiro numa página só.

O objetivo é avaliar a regra que decide quem recebe o crédito no consórcio, comparando essa regra com alternativas que a lei também permitiria, dentro de um simulador ajustado aos dados públicos do Banco Central.

De cima para baixo, é uma cadeia só. A motivação: essa regra foi fixada por lei, afeta milhões de pessoas e nunca foi comparada com nada. O problema: ninguém avaliou, e é difícil avaliar, porque o Banco Central só publica totais e o jogo não tem fórmula fechada. A pergunta: a regra atual é eficiente, comparada às alternativas? A proposição: achamos que existe alternativa melhor e que dá para mostrar isso só com o dado agregado. E o método: dados, modelo, simulador, verificação e calibração, comparação.

O resto da apresentação abre cada uma dessas linhas, na ordem das seções do capítulo.

**Ponte:** Começando pelo que é um consórcio.

**Se perguntarem**

- *Isso não é economia, e não engenharia?* — O objeto é econômico, mas a contribuição é de método computacional: inferir comportamento só com dado agregado, construir e verificar um simulador multiagente, calibrar por otimização sobre simulação.
- *Por que 'eficiente' e não 'justo'?* — São três critérios explícitos, e um deles é a dispersão do tempo de espera, que captura o lado distributivo.

---

## Slide 2 — O que é um consórcio: o caminho do dinheiro

**Fala**

O consórcio é um autofinanciamento coletivo, e o jeito mais fácil de entender é seguir o dinheiro.

À esquerda estão as cotas, cada bolinha é uma. Já explico o que é cota no próximo slide; por ora, pense em cada uma como um participante. Todo mês, todas as cotas em dia pagam a parcela, inclusive as já contempladas, porque receberam o crédito antes mas continuam devendo. Essas parcelas vão para o fundo comum. O fundo também recebe o valor dos lances e o que sobrou do mês anterior.

Todo mês tem uma assembleia, e o fundo é usado nesta ordem. Primeiro o sorteio, entre as cotas em dia. Depois, com o que sobrou, o lance: quem ofereceu mais recebe o crédito, e o valor oferecido entra no fundo. O que não fecha um crédito inteiro fica para o mês seguinte. E quem foi excluído por atraso recebe de volta o que pagou.

A faixa escura é a ideia central: quem está em dia sempre recebe até o fim do grupo. O que se disputa não é se, mas quando.

**Ponte:** Duas peças precisam ficar claras: a cota e os dois caminhos.

**Se perguntarem**

- *O contemplado excluído perde o crédito?* — Na Res. 285, não: mantém a contemplação com crédito parcial proporcional ao que amortizou (art. 33). Exclusão após três vencimentos (art. 32, II).
- *E a taxa de administração e o fundo de reserva?* — São cobrados junto com a parcela; ficam de fora do desenho e do escopo como variáveis de decisão.

---

## Slide 3 — A cota e os dois caminhos para ser contemplado

**Fala**

Cota é a posição de um participante no grupo. Cada cota tem seu valor de crédito, sua parcela e seu número, e é a cota, não a pessoa, que é sorteada ou dá lance. Uma pessoa pode ter várias cotas, e cada uma concorre sozinha. Por isso o trabalho e o Banco Central contam cotas, não pessoas.

Os dois caminhos. O sorteio: toda cota em dia concorre automaticamente, ganha por sorte, sem custo extra.

O lance: só concorre quem quer, e ganha quem oferece mais, em percentual do crédito. O ponto importante é o que se oferece: não é dinheiro a mais, é antecipar parcelas que a pessoa já deve. O saldo devedor cai pelo mesmo valor. O custo real é de liquidez: é o que esse dinheiro renderia se ficasse aplicado.

Existe ainda o lance embutido: em vez de caixa próprio, a pessoa usa parte do próprio crédito como lance, e recebe um crédito menor.

**Ponte:** Fica mais concreto com números.

**Se perguntarem**

- *Lance é dinheiro perdido?* — Não. É antecipação do que seria pago de qualquer forma; o custo é o rendimento que o dinheiro deixa de ter.
- *A ordem sorteio antes de lance é obrigatória?* — Sim, a Res. BCB 285/2023 fixa o sorteio antes do lance (art. 12).
- *Quantas vagas há por mês?* — O número de sorteios é o previsto no contrato; o lance fica com o saldo que sobra. Por isso as vagas de lance variam.

---

## Slide 4 — Uma assembleia em números

**Fala**

Um exemplo ilustrativo, sem taxa e sem fundo de reserva. Grupo de 400 cotas, crédito de 200 mil, prazo de 200 meses: parcela de mil reais, arrecadação de 400 mil por mês.

O sorteio leva 200 mil. Sobram 200 mil. O vencedor do lance, que ofereceu 30 por cento, recebe os outros 200 mil e antecipa 60 mil, que voltam ao fundo. Esses 60 mil não pagam outro crédito e ficam para o mês seguinte.

Três coisas aparecem. O sorteado não paga nada a mais. O vencedor do lance recebe o mesmo crédito, mas trocou dinheiro presente por menos espera. E, o mais importante para o modelo: lances maiores deixam mais saldo e abrem mais vagas. O número de vagas depende do próprio comportamento de lance. Isso volta quando eu falar das dificuldades.

**Ponte:** Isso acontece numa escala grande.

**Se perguntarem**

- *Os números são reais?* — Não, são ilustrativos, para a conta fechar. Os números do trabalho vêm do painel do Bacen.
- *O lance entra mesmo no fundo?* — O lance livre é antecipação paga ao grupo. No embutido, sai do próprio crédito. O efeito exato no saldo está sendo conferido nos regulamentos das administradoras.

---

## Slide 5 — Um mercado grande, com uma troca no centro

**Fala**

Para dar escala: segundo a associação das administradoras, mais de 5 milhões de cotas vendidas em 2025, mais de 500 bilhões de reais em crédito comercializado e cerca de 12,7 milhões de participantes ativos.

E por que alguém entra num consórcio? Por causa de uma troca. Ganha crédito sem juros, o custo é a taxa de administração. Abre mão de ter o bem agora: o crédito não é contratado, é aguardado, e não se sabe quando chega.

É dessa troca que nasce o lance.

**Ponte:** Então, se o consórcio é justamente não escolher quando, por que existe o lance?

**Se perguntarem**

- *Esses números são confiáveis?* — São do anuário da ABAC (2026), fonte setorial, marcados como fonte externa; o PDF está sendo anexado. Os números produzidos pelo trabalho vêm do Bacen.

---

## Slide 6 — Por que existe o lance

**Fala**

Comparando três situações. No empréstimo, você escolhe quando recebe e paga juros. No consórcio só com sorteio, você não paga juros e não escolhe quando recebe: é o exato oposto. O lance fica no meio: ele deixa você comprar prioridade na fila, pagando com liquidez, porque você antecipa o que já devia.

Para quem dá lance, é trocar dinheiro presente por menos espera. Só compensa se receber antes vale mais do que o rendimento que esse dinheiro teria. É um juro implícito, mas escolhido.

Para o grupo, o lance também ajuda: o valor antecipado entra no fundo e paga contemplações futuras, então quem nunca dá lance também tende a receber um pouco antes.

O sorteio é o consórcio puro; o lance é a válvula de escape. A pergunta do trabalho, no fundo, é se essa válvula está bem calibrada.

**Ponte:** E a decisão de dar lance é individual, mas o resultado é coletivo.

**Se perguntarem**

- *Por que o regulador permite o lance?* — É prática histórica do setor, codificada na regulação; dá flexibilidade ao participante e caixa ao grupo. O trabalho não questiona a existência do lance, compara formas de combiná-lo com o sorteio.
- *O lance embutido é diferente?* — É o parente mais próximo do lance na ROSCA: aceita-se um crédito menor para receber antes, quase um desconto.

---

## Slide 7 — Cada participante decide; o Banco Central só vê o total

**Fala**

Todo mês, cada participante decide se dá lance e de quanto. Isso depende de três coisas: da urgência, quanto vale receber antes; da liquidez, quanto dinheiro tem para antecipar; e do que espera que os outros façam, porque é um leilão.

O resultado emerge de milhões dessas decisões sob uma regra fixa.

O que o dado público mostra: quantas cotas foram contempladas, por grupo e mês, e quantas saíram por lance e por sorteio. O que não mostra: quem deu lance, de quanto, e quem perdeu. Esse limite acompanha o trabalho inteiro.

**Ponte:** Com isso dá para ver por que vale a pena estudar o tema.

**Se perguntarem**

- *Não dá para conseguir os lances com uma administradora?* — Seria dado privado, de uma administradora, sem garantia no prazo. O trabalho foi desenhado para funcionar sem isso, e essa é a contribuição metodológica.
- *A repartição lance/sorteio está em que nível?* — Administradora, UF e trimestre. Por grupo e mês só há o total de contemplados.

---

## Slide 8 — Por que estudar isso: três razões

**Fala**

Três razões. A primeira: a regra nunca foi avaliada. Sorteio, lance e a ordem entre eles foram fixados pela lei e pela resolução de 2023, consolidando a prática do setor, sem comparação com alternativas.

A segunda: a regra tem efeito distributivo. Ela decide quem recebe antes e quem espera. Vou detalhar no próximo slide.

A terceira, a que nos interessa como engenheiros: o problema é tratável com dados e computação. O dado é público mas agregado, e o jogo não tem fórmula. As duas coisas levam à mesma saída: simular o grupo, ajustar ao dado e comparar regras no simulador.

**Ponte:** O efeito distributivo merece um slide próprio.

---

## Slide 9 — O efeito distributivo: liquidez não é urgência

**Fala**

Todo mundo em dia recebe. A regra decide a ordem, e a ordem é quase soma zero: se alguém recebe no mês 10 em vez do 80, outro recebe mais tarde. E receber cedo vale dinheiro de verdade: aluguel que deixa de pagar, bem comprado antes.

A matriz mostra quem recebe cedo sob o lance. Quem tem urgência e caixa dá lance e recebe cedo: é a alocação que o lance promete. Quem tem urgência e não tem caixa depende da sorte: quem mais precisa espera. Quem tem caixa e pouca urgência pode furar a fila e ocupar a vaga de quem precisa. O problema é que o lance seleciona por liquidez, e liquidez não é urgência.

Há um contrapeso: o caixa do lance acelera o grupo todo. O trabalho quer medir esse saldo, com dois critérios: bem-estar agregado, ou seja, se o crédito está chegando cedo para quem mais valoriza, e dispersão do tempo de espera, ou seja, se a regra concentra espera longa em alguns.

**Ponte:** Se o problema é relevante, por que ninguém o resolveu?

**Se perguntarem**

- *Isso é um juízo de valor?* — Não: os critérios são explícitos e medidos. O trabalho mostra a ordenação das regras em cada critério; não decide qual critério pesa mais.

---

## Slide 10 — A lacuna: o parente informal já foi estudado; o consórcio, não

**Fala**

O consórcio tem um parente informal muito estudado: a ROSCA, a associação rotativa de poupança e crédito, que existe no mundo todo, tanda no México, chit fund na Índia.

A tabela mostra a diferença: na ROSCA a regra é do grupo, aqui é da lei; lá são poucos conhecidos, aqui milhões de desconhecidos; lá a garantia é pressão social, aqui contrato e supervisão; lá o prêmio é um pote fixo, aqui o número de vagas varia; lá o lance é desconto no pote, aqui antecipação de parcelas.

A literatura tem modelos e evidência sobre ROSCAs comparando sorteio e lance, como Besley, Coate e Loury e os trabalhos do Klonner. Nenhum cobre um mecanismo regulado, em escala nacional, com vagas variáveis. Essa é a lacuna.

**Ponte:** E existem razões concretas para essa lacuna ter ficado aberta.

**Se perguntarem**

- *Por que não aplicar direto o resultado das ROSCAs?* — Porque as diferenças da tabela mudam o problema. Os modelos de ROSCA são ponto de partida e caso de teste do simulador, não a resposta.
- *Tem trabalho brasileiro sobre consórcio?* — Há trabalhos descritivos, jurídicos e atuariais; não encontramos avaliação comparativa do mecanismo. A busca documentada entra no Capítulo 3.

---

## Slide 11 — Por que é difícil responder

**Fala**

A raiz da dificuldade é esta: as regras alternativas nunca foram usadas. Não existe dado sobre elas. Então não dá para comparar olhando os dados; é preciso prever como as pessoas agiriam sob uma regra nova. Isso exige um modelo de comportamento. E construir esse modelo esbarra em duas faltas, que vêm de duas literaturas diferentes.

A primeira é a falta do dado. A econometria de leilões mede comportamento olhando os lances de cada participante e deduzindo quanto cada um valoriza o prêmio. O método clássico faz isso invertendo a distribuição dos lances individuais. Aqui o Banco Central só publica totais. Então o comportamento tem de ser inferido dos totais.

A segunda é a falta da fórmula. A teoria de leilões deduz no papel qual é o lance ótimo. No caso de livro-texto, um leilão de primeiro preço com n participantes, a fórmula é: lance igual a n menos um sobre n vezes o valor. Mas essa fórmula depende de quatro hipóteses, e o consórcio quebra as quatro.

**Ponte:** Vou mostrar quais são.

**Se perguntarem**

- *Qual é o método da econometria de leilões?* — O de Guerre, Perrigne e Vuong (2000): recupera a distribuição de valorações a partir da distribuição de lances observados.
- *Dá para identificar algo só com totais?* — A exploração preliminar indica que sim no nível de administradora: a fração de lance varia muito entre administradoras, o que dá variação para identificar parâmetros. Os números formais estão sendo gerados e entram no Capítulo 5.

---

## Slide 12 — As quatro hipóteses da teoria que o consórcio quebra

**Fala**

Primeira, vagas. A teoria supõe que o número de prêmios é conhecido. No consórcio, as vagas de lance dependem do saldo, e o saldo depende dos próprios lances, como no exemplo da assembleia. Para decidir o lance eu preciso prever as vagas, que dependem dos lances dos outros.

Segunda, tipos. A teoria supõe que cada um difere numa coisa só, quanto valoriza o prêmio. Aqui são duas: urgência e liquidez, que funciona como teto do lance. Alguém urgente sem caixa e alguém tranquilo com caixa podem dar o mesmo lance. Com restrição de orçamento e dois tipos, a fórmula em geral deixa de existir.

Terceira, tempo. A teoria supõe um leilão, uma vez. Aqui são cerca de 200 assembleias: quem perde volta no mês seguinte, então o lance de hoje depende do valor de continuar na fila. E quem tem mais urgência e caixa sai primeiro, então o grupo muda de perfil.

Quarta, exclusão. A teoria supõe que ninguém sai. Aqui quem atrasa três parcelas sai e é restituído: isso tira concorrentes, mas também tira dinheiro do fundo. E atinge justamente quem tem pouca liquidez, então se liga ao ponto dois.

Cada uma sozinha complica; as quatro juntas e ligadas eliminam a fórmula. O simulador não precisa dela: só das regras e de como cada agente decide.

**Ponte:** Com isso, a pergunta e o caminho para respondê-la ficam claros.

**Se perguntarem**

- *Os modelos de ROSCA não resolvem isso?* — Resolvem casos simplificados, removendo pelo menos duas dessas características. Manter as quatro exige resolver numericamente.

---

## Slide 13 — A pergunta de pesquisa e os três passos para respondê-la

**Fala**

A pergunta: em que medida o mecanismo de contemplação vigente é eficiente, sob critérios de bem-estar e de estabilidade do grupo, comparado a alternativas admissíveis sob a mesma regulação?

Como não há dado das regras alternativas, a resposta passa por um modelo, e isso define três passos, cada um dependente do anterior.

Q1: como modelar o lance? É a consequência direta do slide anterior: a fórmula da teoria descreve o comportamento no consórcio, ou é preciso agentes que aprendem?

Q2: o modelo é fiel à realidade? Ajustado só com os totais do Banco Central, ele reproduz o que se observa? Sem isso, nada do que ele disser sobre outras regras vale.

Q3: qual regra é melhor? Com o modelo validado, alguma regra admissível supera a atual, mesmo com a incerteza que sobra nos parâmetros? Esta é a resposta à pergunta central.

Resumindo: Q1 define o comportamento, Q2 garante o modelo, Q3 responde à pergunta.

**Ponte:** Para essa pergunta, temos uma resposta provisória.

**Se perguntarem**

- *Quais são as alternativas?* — Sorteio ponderado pelo tempo de espera e lance de preço uniforme, entre outras admissíveis. Definição formal no Capítulo 4.
- *O que é 'admissível'?* — Respeita a Lei 11.795 e a Res. 285: fundo comum, igualdade entre consorciados, sorteio e lance como formas de contemplação.

---

## Slide 14 — O que esperamos mostrar

**Fala**

A proposição central é a resposta provisória, que o trabalho vai sustentar ou refutar. Duas partes.

A substantiva fala do consórcio: existe ao menos uma regra alternativa, permitida pela lei, que supera a atual em bem-estar e estabilidade.

A metodológica fala do método: dá para verificar isso por simulação ajustada só aos totais, sem ver lances individuais. Essa parte vale para outros sistemas observados só no agregado, e é a contribuição de Engenharia de Computação.

Ela não é assumida: vira uma hipótese em cada um dos três passos.

**Ponte:** Que são estas.

**Se perguntarem**

- *E se a regra atual for a melhor?* — É um resultado válido: H3 rejeitada. A proposição pode ser refutada.
- *Proposição e hipótese não são a mesma coisa?* — A proposição é a resposta geral; as hipóteses são as afirmações menores, uma por passo, cada uma com teste e critério de rejeição.

---

## Slide 15 — Uma hipótese para cada passo

**Fala**

Cada hipótese é a resposta que esperamos encontrar em um passo, com um teste e uma consequência se falhar.

H1, no passo do lance: a fórmula clássica não basta, agentes que aprendem no consórcio dão lances diferentes dela. Testamos colocando agentes de aprendizado por reforço no simulador e comparando com a fórmula. Se falhar, a fórmula basta e entra no simulador; o trabalho segue.

H2, no passo do modelo: o modelo ajustado aos totais acerta estatísticas que não viu no ajuste. Testamos calibrando com um grupo de estatísticas e conferindo no grupo reservado. Se falhar, o modelo não é confiável, e a comparação não é feita; esse limite passa a ser o resultado.

H3, no passo da regra: alguma regra admissível melhora um critério sem piorar os outros, em toda a faixa plausível de parâmetros. Testamos trocando a regra e repetindo com parâmetros variados. Se falhar, a regra atual é a melhor entre as testadas, e isso também é resposta.

Só H2 interrompe o caminho. E o trabalho afirma qual regra é melhor, não quanto, porque a magnitude herda toda a incerteza da calibração.

**Ponte:** Para testar isso, o trabalho precisa produzir algumas coisas.

**Se perguntarem**

- *Por que o experimento de H1 roda depois da calibração, se é o passo 1?* — Logicamente vem primeiro; na execução, os agentes que aprendem precisam do simulador pronto, e treiná-los dentro da calibração seria inviável. A calibração usa uma política de lance com poucos parâmetros.
- *O que é 'teoria estática'?* — A previsão de equilíbrio de um leilão de uma rodada. A literatura recente mostra que algoritmos que aprendem podem se afastar dela (Banchio e Skrzypacz, 2022).

---

## Slide 16 — O que o trabalho vai entregar

**Fala**

O objetivo geral: avaliar computacionalmente a regra de contemplação vigente, com um modelo multiagente ajustado aos dados públicos, e compará-la a alternativas sob critérios explícitos.

Oito objetivos específicos, cada um com um produto e um capítulo. A e B, painel de dados e fatos estilizados, no Capítulo 5. C, o modelo formal, no 4. D, E e F, simulador, verificação e calibração, no 6. G e H, comparação de regras e agentes que aprendem, no 7.

Objetivo é o que se entrega; hipótese é o que se testa com isso.

**Ponte:** Como cada entrega é produzida, na prática.

**Se perguntarem**

- *Algum objetivo já está pronto?* — O painel (a) está em construção, com pipeline versionado; a exploração dos fatos (b) foi feita e está sendo formalizada.

---

## Slide 17 — Como vamos fazer: sete etapas, o que se usa em cada uma

**Fala**

Tudo é feito em Python, versionado no Git, e cada etapa entrega um arquivo que a seguinte consome.

Um, dados: scripts em Python com pandas leem os arquivos do Banco Central e montam os painéis; testes automatizados com pytest conferem a integridade.

Dois, fatos: com pandas e NumPy calculamos as estatísticas que o modelo deve reproduzir, e separamos, antes de qualquer ajuste, o que é para calibrar e o que é para testar. Saem tabelas na pasta de resultados.

Três, modelo: esta etapa é no papel, sem software. Escrevemos as regras do jogo: o estado do grupo, os agentes com urgência e liquidez, as ações e a regra de contemplação. É a especificação que o código implementa.

Quatro, simulador: o modelo vira código em Python orientado a objetos, com NumPy, e sementes aleatórias fixas para que tudo seja reprodutível. A regra é uma peça plugável.

Cinco, verificar e calibrar: testes com pytest conferem o simulador contra casos que têm fórmula; depois o método de momentos simulados, com o otimizador do SciPy, ajusta os parâmetros ao dado.

Seis, comparar: Monte Carlo, ou seja, milhares de grupos simulados por regra, em paralelo.

Sete, aprendizado: agentes de Q-learning, implementados em Python sobre o simulador.

Embaixo, a infraestrutura comum: Git, Makefile, pytest, o script de auditoria que bloqueia número sem arquivo de resultado, e o pandoc que gera a monografia.

**Ponte:** O coração disso é o simulador; vale mostrar o que ele faz por dentro.

**Se perguntarem**

- *Por que Python e não Java ou C++?* — Ecossistema científico (pandas, NumPy, SciPy), velocidade de desenvolvimento e o fato de o pipeline de dados já estar em Python. Os trechos pesados são vetorizados em NumPy; se faltar desempenho, paraleliza-se a simulação.
- *O que é método de momentos simulados?* — Escolhe os parâmetros que deixam as estatísticas simuladas mais próximas das observadas, minimizando uma distância ponderada. Padrão quando o modelo não tem verossimilhança tratável.
- *Por que Q-learning?* — É o algoritmo usado no trabalho de referência sobre leilões com agentes que aprendem (Banchio e Skrzypacz, 2022), simples de implementar e de auditar.

---

## Slide 18 — Dentro do simulador

**Fala**

À esquerda, o que o código faz a cada assembleia. Arrecada as parcelas das cotas em dia. Sorteia entre as cotas em dia. Cada agente decide seu lance, olhando sua urgência, sua liquidez e o estado do grupo. Apura os lances com o saldo que sobrou. Exclui quem atrasou e restitui. Registra as estatísticas e vai para o mês seguinte. Isso se repete por uns 200 meses, para milhares de grupos.

À direita, as peças do código. O Grupo guarda o fundo, o mês e as cotas. O Agente, que é a cota, guarda urgência, liquidez, situação e a política de lance, que tem poucos parâmetros. A Regra de contemplação faz os passos 2 e 4, e todas as regras têm a mesma interface. A Calibração roda o simulador, compara com o Banco Central e ajusta os parâmetros.

É essa interface comum que permite trocar a regra vigente pelas alternativas, como o sorteio ponderado pela espera ou o lance de preço uniforme, sem mexer no resto.

**Ponte:** E a ordem em que tudo isso é usado importa.

**Se perguntarem**

- *Quantos agentes por grupo?* — O número de cotas do grupo, tirado do painel do Bacen; os grupos de imóveis têm centenas a milhares de cotas.

---

## Slide 19 — Por que a ordem importa

**Fala**

Nenhuma conclusão sobre regras sai antes de o simulador passar em dois testes.

Verificação: o simulador está certo? Ele reproduz as soluções que a teoria conhece em casos simples, como uma ROSCA de sorteio puro ou um leilão de uma rodada.

Validação: o simulador parece com a realidade? Acerta estatísticas reais que não usou no ajuste. É a H2.

Só então a comparação, a H3.

Se um teste falhar, o resultado é reportado; o modelo não é mexido até passar.

**Ponte:** Por fim, o que fica dentro e fora.

**Se perguntarem**

- *Diferença entre verificação e validação?* — Verificação: o código implementa o modelo corretamente. Validação: o modelo representa a realidade.

---

## Slide 20 — Até onde vamos, e o que pretendemos contribuir

**Fala**

Dentro: imóveis, a partir de julho de 2024, quando passou a valer a Resolução 285, e a regra de contemplação como objeto. Um regime só evita modelar a mudança de norma dentro dos dados.

Fora: análise jurídica, lances individuais, mercado secundário e concorrência entre administradoras, e taxa e fundo de reserva como decisão.

Contribuições: o modelo do consórcio como jogo dinâmico, com o que a ROSCA não tem; um método para inferir comportamento só com dado agregado, validado fora da amostra; e a primeira comparação sistemática, até onde verificamos, entre a regra vigente e alternativas.

**Ponte:** Para fechar, o capítulo inteiro numa tabela.

**Se perguntarem**

- *Pós-julho/2024 não é pouca série?* — Curta no tempo, larga no corte transversal: muitos grupos e administradoras. Períodos anteriores ficam como sensibilidade.

---

## Slide 21 — O capítulo 1 em uma tabela

**Fala**

Esta tabela é o Quadro 3 do texto. É a estrutura do primeiro slide, agora com hipóteses e objetivos. O resto do texto segue essa ordem: o Capítulo 2 descreve as regras, o 3 a literatura, o 4 o modelo, o 5 os dados, o 6 o simulador e a calibração, o 7 os resultados, o 8 a discussão e o 9 conclui.

Professor, gostaria de saber se essa estrutura ficou clara e se o senhor vê algum elo fraco antes de seguirmos para o Capítulo 2.

**Ponte:** (Abrir para comentários, depois seguir para o Capítulo 2.)
