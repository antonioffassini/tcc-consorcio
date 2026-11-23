---
secao: 7.2
titulo: Testes de sobre-identificação
status: rascunho
responsavel:
insumos:
  - results/
  - ESTADO.md §4, 2026-11-16 (regra de H2), 2026-11-19 (revisão; contaminação declarada) e 2026-11-22 (nova base); §5 itens 21, 24, 28 e 34
fontes:
  - results/h2_teste.csv
  - results/arquivo_2026-11-19/h2_teste.csv
  - results/arquivo_2026-11-16/h2_teste.csv
excecoes:
  - 5,99
  - 2,24
  - 1,96
paginas_alvo: 3
---

# Testes de sobre-identificação

A hipótese H2 afirma que o modelo calibrado só nos agregados publicados reproduz momentos que não foram usados na calibração. Esta seção aplica o teste da seção 6.5, com a regra registrada antes do primeiro resultado, à versão atual do modelo e às duas versões anteriores.

## Resultado na versão atual

**Tabela 7.4 — Teste de H2 na versão atual**

| Momento de teste | Dado | Simulado | Diferença | Erro-padrão total | Razão |
|---|---|---|---|---|---|
| Spearman lance × tamanho | 0,3161 | 0,5213 | 0,2053 | 0,1414 | 1,45 |
| Meses sem contemplação | 0,0663 | 0,0472 | −0,0191 | 0,0175 | −1,09 |
| Wald conjunto, $J$ | | | | | 3,119 |

Fonte: elaborado pelos autores (`results/h2_teste.csv`). O valor-p de $J$ na qui-quadrado com dois graus de liberdade é 0,210.

Pela regra registrada, H2 não é rejeitada: $J$ = 3,119, abaixo de 5,99, e nenhuma razão individual passa do limiar de Bonferroni de 2,24. A regra secundária, só com o Spearman, também não rejeita (razão de 1,45, abaixo de 1,96), e o Spearman simulado tem o mesmo sinal do dado. As três partes da regra concordam.

O modelo gera, sem que isso tenha sido imposto, uma relação positiva entre o tamanho dos grupos da administradora e a fração de contemplações por lance, pela mecânica descrita na seção 5.3: com um sorteio previsto por assembleia, o saldo que sobra para o lance cresce com a arrecadação, e a arrecadação cresce com o tamanho do grupo. O modelo exagera essa relação, com correlação de 0,5213 contra 0,3161. Na fração de meses sem contemplação, fica abaixo do dado, com diferença pequena perto do erro.

## O que o teste consegue ver

Não rejeitar não confirma o modelo, e o teste tem pouco poder. A menor diferença no Spearman que ele detectaria com probabilidade de 80% é 0,3959, maior que o próprio valor observado da correlação; na fração sem contemplação, 0,0490 (`results/h2_teste.csv`). A maior parte da incerteza vem do dado: o erro-padrão do Spearman no bootstrap de administradoras é 0,1402, contra 0,0131 da incerteza dos parâmetros e 0,0124 da simulação. Com cerca de cinquenta administradoras e sete trimestres, uma correlação entre administradoras é medida com imprecisão grande.

O teste é, portanto, capaz de rejeitar um modelo que inverta o sinal da relação ou que a anule com folga. Não é capaz de distinguir modelos que acertem o sinal e a ordem de grandeza.

## As três versões

**Tabela 7.5 — Teste de H2 nas três versões calibradas**

| | 16/11 | 19/11 | 22/11 (atual) |
|---|---|---|---|
| Spearman simulado (dado: 0,3161) | 0,0212 | 0,5320 | 0,5213 |
| Razão no Spearman | −1,78 | 1,53 | 1,45 |
| Meses sem contemplação simulado (dado: 0,0663) | 0,0398 | 0,0531 | 0,0472 |
| $J$ | 4,671 | 2,563 | 3,119 |
| Valor-p | 0,0967 | 0,278 | 0,210 |

Fontes: elaborado pelos autores (`results/arquivo_2026-11-16/h2_teste.csv`, `results/arquivo_2026-11-19/h2_teste.csv`, `results/h2_teste.csv`).

Nenhuma versão é rejeitada pela regra formal. Na de 16 de novembro, a não rejeição vinha da incerteza, e não da proximidade: o Spearman simulado era quase nulo. Foi esse resultado, junto com a leitura dos regulamentos, que levou à revisão de 19 de novembro (seção 7.1). A versão atual difere da de 19 de novembro na escala da urgência, na cláusula da sobra tirada dos regulamentos e na calibração de $\phi_1$; o resultado de H2 praticamente não muda entre as duas.

## O peso das rodadas posteriores

Os testes não valem o mesmo. Só o primeiro é cego: a regra foi escrita antes, e o modelo não havia sido ajustado para os momentos de teste. A revisão de 19 de novembro foi motivada pelos regulamentos, mas feita depois de visto o primeiro resultado, e não se pode descartar que a escolha entre as revisões possíveis tenha sido influenciada pelo que se sabia sobre o Spearman. A versão atual herda essa condição. Duas circunstâncias reduzem, sem eliminar, o problema: as revisões levaram o modelo para regras descritas nos contratos, e não para uma forma escolhida pelo ajuste; e o Spearman simulado excede o dado, o que não seria o resultado de um ajuste dirigido ao momento.

A fração de meses sem contemplação tem uma contaminação anterior, declarada na seção 5.4. A regra secundária, só com o Spearman, existe por isso, e ela também não rejeita.

## Conclusão sobre H2

Pelo critério registrado, H2 não é rejeitada em nenhuma das versões. Na atual, o resultado vem com concordância no sinal e na ordem de grandeza da relação entre tamanho e lance. O teste tem pouco poder e as rodadas posteriores à primeira não são cegas; a afirmação que esta seção sustenta é limitada: o modelo não é contraditado pelos momentos de teste disponíveis e reproduz qualitativamente a relação que a calibração não usou. Isso basta para usá-lo na comparação entre mecanismos, com a ressalva de que a validação é fraca.
