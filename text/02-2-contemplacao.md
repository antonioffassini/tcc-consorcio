---
secao: 2.2
titulo: Contemplação por sorteio e por lance
status: rascunho
responsavel:
insumos:
fontes:
excecoes:
  - 11795
  - 3.432
  - 285
paginas_alvo: 4
---

# Contemplação por sorteio e por lance

A Lei n. 11.795/2008 estabelece que a contemplação do consorciado ocorre por sorteio ou por lance [@brasil2008lei11795]. Esta seção detalha os dois canais e as regras que os articulam, por serem elas o objeto direto da avaliação conduzida neste trabalho.

## Restrição de recursos e ordem de precedência

A regra mais consequente do sistema não trata de como o vencedor é escolhido, mas de quantas contemplações existem. A contemplação está condicionada à existência de recursos suficientes no grupo para a aquisição do bem, conjunto de bens ou serviços a que o grupo esteja referenciado **e** para a restituição aos excluídos. O número de cotas contempladas em uma assembleia não é, portanto, um parâmetro do plano: é uma variável determinada pelo saldo do fundo comum naquele instante.

Sob a Circular n. 3.432/2009, que regulamentou o funcionamento dos grupos até 2023, essa restrição vinha acompanhada de uma regra de precedência explícita: a contemplação por lance somente poderia ocorrer após a contemplação por sorteio, ou caso esta não fosse realizada por insuficiência de recursos [@bcb2009circ3432]. O lance operava, assim, sobre o recurso residual — o que sobra do fundo depois de atendidas as contemplações por sorteio.

A combinação das duas regras produz uma estrutura que não tem paralelo na literatura de associações rotativas de poupança e crédito. O que se disputa por lance não é um prêmio de tamanho fixo, mas um número de vagas estocástico, determinado por um saldo que depende da adimplência agregada do grupo no período e que é consumido prioritariamente pelo sorteio. O participante que oferta um lance decide, portanto, sob incerteza não apenas quanto ao comportamento dos concorrentes, mas quanto à própria existência de vaga.

> **Pendência de verificação.** As disposições de precedência e de condicionamento a recursos aqui descritas foram apuradas na Circular n. 3.432/2009, integralmente revogada. É necessário confirmar o tratamento correspondente na Resolução BCB n. 285/2023 antes de fixar essas regras como hipótese de modelagem no Capítulo 4 [@bcb2023res285].

## Sorteio

O sorteio distribui o crédito de forma aleatória entre as cotas habilitadas. A habilitação exige adimplência: o consorciado em atraso não concorre. O sorteio também é o canal pelo qual, nos termos da lei, os consorciados excluídos podem ter suas cotas contempladas para fins de restituição, questão detalhada na seção 2.4.

Do ponto de vista do participante, o sorteio é o canal de custo marginal zero: participar dele não exige desembolso adicional além da manutenção da adimplência. É o *outside option* contra o qual todo lance é avaliado.

## Lance

O lance é a oferta de antecipação de parcelas com que o participante disputa a alteração de sua posição na ordem de recebimento. As modalidades praticadas — lance livre, em que o valor é definido pelo ofertante; lance fixo, em que o percentual é predefinido em contrato; e lance embutido — variam conforme o contrato de participação e a administradora, dentro do que a regulação admite.

O **lance embutido** merece destaque por alterar a natureza da decisão. Trata-se da oferta de recursos, para fins de contemplação, mediante utilização de parte do próprio valor do crédito previsto para distribuição na respectiva assembleia [@bcb2009circ3432]. Em outras palavras, o participante oferta contra o crédito que receberá, e não contra sua liquidez corrente. A existência dessa modalidade significa que a restrição de liquidez do participante não é absoluta: existem duas tecnologias de lance com custos de oportunidade distintos, e a escolha entre elas é parte do problema de decisão. Um modelo que trate o lance como pura função da liquidez disponível ignora essa margem.

Se o lance não vence a assembleia, o valor ofertado é devolvido ao consorciado, sem penalidade. Isso torna o lance uma opção de exercício repetido a custo de oportunidade — o participante não perde o valor ofertado, mas imobiliza liquidez entre a oferta e a devolução.

## Heterogeneidade de crédito e critério de desempate

É admitida a formação de grupos em que os créditos sejam de valores diferenciados, observado que o crédito de menor valor, vigente ou definido na data de constituição do grupo, não pode ser inferior a cinquenta por cento do crédito de maior valor [@bcb2009circ3432]. Consequentemente, participantes de um mesmo grupo disputam prêmios de magnitudes distintas.

Isso obriga a uma escolha de critério na apuração do vencedor. Uma das formas praticadas é declarar vencedor quem ofertar o maior percentual em relação ao próprio crédito contratado, de modo que lances iguais em valor absoluto sejam desempatados em favor de quem ofertou proporção maior do próprio crédito. Os critérios de desempate constam do contrato e podem variar entre administradoras.

Essa observação tem consequência direta para a formalização: a ação natural do agente não é o valor do lance em reais, mas o **percentual do próprio crédito** ofertado. Adotar essa normalização torna comparáveis participantes com tickets distintos dentro do mesmo grupo e alinha o espaço de ações do modelo ao critério efetivamente aplicado na apuração.
