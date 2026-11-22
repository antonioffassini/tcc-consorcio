---
secao: 7.5
titulo: Robustez da ordenação
status: rascunho
responsavel:
insumos:
  - results/
  - ESTADO.md §4, 2026-11-19 (regra de robustez de H3; modelo de 16/11 como sensibilidade); §5 item 29
fontes:
  - results/h3_robustez_resumo.csv
  - results/h3_robustez_relativas.csv
  - results/h3_relativas.csv
  - results/h3_config_sobra.csv
  - results/h3_config_fracao.csv
excecoes:
  - 0,5
paginas_alvo: 4
---

# Robustez da ordenação

A hipótese H3 tem duas partes: existe um desenho que domina o vigente, e essa ordenação é robusta à incerteza de calibração compatível com os dados. A seção 7.4 mostrou que, no ponto calibrado, nenhum desenho domina $M_0$ pela regra do intervalo de confiança. Esta seção trata da segunda parte por duas vias: repetindo a comparação em parâmetros sorteados do bootstrap de calibração e repetindo-a inteira na versão do modelo de 16 de novembro, que difere do modelo base justamente nas regras que a revisão pelos regulamentos alterou.

## Incerteza de calibração

A comparação foi repetida em dez estimativas de $\Theta$ sorteadas entre as cem do bootstrap de calibração (seção 6.3), com uma réplica cada. A regra de robustez, registrada antes, exige que em pelo menos oito dos dez sorteios nenhuma estimativa pontual de critério piore mais que 1% do nível de $M_0$ e ao menos uma melhore mais que 1%. O limiar de 1% existe porque, com uma réplica por sorteio, não há intervalo de confiança em cada sorteio, e diferenças muito pequenas não devem contar como piora nem como melhora.

**Tabela 7.7 — Robustez no modelo base: dez sorteios de $\Theta$, em % do nível de $M_0$**

| Desenho | Dominância pontual | Bem-estar, mín. a máx. | Dispersão, mín. a máx. |
|---|---|---|---|
| $M_1$, $\beta$ = 0,5 | 0 de 10 | −5,89 a −4,49 | −2,55 a −1,68 |
| $M_1$, $\beta$ = 1 | 0 de 10 | −8,65 a −7,18 | −4,00 a −3,39 |
| $M_1$, $\beta$ = 2 | 0 de 10 | −10,90 a −9,52 | −6,50 a −5,12 |
| $M_2$ | 8 de 10 | 2,07 a 4,07 | 0,532 a 1,22 |

Fonte: `results/h3_robustez_resumo.csv`.

O sinal dos efeitos não muda em nenhum dos dez sorteios. $M_1$ perde bem-estar em todos, com magnitude parecida à do ponto calibrado, e nunca domina. $M_2$ ganha bem-estar em todos, entre 2,07% e 4,07%, e aumenta a dispersão da espera em todos, entre 0,532% e 1,22%. Em oito sorteios o aumento da dispersão fica abaixo do limiar de 1%, e $M_2$ domina pontualmente; nos outros dois, o aumento passa do limiar (`results/h3_robustez_relativas.csv`). Pela regra registrada, a dominância pontual de $M_2$ é robusta.

## As duas partes da regra discordam

O resultado de $M_2$ coloca as duas partes da regra em conflito. A regra do intervalo, no ponto calibrado, diz que $M_2$ não domina, porque a piora na dispersão, embora pequena, está estatisticamente bem determinada. A regra de robustez diz que a dominância pontual se mantém em oito de dez parametrizações, porque a mesma piora fica, na maior parte delas, abaixo de 1%. As duas medem coisas diferentes: a primeira pergunta se a piora existe; a segunda, se ela é grande.

A regra registrada não previa a divergência. O texto relata as duas partes, e não escolhe a mais favorável. Pelo critério completo de H3, que exige dominância no ponto calibrado e robustez, **H3 não se sustenta no modelo base**. O que se sustenta é uma afirmação mais fraca: $M_2$ aumenta o bem-estar e reduz a falha de sorteio em toda a faixa de incerteza de calibração, à custa de um aumento da dispersão da espera da ordem de 1%.

## Sensibilidade à estrutura do modelo

A segunda via de robustez muda a estrutura, e não os parâmetros. Na versão de 16 de novembro, ativas e excluídas disputam o mesmo sorteio, o número de sorteios por assembleia é proporcional à capacidade do grupo e varia entre administradoras, a sobra fica no fundo e o teto do embutido é de 25%. A versão foi calibrada nos três momentos de calibração da época e reproduzia mal a relação entre tamanho e lance (seção 7.2). Ela não é uma alternativa equivalente ao modelo base, mas mostra o que acontece com a conclusão quando as regras contratuais mudam.

**Tabela 7.8 — Diferenças contra $M_0$ no modelo de 16/11, em % do nível de $M_0$ (IC de 95%)**

| Desenho | Bem-estar | Dispersão | Falha de sorteio | Restituição | Domina? | Robustez |
|---|---|---|---|---|---|---|
| $M_1$, $\beta$ = 1 | −4,03 (−4,43; −3,63) | −0,269 (−0,402; −0,149) | −2,07 (−5,37; −0,191) | −1,58 (−1,72; −1,50) | não | 0 de 10 |
| $M_2$ | 2,56 (2,02; 3,12) | −0,254 (−0,411; −0,017) | −2,88 (−8,36; −0,088) | −0,00132 (−0,0797; 0,107) | sim | 8 de 10 |

Fontes: `results/h3_relativas.csv`; `results/h3_robustez_resumo.csv`; `results/h3_config_fracao.csv`.

No modelo de 16 de novembro, $M_2$ domina $M_0$ pela regra do intervalo e de forma robusta: melhora bem-estar, dispersão e estabilidade, sem piora. $M_1$ continua sem dominar, porque perde bem-estar.

A comparação entre as duas versões separa o que é estável do que depende da estrutura. São estáveis o ganho de bem-estar de $M_2$, de 2,56% a 2,77% nas duas versões, a redução da falha de sorteio sob $M_2$ e a perda de bem-estar sob $M_1$. O que muda é o sinal do efeito de $M_2$ sobre a dispersão da espera: negativo no modelo de 16 de novembro, positivo no modelo base. E é exatamente esse sinal que decide se $M_2$ domina.

## O que a varredura não cobre

A robustez examinada aqui cobre a incerteza dos três parâmetros calibrados e uma alternativa estrutural. Não cobre as distribuições de tipos $F_\theta$ e $F_\lambda$ nem os coeficientes fixos da política, $\phi_1$ e $\phi_2$, que ficaram fora da calibração (seção 4.2). [RESULTADO PENDENTE: sensibilidade de H3 a $F_\theta$, $F_\lambda$, $\phi_1$ e $\phi_2$, se houver tempo antes do congelamento] E não cobre a resposta do comportamento à mudança de regra, que é a limitação mais séria da comparação (seção 7.4). Como o ganho de bem-estar de $M_2$ vem, em boa parte, de os vencedores pagarem menos com a mesma política, é justamente esse ganho que mais depende da política fixa.
