---
secao: 1.1
titulo: Contexto e relevância econômica
status: rascunho
responsavel:
insumos:
  - dados agregados ABAC/Bacen
fontes:
excecoes:
  - 11795
  - 4010
  - 2080
  - 4110
  - 5,16
  - 4,49
  - 500
  - 378
  - 32,1
  - 12,74
  - 11,22
  - 13,5
paginas_alvo: 3
---

# Contexto e relevância econômica

O Sistema de Consórcios é um mecanismo de autofinanciamento coletivo regulado no Brasil pela Lei n. 11.795, de 8 de outubro de 2008, e supervisionado pelo Banco Central do Brasil [@brasil2008lei11795]. Em um grupo de consórcio, um conjunto determinado de participantes contribui mensalmente para um fundo comum destinado à aquisição de um bem ou serviço previamente especificado. A cada assembleia, o saldo disponível no fundo é alocado a uma ou mais cotas, que passam à condição de contempladas e recebem a carta de crédito correspondente. A alocação ocorre por dois canais: o sorteio, que distribui o crédito de forma aleatória entre as cotas adimplentes, e o lance, pelo qual o participante oferta a antecipação de parcelas para alterar sua posição na ordem de recebimento.

A dimensão do sistema é macroeconomicamente relevante. Em 2025 foram comercializadas 5,16 milhões de cotas, volume 15% superior às 4,49 milhões do ano anterior, correspondendo a mais de R$ 500 bilhões em créditos comercializados — alta de 32,1% sobre os R$ 378 bilhões apurados em 2024. O número de participantes ativos superou pela primeira vez a marca de doze milhões em julho de 2025, atingindo 12,74 milhões em novembro do mesmo ano, ante 11,22 milhões um ano antes, crescimento de 13,5% [@abac2026anuario]. O sistema opera, portanto, na escala de um mercado de crédito de porte nacional, com participação relevante nos segmentos de imóveis, veículos leves, motocicletas, veículos pesados, serviços e bens móveis duráveis.

Essa dimensão não é acidental. O consórcio ocupa, no orçamento das famílias e das empresas brasileiras, uma posição de substituto parcial do crédito bancário para aquisição de bens de alto valor. A ausência de juros — o custo do participante compõe-se essencialmente da taxa de administração e do fundo de reserva — torna a modalidade comparativamente mais atrativa em ambientes de política monetária restritiva, o que ajuda a explicar a expansão observada no período recente. Em contrapartida, o participante abre mão da disponibilidade imediata do bem: o crédito não é contratado, é aguardado.

Essa troca entre custo financeiro e incerteza temporal é a característica que distingue o consórcio de qualquer outro instrumento de crédito e que o converte em objeto próprio de estudo. O participante não escolhe apenas se adere ao grupo; ao longo de todo o prazo, ele decide recorrentemente se e quanto ofertar de lance, e essa decisão depende de quanto ele valoriza a antecipação do crédito, de quanta liquidez dispõe para antecipar parcelas e de sua conjectura sobre o comportamento dos demais participantes do grupo. O resultado observado — quem é contemplado, quando, e a que custo — não é imposto por nenhum agente central: emerge da interação estratégica descentralizada de milhões de participantes sob um conjunto de regras fixado por norma.

Do ponto de vista da engenharia, trata-se de um mecanismo de alocação de recursos escassos operando em larga escala, com regras explícitas, restrição orçamentária dura e agentes heterogêneos que aprendem com a experiência. É exatamente a classe de sistema que a teoria de desenho de mecanismo e os métodos computacionais de simulação multiagente foram desenvolvidos para analisar.

O sistema é, além disso, densamente instrumentado. As administradoras remetem ao Banco Central, em periodicidade mensal e trimestral, informações consolidadas por grupo, por administradora, por segmento de bem e por unidade da federação, incluindo a quantidade de cotistas contemplados por lance e por sorteio, os quantitativos de desistência e os saldos das contas de recursos de consórcio. Essas informações são publicadas em formato aberto e cobrem série histórica iniciada na década de 1990 [@bcb2026consorcios]. Trata-se, portanto, de um mercado de escala nacional, regras codificadas em lei e observabilidade agregada de longo prazo — combinação incomum e que viabiliza a investigação proposta neste trabalho.
