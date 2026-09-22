# MONOGRAFIA — ESQUELETO COMPLETO

> Documento de trabalho. Gerado a partir de `text/` e `docs/estrutura.tsv`.
> A versão final em `.docx` é produzida por `make docx`, com a formatação ABNT
> aplicada pelo template — **não formate este arquivo à mão**.
> Regras normativas: `docs/GUIA-ABNT.md`.

---

# ELEMENTOS PRÉ-TEXTUAIS

## Capa

ANTÔNIO FREITAS FASSINI
PEDRO FREITAS FASSINI
PEDRO PAULO TELES SILVEIRA

**[TÍTULO — PREENCHER]**

Rascunho de título: *Avaliação computacional do mecanismo de contemplação no Sistema
de Consórcios brasileiro: um modelo multiagente calibrado em dados regulatórios*

São Paulo
2026

## Folha de rosto

ANTÔNIO FREITAS FASSINI
PEDRO FREITAS FASSINI
PEDRO PAULO TELES SILVEIRA

**[TÍTULO]**

Versão Original

> Monografia apresentada à Escola Politécnica da Universidade de São Paulo para
> obtenção do título de Engenheiro.
>
> Área de Concentração: Engenharia de Computação e Sistemas Digitais
>
> Orientador: Prof. Dr. Paulo Sergio Cugnasca

São Paulo
2026

## Ficha catalográfica

*Gerada pela biblioteca da Poli. Fica no verso da folha de rosto.*

## Folha de aprovação

*Obrigatória. Modelo fornecido pela unidade.*

## Agradecimentos

*A escrever.*

## Epígrafe

*Opcional.*

## Resumo

> **Provisório.** O resumo definitivo só pode ser escrito após o congelamento dos
> resultados (Semana 11), porque a NBR 6028 exige que ele contenha objetivo, método,
> resultado e conclusão. Os marcadores abaixo são intencionais e são acusados pela
> auditoria enquanto não forem substituídos.

O Sistema de Consórcios brasileiro movimenta mais de meio trilhão de reais anuais em
créditos comercializados e conta com mais de doze milhões de participantes ativos,
alocando crédito por meio de um mecanismo — sorteio e lance — fixado por regulação e
jamais submetido a avaliação comparativa contra desenhos alternativos. Este trabalho
avalia computacionalmente a eficiência desse mecanismo. Formaliza-se o grupo de
consórcio como um jogo dinâmico de alocação com agentes heterogêneos sob restrição de
liquidez; implementa-se um ambiente de simulação com agentes de aprendizado por
reforço; e calibra-se o modelo por método de momentos simulados contra os agregados
públicos do Banco Central do Brasil, contornando a indisponibilidade de dados
individuais de lance. A validade do procedimento é estabelecida por convergência a
equilíbrios de forma fechada em configurações-limite e por teste de sobre-identificação
em momentos não utilizados na calibração. [RESULTADO PENDENTE: síntese dos achados dos
capítulos 7 e 8.] [RESULTADO PENDENTE: conclusão sobre a ordenação entre desenhos.]

**Palavras-chave:** Desenho de mecanismo; Aprendizado por reforço multiagente;
Consórcios; Teoria de leilões; Simulação computacional.

## Abstract

> *A traduzir após o fechamento do resumo em português.*

**Keywords:** Mechanism design; Multi-agent reinforcement learning; Rotating savings
and credit associations; Auction theory; Computational simulation.

## Lista de ilustrações

*Gerada automaticamente.*

## Lista de tabelas

*Gerada automaticamente.*

## Lista de abreviaturas e siglas

| Sigla | Significado |
|---|---|
| ABAC | Associação Brasileira de Administradoras de Consórcios |
| BCB | Banco Central do Brasil |
| MARL | *Multi-Agent Reinforcement Learning* — Aprendizado por Reforço Multiagente |
| ROSCA | *Rotating Savings and Credit Association* — Associação Rotativa de Poupança e Crédito |
| RL | *Reinforcement Learning* — Aprendizado por Reforço |
| SMM | *Simulated Method of Moments* — Método de Momentos Simulados |
| UF | Unidade da Federação |

*Completar conforme o texto avança. Regra: sigla entra aqui na primeira vez que é usada.*

## Lista de símbolos

*Espelha a notação canônica do `CONTEXT.md` §5. Preencher na Semana 5, quando a notação congela.*

## Sumário

**1 INTRODUÇÃO**
  - 1.1 Contexto e relevância econômica
  - 1.2 Problema de pesquisa
  - 1.3 Hipóteses
  - 1.4 Objetivos
  - 1.5 Contribuições reivindicadas
  - 1.6 Organização do trabalho
**2 FUNDAMENTOS INSTITUCIONAIS DO CONSÓRCIO**
  - 2.1 Mecânica do grupo de consórcio
  - 2.2 Contemplação por sorteio e por lance
  - 2.3 Arcabouço regulatório
  - 2.4 Inadimplência, desistência e efeitos no grupo
  - 2.5 O consórcio como jogo dinâmico de alocação
**3 REVISÃO BIBLIOGRÁFICA**
  - 3.1 Estratégia de busca
  - 3.2 ROSCAs e poupança rotativa
  - 3.3 Teoria de leilões e desenho de mecanismo
  - 3.4 Econometria estrutural com dados incompletos
  - 3.5 Aprendizado por reforço multiagente em mercados
  - 3.6 Síntese e posicionamento
**4 FORMULAÇÃO DO MODELO**
  - 4.1 Ambiente: estados, ações, transições
  - 4.2 Heterogeneidade dos participantes
  - 4.3 Regras de contemplação como mecanismo parametrizado
  - 4.4 Critérios de avaliação
  - 4.5 Escopo e simplificações
**5 BASE DE DADOS E FATOS ESTILIZADOS**
  - 5.1 Fontes de dados
  - 5.2 Pipeline de extração e consolidação
  - 5.3 Fatos estilizados
  - 5.4 Momentos-alvo para calibração
  - 5.5 Limitações dos dados
**6 METODOLOGIA COMPUTACIONAL**
  - 6.1 Arquitetura da simulação
  - 6.2 Agentes de aprendizado por reforço
  - 6.3 Calibração por Simulated Method of Moments
  - 6.4 Validação I: casos-limite com solução fechada
  - 6.5 Validação II: sobre-identificação
  - 6.6 Protocolo experimental e reprodutibilidade
**7 RESULTADOS**
  - 7.1 Ajuste aos momentos observados
  - 7.2 Testes de sobre-identificação
  - 7.3 Equilíbrio emergente vs. teoria clássica
  - 7.4 Comparação entre mecanismos
  - 7.5 Robustez da ordenação
**8 DISCUSSÃO**
  - 8.1 Implicações para o desenho regulatório
  - 8.2 Trade-offs entre critérios
  - 8.3 Ameaças à validade
**9 CONCLUSÃO E TRABALHOS FUTUROS**

**REFERÊNCIAS**
**APÊNDICE A** — Derivações analíticas dos casos-limite
**APÊNDICE B** — Dicionário de dados e tratamento
**APÊNDICE C** — Estrutura do repositório de código
**APÊNDICE D** — Tabelas completas de resultados

---

# ELEMENTOS TEXTUAIS


---

# 1 INTRODUÇÃO

## 1.1 Contexto e relevância econômica

O Sistema de Consórcios é um mecanismo de autofinanciamento coletivo regulado no Brasil pela Lei n. 11.795, de 8 de outubro de 2008, e supervisionado pelo Banco Central do Brasil [@brasil2008lei11795]. Em um grupo de consórcio, um conjunto determinado de participantes contribui mensalmente para um fundo comum destinado à aquisição de um bem ou serviço previamente especificado. A cada assembleia, o saldo disponível no fundo é alocado a uma ou mais cotas, que passam à condição de contempladas e recebem a carta de crédito correspondente. A alocação ocorre por dois canais: o sorteio, que distribui o crédito de forma aleatória entre as cotas adimplentes, e o lance, pelo qual o participante oferta a antecipação de parcelas para alterar sua posição na ordem de recebimento.

A dimensão do sistema é macroeconomicamente relevante. Em 2025 foram comercializadas 5,16 milhões de cotas, volume 15% superior às 4,49 milhões do ano anterior, correspondendo a mais de R$ 500 bilhões em créditos comercializados — alta de 32,1% sobre os R$ 378 bilhões apurados em 2024. O número de participantes ativos superou pela primeira vez a marca de doze milhões em julho de 2025, atingindo 12,74 milhões em novembro do mesmo ano, ante 11,22 milhões um ano antes, crescimento de 13,5% [@abac2026anuario]. O sistema opera, portanto, na escala de um mercado de crédito de porte nacional, com participação relevante nos segmentos de imóveis, veículos leves, motocicletas, veículos pesados, serviços e bens móveis duráveis.

Essa dimensão não é acidental. O consórcio ocupa, no orçamento das famílias e das empresas brasileiras, uma posição de substituto parcial do crédito bancário para aquisição de bens de alto valor. A ausência de juros — o custo do participante compõe-se essencialmente da taxa de administração e do fundo de reserva — torna a modalidade comparativamente mais atrativa em ambientes de política monetária restritiva, o que ajuda a explicar a expansão observada no período recente. Em contrapartida, o participante abre mão da disponibilidade imediata do bem: o crédito não é contratado, é aguardado.

Essa troca entre custo financeiro e incerteza temporal é a característica que distingue o consórcio de qualquer outro instrumento de crédito e que o converte em objeto próprio de estudo. O participante não escolhe apenas se adere ao grupo; ao longo de todo o prazo, ele decide recorrentemente se e quanto ofertar de lance, e essa decisão depende de quanto ele valoriza a antecipação do crédito, de quanta liquidez dispõe para antecipar parcelas e de sua conjectura sobre o comportamento dos demais participantes do grupo. O resultado observado — quem é contemplado, quando, e a que custo — não é imposto por nenhum agente central: emerge da interação estratégica descentralizada de milhões de participantes sob um conjunto de regras fixado por norma.

Do ponto de vista da engenharia, trata-se de um mecanismo de alocação de recursos escassos operando em larga escala, com regras explícitas, restrição orçamentária dura e agentes heterogêneos que aprendem com a experiência. É exatamente a classe de sistema que a teoria de desenho de mecanismo e os métodos computacionais de simulação multiagente foram desenvolvidos para analisar.

O sistema é, além disso, densamente instrumentado. As administradoras remetem ao Banco Central, em periodicidade mensal e trimestral, informações consolidadas por grupo, por administradora, por segmento de bem e por unidade da federação, incluindo a quantidade de cotistas contemplados por lance e por sorteio, os quantitativos de desistência e os saldos das contas de recursos de consórcio. Essas informações são publicadas em formato aberto e cobrem série histórica iniciada na década de 1990 [@bcb2026consorcios]. Trata-se, portanto, de um mercado de escala nacional, regras codificadas em lei e observabilidade agregada de longo prazo — combinação incomum e que viabiliza a investigação proposta neste trabalho.

## 1.2 Problema de pesquisa

As regras de contemplação do consórcio brasileiro não emergiram de um processo competitivo entre desenhos alternativos. Elas foram fixadas por norma e consolidadas pela Lei n. 11.795/2008, que estabelece o sorteio e o lance como os canais admissíveis de contemplação e delimita as modalidades de lance que uma administradora pode oferecer [@brasil2008lei11795]. O desenho vigente é, nesse sentido, uma escolha regulatória — e como toda escolha de mecanismo, admite a pergunta sobre sua eficiência relativa.

Essa pergunta não foi respondida. A literatura brasileira sobre consórcios concentra-se predominantemente na ótica da administradora e no problema atuarial de dimensionamento de reserva técnica e de suficiência do fundo comum. A literatura internacional sobre associações rotativas de poupança e crédito, por sua vez, examina arranjos informais e não regulados, em que o desenho da regra de alocação é endógeno ao grupo e a inadimplência é disciplinada por mecanismos sociais. Nenhum dos dois corpos trata do objeto específico deste trabalho: um mecanismo de alocação regulado, de adesão massiva e prazo longo, em que a regra é exógena aos participantes e o enforcement é contratual e supervisionado.

Há, além disso, uma dificuldade estrutural que ajuda a explicar essa lacuna. A avaliação de um mecanismo de leilão exige, no procedimento econométrico convencional, a observação dos lances individuais — quem ofertou, quanto e quando. Esse dado não é público no sistema brasileiro. O que se observa nas bases regulatórias é o resultado agregado do processo de lances: quantas cotas de cada grupo foram contempladas por lance e quantas por sorteio, em cada período. O problema, portanto, não é apenas de desenho de mecanismo; é também de identificação a partir de observação incompleta.

Deste conjunto decorre a pergunta que orienta este trabalho:

> **Em que medida o mecanismo de contemplação vigente no Sistema de Consórcios brasileiro é eficiente, sob critérios de bem-estar dos participantes e de estabilidade financeira do grupo, quando comparado a desenhos alternativos de alocação admissíveis sob a mesma restrição regulatória?**

A pergunta desdobra-se em três questões subordinadas, que estruturam o desenvolvimento:

**Q1.** Que comportamento de lance emerge quando participantes heterogêneos, diferenciados por urgência na obtenção do crédito e por capacidade de antecipar parcelas, decidem repetidamente sob as regras vigentes — e esse comportamento coincide com a previsão dos modelos clássicos de equilíbrio em leilões?

**Q2.** É possível calibrar um modelo desse comportamento de modo que ele reproduza os agregados efetivamente observados nas bases regulatórias, dispondo-se apenas de observação agregada e não de lances individuais?

**Q3.** Sob os critérios de avaliação adotados, existe desenho alternativo de contemplação que domine o desenho vigente — e, em caso afirmativo, essa dominância é robusta à incerteza remanescente na calibração?

A terceira questão contém a exigência mais severa do trabalho. Uma conclusão sobre desenho de mecanismo obtida a partir de um modelo calibrado só tem valor prescritivo se sobreviver ao fato de que os parâmetros do modelo não são conhecidos com precisão. Por essa razão, o trabalho não busca estimar a magnitude do ganho de um desenho alternativo, e sim verificar se a ordenação entre desenhos se mantém em todo o espaço de parâmetros compatível com os dados observados.

## 1.3 Hipóteses

O trabalho investiga três hipóteses. Cada uma corresponde a um procedimento experimental específico, indicado ao final de seu enunciado.

**H1 — Divergência comportamental.** O comportamento de lance que emerge de participantes que aprendem por interação repetida sob as regras vigentes difere sistematicamente da previsão de equilíbrio dos modelos estáticos de leilão de valor privado, e essa divergência é atribuível às três características do consórcio ausentes daqueles modelos: a restrição de liquidez do participante, o caráter repetido da disputa ao longo do prazo do grupo e a externalidade que cada contemplação impõe à probabilidade de contemplação dos demais. *Verificação: seção 7.3.*

**H2 — Adequação empírica do modelo.** É possível calibrar o modelo de comportamento por método de momentos simulados, utilizando exclusivamente os agregados publicados pelo regulador, de modo que o modelo reproduza momentos não empregados no procedimento de calibração — em particular a variação da fração de contemplações por lance entre grupos de tamanhos, prazos e segmentos distintos. *Verificação: seções 7.1 e 7.2.*

**H3 — Dominância de desenho alternativo.** Existe ao menos um desenho alternativo de contemplação, admissível sob as restrições da regulação vigente, que domina o desenho atual em pelo menos um dos critérios de avaliação adotados sem deteriorar os demais; e essa ordenação entre desenhos é robusta a toda a incerteza de calibração compatível com os dados observados. *Verificação: seções 7.4 e 7.5.*

As três hipóteses são falseáveis nos termos em que estão enunciadas. A rejeição de H2 invalida o uso do modelo para fins prescritivos e, por consequência, retira sustentação a qualquer conclusão derivada de H3 — razão pela qual o procedimento de validação antecede, no desenvolvimento, a comparação entre desenhos.

## 1.4 Objetivos

## Objetivo geral

Avaliar computacionalmente a eficiência do mecanismo de contemplação vigente no Sistema de Consórcios brasileiro, mediante a construção de um modelo multiagente calibrado em dados regulatórios públicos, e compará-lo a desenhos alternativos de alocação sob critérios explícitos de bem-estar dos participantes e de estabilidade financeira do grupo.

## Objetivos específicos

a) Construir, a partir das bases públicas do Banco Central do Brasil, um painel consolidado de grupos de consórcio, documentando o tratamento das descontinuidades de leiaute e emitindo relatório de qualidade da série;

b) Caracterizar os fatos estilizados do sistema, com ênfase na repartição entre contemplações por sorteio e por lance e em sua variação segundo tamanho de grupo, prazo, segmento de bem e período;

c) Formalizar o grupo de consórcio como um jogo dinâmico de alocação com agentes heterogêneos sob restrição de liquidez, explicitando o espaço de estados, o conjunto de ações, a dinâmica de transição e as funções-objetivo;

d) Implementar um ambiente de simulação e agentes de aprendizado por reforço capazes de aproximar políticas de lance sob esse jogo;

e) Validar o procedimento de solução mediante convergência aos equilíbrios de forma fechada conhecidos em configurações-limite do modelo;

f) Calibrar o modelo por método de momentos simulados contra os agregados observados e submetê-lo a teste de sobre-identificação em momentos não utilizados na calibração;

g) Comparar o desenho vigente a desenhos alternativos de contemplação sob os critérios adotados, verificando a robustez da ordenação resultante ao espaço de parâmetros compatível com os dados.

Os objetivos específicos (a) e (b) correspondem ao Capítulo 5; (c) ao Capítulo 4; (d), (e) e (f) ao Capítulo 6; e (g) ao Capítulo 7.

## 1.5 Contribuições reivindicadas

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** O que é novo. Escrever por último, revisar ao fim.
> **Insumos:** nenhum · **Páginas-alvo:** 1

## 1.6 Organização do trabalho

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Mapa dos capítulos.
> **Insumos:** esqueleto fechado · **Páginas-alvo:** 1


---

# 2 FUNDAMENTOS INSTITUCIONAIS DO CONSÓRCIO

## 2.1 Mecânica do grupo de consórcio

O grupo de consórcio é, nos termos da Lei n. 11.795/2008, uma sociedade de fato constituída na data da realização da primeira assembleia geral ordinária, formada por consorciados reunidos pela administradora e dotada de prazo de duração determinado [@brasil2008lei11795]. A administradora não é parte do grupo: é prestadora de serviços com a função de gestora dos negócios do grupo, nos termos do contrato, e o representa ativa e passivamente, em juízo e fora dele. Essa separação é relevante para a formalização adotada neste trabalho, porque implica que os recursos administrados não pertencem à administradora e que o resultado do grupo não é receita dela.

Cada participante adere a uma **cota**, à qual corresponde um crédito de referência — o valor do bem, conjunto de bens ou serviço a que o contrato está vinculado. A prestação mensal do consorciado decompõe-se em três parcelas de natureza distinta: a contribuição ao fundo comum, a taxa de administração devida à administradora, e, quando previsto em contrato, a contribuição ao fundo de reserva. Apenas a primeira compõe o recurso destinado à atribuição de créditos.

O **fundo comum** é constituído pelo montante de recursos representados pelas prestações pagas pelos consorciados para essa finalidade, pelos valores correspondentes a multas e juros moratórios destinados ao grupo, e pelos rendimentos provenientes de sua aplicação financeira. Os recursos dos grupos, coletados pela administradora a qualquer tempo, devem ser depositados em instituição financeira e aplicados enquanto não utilizados. Duas consequências decorrem daí e serão incorporadas ao modelo: o fundo comum é remunerado, de modo que a espera não é financeiramente neutra; e a inadimplência de um participante reduz diretamente o recurso disponível para contemplar os demais.

A **assembleia geral ordinária** é o evento periódico em que a contemplação ocorre. É nela que se apura o saldo disponível, se realizam o sorteio e a apuração dos lances, e se define quais cotas passam à condição de contempladas. O crédito a que faz jus o consorciado contemplado é o valor equivalente ao do bem ou serviço indicado no contrato **vigente na data da assembleia geral ordinária de contemplação**, acrescido dos rendimentos líquidos financeiros proporcionais ao período em que ficar aplicado, entre a data em que colocado à disposição e a data de sua utilização.

Essa regra de determinação do crédito tem implicação econômica direta. Como o crédito é fixado pelo valor do bem vigente na data da contemplação, e não na data da adesão, o consorciado está protegido contra a variação de preço do bem durante a espera — mas, em contrapartida, sua prestação também é reajustada ao longo do plano. O consórcio, portanto, não é um contrato a preço fixo com pagamento diferido: é um contrato de valor indexado ao preço do bem, em que o participante troca custo financeiro por incerteza sobre o momento de recebimento.

O grupo tem prazo determinado e encerramento regulado. Dentro de sessenta dias contados da última assembleia de contemplação, a administradora deve comunicar os consorciados nas situações previstas em lei; o encerramento do grupo deve ocorrer no prazo máximo de cento e vinte dias contados dessa mesma assembleia, e desde que decorridos ao menos trinta dias da comunicação, ocasião em que se procede à prestação de contas definitiva, discriminando as disponibilidades remanescentes dos consorciados e participantes excluídos e os valores pendentes de recebimento objeto de cobrança judicial. Valores recuperados posteriormente são rateados proporcionalmente entre os beneficiários.

A finitude do grupo é característica estrutural, não detalhe administrativo. Ela implica que o problema de decisão do participante é de horizonte finito e que o valor da opção de esperar decresce à medida que o prazo se esgota — todo consorciado adimplente será contemplado até o encerramento. O que está em disputa não é *se* o participante recebe o crédito, mas *quando*.

## 2.2 Contemplação por sorteio e por lance

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

## 2.3 Arcabouço regulatório

Esta seção delimita o conjunto de regras que restringe o espaço de mecanismos admissíveis. O objetivo não é análise jurídica do sistema de consórcios, mas a identificação precisa da fronteira dentro da qual desenhos alternativos de contemplação podem ser propostos no Capítulo 7. Um mecanismo que exija alteração legal e um mecanismo implementável por norma infralegal não têm o mesmo estatuto prescritivo, e o trabalho precisa distingui-los.

## Hierarquia normativa

A **Lei n. 11.795, de 8 de outubro de 2008**, dispõe sobre o Sistema de Consórcio e constitui o topo do arcabouço [@brasil2008lei11795]. Ela define os conceitos básicos do sistema, estabelece que os interesses do grupo prevalecem sobre os de um consorciado individual, exige a separação entre os recursos e o patrimônio da administradora e os dos grupos, e fixa as regras de responsabilização dos administradores. É a lei que estabelece o sorteio e o lance como canais de contemplação e que condiciona a contemplação à suficiência de recursos.

No plano infralegal, a **Circular BCB n. 3.432, de 3 de fevereiro de 2009**, regulamentou a constituição e o funcionamento dos grupos de consórcio, disciplinando a precedência entre sorteio e lance, o lance embutido, a formação de grupos com créditos diferenciados e o cancelamento de contemplação em caso de inadimplência [@bcb2009circ3432]. Ao longo de sua vigência foi alterada por normas posteriores, entre elas a Circular n. 3.785, de 2016, que incluiu obrigações de guarda de documentação, e a Circular n. 4.009, de 2020, que flexibilizou temporariamente regras de constituição de grupos durante a pandemia de covid-19.

A **Resolução BCB n. 285, de 19 de janeiro de 2023**, revogou integralmente a Circular n. 3.432/2009, com efeitos a partir de 1º de janeiro de 2024 [@bcb2023res285]. Entre as alterações, eliminou a exigência de registro dos regulamentos de funcionamento em cartório de registro de títulos e documentos, revisou o conteúdo mínimo obrigatório do contrato de participação, determinou a disponibilização dos contratos padrão em meio eletrônico com histórico de alterações, e estabeleceu que a taxa de administração seja cobrada de forma proporcional aos meses de duração do plano, mediante percentual fixo, com hipóteses restritas de antecipação.

## Implicação metodológica: uma quebra de regime em 2024

A sucessão normativa não é apenas contexto. O painel construído no Capítulo 5 cobre série histórica que atravessa pelo menos três regimes: o anterior à Lei n. 11.795/2008, o da Circular n. 3.432/2009, e o da Resolução BCB n. 285/2023, vigente desde janeiro de 2024. Alterações em regras de constituição de grupo, de cobrança de taxa de administração e de conteúdo contratual afetam tanto o comportamento dos participantes quanto o significado das séries publicadas.

Duas providências decorrem disso e serão adotadas: o tratamento explícito das datas de mudança de regime como possíveis quebras estruturais na série, documentado no Capítulo 5; e a verificação, item a item, de quais das regras descritas na seção 2.2 foram preservadas na Resolução BCB n. 285/2023, uma vez que apenas as regras vigentes podem sustentar conclusões prescritivas.

## Fronteira do espaço de mecanismos

Do conjunto normativo depreende-se a seguinte delimitação, adotada como restrição no Capítulo 4:

a) A contemplação por sorteio e por lance está estabelecida em lei. Um desenho alternativo que suprima qualquer dos dois canais exige alteração legal e, portanto, tem estatuto prescritivo mais fraco;

b) O condicionamento da contemplação à suficiência de recursos é legal e não pode ser relaxado por desenho alternativo;

c) As regras de apuração do lance — modalidades admitidas, critério de desempate, precedência entre canais, tratamento do lance embutido — situam-se em norma infralegal e em contrato. **É neste espaço que residem os desenhos alternativos comparáveis**, e é a ele que o Capítulo 7 se restringe;

d) A prevalência do interesse do grupo sobre o interesse individual, princípio expresso na lei, é o fundamento normativo que legitima adotar o bem-estar agregado dos participantes e a estabilidade do fundo como critérios de avaliação, e não o resultado individual de um consorciado.

## 2.4 Inadimplência, desistência e efeitos no grupo

O tratamento das saídas é o ponto em que o consórcio mais se afasta dos arranjos informais estudados na literatura internacional. Em uma associação rotativa de poupança e crédito tradicional, a saída de um participante é disciplinada por mecanismos sociais e frequentemente implica a dissolução ou reconfiguração do grupo. No consórcio regulado, a saída é um evento contratual previsto, com consequências financeiras codificadas e efeito mensurável sobre os participantes remanescentes.

## Efeito imediato sobre o fundo

O consorciado inadimplente deixa de contribuir ao fundo comum e não concorre nas contemplações enquanto perdurar o atraso. O efeito é duplo e opera em sentidos opostos: reduz o saldo disponível, diminuindo o número de contemplações possíveis na assembleia; e reduz o número de concorrentes habilitados, aumentando a probabilidade de contemplação de cada participante adimplente remanescente.

Qual dos dois efeitos domina não é evidente a priori e depende do tamanho do grupo, do estágio do plano e da magnitude da inadimplência. Essa ambiguidade é uma das razões pelas quais a avaliação do mecanismo exige simulação: o sinal do efeito líquido da inadimplência sobre o bem-estar do participante adimplente não se obtém por inspeção.

Multas e juros moratórios a cargo do consorciado, quando previstos em contrato, são destinados ao grupo e à administradora, não podendo o contrato estipular para o grupo percentual inferior a cinquenta por cento [@brasil2008lei11795]. Parte do custo da inadimplência é, portanto, revertida ao próprio fundo.

Sob a Circular n. 3.432/2009, a assembleia geral ordinária podia determinar o cancelamento da contemplação do consorciado que, não tendo utilizado o respectivo crédito, viesse a ficar inadimplente [@bcb2009circ3432]. A contemplação não é, assim, um estado irreversível: existe um mecanismo de reversão que devolve o crédito ao fundo.

## Exclusão e restituição

O consorciado excluído não contemplado tem direito à restituição da importância paga ao fundo comum, calculada com base no percentual amortizado do valor do bem ou serviço vigente na data da assembleia de contemplação, acrescido dos rendimentos da aplicação financeira a que estão sujeitos os recursos enquanto não utilizados [@brasil2008lei11795]. Não são restituídos os valores pagos a título de taxa de administração e de fundo de reserva, e o contrato pode prever cláusula penal por quebra contratual.

O ponto decisivo para este trabalho é o **momento** da restituição. A restituição ao excluído não é imediata: o entendimento consolidado na jurisprudência sobre os artigos 22 e 30 da lei é o de que a devolução ocorre mediante contemplação da cota excluída em sorteio, ou no encerramento do grupo, o que ocorrer primeiro. O participante excluído continua, portanto, a figurar nos sorteios das assembleias subsequentes — não para receber o crédito, mas para receber de volta o que pagou.

> **Pendência de verificação.** O art. 30 da Lei n. 11.795/2008 foi objeto de veto parcial, e há discussão sobre a compatibilidade do condicionamento da restituição com o Código de Defesa do Consumidor. É necessário consultar o texto consolidado da lei e a jurisprudência mais recente antes de fixar essa regra no modelo. A modelagem do Capítulo 4 deve tratar o mecanismo de restituição como parametrizado, e não como constante.

## Consequência estrutural para a modelagem

A conjunção das regras acima produz uma característica que nenhum modelo da literatura de associações rotativas incorpora: **o conjunto de participantes que disputa o sorteio não coincide com o conjunto de participantes que pode receber crédito**. Cotas excluídas concorrem por restituição; cotas ativas concorrem por crédito; e ambas consomem o mesmo fundo comum, cuja suficiência condiciona toda contemplação.

Em consequência, a probabilidade de contemplação de um participante ativo depende não apenas de quantos concorrentes ativos existem, mas de quantas cotas excluídas aguardam restituição — quantidade que é ela própria função da inadimplência acumulada do grupo. O sistema tem, portanto, realimentação: inadimplência gera exclusões, exclusões aumentam a demanda por recursos do fundo, o que reduz a disponibilidade para contemplações e alonga a espera dos adimplentes.

Esse acoplamento será representado explicitamente na dinâmica de transição do modelo formulado no Capítulo 4, e é uma das dimensões em que os desenhos alternativos avaliados no Capítulo 7 podem diferir do desenho vigente.

## 2.5 O consórcio como jogo dinâmico de alocação

As seções anteriores descreveram o consórcio em linguagem institucional. Esta seção reorganiza a mesma descrição em linguagem de teoria dos jogos, sem ainda introduzir notação formal — reservada ao Capítulo 4 —, com o propósito de tornar explícito por que o objeto exige tratamento computacional.

## Os elementos do jogo

**Jogadores.** Os consorciados de um grupo, em número determinado e heterogêneos em duas dimensões relevantes: a urgência com que valorizam a antecipação do crédito e a liquidez de que dispõem para ofertar lances. Ambas são informação privada de cada participante.

**Horizonte.** Finito e conhecido, correspondente ao prazo de duração do grupo. Todo participante adimplente é contemplado até o encerramento; a disputa é sobre o momento, não sobre o acesso.

**Ações.** A cada assembleia, o participante ativo e adimplente escolhe se oferta lance e, em caso afirmativo, de que magnitude e por qual modalidade — em particular, se contra sua liquidez corrente ou contra o próprio crédito, no caso do lance embutido. Não ofertar é uma ação, e corresponde a aguardar o sorteio.

**Regra de alocação.** Sorteio entre as cotas habilitadas e apuração dos lances, condicionados ambos à suficiência de recursos do fundo comum e sujeitos à precedência descrita na seção 2.2.

**Estado.** Compreende ao menos: o saldo do fundo comum, o número de cotas ativas adimplentes, o número de cotas contempladas até o momento, o número de cotas excluídas aguardando restituição, o período corrente e a posição individual de cada participante.

**Pagamento.** Para o participante, o valor do crédito recebido, descontado pelo tempo de espera segundo sua urgência, líquido do lance efetivamente pago.

## As quatro características que impedem a solução analítica

Cada uma das características abaixo, isoladamente, já dificulta a obtenção de equilíbrio em forma fechada; em conjunto, a inviabilizam para grupos de tamanho realista.

**Prêmio de oferta estocástica.** O número de contemplações por assembleia é endógeno ao saldo do fundo, que por sua vez depende da adimplência agregada. O participante disputa um número incerto de vagas, e não um prêmio único.

**Restrição de liquidez com duas tecnologias.** A capacidade de ofertar é limitada, mas o lance embutido oferece uma via alternativa com custo de oportunidade distinto. A escolha de modalidade é parte da estratégia.

**Repetição com população decrescente.** Cada contemplação retira um concorrente da disputa e altera a distribuição de tipos entre os remanescentes. O jogo da assembleia seguinte não é o mesmo da anterior, e a inferência sobre os tipos dos concorrentes evolui ao longo do plano.

**Realimentação por exclusão.** Inadimplência e exclusão alteram simultaneamente o número de concorrentes e a disponibilidade de recursos, em sentidos opostos, com efeito líquido dependente do estado.

## Consequência

O objeto é um jogo bayesiano dinâmico, de horizonte finito, com informação privada bidimensional, restrição orçamentária, população variável e prêmio de oferta endógena. Os modelos analíticos disponíveis na literatura de associações rotativas de poupança e crédito, revistos no Capítulo 3, obtêm resultados sob simplificações que removem ao menos duas dessas quatro características — tipicamente, assumindo prêmio único por período e ausência de restrição de liquidez.

Duas rotas se abrem a partir daí. A primeira é preservar a solução analítica e aceitar as simplificações, com o risco de que a conclusão sobre eficiência do mecanismo seja consequência delas. A segunda é preservar as características institucionais e obter a solução por métodos computacionais, aceitando que o resultado seja aproximado e exigindo, em contrapartida, validação explícita do procedimento de aproximação.

Este trabalho adota a segunda rota. A escolha impõe um ônus que o Capítulo 6 assume integralmente: demonstrar que o método de solução recupera os equilíbrios conhecidos nas configurações-limite em que a literatura dispõe de forma fechada, antes de aplicá-lo às configurações em que não dispõe.


---

# 3 REVISÃO BIBLIOGRÁFICA

## 3.1 Estratégia de busca

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Bases, strings, critérios de inclusão/exclusão, PRISMA simplificado.
> **Insumos:** log de buscas · **Páginas-alvo:** 2

## 3.2 ROSCAs e poupança rotativa

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Literatura internacional. Posicionar consórcio como caso regulado.
> **Insumos:** PDFs fichados · **Páginas-alvo:** 4

## 3.3 Teoria de leilões e desenho de mecanismo

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Fundamentos que o cap. 4 usa. NÃO é survey exaustivo.
> **Insumos:** PDFs fichados · **Páginas-alvo:** 5

## 3.4 Econometria estrutural com dados incompletos

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Identificação sem observar todos os lances. Base do 6.3.
> **Insumos:** PDFs fichados · **Páginas-alvo:** 4

## 3.5 Aprendizado por reforço multiagente em mercados

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Métodos e precedentes de uso econômico.
> **Insumos:** PDFs fichados · **Páginas-alvo:** 4

## 3.6 Síntese e posicionamento

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** A lacuna. Tabela comparativa dos trabalhos vizinhos.
> **Insumos:** seções 3.2-3.5 · **Páginas-alvo:** 3


---

# 4 FORMULAÇÃO DO MODELO

## 4.1 Ambiente: estados, ações, transições

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Formalização completa. Toda a notação do CONTEXT seção 5.
> **Insumos:** decisões do log · **Páginas-alvo:** 5

## 4.2 Heterogeneidade dos participantes

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Urgência, liquidez, custo de capital. Distribuições paramétricas.
> **Insumos:** decisões do log · **Páginas-alvo:** 3

## 4.3 Regras de contemplação como mecanismo parametrizado

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** O vigente e as alternativas, sob uma parametrização comum.
> **Insumos:** decisões do log · **Páginas-alvo:** 4

## 4.4 Critérios de avaliação

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Bem-estar, estabilidade do fundo, objetivo prudencial. Trade-offs explícitos.
> **Insumos:** decisões do log · **Páginas-alvo:** 3

## 4.5 Escopo e simplificações

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Toda hipótese simplificadora declarada, com efeito esperado.
> **Insumos:** CONTEXT seção 4 · **Páginas-alvo:** 2


---

# 5 BASE DE DADOS E FATOS ESTILIZADOS

## 5.1 Fontes de dados

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Bacen 4010/2080/4110, dados por UF, ABAC. Cobertura e leiaute.
> **Insumos:** data/raw · **Páginas-alvo:** 3

## 5.2 Pipeline de extração e consolidação

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Tratamento da quebra da Carta Circular 3.679/14. Reprodutibilidade.
> **Insumos:** src/pipeline · **Páginas-alvo:** 4

## 5.3 Fatos estilizados

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Repartição lance/sorteio, prazos, desistência. Gráficos.
> **Insumos:** results/fatos · **Páginas-alvo:** 5

## 5.4 Momentos-alvo para calibração

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Quais momentos, por quê, e quais ficam de fora para sobre-identificar.
> **Insumos:** results/momentos · **Páginas-alvo:** 3

## 5.5 Limitações dos dados

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** O que não é observável e o que isso impede de afirmar.
> **Insumos:** nenhum · **Páginas-alvo:** 2


---

# 6 METODOLOGIA COMPUTACIONAL

## 6.1 Arquitetura da simulação

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Componentes, loop, seeds, custo computacional.
> **Insumos:** src/sim · **Páginas-alvo:** 4

## 6.2 Agentes de aprendizado por reforço

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Algoritmo, representação de estado, recompensa, treinamento.
> **Insumos:** src/agents · **Páginas-alvo:** 5

## 6.3 Calibração por Simulated Method of Moments

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Função objetivo, pesos, otimizador, erros-padrão.
> **Insumos:** src/calib · **Páginas-alvo:** 5

## 6.4 Validação I: casos-limite com solução fechada

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Marco de validação do solver.
> **Insumos:** apêndice A; results/validacao · **Páginas-alvo:** 4

## 6.5 Validação II: sobre-identificação

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Teste em momentos não usados na calibração.
> **Insumos:** results/overid · **Páginas-alvo:** 3

## 6.6 Protocolo experimental e reprodutibilidade

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Seeds, versões, comando único.
> **Insumos:** Makefile · **Páginas-alvo:** 2


---

# 7 RESULTADOS

## 7.1 Ajuste aos momentos observados

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** 
> **Insumos:** results/ · **Páginas-alvo:** 4

## 7.2 Testes de sobre-identificação

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** 
> **Insumos:** results/ · **Páginas-alvo:** 3

## 7.3 Equilíbrio emergente vs. teoria clássica

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** 
> **Insumos:** results/ · **Páginas-alvo:** 4

## 7.4 Comparação entre mecanismos

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** 
> **Insumos:** results/ · **Páginas-alvo:** 5

## 7.5 Robustez da ordenação

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** A afirmação central. Varredura do espaço de parâmetros.
> **Insumos:** results/ · **Páginas-alvo:** 4


---

# 8 DISCUSSÃO

## 8.1 Implicações para o desenho regulatório

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Prescritivo com cautela. NÃO redigir norma.
> **Insumos:** cap. 7 · **Páginas-alvo:** 3

## 8.2 Trade-offs entre critérios

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** 
> **Insumos:** cap. 7 · **Páginas-alvo:** 2

## 8.3 Ameaças à validade

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** Honesto e exaustivo. Blindagem contra a banca.
> **Insumos:** nenhum · **Páginas-alvo:** 3


---

# 9 CONCLUSÃO E TRABALHOS FUTUROS

## 9 Conclusão e trabalhos futuros

> *Não escrita. Onda de escrita em `docs/PLANO.md` §5.*
>
> **Escopo:** 
> **Insumos:** tudo · **Páginas-alvo:** 3


---

# ELEMENTOS PÓS-TEXTUAIS

## Referências

*Geradas por `make docx` a partir de `refs/refs.bib`, em ordem alfabética (NBR 6023).*

## Apêndice A — Derivações analíticas dos casos-limite
## Apêndice B — Dicionário de dados e tratamento
## Apêndice C — Estrutura do repositório de código
## Apêndice D — Tabelas completas de resultados
