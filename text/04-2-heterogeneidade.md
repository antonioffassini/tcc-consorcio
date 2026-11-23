---
secao: 4.2
titulo: Heterogeneidade dos participantes
status: rascunho
responsavel:
insumos:
  - decisões do log
  - ESTADO.md §4, 2026-11-15 (heterogeneidade em três camadas; forma das vagas) e 2026-11-19 (revisão pelos regulamentos)
  - ESTADO.md §5 itens 8, 18, 26, 31 e 35; §4, 2026-11-22 (η pelos regulamentos; nova base da urgência)
  - src/sim/grupo.py, src/sim/painel.py
fontes:
  - results/parametros_modelo.csv
  - results/fatos_momentos.csv
  - results/g1_identificacao.csv
  - results/arquivo_2026-11-16/calibracao_theta.csv
  - results/calibracao_theta.csv
excecoes:
  - 14.5.8
  - 9.1.7.5
  - 14.5
  - 35.8
  - 9.1
  - 11.795
  - 285
  - 14.6
  - 9.1.7.3
  - 0,2
  - 0,75
  - 172
paginas_alvo: 3
---

# Heterogeneidade dos participantes

A diferença entre administradoras é o traço mais forte dos dados. No regime posterior à Resolução BCB n. 285/2023, a fração das contemplações de ativas que ocorre por lance tem média de 0,734 e desvio-padrão de 0,116 entre administradoras e trimestres, e 0,94 da sua variância está entre administradoras, e não entre trimestres de uma mesma administradora (`results/fatos_momentos.csv`). O teste de Kruskal-Wallis rejeita a igualdade das distribuições por administradora com folga (estatística 282,4; `results/g1_identificacao.csv`). Um modelo em que todos os grupos fossem iguais reproduziria, no máximo, a média. Esta seção define de onde vem a variação no modelo, em três camadas: a estrutura observada de cada grupo, uma cláusula contratual latente por administradora e os tipos dos participantes.

## Estrutura observada

Cada grupo simulado copia três características de um grupo real do painel por grupo (seção 5.1): o prazo $T_g$, o tamanho $N_g$ (mediana das cotas ativas no período) e a idade, isto é, a assembleia em que o grupo se encontrava em cada mês observado. Para cada administradora, sorteiam-se até doze grupos do painel, e os momentos simulados são calculados exatamente nos meses em que o grupo aparece nos dados (seção 6.1). Essa camada não tem parâmetro: tudo nela é observado. Ela importa porque parte da diferença entre administradoras vem da composição da carteira. Uma administradora com grupos jovens contempla, no mês típico, de forma diferente de outra com grupos perto do encerramento, independentemente da regra.

## Cláusula contratual latente

A segunda camada é o que o regulamento de cada administradora decide e o Bacen não publica. A Lei n. 11.795/2008 e a Resolução BCB n. 285/2023 deixam ao contrato a forma do sorteio e as regras do lance (seção 4.3), e os regulamentos lidos neste trabalho divergem justamente num ponto que afeta a fração de lance: o destino do saldo que sobra depois do lance. Em três dos quatro contratos, a sobra vai a novos sorteios entre as ativas na mesma assembleia [@portoseguro2025regulamento, art. 35.8; @itau2024condicoes, cl. 14.5.8; @sicredi2026regulamento]; no do Santander, o saldo que não basta para uma contemplação passa à assembleia seguinte [@santander2026regulamento, cl. 9.1.7.5]. Quando a sobra é sorteada, cada assembleia com saldo folgado gera contemplações por sorteio além da prevista, e a fração de lance da administradora cai.

O modelo representa essa cláusula como uma variável binária por administradora, e todos os grupos de uma administradora seguem a mesma cláusula, o que reproduz a estrutura dos dados, em que a variação está entre administradoras. Para as quatro administradoras cujo regulamento trata do tema, a cláusula é a do contrato: Porto Seguro, Itaú e Sicredi sorteiam a sobra, e o Santander a leva à assembleia seguinte. As demais recebem a cláusula de sorteio com probabilidade $\eta_0 = 0{,}75$, a proporção observada entre esses quatro contratos, sorteada por administradora com semente fixa (`results/parametros_modelo.csv`). Numa versão anterior, essa probabilidade era calibrada; o bootstrap mostrou que os momentos disponíveis não a identificam, porque com lances frequentes o saldo raramente sobra em valor suficiente para um novo sorteio, e o valor passou a ser tirado das fontes.

A alternativa natural seria um efeito fixo por administradora, com um parâmetro para cada uma das administradoras do painel. Com quatro momentos de calibração, esse modelo não seria identificável. A cláusula binária tirada dos contratos preserva a heterogeneidade entre administradoras sem pedir aos dados o que eles não têm.

Na versão do modelo de 16/11, que o Capítulo 7 mantém como análise de sensibilidade, a heterogeneidade contratual vinha de outra cláusula: o número de sorteios por assembleia, proporcional à capacidade ordinária do grupo, $\kappa_g = \max(1,\ s_j N_g/T_g)$, com $s_j \sim \text{LogNormal}(\log m_s, \sigma_s)$ por administradora. A calibração dessa versão deu $m_s = 0{,}51$ e $\sigma_s = 0{,}34$ (`results/arquivo_2026-11-16/calibracao_theta.csv`). A leitura dos regulamentos mostrou que nenhum deles fixa um número de sorteios por assembleia além do condicionamento ao saldo, e a cláusula foi trocada pela da sobra; a seção 7.1 descreve essa revisão.

## Tipos dos participantes

A terceira camada é a dos tipos, informação privada de cada participante. A urgência $\theta_i$ mede quanto o participante valoriza receber o crédito mais cedo e é lida como taxa anual de desconto: o fator de desconto implícito é $\delta_i = e^{-\theta_i}$ por ano. A liquidez $\lambda_i$ é o montante, em frações do crédito, de que o participante dispõe para ofertar lance livre. As distribuições são

$$
\theta_i \sim F_\theta = \text{LogNormal}(\log 0{,}2,\ 0{,}5),
\qquad
\lambda_i = \bar\lambda\, u_i,\quad u_i \sim \text{Beta}(2, 5),\quad \bar\lambda = 0{,}6,
$$

sorteadas de forma independente entre si e entre participantes (`results/parametros_modelo.csv`). O participante que entra pela recolocação de uma vaga recebe um tipo novo, sorteado das mesmas distribuições.

A escala de $F_\theta$ foi ancorada em ordem de grandeza financeira. Como $\theta_i$ é uma taxa anual contínua, a mediana de 0,2 corresponde a descontar a espera a cerca de 22% ao ano: a taxa básica de juros da economia, mais um prêmio pela pressa [CITAR: série histórica da taxa Selic, Banco Central do Brasil]. Numa versão anterior do modelo, a mediana era 1, o que equivale a cerca de 172% ao ano, valor implausível para quem compra um imóvel. A mudança de escala foi feita antes de qualquer nova comparação, e a seção 7.5 mostra que, com o comportamento de lance mantido, ela não altera a ordenação entre desenhos. A forma lognormal não tem fundamento empírico específico no consórcio, já que nenhuma fonte disponível mede a urgência individual; ela é a escolha usual para uma característica positiva com cauda à direita.

A lognormal dá urgência sempre positiva, com cauda à direita: a maioria dos participantes tem urgência moderada, e poucos têm urgência alta, que são os que, pela política da seção 4.1, ofertam lance. A Beta reescalada limita a liquidez ao intervalo $[0, \bar\lambda]$ e concentra a massa em valores baixos, o que corresponde a um participante típico com pouca reserva própria em relação ao crédito. A independência entre urgência e liquidez é uma simplificação: é plausível que quem tem mais urgência tenha menos reserva, e uma correlação negativa reduziria o lance livre de quem mais quer antecipar o crédito.

O lance embutido atenua a restrição de liquidez. Com teto $\bar b^{e} = 0{,}3$, valor fixado nos regulamentos que o explicitam [@itau2024condicoes, cl. 14.6; @santander2026regulamento, cl. 9.1.7.3], um participante sem liquidez nenhuma ainda pode ofertar até 30% do crédito, à custa de receber menos. As duas tecnologias de lance têm custos diferentes: o lance livre consome reserva própria; o embutido reduz o crédito recebido. O critério de bem-estar da seção 4.4 contabiliza as duas de forma distinta.

O escopo da seção previa, além de urgência e liquidez, o custo de capital do participante. No modelo, esse papel é desempenhado pela própria urgência: $\theta_i$ é a única taxa de desconto do participante e governa tanto o valor de antecipar o crédito quanto o custo de imobilizar liquidez num lance. Separar as duas exigiria um parâmetro que nenhum momento disponível identifica.

## O que é calibrado e o que é fixado

Das três camadas, apenas os parâmetros de comportamento e de restituição, $(\phi_0, \phi_1, \bar r)$, são calibrados. A estrutura observada vem dos dados, e as distribuições $F_\theta$ e $F_\lambda$ ficam fixas nos valores acima. A escolha é forçada pela informação disponível: com quatro momentos de calibração e três parâmetros livres, sobra um único grau de liberdade, e não há como estimar também a forma das distribuições de tipos. A consequência é que os resultados do Capítulo 7 são condicionais a $F_\theta$ e $F_\lambda$, e a sensibilidade a essas escolhas é uma das ameaças discutidas na seção 8.3; a seção 7.5 examina duas formas alternativas de $F_\theta$.
