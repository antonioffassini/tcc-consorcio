---
secao: 4.1
titulo: Ambiente: estados, ações, transições
status: rascunho
responsavel:
insumos:
  - decisões do log
  - ESTADO.md §4, 2026-11-15 (exclusão, inadimplência, recolocação; lance embutido) e 2026-11-19 (sequência da assembleia)
  - ESTADO.md §5 itens 1, 2, 5, 13 e 20
  - src/sim/grupo.py
  - CONTEXT.md §5
fontes:
  - results/parametros_modelo.csv
  - results/parametros_fixos.csv
excecoes:
  - 285
  - 362
paginas_alvo: 5
---

# Ambiente: estados, ações, transições

O Capítulo 2 descreveu o grupo de consórcio como jogo dinâmico de alocação, sem notação. Esta seção fixa o ambiente simulado: o que compõe o estado do grupo, o que cada participante decide e como o estado passa de uma assembleia à seguinte. A regra de contemplação aparece aqui apenas como um lugar na sequência da assembleia; sua especificação, comum ao mecanismo vigente e às alternativas, é objeto da seção 4.3. Os tipos dos participantes e sua distribuição ficam para a seção 4.2.

## Unidades e horizonte

O grupo $g$ tem prazo $T_g$ e é formado por $N_g$ cotas; quando não houver ambiguidade, o índice do grupo é omitido. O tempo é discreto e corresponde às assembleias mensais, $t \in \{1,\dots,T\}$. Todos os valores monetários são medidos em frações do crédito $C$, normalizado a $1$: uma cota que recebe o crédito retira do fundo comum uma unidade, e uma parcela é uma fração dessa unidade. O lance é sempre um percentual do próprio crédito, o que corresponde ao critério de desempate percentual previsto para grupos com créditos diferenciados e torna o modelo indiferente ao valor nominal do bem.

O modelo trata um grupo de cada vez. Não há interação entre grupos nem entre administradoras: cada grupo tem fundo próprio, e o que ocorre num deles não altera o saldo, as regras ou a composição dos demais.

## Situação da cota

Cada cota $i$ ocupa, em cada assembleia, uma de cinco situações. A cota **ativa** é a não contemplada que está em dia e concorre à contemplação. A **contemplada** já recebeu o crédito e continua pagando parcelas até quitar o saldo devedor. A **inadimplente** deixou de pagar, continua contada entre as cotas do grupo, mas não concorre nem ao sorteio nem ao lance. A **excluída** foi desligada do grupo e aguarda a restituição do que pagou. A **restituída** recebeu essa restituição e sai do grupo.

A distinção entre ativa e inadimplente segue a regra de que a exclusão por falta de pagamento ocorre após três vencimentos sem pagamento (art. 32, II, da Resolução BCB n. 285/2023, na redação dada pela Resolução BCB n. 362/2023) [@bcb2023res285]. O modelo aplica a inadimplência apenas à cota ativa ainda não contemplada. A cota contemplada que deixa de pagar conserva a contemplação, com crédito parcial proporcional ao que amortizou (art. 33 da Resolução); representar esse caso exigiria acompanhar o uso do crédito, o que está fora do escopo (seção 4.5).

## Estado

O estado agregado no início da assembleia $t$ é

$$
s_t = (R_t,\ n_t,\ K_t,\ X_t,\ t),
$$

em que $R_t$ é o saldo do fundo comum, $n_t$ é o número de cotas do conjunto $A_t$ de cotas ativas e adimplentes, $K_t$ é o número de cotas já contempladas e $X_t$ o de excluídas ainda não restituídas. O estado individual $z_{i,t}$ reúne a situação da cota, o saldo devedor, o valor já pago, a assembleia de entrada e a liquidez $\lambda_{i,t}$. A liquidez é constante no modelo, $\lambda_{i,t} = \lambda_i$, porque não há renda que a reponha nem consumo que a reduza entre assembleias; ela só é consumida quando a cota vence um lance.

O grupo é aberto. A vaga deixada por uma cota excluída pode ser recolocada para um novo participante, que entra com o grupo em andamento, assume o saldo devedor integral de uma cota e paga parcelas maiores, porque dispõe de menos assembleias para quitá-lo. O número de cotas que passaram pelo grupo pode, assim, superar $N$, embora o número de cotas pagantes fique próximo de $N$. Esse traço dá conteúdo ao desenho $M_1$ da seção 4.3, cujo peso depende do tempo decorrido desde a entrada, $a_{i,t}$: num grupo fechado, todas as cotas não contempladas teriam o mesmo $a_{i,t}$.

## Ações

A cada assembleia, a única decisão do participante é o lance. A cota $i \in A_t$ escolhe $b_{i,t} \in [0, \bar b_{i,t}]$, composto de uma parte livre, paga com liquidez própria, e de uma parte embutida, abatida do crédito a receber. O lance máximo viável é

$$
\bar b_{i,t} = \lambda_i + \bar b^{e},
$$

limitado ainda pelo saldo devedor da cota. A modalidade $m_{i,t}$ não é escolhida em separado: o participante cobre o lance com liquidez própria até $\lambda_i$ e completa com embutido até o teto $\bar b^{e}$. A ordem supõe que, enquanto houver recursos próprios, o participante prefere não reduzir o crédito que vai receber, o que é plausível quando o crédito se destina a um bem de valor dado. Não ofertar é a ação $b_{i,t} = 0$ e corresponde a aguardar o sorteio.

O lance desejado é dado pela política paramétrica $\pi_\phi$, linear na urgência do participante e no prazo restante do grupo:

$$
b^*_{i,t} = \max\!\left(0,\ \phi_0 + \phi_1 \theta_i + \phi_2 \frac{T - t}{T}\right),
\qquad b_{i,t} = \min\!\left(b^*_{i,t},\ \bar b_{i,t}\right).
$$

A especificação não pretende ser a melhor resposta de um participante racional. É uma regra comportamental com poucos parâmetros, suficiente para que os agregados do Bacen a identifiquem (seção 6.3). Os coeficientes $\phi_1$ e $\phi_2$ ficam fixos em 0,1 e -0,1 (`results/parametros_modelo.csv`): o lance cresce com a urgência e com a proximidade do encerramento do grupo. Apenas o intercepto $\phi_0$ é calibrado. A distância entre essa regra e a política que emergiria de participantes que aprendem por interação repetida é o objeto da hipótese H1 (seção 7.3).

## Transições

A assembleia $t$ percorre sete passos, sempre na mesma ordem. Os passos 2 a 5 constituem o mecanismo de contemplação $M$ e são detalhados na seção 4.3; aqui interessa o efeito de cada um sobre o estado.

**1. Arrecadação.** Cada cota ativa adimplente e cada contemplada com saldo devedor paga sua parcela, e o fundo recebe

$$
R_t \leftarrow R_t + \sum_{i\ \text{pagante}} p_i,
\qquad p_i = \frac{1}{T - t + a_{i,t}},
$$

em que $T - t + a_{i,t}$ é o número de assembleias que restavam na entrada da cota. A parcela é constante ao longo da vida da cota. O lance vencedor reduz o saldo devedor, e o efeito é encurtar o prazo de pagamento, e não reduzir a parcela. A Resolução destina o lance à amortização de prestações vincendas e deixa ao contrato a forma de fazê-lo (art. 12, parágrafo único) [@bcb2023res285]; o encurtamento é a forma mais simples de simular.

**2. Sorteio entre ativas.** Havendo cota elegível em $A_t$ e $R_t \ge 1$, uma cota é sorteada e recebe o crédito: $R_t \leftarrow R_t - 1$. Se $R_t < 1$, o sorteio previsto não ocorre. Esse evento define o critério de estabilidade $\mathcal{S}(M)$ da seção 4.4.

**3. Sorteio entre excluídas.** As excluídas não restituídas disputam um sorteio próprio. A sorteada recebe o valor que pagou até a exclusão, se o saldo o cobre. A primeira restituição da assembleia não tem outro limite; as seguintes ocorrem enquanto a soma restituída na assembleia não ultrapassa o teto $\bar r$.

**4. Lance.** As cotas de $A_t$ ainda não contempladas ofertam $b_{i,t}$. Um vencedor com lance $b$, do qual $e$ é embutido, paga $b - e$ ao fundo e recebe $1 - e$, de modo que

$$
R_t \leftarrow R_t - (1 - b_{i,t}),
$$

e a contemplação por lance é viável quando $R_t \ge 1 - b_{i,t}$. O número de vagas por lance $g^b_t$ resulta do saldo e das ofertas, e não de um parâmetro: o prêmio disputado é estocástico, como se discutiu na seção 2.5.

**5. Sobra.** Se o contrato da administradora prevê sorteio da sobra, novas cotas ativas são sorteadas enquanto $R_t \ge 1$; caso contrário, o saldo passa à assembleia seguinte.

**6. Inadimplência e exclusão.** Cada cota ativa não contemplada torna-se inadimplente com probabilidade $h(t/T)$, e a inadimplente que completa três vencimentos sem pagar é excluída. O risco $h(\cdot)$ é constante por faixa de idade do grupo e cai com ela, de 0,038 ao mês no primeiro décimo do prazo para 0,00137 no último terço. Os seis valores foram estimados diretamente no painel do Bacen e não passam pela calibração (`results/parametros_fixos.csv`; seção 5.3).

**7. Recolocação.** Cada vaga excluída é recolocada, com probabilidade $\rho$, para um participante novo, cujo tipo é sorteado da mesma distribuição dos participantes iniciais (seção 4.2). No painel, a reposição líquida de vagas no primeiro terço do prazo supera as exclusões, na razão de 1,24; como o modelo não cria vagas além das excluídas, adota-se $\rho = 1$ (`results/parametros_fixos.csv`).

Ao fim do prazo, excluídas e inadimplentes que restam são restituídas com o saldo remanescente até que ele se esgote. A conservação do dinheiro — o que entrou por parcelas e lances livres é igual ao que saiu em créditos e restituições, mais o saldo final — é verificada em teste automatizado para cada mecanismo e configuração (seção 6.4).

## O que fica de fora do ambiente

Três simplificações limitam diretamente o que o ambiente representa. Não há taxa de administração nem fundo de reserva, que o trabalho não trata como variáveis de escolha; $R_t$ é, portanto, o fundo comum líquido, e os sorteios adicionais com recursos do fundo de reserva previstos na Resolução (art. 22, IV) não existem no modelo. Não há mercado secundário de cotas: a cota só deixa a disputa por contemplação ou por exclusão. E a liquidez não se renova, de modo que o participante sem recursos para ofertar no início do grupo também não os terá adiante. A seção 4.5 reúne essas e as demais hipóteses, com o sentido esperado de cada uma sobre os resultados.
