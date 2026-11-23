---
secao: 8.3
titulo: Ameaças à validade
status: rascunho
responsavel:
insumos:
  - nenhum
  - ESTADO.md §4 e §5 (itens 17, 21, 24 a 35)
  - seções 4.5, 5.5, 7.1, 7.2, 7.4 e 7.5
fontes:
  - results/sens_forma_ajuste.csv
  - results/sens_forma_relativas.csv
  - results/texto_2211_apresentacao.csv
  - results/h2_teste.csv
  - results/calibracao_theta.csv
excecoes:
  - 9.1
  - 285
  - 9.1.7.3
  - 0,05
paginas_alvo: 3
---

# Ameaças à validade

Esta seção reúne o que pode tornar errada a leitura dos resultados do Capítulo 7. As ameaças estão agrupadas em validade interna, de construto, externa e de conclusão, seguindo a distinção entre verificar o modelo e validá-lo para um uso específico [@sargent2015introductory]. Para cada uma, indica-se o que foi feito para reduzi-la e o que permanece.

## Validade interna: o modelo faz o que se pensa que faz?

**Erro de implementação.** Um erro no código produziria resultados plausíveis e falsos. A bateria de testes da seção 6.4 verifica a contabilidade do fundo, as regras de alocação e as propriedades conhecidas dos leilões de uma vaga, e todos os resultados foram gerados com código que passava em todos os testes. A bateria encontrou dois erros durante o desenvolvimento (seção 7.1). O que permanece é o erro que nenhum teste cobre; a comparação com a implementação independente em Java (seção 6.5) foi desenhada para isso, mas ainda não foi concluída.

**Erro de interpolação.** A calibração minimiza uma superfície interpolada, e não o simulador. O ponto calibrado foi conferido por simulação direta, e a diferença entre os momentos da superfície e da simulação direta é pequena perto dos erros-padrão (Tabela 7.1). O bootstrap, porém, roda inteiramente na superfície, e a incerteza dos parâmetros pode estar subestimada.

**Graus de liberdade do pesquisador.** O modelo passou por quatro versões, e cada revisão é uma oportunidade de ajustar o modelo ao que se queria encontrar. As defesas adotadas foram registrar no log, com data, cada decisão de modelagem, a partição dos momentos e as regras de H2, H3, da família $M_3$ e dos agentes antes de conhecer os resultados correspondentes, e manter as versões anteriores como sensibilidade. A defesa é incompleta em quatro pontos, que o texto declara: um momento de teste estava parcialmente contaminado pela primeira rodada do protótipo (seção 5.4); a revisão de 19 de novembro foi feita depois de conhecido o primeiro teste de H2 (seção 7.2); a família $M_3$ foi especificada depois de se ver $M_2$ falhar na regra do intervalo, e o objetivo declarado da busca era encontrar um desenho que superasse o vigente ou mostrar que não havia; e o prazo planejado para encerrar os experimentos foi reaberto uma vez, para a nova escala da urgência, a cláusula da sobra tirada dos regulamentos e a família $M_3$. A escolha do $M_3$ em uma amostra e a avaliação em amostras novas (seção 7.4) protege contra a sorte das sementes, mas não contra a escolha da família: um desenho encontrado depois de uma busca dirigida vale como proposta a confirmar, e não como descoberta independente.

## Validade de construto: os critérios medem o que se quer medir?

**Utilidade.** O critério de bem-estar usa uma utilidade específica: o crédito descontado pela espera à taxa de urgência, menos o custo de antecipar parcelas com o lance livre. Outra forma funcional — aversão ao risco sobre a data de contemplação, por exemplo — daria peso diferente à dispersão da espera e poderia inverter a avaliação de $M_1$, que perde bem-estar exatamente porque a utilidade adotada é neutra ao risco na espera. A dispersão é tratada como critério separado para não esconder isso.

**Escala e forma da urgência.** A urgência $\theta_i$ é lida como taxa anual contínua, com mediana ancorada em ordem de grandeza financeira. A escala foi revista uma vez, por implausível, antes de nova comparação, e a seção 7.5 mostra que a mudança de escala, com o comportamento mantido, não altera a ordenação. A forma lognormal não tem fundamento empírico específico no consórcio, e é a ameaça mais séria ao resultado de H3: sob uma Gamma e sob uma mistura de dois tipos, recalibradas em versão simplificada, $M_3^{rs}(0{,}05)$ deixa de dominar o vigente, porque a dispersão da espera piora (seção 7.5). O ganho de bem-estar se mantém nas duas. A lognormal é a forma que melhor se ajusta aos dados entre as três testadas, e a mistura é rejeitada no teste de sobreidentificação; a Gamma, porém, não é rejeitada. A dominância encontrada em H3 é, portanto, condicional à forma de $F_\theta$, que os dados agregados disponíveis só discriminam em parte.

**Instabilidade.** A instabilidade do fundo é medida pela falha do sorteio previsto por falta de saldo. É um indicador de aperto do fundo, e não de risco de insolvência: no modelo, o grupo nunca fica com saldo negativo, porque a contemplação é condicionada ao saldo. Outras dimensões de estabilidade, como o descasamento entre créditos entregues e parcelas a receber, não foram medidas.

## Validade externa: os resultados valem fora do modelo?

**Crítica de Lucas.** É a ameaça mais séria à comparação com política fixa. A política de lance foi calibrada sob a regra vigente e, na seção 7.4, mantida sob as alternativas. Sob preço uniforme, a melhor resposta do participante muda, e o ganho de bem-estar de $M_2$ e de $M_3$ vem em parte de os vencedores pagarem menos com a mesma política. Além disso, como o número de vagas no consórcio depende do próprio preço, nem a propriedade de Vickrey, de que ofertar o valor é dominante, está garantida (seção 4.3). A hipótese H4 enfrenta essa ameaça treinando agentes sob cada desenho (seção 7.6), e o resultado muda a conclusão: com o lance adaptado, nenhum desenho domina o vigente. O que H4 deixa de fora é igualmente importante: os agentes não são calibrados aos dados, sob os desenhos alternativos treinaram com uma única semente, e compartilham uma tabela, o que representa o aprendizado de uma população de participantes semelhantes, e não a interação estratégica entre poucos participantes que se observam.

**Busca depois do resultado.** H5 foi formulada depois de ver H4, e a família de desenhos foi desenhada a partir do diagnóstico de H4; a linha de sorteio ponderado pela espera entrou por emenda, depois de um teste de fumaça do código que mostrou o lance fixo alongando a espera. O que protege o resultado é o protocolo: oito variantes registradas antes de qualquer treino, escolha no conjunto A, teste no conjunto B, com grupos e sementes não usados na escolha, e verificações secundárias com a política calibrada e sob outra forma da urgência. O que ele não elimina é que uma busca guiada pelo resultado anterior tem mais chances de encontrar um desenho favorável do que uma família fixada no início do trabalho. A segunda semente de treino, verificação decidida depois do teste, mostrou que a dominância de $M_4$ com o lance aprendido depende da semente (seção 7.6); com a política calibrada, o ganho de bem-estar de $M_4$ tem intervalo que cruza o zero. Os agentes sob $M_2$ e $M_3^{rs}(0{,}05)$, em H4, foram treinados com uma semente, e a mesma fragilidade não pode ser descartada ali.

**Distribuições de tipos e coeficientes fixados.** As distribuições de urgência e de liquidez e o coeficiente do prazo restante na política não foram calibrados. As sensibilidades registradas para a forma de $F_\lambda$, para a cláusula da sobra das administradoras sem regulamento lido ($\eta_0$) e para o rendimento do saldo do fundo foram cortadas por prazo. Uma população com mais liquidez, ou com urgência e liquidez correlacionadas, poderia mudar a magnitude dos efeitos e, no caso de $M_3$, o sinal do efeito sobre a dispersão da espera, que é o ponto frágil do desenho (seção 7.5).

**Cláusulas contratuais de quatro administradoras.** As regras da assembleia vêm de quatro regulamentos arquivados; um quinto, lido em novembro, saiu do site antes de ser arquivado. Nas administradoras não lidas, o destino da sobra é sorteado com a proporção observada nos quatro contratos, e não há como saber se elas a seguem. A comparação entre o modelo base e o de 16 de novembro mostra que a conclusão sobre $M_2$ depende dessas cláusulas. Numa versão anterior, essa proporção era calibrada, e o bootstrap mostrou que os momentos disponíveis não a identificavam; por isso passou a vir dos contratos.

**Desenho vigente sem lance mínimo.** O $M_0$ modelado não tem lance mínimo, e pelo menos uma administradora pratica 10% do valor da cota [@santander2026regulamento, cl. 9.1.7.3]. O ganho de $M_3^{rs}(0{,}05)$ é medido contra um vigente sem esse piso; contra um vigente que já o tenha, parte do ganho pode não existir. A decomposição da seção 7.4 mostra que a parte do ganho que viria só dessas práticas é pequena, de 0,26% no bem-estar; a maior parte vem do preço uniforme.

**Rendimento do saldo do fundo.** O modelo não remunera o saldo do fundo. Como crédito e parcelas são corrigidos pelo índice do bem e o saldo aplicado rende a taxa de aplicação, o saldo parado rende, em unidades de crédito, a diferença real entre as duas. A omissão não é neutra entre desenhos: os que retêm mais saldo, como $M_2$, ganhariam um pouco mais. A sensibilidade foi registrada e cortada por prazo.

**Recorte.** O trabalho cobre o segmento de imóveis, no regime da Resolução BCB n. 285/2023. Segmentos com prazos curtos, como veículos, têm grupos menores e outra relação entre arrecadação e crédito, e os resultados não se transferem sem nova calibração.

**O que o modelo não contém.** Taxa de administração, fundo de reserva, mercado secundário de cotas, inadimplência de contemplados, entrada de novos grupos e concorrência entre administradoras estão fora do modelo (seção 4.5). Um desenho que mude o valor de participar de um grupo poderia mudar quem adere, e essa seleção não está representada.

## Validade de conclusão: os números sustentam o que se afirma?

**Poder do teste de H2.** O teste de H2 não rejeita o modelo, mas a menor diferença que ele detectaria no Spearman, com poder de 80%, é 0,3959, maior que a própria correlação observada (`results/h2_teste.csv`). A não rejeição diz pouco. O que sustenta o uso do modelo é a concordância qualitativa no sinal e na ordem de grandeza, e não o teste formal.

**Inconsistência entre fontes.** Os fluxos trimestrais do arquivo por UF não batem com a soma dos grupos em parte das administradoras (seção 5.2). Nenhum momento combina as duas fontes, mas a fração de lance vem de uma fonte cuja consistência com a outra não foi esclarecida.

**Regra de decisão de H3.** A regra combina um critério de intervalo, no ponto calibrado, e um de magnitude, na robustez. Em versões anteriores do modelo, os dois discordaram para $M_2$, e a precedência do intervalo, implícita na regra registrada, decidiu. Para $M_3^{rs}(0{,}05)$, os dois concordam, mas a robustez passa exatamente no limiar de oito em dez: um sorteio a menos e a conclusão seria outra.

**Muitas comparações.** Foram comparados quinze desenhos contra o vigente, em quatro critérios, em mais de uma versão do modelo. Os intervalos são de 95% por critério, sem correção para comparações múltiplas. A avaliação do desenho escolhido em amostras novas reduz o risco de que a escolha reflita falsos positivos, mas diferenças pequenas, como as do tempo de restituição, podem sê-lo.
