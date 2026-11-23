---
secao: 1.7
titulo: Metodologia
status: rascunho
responsavel:
insumos:
fontes:
excecoes:
paginas_alvo: 2
---

# Metodologia

Esta seção apresenta a visão geral do método; os detalhes de cada etapa são tratados nos Capítulos 4 a 6. O trabalho segue sete etapas encadeadas, organizadas de modo que nenhuma conclusão sobre os desenhos de contemplação seja tirada antes que o modelo tenha sido verificado e validado.

**1. Dados.** As bases públicas do Banco Central são consolidadas em dois painéis: um por grupo e mês, que informa quantas cotas foram contempladas, e outro por administradora e trimestre, que informa a repartição das contemplações entre sorteio e lance. Os dados são processados por código versionado, de forma que todo número apresentado no texto possa ser regenerado a partir dos arquivos originais.

**2. Fatos estilizados.** A partir dos painéis, são calculadas as estatísticas que o modelo deverá reproduzir, como a fração de contemplações por lance e sua variação entre administradoras e ao longo do tempo. Essas estatísticas são divididas, antes de qualquer ajuste, em um conjunto usado para calibrar o modelo e outro reservado para testá-lo.

**3. Formalização.** O grupo de consórcio é descrito como um jogo dinâmico. Cada participante tem uma urgência em receber o crédito e uma liquidez disponível para lance, ambas conhecidas apenas por ele. O estado do grupo reúne o saldo do fundo comum e o número de cotas ativas, contempladas e excluídas. A regra de contemplação é tratada como um componente substituível do modelo, o que permite comparar o mecanismo vigente com alternativas sob a mesma estrutura.

**4. Simulação.** O jogo é implementado como um simulador que reproduz, assembleia a assembleia, a arrecadação, a apuração das vagas, o sorteio, a apuração dos lances, as exclusões e as restituições. O comportamento de lance dos participantes simulados é dado por uma política com poucos parâmetros.

**5. Verificação e calibração.** Antes de qualquer uso, o simulador é testado em configurações simplificadas para as quais a teoria dispõe de solução analítica; ele deve reproduzir essas soluções. Em seguida, os parâmetros de comportamento são ajustados por método de momentos simulados: escolhem-se os parâmetros que tornam as estatísticas produzidas pela simulação mais próximas das observadas nos dados. O modelo ajustado é então avaliado nas estatísticas reservadas (H2).

**6. Comparação de mecanismos.** Com o modelo validado, a regra de contemplação é substituída por desenhos alternativos, e cada desenho é avaliado por simulação repetida segundo quatro critérios: o bem-estar agregado dos participantes, a dispersão do tempo de espera até a contemplação, a instabilidade do fundo e o tempo de restituição aos excluídos. A comparação é repetida em toda a faixa de parâmetros compatível com os dados, para verificar se a ordenação entre desenhos se mantém (H3).

**7. Aprendizado por reforço.** Em experimento separado, os participantes de política fixa são substituídos por agentes que aprendem a ofertar lances por tentativa e erro, e o comportamento aprendido é comparado com a previsão dos modelos estáticos de leilão (H1). Em seguida, os agentes são treinados sob cada desenho alternativo, e a comparação da etapa 6 é refeita com o lance adaptado a cada regra (H4). O aprendizado por reforço é mantido fora da etapa de calibração porque treinar agentes até a convergência a cada avaliação do ajuste tornaria o custo computacional inviável.

A ordem das etapas tem uma razão. A comparação entre desenhos (etapa 6) é uma conclusão obtida dentro do simulador; ela só é informativa se o simulador estiver correto (etapa 5, verificação) e se representar adequadamente o comportamento observado (etapa 5, validação). Se a verificação ou a validação falharem, o resultado é reportado como tal, e o modelo não é modificado até que os testes passem.
