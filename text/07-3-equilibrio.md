---
secao: 7.3
titulo: Lance aprendido e teoria estática
status: rascunho
responsavel:
insumos:
  - results/agentes/
  - ESTADO.md §4, 2026-11-22 (critério de H1, protocolo dos agentes, tentativas 1 e 2), escritos antes de rodar
  - src/analysis/agentes_rl.py
fontes:
  - results/agentes/h1_teste.csv
  - results/agentes/h1_detalhe.csv
  - results/agentes/treino_M0_s0_t2.csv
  - results/agentes/treino_M0_s1_t2.csv
excecoes:
  - 0,05
  - 200
  - 15.000
paginas_alvo: 3
---

# Lance aprendido e teoria estática

A hipótese H1 pergunta se o lance de participantes que aprendem sob a regra vigente pode ser descrito pela teoria estática de leilões. Se pudesse, o trabalho não precisaria de agentes nem de simulação para prever o comportamento. Esta seção compara o lance aprendido pelos agentes da seção 6.2, sob $M_0$, com a previsão estática registrada antes do treino.

## A previsão estática

A previsão para cada participante é $b^{st}_i = \min(\lambda_i + \bar b^e,\ v_i)$, com $v_i = 1 - e^{-\theta_i \bar w_i/12}$. O valor $v_i$ é o ganho de ser contemplado agora em vez de esperar o sorteio, cuja espera esperada $\bar w_i$ é a metade dos meses restantes no grupo. Com muitos ofertantes, o lance de equilíbrio no leilão de primeiro preço com valores privados se aproxima do próprio valor, e a liquidez mais o teto do embutido limitam o quanto se pode ofertar. É a resposta que a teoria clássica daria sem modelar o fundo, a repetição das assembleias nem o efeito de cada contemplação sobre os demais. Para o cálculo, os meses restantes usam o prazo típico de 200 assembleias.

## Convergência

Na segunda tentativa, os agentes convergiram sob $M_0$ nas duas sementes: depois de a exploração chegar ao piso, no episódio 15.000, a ação de maior valor ficou estável em mais de 0,999 da massa de estados visitados (`results/agentes/treino_M0_s0_t2.csv`, `results/agentes/treino_M0_s1_t2.csv`). O lance médio aprendido, ponderado pela frequência dos estados, é de 0,4717 e 0,4765 do crédito nas duas sementes.

## Resultado

A diferença absoluta média entre o lance aprendido e a previsão estática, ponderada pela frequência com que cada estado é visitado, é de 0,0721 crédito na primeira semente e de 0,0707 na segunda, acima do limiar registrado de 0,05 (`results/agentes/h1_teste.csv`). Pelo critério, **H1 é aceita**: a teoria estática não descreve o lance aprendido. A diferença, porém, não é grande. Em média, os agentes ofertam 0,4717 contra 0,4354 da previsão, cerca de quatro pontos percentuais do crédito acima.

A média esconde um padrão que aparece quando se separa a população por urgência e pelo momento do grupo.

**Tabela 7.6 — Lance aprendido e previsão estática por quintil de urgência e fase do grupo (semente 0)**

| Quintil de urgência | Fase do grupo | Previsão estática | Lance aprendido | Diferença |
|---|---|---|---|---|
| 1º (menos urgente) | início | 0,4396 | 0,4805 | 0,0409 |
| 1º | fim | 0,0988 | 0,2444 | 0,1456 |
| 3º | início | 0,4711 | 0,4830 | 0,0118 |
| 3º | segundo quarto | 0,4194 | 0,2925 | −0,1269 |
| 5º (mais urgente) | início | 0,4710 | 0,4832 | 0,0122 |
| 5º (mais urgente) | segundo quarto | 0,4681 | 0,2896 | −0,1785 |
| 5º (mais urgente) | fim | 0,2968 | 0,1734 | −0,1234 |

Fonte: elaborado pelos autores (`results/agentes/h1_detalhe.csv`). "Início" = mais de três quartos do prazo pela frente; "segundo quarto" = entre um quarto e metade; "fim" = menos de um quarto.

No início do grupo, aprendizado e teoria quase coincidem: todos ofertam perto do máximo que a liquidez e o embutido permitem. A diferença aparece adiante, em dois sentidos opostos. Os participantes mais urgentes ofertam bem menos do que a teoria prevê na segunda metade do grupo; os menos urgentes ofertam mais perto do fim. A teoria estática faz o lance crescer com a urgência em qualquer fase; o lance aprendido é muito menos sensível a ela depois do início.

Uma leitura possível é a do próprio mecanismo. Na regra vigente, cada vencedor paga o próprio lance, e quem ganha com um lance alto paga caro por isso; o participante urgente aprende que, no meio do grupo, um lance menor ainda vence com frequência, porque o saldo disponível e a concorrência mudam de uma assembleia para outra, e a informação do menor lance vencedor anterior lhe diz onde está o corte. A teoria estática não tem esse corte a observar. A leitura é uma interpretação, e não um resultado testado: a seção não decompõe o comportamento aprendido nas suas causas.

## Alcance

O resultado diz que, no ambiente calibrado, um participante que otimiza não segue a regra estática, e que a diferença é moderada na média e grande em partes da população. Ele não diz que os participantes reais se comportam como os agentes: os agentes não foram calibrados aos dados (seção 6.2). O papel de H1 no trabalho é justificar que a avaliação dos desenhos com comportamento adaptado, na seção 7.6, precisa de simulação.
