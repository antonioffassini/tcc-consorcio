---
secao: 2.4
titulo: Inadimplência, desistência e efeitos sobre o grupo
status: rascunho
responsavel:
insumos:
fontes:
excecoes:
  - 11795
  - 3.432
paginas_alvo: 3
---

# Inadimplência, desistência e efeitos sobre o grupo

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
