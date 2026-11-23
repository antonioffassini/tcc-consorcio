---
secao: 2.4
titulo: Inadimplência, desistência e efeitos sobre o grupo
status: rascunho
responsavel:
insumos:
fontes:
excecoes:
  - 285
  - 30
  - 11.795
  - 9.1.6
  - 14.3
  - 35.1
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

Sob a Circular n. 3.432/2009, a assembleia geral ordinária podia determinar o cancelamento da contemplação do consorciado que, não tendo utilizado o respectivo crédito, viesse a ficar inadimplente [@bcb2009circ3432]. A Resolução BCB n. 285/2023 alterou esse tratamento: o consorciado contemplado que for excluído mantém assegurada a contemplação, com disponibilização de crédito parcial correspondente ao percentual amortizado do valor atualizado do bem, deduzidas as obrigações financeiras pendentes (art. 33). A mesma norma considera excluído o consorciado que deixe de cumprir as obrigações financeiras por três vencimentos (art. 32, II, na redação dada em dezembro de 2023) [@bcb2023res285]. No regime vigente, portanto, a exclusão do contemplado não cancela a contemplação; altera o valor do crédito a que ele tem direito.

## Exclusão e restituição

O consorciado excluído não contemplado tem direito à restituição da importância paga ao fundo comum, calculada com base no percentual amortizado do valor do bem ou serviço vigente na data da assembleia de contemplação, acrescido dos rendimentos da aplicação financeira a que estão sujeitos os recursos enquanto não utilizados [@brasil2008lei11795]. Não são restituídos os valores pagos a título de taxa de administração e de fundo de reserva, e o contrato pode prever cláusula penal por quebra contratual.

O ponto decisivo para este trabalho é o **momento** da restituição. No texto consolidado da Lei n. 11.795/2008, o art. 30 mantém apenas o caput, e o momento da devolução fica a cargo dos contratos. Os regulamentos lidos neste trabalho resolvem a questão da mesma forma: a cota excluída é restituída quando contemplada num sorteio próprio, e não no encerramento do grupo. Na maioria deles, esse sorteio é separado do sorteio das cotas ativas e realizado depois dele: a Porto Seguro contempla primeiro o consorciado ativo e depois o excluído, limitando as devoluções adicionais da mesma assembleia a uma fração do crédito de menor valor do grupo (art. 35.1) [@portoseguro2025regulamento]; o Itaú fixa a ordem sorteio de ativos, sorteio de excluídos e lance (cl. 14.3) [@itau2024condicoes]; e o Santander dedica uma seção própria à contemplação do excluído por sorteio, apenas para restituição de valores (seção 9.1.6) [@santander2026regulamento]. A Sicredi é a exceção, com ativos e excluídos concorrendo no mesmo sorteio [@sicredi2026regulamento]. O participante excluído continua, portanto, a figurar nos sorteios das assembleias subsequentes, não para receber o crédito, mas para receber de volta o que pagou.

## Consequência estrutural para a modelagem

A conjunção das regras acima produz uma característica que nenhum modelo da literatura de associações rotativas incorpora: **o conjunto de participantes que disputa os sorteios não coincide com o conjunto de participantes que pode receber crédito**. Cotas excluídas concorrem por restituição, em sorteio próprio; cotas ativas concorrem por crédito; e ambas consomem o mesmo fundo comum, cuja suficiência condiciona toda contemplação.

Em consequência, a probabilidade de contemplação de um participante ativo depende não apenas de quantos concorrentes ativos existem, mas de quantas cotas excluídas aguardam restituição — quantidade que é ela própria função da inadimplência acumulada do grupo. O sistema tem, portanto, realimentação: inadimplência gera exclusões, exclusões aumentam a demanda por recursos do fundo, o que reduz a disponibilidade para contemplações e alonga a espera dos adimplentes.

Esse acoplamento será representado explicitamente na dinâmica de transição do modelo formulado no Capítulo 4, e é uma das dimensões em que os desenhos alternativos avaliados no Capítulo 7 podem diferir do desenho vigente.
