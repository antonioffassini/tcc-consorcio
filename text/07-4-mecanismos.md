---
secao: 7.4
titulo: Comparação entre mecanismos
status: rascunho
responsavel:
insumos:
  - results/
  - ESTADO.md §4, 2026-11-19 (critérios e regra de H3, escritos antes de rodar); §5 item 29
  - src/analysis/comparacao.py
fontes:
  - results/h3_metricas_sobra.csv
  - results/h3_diferencas_sobra.csv
  - results/h3_relativas.csv
  - results/h3_config_sobra.csv
excecoes:
  - 0,5
paginas_alvo: 5
---

# Comparação entre mecanismos

Esta seção compara o mecanismo vigente $M_0$ com os desenhos $M_1$, em três intensidades do peso pela espera, e $M_2$, no modelo base calibrado na seção 7.1. Os critérios são os da seção 4.4, e a regra de decisão foi registrada no log do projeto em 19 de novembro, antes de a comparação rodar.

## Desenho do experimento

Cada um dos 1.629 grupos simulados — três réplicas do desenho de grupos do painel — foi simulado do início ao encerramento sob os cinco mecanismos, com os mesmos números aleatórios: os mesmos participantes, com os mesmos tipos, e os mesmos choques de inadimplência (`results/h3_config_sobra.csv`). A cláusula da sobra de cada administradora foi sorteada com a probabilidade calibrada $\hat\eta$ e mantida entre mecanismos. A política de lance $\pi_\phi$ é a mesma nos cinco.

Para cada grupo, calcularam-se os quatro critérios: o bem-estar $\mathcal{W}$, média da utilidade realizada das cotas não excluídas; a dispersão da espera $\mathcal{E}$, desvio-padrão do tempo até a contemplação nas mesmas cotas; a estabilidade $\mathcal{S}$, fração das assembleias em que o sorteio previsto não ocorre por falta de saldo; e o prazo de restituição $\mathcal{R}$, meses entre a exclusão e a restituição. As diferenças contra $M_0$ são pareadas por grupo e agregadas com o peso de cada grupo no painel; os intervalos de 95% vêm de um bootstrap de administradoras com 500 reamostragens.

A regra é a da seção 4.4: um desenho domina $M_0$ se melhora ao menos um critério com o intervalo inteiro do lado favorável e não piora nenhum com o intervalo inteiro do lado desfavorável.

## Níveis sob o mecanismo vigente

Sob $M_0$, o bem-estar médio é 0,1837 crédito por cota; o desvio-padrão da espera, 47,1 meses, para uma espera média de 53,4 meses; o sorteio previsto falha por falta de saldo em 0,89% das assembleias; e o excluído espera, em média, 116,3 meses pela restituição, porque a maior parte delas ocorre só no encerramento do grupo (`results/h3_metricas_sobra.csv`). A fração de contemplações por lance na vida inteira dos grupos é 0,706.

## Resultado

**Tabela 7.6 — Diferenças contra $M_0$, modelo base, em % do nível de $M_0$ (IC de 95%)**

| Desenho | Bem-estar $\mathcal{W}$ | Dispersão $\mathcal{E}$ | Falha de sorteio $\mathcal{S}$ | Restituição $\mathcal{R}$ | Domina? |
|---|---|---|---|---|---|
| $M_1$, $\beta$ = 0,5 | −5,01 (−6,06; −4,12) | −2,03 (−2,77; −1,65) | 0,226 (−0,823; 1,015) | −0,096 (−0,168; −0,024) | não |
| $M_1$, $\beta$ = 1 | −7,67 (−9,05; −6,40) | −3,63 (−4,56; −2,98) | 0,113 (−1,568; 1,590) | 0,0104 (−0,120; 0,112) | não |
| $M_1$, $\beta$ = 2 | −10,27 (−12,28; −8,28) | −5,53 (−7,00; −4,53) | 0,643 (−0,429; 2,154) | −0,141 (−0,241; −0,0175) | não |
| $M_2$ | 2,77 (2,12; 3,62) | 0,671 (0,527; 0,865) | −3,11 (−8,42; −0,925) | −0,122 (−0,285; 0,092) | não |

Fonte: `results/h3_relativas.csv`, derivado de `results/h3_diferencas_sobra.csv` e `results/h3_metricas_sobra.csv`. Para $\mathcal{W}$, valores positivos são melhora; para os demais, negativos.

**Nenhum desenho domina $M_0$ no modelo base.** Os dois desenhos alternativos melhoram algum critério de forma inequívoca, e os dois pioram outro também de forma inequívoca.

**$M_1$ troca bem-estar por igualdade.** O peso pela espera reduz o desvio-padrão do tempo de espera em 0,96 a 2,61 meses, conforme $\beta$, e reduz o bem-estar em 5% a 10%. O mecanismo da perda é direto. Sob o sorteio uniforme, um participante recém-chegado e com urgência alta tem a mesma chance que um participante antigo; sob $M_1$, sua chance cai, e ele espera mais. Como a utilidade desconta a espera pela urgência, deslocar a contemplação de quem tem urgência alta para quem esperou mais reduz a soma das utilidades, mesmo quando a espera média quase não muda: ela sobe de 0,282 a 0,664 mês, conforme $\beta$. $M_1$ também reduz ligeiramente o prazo de restituição, mas a diferença é de décimos de ponto percentual. Sobre a estabilidade, não tem efeito distinguível.

**$M_2$ aumenta o bem-estar e a estabilidade, à custa de mais dispersão.** O lance de preço uniforme aumenta o bem-estar em 2,77% e reduz em 3,11% a fração de assembleias com falha de sorteio, ambos com intervalo inteiro favorável. Mas aumenta o desvio-padrão da espera em 0,316 mês, ou 0,671%, com intervalo inteiro desfavorável. Pela regra registrada, $M_2$ não domina $M_0$.

## Por que $M_2$ produz esse resultado

O efeito de $M_2$ sobre o bem-estar vem de quanto os vencedores pagam. Sob o preço uniforme, cada vencedor paga a maior oferta recusada, que é menor ou igual à própria oferta. Com a política fixa, os participantes ofertam o mesmo sob as duas regras, e os vencedores de $M_2$ antecipam menos parcelas. No critério da seção 4.4, a parte livre do lance custa ao participante o valor de antecipar essas parcelas, e o custo cai.

O mesmo efeito tem um preço para o grupo. Com menos dinheiro de lance entrando no fundo, o saldo disponível nas assembleias seguintes é menor, o que contempla menos cotas por lance mais adiante: a espera média sob $M_2$ é 0,724 mês maior que sob $M_0$ (`results/h3_relativas.csv`). A dispersão aumenta pela mesma razão. Ao mesmo tempo, o sorteio previsto falha menos, provavelmente porque a regra de viabilidade de $M_2$ — todos os vencedores pagam o mesmo preço, e o número de vagas é o maior compatível com o saldo a esse preço — preserva mais saldo nas assembleias em que o fundo está apertado. Essa última leitura é uma hipótese sobre o mecanismo, compatível com o teste da seção 6.4 segundo o qual $M_2$ contempla no máximo tantas cotas quanto $M_0$ com as mesmas ofertas, mas não foi isolada em experimento próprio.

## O que a comparação não mede

A política de lance é a mesma sob os cinco mecanismos. Sob $M_2$, porém, a melhor resposta do participante muda: no leilão de uma vaga, ofertar o próprio valor passa a ser dominante (seção 6.4), e participantes que se ajustassem à nova regra ofertariam mais do que sob $M_0$. Esse ajuste reduziria parte do ganho de bem-estar medido aqui — no leilão único com respostas ótimas, a receita esperada das duas regras é a mesma — e também parte da perda de saldo. A comparação mede, portanto, o efeito de trocar a regra mantendo o comportamento, e não o efeito de equilíbrio da troca. Essa é a crítica de Lucas aplicada ao problema [CITAR: Lucas (1976), Econometric policy evaluation: a critique — candidata, conferir]. [DECISÃO PENDENTE: papel do RL na comparação — reotimizar a política sob $M_2$ como teste de robustez]

A mesma limitação vale, em grau menor, para $M_1$: participantes que soubessem que a chance no sorteio cresce com o tempo de grupo poderiam ofertar menos no início. Nenhum dos dois efeitos de reação está no modelo.
