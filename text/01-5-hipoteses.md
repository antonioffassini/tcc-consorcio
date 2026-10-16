---
secao: 1.5
titulo: Hipóteses
status: rascunho
responsavel:
insumos:
fontes:
excecoes:
  - 2022
paginas_alvo: 2
---

# Hipóteses

As hipóteses são afirmações verificáveis que, em conjunto, sustentam a proposição central. Cada uma responde a uma das questões da seção 1.3 e corresponde a um procedimento específico de verificação.

**Quadro 2 — Hipóteses, questões e verificação**

| Hipótese | Responde a | Verificação |
|---|---|---|
| H1 — Divergência comportamental | Q1 | Experimento com agentes de aprendizado por reforço (seção 7.3) |
| H2 — Adequação empírica do modelo | Q2 | Ajuste por momentos simulados e teste em momentos reservados (seções 7.1 e 7.2) |
| H3 — Superioridade de desenho alternativo | Q3 | Comparação entre mecanismos e varredura de robustez (seções 7.4 e 7.5) |

Fonte: elaborado pelos autores.

**H1 — Divergência comportamental.** O comportamento de lance de participantes que aprendem por interação repetida sob as regras vigentes difere sistematicamente da previsão de equilíbrio dos modelos estáticos de leilão de valor privado. A divergência é atribuível a três características do consórcio ausentes desses modelos: a restrição de liquidez, a repetição da disputa ao longo do prazo do grupo e o efeito que cada contemplação produz sobre as chances dos demais. A hipótese é verificada colocando, no ambiente simulado, agentes que aprendem por tentativa e erro, sem regra de comportamento imposta, e comparando os lances que eles aprendem com os lances previstos pela teoria estática. Trabalho análogo em leilões repetidos encontrou divergência desse tipo [@banchio2022artificial]. H1 é rejeitada se os lances aprendidos não diferirem da previsão teórica de modo sistemático.

**H2 — Adequação empírica do modelo.** O modelo de comportamento, ajustado por método de momentos simulados com uso exclusivo dos agregados publicados pelo regulador, reproduz estatísticas dos dados que não foram empregadas no ajuste. O conjunto de estatísticas usadas para ajustar e o conjunto reservado para testar são definidos antes de qualquer ajuste, nos níveis de agregação em que o dado público os disponibiliza. H2 é rejeitada se o modelo ajustado não reproduzir as estatísticas reservadas dentro da margem de erro estabelecida.

**H3 — Superioridade de desenho alternativo.** Existe ao menos um desenho alternativo de contemplação, admissível sob a regulação vigente, que melhora o desempenho do grupo em pelo menos um dos critérios de avaliação sem piorar os demais; e essa ordenação entre desenhos se mantém em toda a faixa de parâmetros compatível com os dados observados. O trabalho afirma a ordenação entre desenhos, e não a magnitude do ganho. H3 é rejeitada se nenhum desenho alternativo superar o vigente, ou se a ordenação se inverter dentro da faixa de parâmetros admissível.

As hipóteses não são independentes entre si. H3 é uma conclusão obtida no ambiente simulado e só tem valor se esse ambiente for empiricamente adequado; a rejeição de H2 retira, portanto, sustentação a H3. Por essa razão, a validação do modelo antecede a comparação entre desenhos. H1 é verificada em experimento separado: sua rejeição reduz a contribuição metodológica do trabalho, mas não compromete a proposição central.
