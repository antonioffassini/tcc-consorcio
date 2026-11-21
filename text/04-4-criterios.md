---
secao: 4.4
titulo: Critérios de avaliação
status: rascunho
responsavel:
insumos:
  - decisões do log
  - ESTADO.md §4, 2026-11-19 (critérios e regra de decisão de H3, escritos antes da comparação)
  - src/analysis/comparacao.py
fontes:
excecoes:
paginas_alvo: 3
---

# Critérios de avaliação

Comparar mecanismos de contemplação exige dizer, antes de olhar os resultados, o que conta como melhor. Um mecanismo pode antecipar o crédito de quem tem pressa e, ao mesmo tempo, tornar a espera dos demais mais incerta; pode também acelerar as contemplações à custa de deixar o fundo sem saldo para o sorteio do mês seguinte. Por isso a avaliação usa quatro critérios separados, e não um índice único. Esta seção define cada um, explica a escolha e fixa a regra pela qual a hipótese H3 é decidida. Critérios e regra foram registrados no log do projeto antes da primeira rodada de comparação.

## Bem-estar dos participantes

O critério de bem-estar mede quanto vale, para cada participante, o crédito que recebe, levando em conta quando o recebe e quanto pagou para antecipá-lo. Para a cota $i$, a utilidade realizada é

$$
U_i \;=\; e^{-\theta_i w_i/12}\,(1-e_i)\;-\;\ell_i\left(1-e^{-\theta_i r_i/12}\right),
$$

em que $w_i$ é o número de assembleias entre a entrada da cota no grupo e a sua contemplação, $e_i$ e $\ell_i$ são as partes embutida e livre do lance pago na contemplação (nulas se a cota foi sorteada), e $r_i$ é o número de assembleias que ainda restavam do prazo quando ela foi contemplada. A urgência $\theta_i$ é lida como taxa anual, daí a divisão por doze.

O primeiro termo é o valor presente do crédito efetivamente recebido: quanto mais urgente o participante e mais longa a espera, menos vale a carta, e o lance embutido reduz o que ele recebe. O segundo termo é o custo do lance livre. Como o lance amortiza as últimas parcelas da cota (seção 4.3), pagar $\ell_i$ hoje substitui parcelas que só seriam pagas $r_i$ assembleias depois; o custo para o participante é a diferença entre pagar agora e pagar no fim, avaliada pela sua própria urgência. O lance livre não é tratado como perda, porque o dinheiro continua abatendo a dívida da própria cota.

O bem-estar agregado $\mathcal{W}(M)$ é a média de $U_i$ sobre as cotas que permanecem no grupo até a contemplação. Uma cota não contemplada até a última assembleia conta como contemplada nela, que é o que ocorre no encerramento do grupo. As cotas excluídas ficam fora dessa média e entram pelo quarto critério.

A forma de $U_i$ é deliberadamente simples. Ela não captura aversão ao risco, nem o uso que o participante faria do bem, nem o custo de recorrer a crédito fora do consórcio enquanto espera. O objetivo não é medir o bem-estar em reais, e sim ordenar mecanismos sob uma métrica que use apenas o que o modelo determina: a urgência de cada um, quando recebeu e quanto pagou.

## Dispersão do tempo de espera

O segundo critério, $\mathcal{E}(M)$, é o desvio-padrão de $w_i$ entre as mesmas cotas. Ele não mede a espera média, que depende sobretudo da capacidade do grupo e muda pouco entre mecanismos, e sim a incerteza que o participante enfrenta ao entrar. Um grupo em que metade é contemplada no primeiro ano e a outra metade só no último tem a mesma espera média de um grupo em que todos esperam o mesmo tempo, mas expõe cada participante a um risco muito maior. O critério é relevante para o consórcio em particular porque a escolha de entrar num grupo, em vez de financiar o bem, costuma depender de uma expectativa sobre quando a carta virá.

## Estabilidade do fundo

O terceiro critério, $\mathcal{S}(M)$, é a fração das assembleias em que o sorteio previsto não ocorre por falta de saldo, havendo cota ativa elegível. É uma medida direta de quando o fundo comum deixa de cumprir o que o contrato promete ao participante que não oferta lance. A escolha dessa medida, e não de outras possíveis como o saldo ocioso ou o risco de insolvência no encerramento, segue de duas observações. O saldo ocioso tem leitura ambígua: saldo alto pode significar tanto folga quanto ineficiência na alocação. E a insolvência do grupo não ocorre no modelo, em que as saídas nunca excedem as entradas (seção 6.4). O que pode ocorrer, e varia com o mecanismo, é o fundo chegar à assembleia sem saldo para o sorteio, o que acontece, por exemplo, quando um lance livre alto e um embutido alto esvaziam o caixa no mês anterior.

## Restituição aos excluídos

O quarto critério, $\mathcal{R}(M)$, é o número médio de assembleias entre a exclusão de uma cota e a restituição do que ela pagou; a restituição no encerramento conta como ocorrida na última assembleia. O excluído é parte do grupo, tem direito à restituição por sorteio e, nos dados, recebe a maior parte das contemplações por sorteio (seção 5.3). Um mecanismo que melhore a situação de quem continua pagando à custa de quem saiu precisa aparecer na avaliação, e é esse o papel do critério.

## Regra de decisão para H3

A hipótese H3 afirma que existe ao menos um desenho admissível que domina o vigente em pelo menos um critério sem deteriorar os demais, e que essa ordenação resiste à incerteza de calibração. A regra que a decide tem duas partes.

A primeira é a comparação no ponto calibrado. Cada grupo do desenho experimental é simulado da formação ao encerramento sob cada mecanismo, com as mesmas sementes, de modo que as diferenças entre mecanismos não incluam ruído de amostragem entre grupos. Para cada critério, calcula-se a diferença média em relação a $M_0$, ponderada pela composição do painel de dados, com intervalo de confiança de 95% obtido por reamostragem de administradoras. O mecanismo $M$ domina $M_0$ se ao menos um critério melhora com o intervalo inteiro do lado favorável e nenhum critério tem o intervalo inteiro do lado desfavorável.

A segunda parte é a robustez. A comparação é repetida para dez vetores de parâmetros sorteados entre os obtidos no bootstrap da calibração (seção 6.3). Em cada um, considera-se que um critério melhora ou piora quando a diferença pontual ultrapassa 1% do nível observado em $M_0$. A dominância é considerada robusta se se mantiver em ao menos oito dos dez sorteios.

Os limiares de 95%, 1% e oito em dez são convenções, e outras seriam defensáveis. O que importa para a validade do teste é que foram fixados antes de qualquer resultado da comparação. Em todos os mecanismos, a política de lance dos participantes é a mesma; a seção 4.5 discute o que isso implica para a leitura da regra.
