---
secao: 1.2
titulo: Motivação
status: rascunho
responsavel:
insumos:
fontes:
excecoes:
  - 11795
  - 285
paginas_alvo: 2
---

# Motivação

Três razões motivam o estudo do mecanismo de contemplação do consórcio.

**A regra de contemplação é uma escolha regulatória que nunca foi avaliada.** O sorteio e o lance, e a ordem entre eles, foram fixados pela Lei n. 11.795/2008 e pela regulamentação do Banco Central, hoje a Resolução BCB n. 285/2023 [@brasil2008lei11795; @bcb2023res285]. Essas regras não resultaram da comparação entre desenhos alternativos; foram codificadas a partir da prática do setor. Como toda regra de alocação de um recurso escasso, elas determinam quem recebe primeiro, quanto paga por isso e quem espera. É legítimo perguntar se outra regra, igualmente admissível pela lei, produziria resultados melhores para os participantes ou para a estabilidade do grupo. Para o consórcio brasileiro, essa pergunta não tem resposta na literatura.

**A escolha da regra tem consequências distributivas relevantes.** Num grupo de consórcio, a ordem de contemplação redistribui valor entre participantes. Quem tem pressa e dinheiro disponível pode antecipar a contemplação por meio do lance; quem não tem depende do sorteio e tende a esperar mais. Ao mesmo tempo, o fundo comum é compartilhado: cada contemplação, cada desistência e cada atraso alteram os recursos disponíveis para os demais. Pequenas diferenças na regra de alocação, multiplicadas pela escala do sistema, podem alterar de forma apreciável quem é atendido e em que momento.

**O problema é tratável com dados públicos e métodos computacionais.** O dado regulatório publicado pelo Banco Central é extenso e cobre um período longo, mas é agregado: informa quantas cotas foram contempladas por lance e por sorteio, não quem ofertou quanto. Além disso, o jogo entre os participantes de um grupo não admite solução analítica nas condições realistas descritas no Capítulo 2. As duas dificuldades, a observação apenas agregada e a ausência de solução em forma fechada, apontam para a mesma abordagem: representar o grupo como um sistema de agentes, simulá-lo computacionalmente, ajustar o comportamento simulado aos agregados observados e, então, comparar regras dentro do simulador. Essa combinação de modelagem de sistemas multiagente, simulação, otimização numérica e validação de modelo situa o trabalho na área de Engenharia de Computação; a economia fornece o domínio de aplicação e os critérios de avaliação.
