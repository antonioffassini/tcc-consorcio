---
secao: 8.2
titulo: Trade-offs entre critérios
status: rascunho
responsavel:
insumos:
  - cap. 7
fontes:
  - results/h3_relativas_sobra_reg.csv
  - results/m3_decomposicao_B.csv
  - results/texto_2211_apresentacao.csv
excecoes:
paginas_alvo: 2
---

# Trade-offs entre critérios

Os quatro critérios da seção 4.4 não andam juntos, e a regra de dominância foi escolhida justamente para não precisar pesá-los uns contra os outros: um desenho só domina se não piorar nenhum. Esta seção reúne os conflitos que a comparação revelou, porque eles dizem mais sobre o mecanismo do que a lista de quem domina.

## Bem-estar contra igualdade da espera

O conflito mais nítido é o de $M_1$. Favorecer no sorteio quem espera há mais tempo reduz a dispersão da espera, entre 2,27% e 5,56% conforme a intensidade, e reduz o bem-estar, entre 1,10% e 2,67% (`results/h3_relativas_sobra_reg.csv`). Os dois critérios medem coisas que um regulador pode querer ao mesmo tempo: que ninguém espere muito mais que os outros e que o crédito chegue a quem mais precisa dele cedo. Com urgências diferentes, as duas metas puxam em direções opostas, porque igualar a espera significa ignorar a urgência.

## Preço do lance contra saldo do fundo

O preço uniforme cobra menos de quem vence. O vencedor ganha, mas entra menos dinheiro no fundo, e o fundo contempla menos gente adiante. Sob $M_2$, isso aparece como mais bem-estar e menos instabilidade, porque os vencedores amortizam menos e o fundo não falha tanto no sorteio previsto, e como mais dispersão da espera, de 0,81%. O mesmo preço que melhora a situação de quem vence piora a dos que ficam.

$M_3^{rs}(0{,}05)$ resolve esse conflito quando o comportamento é mantido: o lance mínimo limita a queda do preço, e o sorteio obrigatório da sobra devolve na mesma assembleia o dinheiro que o leilão deixou de usar. A decomposição da seção 7.4 mostra que nenhuma das duas peças faz isso sozinha. Quando o lance se adapta à regra, porém, o conflito reaparece (seção 7.6): os participantes passam a ofertar acima do mínimo, o sorteio da sobra quase não é acionado, e o ganho de bem-estar volta a vir com mais dispersão da espera. Complementos que dependem de o participante deixar saldo atenuam esse conflito, mas o aprendizado os desfaz. O complemento mais promissor é o que atua sobre algo que o participante não controla: em $M_4$, o peso da espera no sorteio devolve igualdade à espera por um canal que o lance não alcança (seção 7.6). Mas ele também tem preço: quanto mais forte o peso, mais igualdade e menos bem-estar, e a intensidade em que os dois ganhos coexistem com o lance aprendido não se mostrou estável entre sementes de treino. Há ainda um custo de outra natureza: a espera média cresce um pouco, porque o sorteio passa a favorecer quem já esperou, e a urgência de quem entrou há pouco pesa menos.

## O que o desenho proposto troca

Mesmo $M_3^{rs}(0{,}05)$ troca alguma coisa, fora dos critérios. A espera média sobe 1,85%, enquanto a dispersão fica igual: o desenho antecipa quem tem mais urgência à custa de uma espera um pouco maior para a média. E a fração de contemplações por lance cai de 0,6895 para 0,4378, porque parte do saldo passa a ir ao sorteio. Para o participante médio, esses dois efeitos não aparecem no bem-estar; para quem lê o mercado pela fração de lance, mudam o indicador.

## Generalizar o que existe contra mudar o preço

A decomposição oferece duas opções ao regulador. Estender a todo o sistema o lance mínimo e o sorteio obrigatório da sobra, sem mudar o preço, domina o vigente com ganho pequeno de bem-estar, de 0,26%, e redução de 1,00% na dispersão da espera (`results/m3_decomposicao_B.csv`). Adotar também o preço uniforme multiplica o ganho de bem-estar e reduz a instabilidade, mas abre mão da redução da dispersão. A primeira opção é a mais igualitária; a segunda, a de maior ganho médio. A regra de dominância não escolhe entre as duas, porque ambas dominam o vigente.
