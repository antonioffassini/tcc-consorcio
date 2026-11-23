---
secao: 7.5
titulo: Robustez da ordenação
status: rascunho
responsavel:
insumos:
  - results/
  - ESTADO.md §4, 2026-11-19 (regra de robustez de H3) e 2026-11-22 (nova base, rodada invariante, conjuntos A e B, corte das sensibilidades); §5 itens 29, 33 e 34
fontes:
  - results/sens_forma_ajuste.csv
  - results/sens_forma_relativas.csv
  - results/sens_mistura/calibracao_momentos.csv
  - results/sens_gamma/calibracao_momentos.csv
  - results/texto_2211_apresentacao.csv
  - results/h3_robustez_resumo_sobra_reg.csv
  - results/h3_relativas_sobra_reg.csv
  - results/m3_relativas_B.csv
  - results/h3_relativas.csv
  - results/h3_robustez_resumo.csv
  - results/sens_invariante/h3_diferencas_sobra.csv
excecoes:
  - 172
  - 0,05
  - 0,2
  - 0,5
paginas_alvo: 4
---

# Robustez da ordenação

A hipótese H3 tem duas partes: existe um desenho que domina o vigente, e essa ordenação é robusta à incerteza de calibração compatível com os dados. A seção 7.4 tratou da primeira. Esta seção trata da segunda por três vias: repetindo a comparação em parâmetros sorteados do bootstrap de calibração, mudando a escala da urgência sem mudar o comportamento e comparando as versões anteriores do modelo, que diferem da atual justamente nas regras contratuais revistas.

## Incerteza de calibração

A comparação foi repetida em dez estimativas de $\Theta$ sorteadas entre as do bootstrap de calibração (seção 6.3), com uma réplica cada. A regra, registrada antes, exige que em pelo menos oito dos dez sorteios nenhuma estimativa pontual de critério piore mais que 1% do nível de $M_0$ e ao menos uma melhore mais que 1%. O limiar de 1% existe porque, com uma réplica por sorteio, não há intervalo de confiança em cada sorteio, e diferenças muito pequenas não devem contar como piora nem como melhora.

**Tabela 7.11 — Robustez: dez sorteios de $\Theta$, em % do nível de $M_0$**

| Desenho | Amostra | Dominância pontual | Bem-estar, mín. a máx. | Dispersão, mín. a máx. |
|---|---|---|---|---|
| $M_1$, $\beta=0{,}5$ | calibrada | 2 de 10 | −1,27 a −0,79 | −2,78 a −1,96 |
| $M_1$, $\beta=1$ | calibrada | 0 de 10 | −2,07 a −1,43 | −4,51 a −3,34 |
| $M_1$, $\beta=2$ | calibrada | 0 de 10 | −2,83 a −2,16 | −6,47 a −5,10 |
| $M_2$ | calibrada | 7 de 10 | 0,11 a 1,76 | 0,10 a 1,25 |
| $M_2$ | conjunto B | 6 de 10 | 0,35 a 1,87 | 0,24 a 1,67 |
| $M_3^{rs}(0{,}05)$ | conjunto B | **8 de 10** | 0,11 a 2,14 | −3,63 a 1,23 |

Fonte: elaborado pelos autores (`results/h3_robustez_resumo_sobra_reg.csv`).

$M_1$ perde bem-estar em todos os sorteios. $M_2$ ganha bem-estar em todos, mas aumenta a dispersão em todos, e essa piora passa do limiar em três ou quatro dos dez: não atinge os oito exigidos. $M_3^{rs}(0{,}05)$ domina pontualmente em oito dos dez sorteios e passa na regra. Nos dois restantes, a dispersão da espera sobe acima de 1%; o sinal do efeito sobre a dispersão é, portanto, o ponto frágil do desenho, como já era o de $M_2$.

Com a dominância no conjunto B pela regra do intervalo (seção 7.4) e a robustez de oito em dez, **$M_3^{rs}(0{,}05)$ cumpre as duas partes de H3**. $M_2$ e $M_1$ não cumprem nenhuma.

## Escala da urgência

A escala da urgência foi a primeira suspeita sobre a versão anterior do modelo: com a mediana de $\theta$ em 1, o participante típico descontava a espera a cerca de 172% ao ano. Para isolar esse efeito, a comparação da versão de 19 de novembro foi repetida com $\theta$ multiplicado por 0,2 e $\phi_1$ dividido por 0,2. Com os mesmos números aleatórios, os lances são idênticos; só muda o peso da espera no bem-estar. A ordenação não mudou: $M_2$ continua sem dominar pela piora na dispersão, e os $M_1$ continuam perdendo bem-estar (`results/sens_invariante/h3_diferencas_sobra.csv`). A conclusão sobre os desenhos não dependia, portanto, da escala implausível.

## Versões anteriores do modelo

A terceira via muda a estrutura, e não os parâmetros. Na versão de 16 de novembro, ativas e excluídas disputam o mesmo sorteio, o número de sorteios por assembleia varia entre administradoras e a sobra fica no fundo. Nela, $M_2$ dominava $M_0$ pela regra do intervalo e de forma robusta, com ganho de bem-estar de 2,56% (`results/h3_relativas.csv`). Na versão atual, o mesmo $M_2$ não domina: o que muda de sinal entre as versões é o efeito sobre a dispersão da espera.

A comparação separa o que é estável do que depende da estrutura. São estáveis, em todas as versões, o ganho de bem-estar do preço uniforme, a redução da instabilidade do fundo e a perda de bem-estar de $M_1$. O que depende das regras contratuais é o efeito sobre a dispersão, e é exatamente ele que $M_3$ corrige ao mandar a sobra a sorteio.

## Forma da distribuição de urgência

A lognormal de $F_\theta$ não tem fundamento empírico no consórcio; foi escolhida por ser positiva, assimétrica e de cauda longa, como se espera de uma taxa de urgência. Para medir quanto o resultado depende dela, o modelo foi recalibrado com duas formas alternativas de mesma mediana aproximada: uma Gamma de forma 2 e média 0,2, de cauda mais curta, e uma mistura de dois tipos, com 0,4 dos participantes de urgência 0,6 e o restante de urgência 0,14, que representa uma população dividida entre quem precisa do bem logo e quem poupa. Por prazo, a versão é simplificada: uma réplica de calibração, $\phi_1$ fixo no valor calibrado da base, e comparação apenas de $M_2$ e $M_3^{rs}(0{,}05)$, sem refazer a busca na família $M_3$.

**Tabela 7.12 — Sensibilidade à forma de $F_\theta$, em % do nível de $M_0$ sob cada forma (IC de 95%)**

| Forma | Desenho | $\mathcal{W}$ | $\mathcal{E}$ | $\mathcal{S}$ | Domina? |
|---|---|---|---|---|---|
| Gamma | $M_2$ | 1,46 (1,20; 1,69) | 1,09 (0,80; 1,35) | −1,56 (−6,59; 2,65) | não |
| Gamma | $M_3^{rs}(0{,}05)$ | 1,53 (1,25; 1,74) | 1,10 (0,75; 1,43) | −1,69 (−6,83; 2,55) | não |
| Mistura | $M_2$ | 1,83 (1,56; 2,07) | 1,26 (0,92; 1,57) | −0,79 (−2,14; 0,10) | não |
| Mistura | $M_3^{rs}(0{,}05)$ | 5,68 (5,03; 6,40) | 12,64 (11,51; 13,70) | −1,45 (−3,44; −0,43) | não |

Fonte: elaborado pelos autores (`results/sens_forma_relativas.csv`).

Antes de ler a comparação, é preciso saber se as formas alternativas são tão compatíveis com os dados quanto a lognormal, porque a forma deve ser escolhida pela aderência, e não pelo resultado da comparação. As três foram calibradas no mesmo protocolo simplificado e submetidas ao teste de sobreidentificação da seção 7.2.

**Tabela 7.13 — Aderência aos dados das três formas de $F_\theta$, protocolo simplificado**

| Forma | $Q$ no ótimo | $t$ Spearman (H2) | Wald conjunto (H2) | Rejeitada em H2? |
|---|---|---|---|---|
| Lognormal | 2,79 | 1,21 | 1,62 | não |
| Gamma | 4,76 | 1,55 | 4,46 | não |
| Mistura | 8,55 | 1,60 | 7,29 | sim |

Fonte: elaborado pelos autores (`results/sens_forma_ajuste.csv`). $Q$ calculado com os momentos simulados diretamente no ponto calibrado; limiar do Wald 5,99.

A lognormal tem o melhor ajuste aos momentos de calibração e o melhor desempenho nos momentos reservados. A mistura é rejeitada no teste conjunto, e a Gamma, embora não rejeitada, ajusta pior. Pela regra registrada antes desta rodada, a lognormal é mantida como especificação de referência. A comparação de desenhos sob as alternativas continua relevante como sensibilidade, porque o teste tem pouco poder e a Gamma não pode ser descartada.

Sob as duas formas, $M_3^{rs}(0{,}05)$ deixa de dominar $M_0$. O ganho de bem-estar permanece, com o intervalo inteiro do lado favorável; o que se perde, de novo, é a neutralidade sobre a dispersão da espera, que passa a piorar. Sob a mistura, a piora é grande: com uma fração de participantes muito urgentes, o lance mínimo e o preço uniforme fazem esses participantes vencerem cedo e com frequência, e a espera dos demais se alonga. O desenho foi escolhido sob a lognormal, e não se buscou outro valor de lance mínimo sob cada forma; é possível que exista um que recupere a dominância, mas isso não foi testado.

## O que a varredura não cobre

A robustez examinada cobre a incerteza dos três parâmetros calibrados, a escala da urgência e duas alternativas estruturais. A forma de $F_\theta$ foi examinada na versão simplificada acima. Não cobre a forma de $F_\lambda$, a cláusula da sobra das administradoras cujo regulamento não foi lido nem o rendimento do saldo do fundo: essas sensibilidades foram registradas e cortadas por prazo (seção 8.3). E não cobre a resposta do comportamento à mudança de regra, que é tratada na seção 7.6.
