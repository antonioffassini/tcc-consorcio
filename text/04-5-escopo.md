---
secao: 4.5
titulo: Escopo e simplificações
status: rascunho
responsavel:
insumos:
  - CONTEXT seção 4
  - ESTADO.md §4 (decisões de 15/11, 16/11 e 19/11)
fontes:
  - results/parametros_fixos.csv
excecoes:
  - 285
paginas_alvo: 2
---

# Escopo e simplificações

Todo modelo deixa coisas de fora, e o que importa é saber o quê e em que direção isso pode mover as conclusões. Esta seção lista as simplificações do modelo descrito nas seções 4.1 a 4.4, separando as que delimitam o objeto das que aproximam o comportamento, e indica, quando possível, o efeito esperado de cada uma sobre a comparação entre mecanismos.

## O que fica fora do objeto

O trabalho trata apenas de grupos de imóveis no regime posterior à Resolução BCB n. 285/2023. Os demais segmentos têm prazos, tíquetes e participação de lance diferentes, e não há razão para supor que a ordenação entre mecanismos se transfira a eles sem nova calibração.

A taxa de administração e o fundo de reserva não são modelados. Ambos são cobrados como frações fixas do crédito e não dependem do mecanismo de contemplação, de modo que sua omissão desloca o nível das parcelas, mas não as diferenças entre mecanismos. A exceção é o uso do fundo de reserva para sorteios adicionais, previsto pela norma e por alguns contratos; ao omiti-lo, o modelo subestima o número de sorteios em grupos com reserva acumulada.

Não se modelam o mercado secundário de cotas, a concorrência entre administradoras nem a formação de novos grupos. A transferência de cotas contempladas poderia alterar o valor do lance para quem pretende revender a carta, efeito que o modelo não captura.

## O que é aproximado

**Política de lance fixa entre mecanismos.** É a simplificação de maior consequência. Os participantes ofertam segundo uma política paramétrica, calibrada sob o mecanismo vigente, e essa política é mantida quando o mecanismo muda. Sob $M_2$, porém, o participante racional não tem motivo para ofertar abaixo do valor que atribui à contemplação, e sob $M_1$ quem espera há mais tempo tem menos motivo para ofertar. A comparação mede, portanto, o efeito da regra sobre um comportamento dado, e não o efeito da regra quando o comportamento se ajusta a ela. É a objeção conhecida como crítica de Lucas: parâmetros de comportamento estimados sob uma regra não são, em geral, invariantes à troca de regra [CITAR: Lucas (1976), Econometric policy evaluation: a critique]. A direção do viés não é a mesma para todos os mecanismos. Em $M_2$, com ofertas mais próximas do valor, a receita de lance tende a ser maior do que a simulada, o que favoreceria $M_2$ na estabilidade do fundo. Em $M_1$, com menos lances de quem espera há mais tempo, a fração de contemplações por sorteio tende a crescer. O papel dos agentes de aprendizado por reforço na correção desse problema é tratado no Capítulo 6 [DECISÃO PENDENTE: papel do RL na comparação].

**Tipos fixos ao longo do plano.** A urgência e a liquidez de cada participante são sorteadas na entrada e não mudam. Na prática, a liquidez varia com renda e emprego, e a urgência pode surgir no meio do plano, por exemplo com a necessidade de mudar de imóvel. O efeito provável é subestimar a variação dos lances ao longo da vida do grupo.

**Inadimplência exógena.** A inadimplência que leva à exclusão segue um risco que depende apenas da idade do grupo, estimado diretamente no painel de dados (`results/parametros_fixos.csv`). Ela não depende do mecanismo. Se um mecanismo que reduz a incerteza da espera também reduz a desistência, como seria plausível, o modelo deixa de capturar esse benefício.

**Recolocação integral das vagas.** Toda vaga excluída é recolocada para um novo participante no mês seguinte. Nos dados, a reposição líquida de vagas no primeiro terço do prazo supera as exclusões (`results/parametros_fixos.csv`), e o modelo a limita a uma vaga por exclusão, porque não cria vagas novas. A simplificação é favorável ao critério de estabilidade, já que mantém constante o número de cotas pagantes.

**Contratos representativos.** As regras de sorteio de excluídas, o teto do embutido e o destino da sobra foram tirados de regulamentos de cinco administradoras (seção 4.3), não de um levantamento do mercado. O teto de restituição por assembleia e a fração de administradoras que sorteiam a sobra são calibrados, mas a forma dessas cláusulas é a observada nesses contratos. Um único sorteio de ativa por assembleia ($\kappa_g = 1$) é a regra subsidiária de um dos contratos e a mais simples compatível com os demais.

**Sem custos de transação nem de informação.** O participante conhece as regras e oferta sem custo; não há aprendizado sobre os lances vencedores anteriores. A ata de cada assembleia divulga os percentuais ofertados, e participantes reais provavelmente ajustam seus lances a essa informação.

## Leitura conjunta

As simplificações não pesam igual para os três mecanismos. A política fixa é a mais relevante para $M_2$, cuja vantagem teórica depende justamente da mudança de comportamento. As simplificações sobre inadimplência e recolocação afetam os três mecanismos da mesma forma e deslocam níveis mais do que diferenças. Os resultados do Capítulo 7 são lidos com essa assimetria em mente.
