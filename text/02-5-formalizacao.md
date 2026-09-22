---
secao: 2.5
titulo: O consórcio como jogo dinâmico de alocação
status: rascunho
responsavel:
insumos:
fontes:
excecoes:
paginas_alvo: 3
---

# O consórcio como jogo dinâmico de alocação

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
