---
secao: 4.3
titulo: Regras de contemplação como mecanismo parametrizado
status: rascunho
responsavel:
insumos:
  - decisões do log
  - ESTADO.md §4, 2026-11-15, 2026-11-16 e 2026-11-19 (sequência da assembleia, excluídas, sobra, embutido, M1, M2, política fixa)
  - ESTADO.md §5 itens 23 e 26 (admissibilidade; regulamentos)
  - src/sim/regras.py
  - src/sim/grupo.py
fontes:
  - results/calibracao_momentos.csv
excecoes:
  - 11795
  - 11.795
  - 285
  - 30
  - 14.6
paginas_alvo: 5
---

# Regras de contemplação como mecanismo parametrizado

A comparação entre desenhos de contemplação só faz sentido se os desenhos diferirem naquilo que se quer avaliar e em mais nada. Esta seção fixa essa condição. O mecanismo $M$ é decomposto em três partes: a restrição de recursos e a ordem das operações na assembleia, que são as mesmas para todos os desenhos; a regra de sorteio das cotas ativas; e a regra de lance. O mecanismo vigente $M_0$ e as duas alternativas avaliadas, $M_1$ e $M_2$, diferem apenas na segunda ou na terceira parte. Antes disso, define-se o que torna uma alternativa admissível, já que a hipótese H3 só se refere a desenhos admissíveis sob a regulação vigente.

## A assembleia no modelo

Em cada assembleia $t$, o fundo comum dispõe do saldo $R_t$, medido em frações do crédito $C$. A norma fixa três restrições que valem para qualquer desenho. A contemplação está condicionada à existência de recursos suficientes no grupo, tanto para a entrega do crédito quanto para a restituição aos excluídos (art. 23 da Lei n. 11.795/2008) [@brasil2008lei11795]; por isso o número de vagas $g_t$ é um resultado de $R_t$ e das ofertas, e não um parâmetro do desenho. O lance só pode ser realizado depois das contemplações por sorteio previstas para a assembleia, ou se estas não ocorrerem por falta de recursos (art. 12, I, da Resolução BCB n. 285/2023) [@bcb2023res285]. E concorrem à contemplação apenas o consorciado ativo e os excluídos, estes para efeito de restituição dos valores pagos (arts. 21 e 22, § 2º, da Lei).

O restante da sequência é definido pelo contrato de adesão, e o modelo segue o que se observou em regulamentos de grupos de imóveis de cinco administradoras [CITAR: portoseguro2025regulamento; itau2024condicoes; santander2025regulamento; ademicon2024contrato; sicredi2026regulamento — referências verificadas, PDFs pendentes]. Em quatro deles, o sorteio das cotas excluídas é separado e posterior ao das ativas; em um, ativas e excluídas disputam o mesmo sorteio. Nenhum fixa o número de sorteios por assembleia, que fica condicionado ao saldo do fundo. Quanto aos recursos que sobram depois do lance, três contratos os destinam a novos sorteios entre as ativas na mesma assembleia, e um os leva à assembleia seguinte.

Com base nisso, a assembleia simulada segue cinco etapas:

1. arrecadação das parcelas das cotas adimplentes;
2. sorteio de uma cota ativa elegível ($\kappa_g = 1$), que recebe o crédito se o saldo o cobre;
3. sorteio de cotas excluídas ainda não restituídas, separado do anterior: a primeira restituição ocorre se houver saldo, e as seguintes enquanto a soma restituída na assembleia não ultrapassar $\bar r$ créditos;
4. lance sobre o saldo residual;
5. se o contrato da administradora o prevê, novos sorteios entre as ativas enquanto o saldo cobrir um crédito; caso contrário, o saldo passa à assembleia seguinte.

O teto $\bar r$ tem inspiração no limite por assembleia que um dos contratos impõe às devoluções a excluídos. O destino da sobra é tratado como cláusula da administradora: uma fração $\eta$ delas adota o sorteio da sobra. Os dois parâmetros, $\bar r$ e $\eta$, são calibrados (seção 6.3). A variante em que ativas e excluídas disputam o mesmo sorteio é mantida como análise de sensibilidade.

O lance vencedor é destinado à amortização de prestações vincendas (art. 12, parágrafo único, da Resolução) e, quando embutido, é deduzido do crédito a ser entregue (art. 13, parágrafo único) [@bcb2023res285]. O lance ofertado pela cota $i$, $b_{i,t}$, é um percentual do próprio crédito, composto por uma parte livre, paga com liquidez própria, e uma parte embutida, limitada a $\bar b^{e}$. Nos dois contratos que fixam esse teto no regulamento, ele corresponde a 30% do crédito [CITAR: itau2024condicoes, cl. 14.6; santander2025regulamento, cl. 72 — PDFs pendentes]. Se o vencedor oferta $b$, da qual uma parte $e$ é embutida, o fundo recebe $b-e$ e entrega $1-e$; a saída líquida é $1-b$, e a contemplação por lance de uma cota é viável quando $R_t \ge 1-b$.

## Critério de admissibilidade

A Lei remete ao contrato a forma da contemplação: ela ocorre por sorteio ou por lance, "na forma prevista no contrato de participação em grupo de consórcio, por adesão" (art. 22, § 1º) [@brasil2008lei11795]. A Resolução repete a remissão ao exigir que o contrato estabeleça as condições para concorrer à contemplação por sorteio e sua forma, bem como as regras da contemplação por lance (art. 2º, XII) [@bcb2023res285]. Nenhum dos dois textos exige sorteio equiprovável, nem que o vencedor do lance pague exatamente o que ofertou.

Este trabalho adota, então, o seguinte critério: um desenho alternativo é admissível se altera apenas o que a norma delega ao contrato — a forma do sorteio e as regras do lance — e preserva quem concorre, a condição de recursos, a precedência do sorteio e o destino do lance. O critério é uma leitura dos textos normativos, e não uma interpretação firmada por regulador ou tribunal. A diversidade de cláusulas encontrada nos contratos, todos posteriores à Resolução n. 285, mostra que a forma do sorteio e o destino da sobra já variam entre administradoras sem objeção normativa conhecida.

## O mecanismo vigente, $M_0$

Em $M_0$, todo sorteio entre ativas é uniforme: cada cota elegível tem a mesma probabilidade de ser escolhida, independentemente de quando entrou no grupo. O sorteio de excluídas também é uniforme entre elas. O lance segue a regra de pagamento pelo próprio lance (*pay-as-bid*): as ofertas são ordenadas por percentual, e a de maior percentual é contemplada se $R_t \ge 1-b$; o saldo é atualizado e a seguinte é examinada. Como a viabilidade depende só de $b$ e as ofertas estão em ordem decrescente, a primeira oferta inviável encerra a disputa. Cada vencedor amortiza exatamente o que ofertou.

## $M_1$: sorteio das ativas ponderado pela espera

$M_1$ altera apenas o sorteio entre ativas. Cada cota elegível $i$ recebe peso $(1+a_{i,t})^{\beta}$, em que $a_{i,t}$ é o número de meses desde a sua entrada no grupo, e a probabilidade de ser sorteada é o seu peso dividido pela soma dos pesos dos elegíveis. Com $\beta = 0$, $M_1$ coincide com $M_0$; o valor de referência é $\beta = 1$, e o Capítulo 7 avalia também $\beta = 0{,}5$ e $\beta = 2$.

Num grupo fechado, todas as cotas não contempladas entraram na mesma assembleia, e o peso pela espera reproduziria o sorteio uniforme. O grupo de consórcio real, porém, é aberto: as vagas de cotas excluídas são recolocadas para novos participantes, que entram com o grupo em andamento. Nos dados, a reposição de vagas acompanha as exclusões, e o número de cotas ativas permanece estável ao longo da vida do grupo (seção 5.3). No sorteio uniforme, quem entrou ontem tem a mesma chance de quem espera há anos. $M_1$ desloca a probabilidade para quem espera há mais tempo, e por isso afeta diretamente a dispersão do tempo de espera, um dos critérios da seção 4.4.

O peso não é manipulável pelo participante, que não escolhe quando entrou no grupo, e não altera nenhum dos elementos que o critério de admissibilidade preserva. Uma alternativa considerada e descartada foi ponderar pela situação da cota, reduzindo o peso das excluídas num sorteio comum. Nos contratos examinados, o sorteio de excluídas já é, na maioria, separado e posterior ao das ativas, de modo que essa alternativa apenas reproduziria a prática.

## $M_2$: lance de preço uniforme

$M_2$ mantém o sorteio uniforme e muda a regra de pagamento do lance. As ofertas continuam ordenadas por percentual, e as $k$ maiores vencem. Todas pagam o mesmo preço, $p^{u}_t$, igual à maior oferta recusada, isto é, a $(k+1)$-ésima maior oferta; se não houver oferta recusada, o preço é nulo.

O número de vencedores passa a depender do preço. Cada vencedor amortiza $p^{u}_t$ — com a parte livre até o que ofertou de livre e o restante com embutido — e recebe $1$ menos a parte embutida. A saída líquida do fundo por vencedor é $1-p^{u}_t$, igual para todos. Denotando por $b_{(k+1)}$ a $(k+1)$-ésima maior oferta, a disputa com $k$ vencedores é viável se

$$
R_t \;\ge\; k\,\bigl(1-b_{(k+1)}\bigr).
$$

Como $b_{(k+1)}$ não cresce com $k$, o lado direito cresce com $k$, e $g^b_t$ é o maior $k$ que satisfaz a desigualdade.

Sob as mesmas ofertas, $M_2$ contempla por lance no máximo tantas cotas quanto $M_0$. Em $M_0$, $k$ vencedores são viáveis se $R_t \ge \sum_{i=1}^{k}(1-b_{(i)})$; como cada $b_{(i)}$ com $i \le k$ é maior ou igual a $b_{(k+1)}$, a condição de $M_2$ é mais exigente, e os vencedores de $M_2$ são sempre os primeiros da ordem de $M_0$. O preço menor pago pelos vencedores custa vagas, porque entra menos dinheiro no fundo por contemplação.

A motivação de $M_2$ vem da teoria de leilões. Com uma única vaga, $M_2$ é o leilão de segundo preço, em que ofertar o próprio valor é estratégia dominante, e $M_0$ é o leilão de primeiro preço, em que o participante reduz a oferta abaixo do valor. Com valores privados independentes e uniformes entre $n$ participantes, a oferta de equilíbrio no primeiro preço é $(n-1)/n$ do valor, e as receitas esperadas dos dois formatos coincidem [CITAR: vickrey1961counterspeculation; krishna2010auction, cap. 2 — referências verificadas, PDF pendente]. Para vagas múltiplas com demanda unitária, o pagamento pela maior oferta recusada é a generalização que preserva a dominância da oferta pelo valor [CITAR: krishna2010auction, parte II — PDF pendente; conferir o capítulo exato ao ler]. No consórcio, essas propriedades valem só de forma aproximada: o valor da contemplação antecipada depende do que ocorrerá nas assembleias seguintes, e a restrição de liquidez limita a oferta.

Quanto à admissibilidade, $M_2$ altera apenas a regra de apuração do lance, que a Resolução delega ao contrato (art. 2º, XII). Resta uma questão de leitura: os arts. 12 e 13 falam em "valor do lance vencedor". Este trabalho entende esse valor como o montante que o contrato define como devido pelo vencedor, e não necessariamente o percentual ofertado. A ata da assembleia continua obrigada a relacionar as cotas ofertantes e os percentuais oferecidos (art. 48) [@bcb2023res285], de modo que a apuração por preço uniforme não reduz a transparência exigida. A Resolução não trata do ponto de forma explícita.

## Síntese e o que permanece fixo

O Quadro 4.1 resume os três desenhos. Em todos, a sequência da assembleia, o sorteio de excluídas e o destino da sobra são os da subseção sobre a assembleia no modelo.

| | Sorteio entre ativas | Lance: quem vence | Lance: quanto paga |
|---|---|---|---|
| $M_0$ | uniforme | maiores ofertas, enquanto $R_t \ge 1-b$ | a própria oferta |
| $M_1$ | peso $(1+a_{i,t})^{\beta}$ | como $M_0$ | como $M_0$ |
| $M_2$ | como $M_0$ | as $k$ maiores, com $R_t \ge k(1-p^{u}_t)$ | $p^{u}_t$, a maior oferta recusada |

: Quadro 4.1 — Desenhos de contemplação avaliados. Fonte: elaboração própria.

Na implementação, cada desenho é um par de regras, uma de sorteio e uma de lance, passado ao mesmo simulador. A troca de desenho não altera nenhuma outra parte do código, e o desenho vigente executado por esse caminho reproduz exatamente o resultado do simulador original. Os testes que verificam cada regra isoladamente, incluindo os casos de leilão com uma única vaga, são descritos na seção 6.4.

Um elemento fica fixo entre desenhos por escolha de modelagem, e não por exigência normativa: a política de lance dos participantes, $\pi_\phi$. Sob $M_2$, a melhor resposta de um participante racional muda, já que deixa de haver motivo para reduzir a oferta abaixo do valor; sob $M_1$, quem espera há mais tempo tem menos motivo para ofertar. Manter a mesma política nos três desenhos isola o efeito da regra sobre um comportamento dado, mas não captura a adaptação do comportamento à regra nova. As implicações dessa escolha são tratadas na seção 4.5.
