---
secao: 4.3
titulo: Regras de contemplação como mecanismo parametrizado
status: rascunho
responsavel:
insumos:
  - decisões do log
  - ESTADO.md §4, 2026-11-15 e 2026-11-16 (vagas de sorteio, lance embutido, M1, M2, política fixa)
  - src/sim/regras.py
  - src/sim/grupo.py
fontes:
  - results/sim_heterogeneidade.csv
excecoes:
  - 11795
  - 11.795
  - 285
paginas_alvo: 4
---

# Regras de contemplação como mecanismo parametrizado

A comparação entre desenhos de contemplação só faz sentido se os desenhos diferirem naquilo que se quer avaliar e em mais nada. Esta seção fixa essa condição. O mecanismo $M$ é decomposto em três partes: a restrição de recursos e a ordem de precedência, que são as mesmas para todos os desenhos; a regra de sorteio; e a regra de lance. O mecanismo vigente $M_0$ e as duas alternativas avaliadas, $M_1$ e $M_2$, são então descritos como escolhas distintas apenas na segunda ou na terceira parte. Antes disso, define-se o que torna uma alternativa admissível, já que a hipótese H3 só se refere a desenhos admissíveis sob a regulação vigente.

## Elementos comuns a todos os desenhos

Em cada assembleia $t$, o fundo comum dispõe do saldo $R_t$, medido em frações do crédito $C$. A sequência de operações é a mesma em qualquer desenho e é fixada pela norma, não pelo contrato.

Primeiro, a contemplação está condicionada à existência de recursos suficientes no grupo, tanto para a entrega do crédito quanto para a restituição aos excluídos (art. 23 da Lei n. 11.795/2008) [@brasil2008lei11795]. O número de vagas $g_t$ não é, portanto, um parâmetro do desenho, e sim o resultado de $R_t$ e das ofertas.

Segundo, o lance só pode ser realizado depois das contemplações por sorteio previstas para a assembleia, ou se estas não ocorrerem por falta de recursos (art. 12, I, da Resolução BCB n. 285/2023) [@bcb2023res285]. O sorteio consome primeiro o saldo, até o número de vagas previsto em contrato, $\kappa_g$ (seção 4.2), e o lance disputa o saldo residual. Assim, $g^s_t \le \kappa_g$, e $g^b_t$ é determinado pelo que sobra.

Terceiro, concorrem à contemplação apenas o consorciado ativo — o que mantém vínculo obrigacional com o grupo, excetuados o inadimplente não contemplado e o excluído — e os excluídos, estes para efeito de restituição dos valores pagos (arts. 21 e 22, § 2º, da Lei) [@brasil2008lei11795]. No modelo, isso define o conjunto de elegíveis ao sorteio: cotas ativas não contempladas e adimplentes, e cotas excluídas ainda não restituídas. Ao lance concorrem só as primeiras.

Quarto, o lance vencedor é destinado à quitação ou à amortização de prestações vincendas (art. 12, parágrafo único, da Resolução) e, quando embutido, é deduzido do crédito a ser entregue na própria assembleia (art. 13, parágrafo único) [@bcb2023res285]. O lance ofertado pela cota $i$, $b_{i,t}$, é expresso como percentual do próprio crédito e se compõe de uma parte livre, paga com liquidez própria, e de uma parte embutida, limitada a $\bar b^{e}$. Se o vencedor oferta $b$, da qual uma parte $e$ é embutida, o fundo recebe $b-e$ e entrega $1-e$; a saída líquida é $1-b$. A contemplação por lance de uma cota é viável, então, quando $R_t \ge 1-b$.

Esses quatro elementos são idênticos nos três desenhos. O que muda é a forma de escolher, entre os elegíveis, quem recebe cada vaga, e o quanto paga quem vence por lance.

## Critério de admissibilidade

A Lei remete ao contrato a forma da contemplação: ela ocorre por sorteio ou por lance, "na forma prevista no contrato de participação em grupo de consórcio, por adesão" (art. 22, § 1º) [@brasil2008lei11795]. A Resolução repete a remissão ao exigir que o contrato estabeleça as condições para concorrer à contemplação por sorteio e sua forma, bem como as regras da contemplação por lance (art. 2º, XII) [@bcb2023res285]. Nenhum dos dois textos exige sorteio equiprovável, nem que o vencedor do lance pague exatamente o que ofertou. Ambos fixam, porém, os quatro elementos da subseção anterior.

Este trabalho adota, então, o seguinte critério: um desenho alternativo é admissível se altera apenas o que a norma delega ao contrato — a forma do sorteio e as regras do lance — e preserva quem concorre, a condição de recursos, a precedência do sorteio e o destino do lance. O critério é uma leitura dos textos normativos, e não uma interpretação firmada por regulador ou tribunal. Saber se alguma administradora já pratica variações desse tipo exigiria consultar regulamentos de grupos, o que não foi feito [CITAR: regulamentos de grupos de consórcio que fixem forma de sorteio ou de apuração de lance diferente da vigente, se houver].

O critério tem uma consequência imediata para $M_1$, discutida adiante: um sorteio que retire os excluídos da disputa não é admissível, porque o art. 22, § 2º, lhes garante concorrer à contemplação para restituição.

## O mecanismo vigente, $M_0$

No desenho vigente, o sorteio é uniforme entre os elegíveis: em cada uma das até $\kappa_g$ extrações, cada cota elegível tem a mesma probabilidade de ser escolhida. Se a sorteada é ativa, recebe o crédito; se é excluída, recebe a restituição do que pagou. A extração cessa quando o saldo não cobre o valor devido à sorteada.

O lance segue a regra de pagamento pelo próprio lance (*pay-as-bid*). As ofertas são ordenadas por percentual, e a de maior percentual é contemplada se $R_t \ge 1-b$; o saldo é atualizado e a seguinte é examinada. Como a condição de viabilidade depende só de $b$ e as ofertas estão em ordem decrescente, a primeira oferta inviável encerra a disputa. Cada vencedor amortiza exatamente o que ofertou.

## $M_1$: sorteio ponderado pela situação da cota

Uma alternativa natural ao sorteio uniforme é ponderá-lo pela espera, aumentando a chance de quem está há mais tempo no grupo. Num grupo fechado, porém, todas as cotas não contempladas entraram na mesma assembleia e têm a mesma espera, de modo que o peso pela espera reproduz o sorteio uniforme. Ele só distinguiria cotas num grupo em que vagas excluídas são recolocadas para novos participantes, o que ocorre nos dados (seção 5.3), mas faria o resultado da comparação depender inteiramente da taxa de recolocação.

$M_1$ pondera o sorteio pela situação da cota. Cada cota ativa elegível tem peso $1$; cada excluída não restituída tem peso $\omega \in (0, 1]$. A probabilidade de uma cota elegível ser sorteada é o seu peso dividido pela soma dos pesos dos elegíveis. Com $\omega = 1$, $M_1$ coincide com $M_0$. O lance permanece como em $M_0$.

Três razões sustentam essa escolha. A primeira é que a situação da cota separa os elegíveis mesmo no grupo fechado, desde que haja exclusão. A segunda é que o peso não pode ser manipulado pelo participante: para ter peso menor seria preciso ser excluído, o que custa a própria carta de crédito. Ponderar pelo número de lances perdidos, por exemplo, foi descartado por esse motivo, já que lance perdido não custa nada e todos teriam incentivo a ofertar sempre. A terceira é que o peso age na margem que pesa nos dados: a fração das contemplações por sorteio que vai a cotas excluídas é de 0,734 no painel de administradoras posterior à Resolução n. 285 (`results/sim_heterogeneidade.csv`). Na maior parte das assembleias, o sorteio funciona mais como canal de restituição do que como canal de crédito.

O que $M_1$ troca é prazo de restituição do excluído por prazo de crédito da ativa. Reduzir $\omega$ antecipa a carta de quem continua pagando e posterga a devolução a quem saiu, o que também altera o perfil de saídas do fundo ao longo da vida do grupo. É o conflito entre os critérios de bem-estar e de estabilidade definidos na seção 4.4, e por isso $M_1$ é avaliado numa grade de valores de $\omega$, e não num valor único (Capítulo 7).

O limite $\omega = 0$ fica fora do conjunto admissível. Nele, nenhum excluído é sorteado enquanto houver ativa elegível, e na prática a restituição passa a ocorrer só no encerramento do grupo, o que contraria o art. 22, § 2º, da Lei. O caso é simulado apenas como referência de limite e não entra na avaliação de H3.

## $M_2$: lance de preço uniforme

$M_2$ mantém o sorteio uniforme e muda a regra de pagamento do lance. As ofertas continuam ordenadas por percentual, e as $k$ maiores vencem. Todas pagam o mesmo preço, $p^{u}_t$, igual à maior oferta recusada, isto é, a $(k+1)$-ésima maior oferta; se não houver oferta recusada, o preço é nulo.

O número de vencedores passa a depender do preço. Cada vencedor amortiza $p^{u}_t$ — com a parte livre até o que ofertou de livre e o restante com embutido — e recebe $1$ menos a parte embutida. A saída líquida do fundo por vencedor é $1-p^{u}_t$, igual para todos. Denotando por $b_{(k+1)}$ a $(k+1)$-ésima maior oferta, a disputa com $k$ vencedores é viável se

$$
R_t \;\ge\; k\,\bigl(1-b_{(k+1)}\bigr).
$$

Como $b_{(k+1)}$ não cresce com $k$, o lado direito cresce com $k$, e $g^b_t$ é o maior $k$ que satisfaz a desigualdade.

A comparação com $M_0$ sob as mesmas ofertas é direta. Em $M_0$, $k$ vencedores são viáveis se $R_t \ge \sum_{i=1}^{k}(1-b_{(i)})$. Como cada $b_{(i)}$ com $i \le k$ é maior ou igual a $b_{(k+1)}$, a condição de $M_2$ é mais exigente: $M_2$ contempla por lance no máximo tantas cotas quanto $M_0$, e sempre as mesmas primeiras da ordem. O preço menor pago pelos vencedores custa vagas, porque entra menos dinheiro no fundo por contemplação. É essa contrapartida que a comparação do Capítulo 7 precisa medir.

A motivação de $M_2$ vem da teoria de leilões. Com uma única vaga, $M_2$ é o leilão de segundo preço, em que ofertar o próprio valor é estratégia dominante, e $M_0$ é o leilão de primeiro preço, em que o participante reduz a oferta abaixo do valor. Com valores privados independentes e uniformes entre $n$ participantes, a oferta de equilíbrio no primeiro preço é $(n-1)/n$ do valor, e as receitas esperadas dos dois formatos coincidem [CITAR: vickrey1961counterspeculation; krishna2010auction, cap. 2 — referências verificadas, PDF pendente]. Para vagas múltiplas com demanda unitária, o pagamento pela maior oferta recusada é a generalização que preserva a dominância da oferta pelo valor; a variante em que todos pagam a menor oferta vencedora não a preserva [CITAR: krishna2010auction, parte II (leilões de múltiplos objetos) — PDF pendente; conferir o capítulo exato ao ler]. No consórcio, essas propriedades valem só de forma aproximada: o valor da contemplação antecipada depende do que ocorrerá nas assembleias seguintes, e a restrição de liquidez limita a oferta. Essa limitação é discutida na seção 4.5.

Quanto à admissibilidade, $M_2$ altera apenas a regra de apuração do lance, que a Resolução delega ao contrato (art. 2º, XII). O destino do valor pago continua o do art. 12, parágrafo único, e a dedução do embutido, a do art. 13, parágrafo único. Resta uma questão de leitura: os dois dispositivos falam em "valor do lance vencedor". Este trabalho entende esse valor como o montante que o contrato define como devido pelo vencedor, e não necessariamente o percentual ofertado. A ata da assembleia continua obrigada a relacionar as cotas ofertantes e os percentuais oferecidos (art. 48) [@bcb2023res285], de modo que a apuração por preço uniforme não reduz a transparência exigida. A Resolução não trata do ponto de forma explícita.

## Síntese e o que permanece fixo

O Quadro 4.1 resume os três desenhos.

| | Sorteio | Lance: quem vence | Lance: quanto paga |
|---|---|---|---|
| $M_0$ | uniforme entre elegíveis | maiores ofertas, enquanto $R_t \ge 1-b$ | a própria oferta |
| $M_1$ | peso $1$ para ativa, $\omega$ para excluída | como $M_0$ | como $M_0$ |
| $M_2$ | como $M_0$ | as $k$ maiores, com $R_t \ge k(1-p^{u}_t)$ | $p^{u}_t$, a maior oferta recusada |

: Quadro 4.1 — Desenhos de contemplação avaliados. Fonte: elaboração própria.

Na implementação, cada desenho é um par de regras, uma de sorteio e uma de lance, passado ao mesmo simulador, que executa a sequência comum de arrecadação, sorteio, lance e exclusão. A troca de desenho não altera nenhuma outra parte do código, e o desenho vigente executado por esse caminho reproduz exatamente o resultado do simulador original. Os testes que verificam cada regra isoladamente, incluindo os casos de leilão com uma única vaga, são descritos na seção 6.4.

Um elemento fica fixo entre desenhos por escolha de modelagem, e não por exigência normativa: a política de lance dos participantes, $\pi_\phi$. Sob $M_2$, a melhor resposta de um participante racional muda, já que deixa de haver motivo para reduzir a oferta abaixo do valor. Manter a mesma política nos três desenhos isola o efeito da regra sobre um comportamento dado, mas não captura a adaptação do comportamento à regra nova. As implicações dessa escolha para a leitura dos resultados são tratadas na seção 4.5.
