---
secao: 1.5
titulo: Hipóteses
status: rascunho
responsavel:
insumos:
fontes:
excecoes:
  - 2022
  - 1976
paginas_alvo: 2
---

# Hipóteses

As hipóteses são afirmações verificáveis que, em conjunto, sustentam a proposição central. Cada uma responde a uma das questões da seção 1.3 e corresponde a um procedimento específico de verificação.

**Quadro 2 — Hipóteses, questões e verificação**

| Hipótese | Papel | Responde a | Verificação |
|---|---|---|---|
| H1 — Insuficiência da teoria estática | auxiliar | Q1 | Agentes de aprendizado por reforço sob o desenho vigente (seção 7.3) |
| H2 — Adequação empírica do modelo | validação | Q2 | Ajuste por momentos simulados e teste em momentos reservados (seções 7.1 e 7.2) |
| H3 — Dominância de desenho alternativo | comparação | Q3 | Comparação entre mecanismos com comportamento fixo e varredura de robustez (seções 7.4 e 7.5) |
| H4 — Persistência da ordenação com lance adaptado | central | Q4 | Comparação entre mecanismos com agentes treinados sob cada desenho (seção 7.6) |

Fonte: elaborado pelos autores.

**H1 — Insuficiência da teoria estática.** O lance de participantes que aprendem por interação repetida sob as regras vigentes difere da previsão dos modelos estáticos de leilão de valor privado. A diferença decorre de três características do consórcio ausentes desses modelos: a restrição de liquidez, a repetição da disputa ao longo do prazo do grupo e o efeito que cada contemplação produz sobre as chances dos demais. Se a hipótese se confirmar, a avaliação do mecanismo não pode ser feita com fórmulas fechadas e exige simulação; é esse o seu papel no trabalho. A verificação coloca no ambiente simulado agentes que aprendem por tentativa e erro, sem regra de comportamento imposta, e compara os lances aprendidos com os previstos pela teoria estática. Trabalho análogo em leilões repetidos encontrou diferenças desse tipo [@banchio2022artificial]. H1 é rejeitada se os lances aprendidos ficarem, em média, a menos de cinco pontos percentuais do crédito da previsão estática.

**H2 — Adequação empírica do modelo.** O modelo de comportamento, ajustado por método de momentos simulados com uso exclusivo dos agregados publicados pelo regulador, reproduz estatísticas dos dados que não foram empregadas no ajuste. O conjunto de estatísticas usadas para ajustar e o conjunto reservado para testar são definidos antes de qualquer ajuste, nos níveis de agregação em que o dado público os disponibiliza. H2 é rejeitada se o modelo ajustado não reproduzir as estatísticas reservadas dentro da margem de erro estabelecida.

**H3 — Dominância de desenho alternativo.** Existe ao menos um desenho alternativo de contemplação, admissível sob a regulação vigente, que melhora o desempenho do grupo em pelo menos um dos critérios de avaliação sem piorar os demais; e essa ordenação se mantém diante da incerteza que resta sobre os parâmetros calibrados. Nesta hipótese, o comportamento de lance é o mesmo em todos os desenhos. O trabalho afirma a ordenação entre desenhos, e não a magnitude do ganho. H3 é rejeitada se nenhum desenho alternativo superar o vigente pela regra de decisão fixada antes da comparação.

**H4 — Persistência da ordenação com lance adaptado.** A ordenação obtida em H3 se mantém quando os participantes adaptam o lance a cada desenho. Comparar regras mantendo fixo o comportamento estimado sob a regra vigente expõe a conclusão à objeção de que o comportamento muda quando a regra muda [@lucas1976econometric]. H4 responde a essa objeção treinando os agentes de aprendizado sob cada desenho e repetindo a comparação. É a hipótese central do trabalho: uma recomendação de desenho só se sustenta se sobreviver à reação dos participantes. H4 é rejeitada se o desenho que domina o vigente em H3 deixar de dominá-lo quando o lance é aprendido sob cada regra.

As hipóteses não são independentes entre si. H3 e H4 são conclusões obtidas no ambiente simulado e só têm valor se esse ambiente for empiricamente adequado; a rejeição de H2 retira, portanto, sustentação às duas. Por essa razão, a validação do modelo antecede a comparação entre desenhos. H1 e H4 usam os mesmos agentes: se o aprendizado não convergir sob o desenho vigente, as duas deixam de ser verificáveis, enquanto H2 e H3 permanecem.
