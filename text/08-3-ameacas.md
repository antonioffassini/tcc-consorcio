---
secao: 8.3
titulo: Ameaças à validade
status: rascunho
responsavel:
insumos:
  - nenhum
  - ESTADO.md §4 e §5 (itens 17, 21, 24 a 29)
  - seções 4.5, 5.5, 7.1, 7.2, 7.4 e 7.5
fontes:
  - results/h2_teste.csv
  - results/calibracao_theta.csv
excecoes:
  - 285
paginas_alvo: 3
---

# Ameaças à validade

Esta seção reúne o que pode tornar errada a leitura dos resultados do Capítulo 7. As ameaças estão agrupadas segundo a classificação usual em validade interna, de construto, externa e de conclusão [CITAR: referência de ameaças à validade em estudos de simulação ou de engenharia de software, por exemplo Wohlin et al. — candidata, conferir]. Para cada uma, indica-se o que foi feito para reduzi-la e o que permanece.

## Validade interna: o modelo faz o que se pensa que faz?

**Erro de implementação.** Um erro no código produziria resultados plausíveis e falsos. A bateria de testes da seção 6.4 verifica a contabilidade do fundo, as regras de alocação e as propriedades conhecidas dos leilões de uma vaga, e todos os resultados foram gerados com código que passava em todos os testes. A bateria encontrou dois erros durante o desenvolvimento (seção 7.1). O que permanece é o erro que nenhum teste cobre; a comparação com a implementação independente em Java (seção 6.5) foi desenhada para isso, mas ainda não foi concluída.

**Erro de interpolação.** A calibração minimiza uma superfície interpolada, e não o simulador. O ponto calibrado foi conferido por simulação direta, e a diferença entre os momentos da superfície e da simulação direta é pequena perto dos erros-padrão (Tabela 7.1). O bootstrap, porém, roda inteiramente na superfície, e a incerteza dos parâmetros pode estar subestimada.

**Graus de liberdade do pesquisador.** O modelo passou por três versões, e cada revisão é uma oportunidade de ajustar o modelo ao que se queria encontrar. As defesas adotadas foram registrar no log, com data, cada decisão de modelagem, a partição dos momentos, a regra de H2 e a regra de H3 antes de conhecer os resultados correspondentes, e manter a versão anterior como sensibilidade. A defesa é incompleta em dois pontos, declarados nas seções 5.4 e 7.2: um momento de teste estava parcialmente contaminado pela primeira rodada do protótipo, e a revisão de 19 de novembro foi feita depois de conhecido o primeiro teste de H2. A revisão seguiu o que os contratos dizem, e não o que o ajuste pedia, mas isso não é verificável por terceiros da mesma forma que uma regra registrada.

## Validade de construto: os critérios medem o que se quer medir?

**Utilidade.** O critério de bem-estar usa uma utilidade específica: o crédito descontado pela espera à taxa de urgência, menos o custo de antecipar parcelas com o lance livre. Outra forma funcional — aversão ao risco sobre a data de contemplação, por exemplo — daria peso diferente à dispersão da espera e poderia inverter a avaliação de $M_1$, que perde bem-estar exatamente porque a utilidade adotada é neutra ao risco na espera. A dispersão é tratada como critério separado para não esconder isso.

**Urgência anual.** A urgência $\theta_i$ é lida como taxa anual. Lida como taxa mensal, com a mesma distribuição, o desconto seria muito maior e o peso da espera no bem-estar também. A escolha foi registrada antes da comparação, mas não é identificada pelos dados.

**Estabilidade.** A estabilidade do grupo é medida pela falha do sorteio previsto por falta de saldo. É um indicador de aperto do fundo, e não de risco de insolvência: no modelo, o grupo nunca fica com saldo negativo, porque a contemplação é condicionada ao saldo. Outras dimensões de estabilidade, como o descasamento entre créditos entregues e parcelas a receber, não foram medidas.

## Validade externa: os resultados valem fora do modelo?

**Crítica de Lucas.** É a ameaça mais séria. A política de lance foi calibrada sob a regra vigente e mantida sob as alternativas. Sob o preço uniforme de $M_2$, a melhor resposta do participante muda, e participantes que se ajustassem ofertariam mais. O ganho de bem-estar de $M_2$ vem, em boa parte, de os vencedores pagarem menos com a mesma política — o que, no leilão de uma vaga com respostas ótimas, desapareceria, pela equivalência de receita. Os resultados de $M_2$ são, portanto, o efeito de impacto da troca de regra, e não o efeito de equilíbrio. [DECISÃO PENDENTE: papel do RL na comparação]

**Distribuições de tipos fixadas.** As distribuições de urgência e de liquidez e dois dos três coeficientes da política não foram calibrados. A robustez da seção 7.5 cobre só a incerteza dos parâmetros calibrados. Uma população com mais liquidez, ou com urgência e liquidez correlacionadas, poderia mudar a magnitude dos efeitos e, no caso de $M_2$, o sinal do efeito sobre a dispersão, que é pequeno.

**Cláusulas contratuais de cinco administradoras.** As regras da assembleia vêm de cinco regulamentos. As demais administradoras podem ter cláusulas diferentes, e a comparação entre o modelo base e o de 16 de novembro mostra que a conclusão sobre $M_2$ depende delas. A fração de administradoras que sorteiam a sobra foi calibrada, mas é mal identificada: o intervalo do bootstrap cobre de 0 a 1 (`results/calibracao_theta.csv`).

**Recorte.** O trabalho cobre o segmento de imóveis, no regime da Resolução BCB n. 285/2023. Segmentos com prazos curtos, como veículos, têm grupos menores e outra relação entre arrecadação e crédito, e os resultados não se transferem sem nova calibração.

**O que o modelo não contém.** Taxa de administração, fundo de reserva, mercado secundário de cotas, inadimplência de contemplados, entrada de novos grupos e concorrência entre administradoras estão fora do modelo (seção 4.5). Um desenho que mude o valor de participar de um grupo poderia mudar quem adere, e essa seleção não está representada.

## Validade de conclusão: os números sustentam o que se afirma?

**Poder do teste de H2.** O teste de H2 não rejeita o modelo, mas a menor diferença que ele detectaria no Spearman, com poder de 80%, é 0,3952, maior que a própria correlação observada (`results/h2_teste.csv`). A não rejeição diz pouco. O que sustenta o uso do modelo é a concordância qualitativa no sinal e na ordem de grandeza, e não o teste formal.

**Inconsistência entre fontes.** Os fluxos trimestrais do arquivo por UF não batem com a soma dos grupos em parte das administradoras (seção 5.2). Nenhum momento combina as duas fontes, mas a fração de lance vem de uma fonte cuja consistência com a outra não foi esclarecida.

**Regra de decisão de H3.** A regra combinou um critério de intervalo, no ponto calibrado, e um de magnitude, na robustez. Para $M_2$, os dois discordam. A divergência foi relatada sem escolha, mas a conclusão de que H3 não se sustenta no modelo base depende de a regra do intervalo ter precedência, o que a regra registrada implica sem dizer explicitamente.

**Muitas comparações.** Foram comparados quatro desenhos contra o vigente, em quatro critérios, em duas versões do modelo. Os intervalos são de 95% por critério, sem correção para comparações múltiplas. Algumas diferenças pequenas, como as do prazo de restituição sob $M_1$, podem ser falsos positivos.
