# Diário de bordo — roteiro de fala

## 1. Diário de bordo

Bom dia. Hoje não vou só mostrar resultados: vou contar como chegamos a eles. O trabalho passou por seis fases, o modelo teve quatro versões, e cada hipótese nasceu de um problema que a anterior revelou. Esse caminho é parte do resultado, porque mostra o que os dados públicos conseguem rejeitar e o que só a simulação com agentes revela.

## 2. Sorteio e lance nunca foram postos à prova

O trabalho em uma página. O consórcio aloca crédito por sorteio e por lance, e essas regras, fixadas pela Lei 11.795 e pela norma do Banco Central, nunca foram comparadas com alternativas. Modelamos o grupo como um jogo de alocação entre participantes diferentes entre si e com liquidez limitada, calibramos a simulação nos dados públicos do Bacen, que não trazem os lances individuais, e comparamos o desenho vigente com alternativas admissíveis pela lei. Os critérios são quatro: bem-estar dos participantes, dispersão da espera, instabilidade do fundo e tempo de restituição dos excluídos. Um desenho só é melhor se melhora algum sem piorar nenhum.

## 3. Quatro perguntas, cada uma com regra de rejeição prévia

As quatro hipóteses, cada uma com regra de rejeição escrita antes de rodar. H1 é auxiliar: se a teoria estática bastasse, não precisaríamos de simulação. H2 é a validação: o modelo tem de acertar o que não viu. H3 é a comparação com comportamento fixo. H4 é a central: uma recomendação de desenho só vale se sobreviver à reação dos participantes. Vamos voltar a cada uma delas ao longo da história.

## 4. Seis fases, quatro versões do modelo

Esta é a linha do enredo. Na fase 2 apresentamos o protótipo. Na fase 3 o modelo ganhou heterogeneidade e foi calibrado. Na fase 4 descobrimos que ele estava errado em pontos que só os contratos revelaram, e o refizemos. Na fase 5 entraram os agentes que aprendem, e eles derrubaram parte do resultado. A fase 6 é a resposta a essa queda.

## 5. As sete etapas, no protótipo e hoje

No fim da fase 2 tínhamos as quatro primeiras etapas, com o simulador ainda em protótipo. Hoje as sete estão feitas.

## 6. O modelo apanha dos dados

Primeiro ato: o modelo. A história aqui é de humildade. Fizemos um protótipo razoável, e os agregados do Banco Central foram mostrando, um a um, onde ele estava errado.

## 7. Uma assembleia, mês a mês

A ordem é sempre a mesma: arrecada, sorteia uma cota ativa, sorteia as excluídas num sorteio separado com teto de restituição, faz o leilão de lance com o saldo residual e, dependendo do contrato, sorteia de novo com o que sobrou. Os itens em laranja vieram da leitura dos regulamentos, nas fases 4 e 5. O que se disputa não é se a cota recebe, mas quando.

## 8. O que derrubou cada versão

Este gráfico conta o primeiro ato. O protótipo, v1, simulava grupos fechados e punha ativas e excluídas no mesmo sorteio: errava os meses sem contemplação, a dispersão entre administradoras e a fração dos sorteios que vai a excluídas. A v2 corrigiu tudo isso e ajustava os momentos de calibração quase perfeitamente. Mas, no teste com a estatística que ela não tinha visto, a correlação entre tamanho do grupo e lance deu praticamente zero. Esse foi o momento de maior tensão do trabalho.

## 9. Ajustava tudo e errava o que não viu

A v2 era bonita: os quatro momentos de calibração batiam. O teste fora da amostra mostrou que uma das regras anulava, por construção, a relação entre tamanho e lance. Fomos aos contratos de Porto Seguro, Itaú, Santander e Sicredi e reescrevemos o simulador cláusula por cláusula. A v3 acerta o sinal. O custo é que o segundo teste já não é cego, porque revisamos depois de ver o primeiro, e dizemos isso no texto. Na v4 ainda corrigimos a escala da urgência, que equivalia a descontar a espera a 172% ao ano.

## 10. A sobra do lance: quem sorteia de novo

Uma das perguntas de vocês foi por que calibrar η se ele está no contrato. Correto: agora ele vem do contrato. Nas quatro administradoras cujo regulamento lemos, três mandam a sobra a novo sorteio e o Santander a guarda. Para as outras, usamos 0,75, a proporção observada. Isso tirou um parâmetro da calibração e permitiu incluir φ₁ no vetor calibrado.

## 11. Três parâmetros, quatro momentos

Calibramos três parâmetros: φ₀, o nível do lance; φ₁, quanto a urgência pesa no lance, que agora é calibrado e não fixo; e r̄, o teto de restituição das excluídas. A distância Q no ótimo é 1,90 com um grau de liberdade. Todos os quatro momentos ficam dentro de dois erros-padrão.

## 12. Os quatro momentos dentro de dois erros-padrão

Em cinza, o dado do Bacen com dois erros-padrão; em azul, o modelo calibrado. Os quatro momentos ficam dentro da faixa. A taxa de contemplação aparece multiplicada por cem para caber na escala.

## 13. O modelo acerta o que não viu

As estatísticas reservadas são as que a calibração não usa. A principal é a correlação entre o tamanho dos grupos da administradora e a fração de lance. O modelo reproduz o sinal e a ordem de grandeza. O teste tem pouco poder, e dizemos isso no texto.

## 14. A primeira resposta

Segundo ato. Com o modelo validado, fizemos a pergunta original do trabalho, H3: algum desenho admissível domina o vigente? Para isso adotamos uma premissa forte, que vai voltar para nos cobrar: o comportamento de lance é o mesmo sob todas as regras.

## 15. Do vigente ao preço uniforme

M0 é a regra vigente: quem dá o maior lance ganha e paga o que ofertou. M1 mexe no sorteio: quem espera há mais tempo tem mais chance. M2 mexe no lance: todos os vencedores pagam o mesmo preço, o primeiro lance recusado. A família M3 combina o preço uniforme com dois instrumentos que o mercado já usa, o lance mínimo e o sorteio da sobra.

## 16. M3ʳˢ(0,05) domina o vigente

Com o comportamento de lance mantido, M1 reduz a dispersão mas custa bem-estar. M2 aumenta o bem-estar e reduz a instabilidade, mas aumenta a dispersão. M3 com lance mínimo de 5% e sorteio da sobra pega o ganho do M2 e neutraliza a dispersão: o intervalo dela cruza o zero. Pela regra do intervalo de confiança, domina o vigente. H3 é aceita, com o comportamento fixo.

## 17. Escolher num conjunto, testar em outro

Conjunto A e conjunto B: é a mesma lógica de treino e teste em aprendizado de máquina. Com onze variantes, uma pode ganhar por acaso. Então escolhemos no conjunto A e só aceitamos se a escolhida também dominar no conjunto B, com outros grupos sorteados e outras sementes. E ainda passamos por dez sorteios dos parâmetros calibrados: dominou em oito.

## 18. O motor é o preço uniforme

A pergunta de vocês foi: se o M3 é o que o mercado já faz, o que trouxemos de novo? A decomposição responde. Lance mínimo e sorteio da sobra, sozinhos, já são práticas de mercado, D2, e já dominam o vigente, mas com ganho de bem-estar pequeno: 0,26%. O que multiplica o ganho por cinco é o preço uniforme, que o mercado não pratica. Os outros dois instrumentos é que tornam o preço uniforme aceitável, porque neutralizam o aumento de dispersão.

## 19. E se o participante mudar de comportamento?

O resultado de H3 era bom demais para não ser questionado. A premissa de comportamento fixo é exatamente o que a crítica de Lucas proíbe: mudar a regra muda a decisão. E a teoria de leilão não resolve, porque o consórcio não é um leilão único. É exatamente o que H1 e H4 testam: H1, se a teoria estática descreve quem aprende; e H4, a central, se a dominância sobrevive quando o lance se adapta. Para responder, precisávamos de agentes que aprendem.

## 20. Os agentes aprendem

Terceiro ato, a parte de inteligência artificial.

## 21. Agentes que aprendem a dar lance

Os agentes usam Q-learning tabular de Monte Carlo. Cada cota observa sua urgência, sua liquidez, o prazo restante e o lance de corte da assembleia anterior; escolhe um lance; e no fim do grupo recebe sua utilidade. O próximo slide conta as duas tentativas de treino. Os agentes chegam a uma fração de lance de 0,775, perto dos 0,734 dos dados, sem serem calibrados a ela.

## 22. Duas tentativas, um critério endurecido

Na primeira tentativa, com passo constante e recompensa muito ruidosa, a melhor ação ficava alternando entre lances de valor quase igual, e a convergência parou em três quartos dos estados. Trocamos o passo pela média amostral. Aí o critério foi atingido cedo demais, com exploração ainda alta. Em vez de comemorar, endurecemos: a convergência só passa a contar depois de a exploração chegar ao piso. Com isso, mais de 99,9% dos estados estáveis, nas duas sementes.

## 23. Quem aprende não dá o lance da teoria

No início do grupo, teoria e agentes ficam juntos, perto de 0,47. No fim, divergem: os pouco urgentes ofertam mais que a teoria e os muito urgentes, menos. A diferença média é 0,072, acima do limiar de 0,05 registrado antes. Conclusão de H1: a teoria estática não descreve quem otimiza no grupo.

## 24. Com agentes, nenhum desenho domina

Aqui está o ponto alto do uso de IA. Retreinamos os agentes sob M2 e sob M3. O ganho de bem-estar não só se mantém como cresce, de 1,28% para 2,49%. Mas a dispersão passa a piorar com o intervalo inteiro do lado desfavorável. Pela regra, H4 é rejeitada. A simulação com comportamento fixo não teria mostrado isso.

## 25. Os agentes desfazem o atenuante

O mecanismo é este: no consórcio, o lance financia as contemplações do mês. Se o vencedor paga menos, o fundo contempla menos gente por mês e a espera dos outros alonga. Com política fixa, o lance mínimo e a sobra compensavam. Os agentes aprendem a ofertar acima do mínimo, a sobra quase não aparece e o atenuante some.

## 26. A forma se escolhe pelo dado, não pelo resultado

Vocês levantaram que escolher a distribuição pelo resultado seria ajuste pelo desfecho. Registramos a regra antes de rodar: comparar as três formas pela aderência, com o mesmo protocolo. A lognormal ajusta melhor e a mistura é rejeitada no teste. Mas a Gamma não é rejeitada, e sob ela o M3 deixa de dominar. Fica como sensibilidade no texto.

## 27. A busca

Quarto ato. A rejeição de H4 deixou uma pergunta: existe desenho admissível que domine o vigente mesmo com o lance adaptado? Essa é H5. Ela foi formulada depois de ver H4, e por isso é exploratória, e dizemos isso.

## 28. A primeira ideia falhou antes de começar

A primeira ideia foi o lance fixo: com preço postado, o participante só decide aceitar ou não, e não há o que sombrear. Antes de treinar, rodamos um teste de fumaça só para ver o código funcionar, e ele já mostrou o problema: o preço postado fica abaixo dos lances que os agentes dariam, a arrecadação cai e a espera alonga. Isso apontou o canal certo: algo que o participante não controla. A espera já cumprida. Fizemos a emenda, registrada, e ficaram oito variantes.

## 29. Três peças, cada uma com uma função

Formalmente, M4 é o M3 escolhido na fase anterior com uma única mudança: no sorteio das cotas ativas, cada cota pesa um mais o número de meses no grupo, elevado a 0,25. É um peso suave. O preço uniforme continua a dar o ganho de bem-estar; o lance mínimo e a sobra seguram o preço e o saldo; o peso da espera devolve igualdade por um canal que o lance não alcança.

## 30. Oito variantes, escolha no conjunto A

Registramos oito variantes antes de treinar: quatro de lance fixo com lance livre, duas só de lance fixo e duas com o sorteio ponderado pela espera. A segunda linha entrou por emenda registrada, depois de um teste de fumaça do código. No conjunto A, com os agentes retreinados em cada variante, nenhuma de lance fixo domina: o preço postado arrecada menos que os lances altos dos agentes, e o fundo contempla menos por mês. As duas com peso da espera dominam. Pela regra, fica a de maior bem-estar entre as que dominam: β igual a 0,25. É o M4.

## 31. M4 domina o vigente na semente registrada

No conjunto B, que não foi usado na escolha, M4 domina o vigente com os agentes da semente registrada: bem-estar mais 0,81%, dispersão menos 0,93%, instabilidade menos 1,33%. Domina também com a política calibrada, em nove de dez sorteios dos parâmetros, e sob a distribuição Gamma da urgência, justamente as situações em que o M3 falhava. A espera média sobe 1,6%, e relatamos isso. O próximo slide mostra o limite.

## 32. O resultado depende do treino

Fizemos a verificação que faltava: uma segunda semente de treino dos agentes. Com ela, M4 deixa de dominar: o bem-estar sobe ainda mais, mas a dispersão e a instabilidade pioram, como no M3. A variante com peso mais forte da espera, β igual a 1, não piora nenhum critério nas duas sementes, mas o ganho de bem-estar desaparece. Então a conclusão honesta é: o preço uniforme dá o bem-estar; o peso da espera é o instrumento para devolver igualdade; e a intensidade em que os dois ganhos convivem com agentes que aprendem não é estável entre sementes. É um resultado que só a simulação com agentes mostra.

## 33. O bem-estar é firme; a igualdade depende do treino

Aqui está o quadro completo com agentes. Todas as barras de bem-estar estão do lado bom. Na dispersão, só o M4 com a semente registrada fica do lado bom. É esse o resultado honesto: o preço uniforme é firme, o peso da espera é a direção.

## 34. De onde veio cada hipótese

Recapitulando o enredo. H3 é a pergunta com que começamos. H2 nasceu da limitação dos dados: sem lances individuais, validamos com estatísticas reservadas. H1 e H4 nasceram de uma objeção à nossa própria premissa. H5 nasceu do diagnóstico da queda de H4. Cada hipótese posterior ao resultado que a motivou está declarada como tal no texto.

## 35. As cinco hipóteses

A mensagem final tem duas partes. O preço uniforme melhora o bem-estar dos participantes e a estabilidade do fundo em todos os testes. Sozinho, porém, custa igualdade na espera quando os participantes aprendem. Ponderar o sorteio pela espera contém esse custo por um canal que o lance não alcança; M4 domina o vigente na semente registrada, mas a dominância com agentes não é estável entre sementes, então apresentamos o peso da espera como direção, não como prescrição.

## 36. Texto em rascunho sobre os números reais

Todo o texto está em rascunho sobre os números reais. A auditoria automática garante duas coisas: nenhum número sem tabela de origem e nenhuma citação sem PDF. O que falta: o lado Java do docking, o P5 de revisão adversarial e a revisão do orientador.

## 37. Até a entrega

Os próximos passos são revisão, docking e fechamento. Os dois riscos que levamos à banca, já declarados no texto: os agentes sob os desenhos alternativos treinaram com uma semente, e a forma da distribuição de urgência os dados agregados só identificam em parte.

## 38. refs1

Referências usadas nesta apresentação; todas com PDF conferido na página de rosto em refs/pdfs.

## 39. refs2

Referências usadas nesta apresentação; todas com PDF conferido na página de rosto em refs/pdfs.

## 40. refs3

Referências usadas nesta apresentação; todas com PDF conferido na página de rosto em refs/pdfs.
