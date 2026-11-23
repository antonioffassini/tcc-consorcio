---
secao: 7.6
titulo: Comparação com lance adaptado
status: rascunho
responsavel:
insumos:
  - results/agentes/
  - ESTADO.md §4, 2026-11-22 (critério de H4, protocolo dos agentes), escrito antes de rodar
  - src/analysis/agentes_rl.py
fontes:
  - results/h5_politica/h5_robustez_resumo.csv
  - results/agentes/h5_relativas_B_s1.csv
  - results/agentes/h5_diferencas_A.csv
  - results/agentes/h5_relativas_B.csv
  - results/agentes/h5_relativas_A.csv
  - results/agentes/h4_metricas.csv
  - results/agentes/h4_relativas.csv
  - results/agentes/treino_M2_s0_t2.csv
  - results/agentes/treino_M3rs_p0.05_s0_t2.csv
  - results/m3_relativas_B.csv
  - results/texto_2211_apresentacao.csv
excecoes:
  - 0,3
  - 0,2
  - 1
  - 0,25
  - 0,05
  - 7.500
paginas_alvo: 3
---

# Comparação com lance adaptado

As seções 7.4 e 7.5 compararam os desenhos mantendo a mesma política de lance em todos. A hipótese H4 pergunta se a ordenação obtida assim sobrevive quando os participantes adaptam o lance a cada regra. É a resposta deste trabalho à objeção de que avaliar uma regra nova com o comportamento estimado sob a antiga confunde o efeito da regra com a falta de reação a ela [@lucas1976econometric].

## Desenho do experimento

Os agentes da seção 6.2, já convergidos sob $M_0$, foram treinados de novo sob $M_2$ e sob $M_3^{rs}(0{,}05)$, partindo da tabela aprendida sob a regra vigente. O treino durou 7.500 episódios em cada desenho, e nos dois a ação de maior valor ficou estável em mais de 0,996 da massa de estados (`results/agentes/treino_M2_s0_t2.csv`, `results/agentes/treino_M3rs_p0.05_s0_t2.csv`). Com a tabela de cada desenho, sem exploração, os três desenhos foram simulados no conjunto B da seção 7.4, com os mesmos grupos e sementes, e comparados pelos mesmos critérios e pela mesma regra do intervalo de confiança.

## Níveis sob o mecanismo vigente

Com o lance aprendido, o nível do bem-estar sob $M_0$ é 0,3489 crédito por cota, a espera média é de 36,95 meses e 0,7754 das contemplações ocorrem por lance (`results/agentes/h4_metricas.csv`). Os agentes ofertam mais do que a política calibrada: são contemplados mais cedo, pagam mais por isso e terminam com bem-estar menor. A fração de lance que produzem fica perto da observada nos dados, embora eles não tenham sido calibrados a ela.

## Resultado

**Tabela 7.14 — Comparação com lance aprendido sob cada desenho, conjunto B, em % do nível de $M_0$ (IC de 95%)**

| Desenho | $\mathcal{W}$ | $\mathcal{E}$ | $\mathcal{S}$ | $\mathcal{R}$ | Domina? |
|---|---|---|---|---|---|
| $M_2$ | 2,03 (1,88; 2,18) | 0,70 (0,54; 0,93) | −0,65 (−1,80; −0,15) | −0,07 (−0,11; −0,02) | não |
| $M_3^{rs}(0{,}05)$ | 2,49 (2,28; 2,69) | 1,51 (1,39; 1,67) | −0,60 (−2,20; 0,49) | −0,06 (−0,14; 0,00) | não |

Fonte: elaborado pelos autores (`results/agentes/h4_relativas.csv`).

Com o lance adaptado, nenhum dos dois desenhos domina o vigente. Os dois aumentam o bem-estar, com o intervalo inteiro do lado favorável, e os dois aumentam a dispersão da espera, também com o intervalo inteiro do lado desfavorável. Pela regra registrada, **H4 é rejeitada**: o desenho que domina $M_0$ com comportamento fixo deixa de dominá-lo quando o lance se adapta.

## O que muda e o que se mantém

O ganho de bem-estar do preço uniforme se mantém e aumenta. Com a política fixa, $M_3^{rs}(0{,}05)$ melhorava o bem-estar em 1,28% (`results/m3_relativas_B.csv`); com o lance aprendido, em 2,49%. A objeção de Lucas sugeria o contrário: que, sob preço uniforme, os participantes ofertariam mais e o ganho de pagar menos desapareceria. Não é o que acontece no ambiente simulado. O lance médio aprendido sob preço uniforme é ligeiramente menor que sob a regra vigente, e o ganho de bem-estar cresce.

O que não se mantém é a neutralidade sobre a dispersão. Com a política fixa, o lance mínimo excluía do leilão os ofertantes de lance baixo, e o sorteio obrigatório da sobra devolvia o saldo na mesma assembleia; era isso que anulava o aumento da dispersão causado pelo preço uniforme. Os agentes aprendem a ofertar acima do mínimo: a fração de contemplações por lance cai só 1,04% sob $M_3^{rs}(0{,}05)$, contra a queda grande observada com a política fixa, o sorteio da sobra quase não é acionado e o desenho passa a se comportar como $M_2$, com dispersão ainda maior.

## Leitura

O resultado separa duas afirmações. A primeira se sustenta nas duas formas de comportamento, nas amostras de escolha e de avaliação e, com comportamento fixo, na varredura de robustez: **o preço uniforme aumenta o bem-estar dos participantes e reduz a instabilidade do fundo**. A segunda não se sustenta: **que um desenho admissível possa fazer isso sem custo para a igualdade da espera**. Com comportamento adaptado, o ganho de bem-estar vem acompanhado de mais dispersão, e a escolha entre o desenho vigente e o preço uniforme passa a depender do peso que se dá a cada critério.

Duas limitações qualificam o resultado. O treino sob $M_2$ e $M_3^{rs}(0{,}05)$ usou uma semente, enquanto sob $M_0$ foram duas; e os agentes não são calibrados aos dados (seção 6.2), de modo que o nível de bem-estar que produzem não é comparável ao da política calibrada, apenas as diferenças entre desenhos sob o mesmo comportamento.

## Um desenho robusto ao aprendizado

A rejeição de H4 deixa uma pergunta que este trabalho formulou só depois de vê-la, e que por isso é tratada como exploratória: existe um desenho admissível que domine o vigente mesmo quando o lance se adapta (hipótese H5)? O diagnóstico de H4 orientou a busca. O atenuante de $M_3^{rs}(0{,}05)$ dependia de os participantes deixarem saldo para o sorteio da sobra, e é justamente isso que o aprendizado desfaz. Um atenuante robusto deve atuar sobre algo que o participante não controla.

Foram registradas, antes de qualquer treino, oito variantes em duas linhas. A primeira é o lance fixo, praticado por algumas administradoras: um percentual postado, e um sorteio entre os que aceitam pagá-lo, à frente do lance livre ou no lugar dele (seção 2.2). Num preço postado, o participante só decide aceitar ou não, e não há lance a sombrear. A segunda é $M_3^{rs}(0{,}05)$ com o sorteio das cotas ativas ponderado pela espera já cumprida, com $\beta$ igual a 0,25 ou 1, como em $M_1$. A segunda linha foi acrescentada depois de um teste de fumaça do código, de um grupo, sem intervalos de confiança, que mostrou o lance fixo alongando a espera; a emenda está registrada. Os agentes foram treinados de novo sob cada variante, a escolha foi feita no conjunto A pela regra de dominância, com desempate pelo maior bem-estar, e o teste, no conjunto B.

**Tabela 7.15 — Família de H5 no conjunto A, com lance aprendido, em % do nível de $M_0$**

| Variante | $\mathcal{W}$ | $\mathcal{E}$ | $\mathcal{S}$ | $\mathcal{R}$ | Domina? |
|---|---|---|---|---|---|
| 1 fixo de 0,2 + livre pay-as-bid | 2,81 | 3,18 | 9,43 | 0,84 | não |
| 1 fixo de 0,2 + $M_3^{rs}(0{,}05)$ | 4,57 | 4,94 | 7,75 | 0,91 | não |
| 2 fixos de 0,2 + $M_3^{rs}(0{,}05)$ | 6,90 | 7,50 | 8,89 | 1,65 | não |
| 1 fixo de 0,3 + $M_3^{rs}(0{,}05)$ | 4,03 | 2,99 | 6,60 | 0,68 | não |
| Só fixo de 0,2 | 20,82 | 22,82 | −35,01 | 2,12 | não |
| Só fixo de 0,3 | 18,20 | 16,70 | −21,52 | 1,97 | não |
| $M_3^{rs}(0{,}05)$, espera $\beta = 0{,}25$ | 1,07 | −0,83 | −1,22 | −0,16 | sim |
| $M_3^{rs}(0{,}05)$, espera $\beta = 1$ | −0,16 | −2,97 | −1,51 | −0,18 | sim |

Fonte: elaborado pelos autores (`results/agentes/h5_relativas_A.csv`).

Nenhuma variante de lance fixo domina. Todas aumentam o bem-estar, mas pioram a dispersão e o tempo de restituição, e a espera média cresce entre 2,48 e 12,95 meses (`results/agentes/h5_diferencas_A.csv`). O mecanismo é o mesmo de H4, em forma mais aguda: o preço postado fica abaixo dos lances que os agentes ofertam sob a regra vigente, a arrecadação cai, e o fundo contempla menos cotas por mês. As duas variantes com sorteio ponderado pela espera dominam. Pela regra registrada, a escolhida é a de $\beta = 0{,}25$, que tem o maior bem-estar; ela é chamada $M_4$ daqui em diante.

**Tabela 7.16 — $M_4$ no conjunto B e nas verificações secundárias, em % do nível de $M_0$ (IC de 95%)**

| Avaliação | $\mathcal{W}$ | $\mathcal{E}$ | $\mathcal{S}$ | $\mathcal{R}$ | Domina? |
|---|---|---|---|---|---|
| Lance aprendido | 0,81 (0,34; 1,38) | −0,93 (−1,40; −0,35) | −1,33 (−3,35; −0,52) | −0,10 (−0,20; 0,02) | sim |
| Política calibrada | 0,15 (−0,07; 0,29) | −2,32 (−3,02; −1,76) | −2,95 (−7,39; −1,07) | −0,15 (−0,29; 0,03) | sim |
| Política calibrada, $F_\theta$ Gamma | 1,43 (0,83; 1,78) | −0,22 (−0,93; 0,36) | −1,95 (−6,62; 1,12) | −0,21 (−0,39; 0,09) | sim |

Fonte: elaborado pelos autores (`results/agentes/h5_relativas_B.csv`).

No conjunto B, com lance aprendido, $M_4$ domina o vigente: aumenta o bem-estar, reduz a dispersão da espera e a instabilidade do fundo, e não piora o tempo de restituição. Pela regra registrada, **H5 não é rejeitada**; a seção seguinte mostra o quanto esse resultado depende do treino. A dominância se mantém com a política calibrada e sob a forma Gamma da urgência, as duas situações em que $M_3^{rs}(0{,}05)$ a perdia ou dependia dela. A espera média cresce 1,62%, porque o sorteio passa a favorecer quem espera há mais tempo e o lance mínimo exclui parte dos lances baixos; a espera média não é critério de avaliação, mas o aumento é relatado.

A razão da robustez está na divisão de trabalho entre as peças. O preço uniforme continua a produzir o ganho de bem-estar e a redução da instabilidade. O peso da espera no sorteio compensa o aumento de dispersão que o preço uniforme causa quando os agentes aprendem, e o faz por um canal que o lance não alcança: a espera já cumprida de cada cota não depende do que ela oferta. O resultado tem dois limites de origem, discutidos na seção 8.3: H5 foi formulada depois de H4, e o ganho de bem-estar com a política calibrada tem intervalo que cruza o zero.

## Verificações depois do teste

Duas verificações foram decididas depois do teste no conjunto B e são relatadas como saíram. Com a política calibrada, nos dez sorteios dos parâmetros calibrados da seção 7.5, $M_4$ domina o vigente em nove (`results/h5_politica/h5_robustez_resumo.csv`), acima do limiar de oito usado para $M_3^{rs}(0{,}05)$. Com uma segunda semente de treino dos agentes, o resultado muda.

**Tabela 7.17 — Variantes com peso da espera, segunda semente dos agentes, conjunto B, em % do nível de $M_0$ (IC de 95%)**

| Variante | $\mathcal{W}$ | $\mathcal{E}$ | $\mathcal{S}$ | $\mathcal{R}$ | Domina? |
|---|---|---|---|---|---|
| $M_4$ ($\beta = 0{,}25$) | 2,46 (1,73; 3,13) | 2,17 (1,50; 2,54) | 0,96 (0,07; 2,92) | −0,02 (−0,11; 0,07) | não |
| $\beta = 1$ | 0,06 (−1,03; 1,29) | −0,21 (−2,19; 1,33) | 0,04 (−1,47; 1,06) | −0,10 (−0,19; −0,01) | sim |

Fonte: elaborado pelos autores (`results/agentes/h5_relativas_B_s1.csv`).

Com a segunda semente, $M_4$ deixa de dominar: o bem-estar sobe mais do que com a primeira, mas a dispersão e a instabilidade pioram, como em $M_3^{rs}(0{,}05)$. A variante com peso mais forte, $\beta = 1$, treinada com a segunda semente só para este diagnóstico, não piora nenhum critério nas duas sementes, mas seu ganho de bem-estar desaparece, e com a segunda semente o único critério que melhora é o tempo de restituição.

A leitura que o conjunto dos resultados sustenta é mais estreita do que a da seção anterior. Pela regra registrada, H5 não é rejeitada, mas a dominância de $M_4$ depende da semente de treino dos agentes. O que se mantém nas duas sementes é uma fronteira: o peso da espera no sorteio troca bem-estar por igualdade na espera, e existe uma intensidade, $\beta = 1$, em que nenhum critério piora em relação ao vigente com o lance aprendido. Um desenho que melhore ao mesmo tempo o bem-estar e a dispersão, com o comportamento adaptado e de forma robusta ao treino, não foi encontrado.
