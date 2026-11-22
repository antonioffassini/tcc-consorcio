---
secao: 7.2
titulo: Testes de sobre-identificação
status: rascunho
responsavel:
insumos:
  - results/
  - ESTADO.md §4, 2026-11-16 (regra de H2) e 2026-11-19 (revisão; contaminação declarada); §5 itens 21, 24 e 28
fontes:
  - results/h2_teste.csv
  - results/arquivo_2026-11-16/h2_teste.csv
  - results/versoes_modelo.csv
excecoes:
  - 5,99
  - 2,24
  - 1,96
paginas_alvo: 3
---

# Testes de sobre-identificação

A hipótese H2 afirma que o modelo calibrado só nos agregados publicados reproduz momentos que não foram usados na calibração. Esta seção aplica o teste da seção 6.5, com a regra registrada antes do resultado, ao modelo revisado e à versão de 16 de novembro.

## Resultado no modelo revisado

**Tabela 7.4 — Teste de H2 no modelo revisado**

| Momento de teste | Dado | Simulado | Diferença | Erro-padrão total | Razão |
|---|---|---|---|---|---|
| Spearman lance × tamanho | 0,3161 | 0,5320 | 0,2159 | 0,1411 | 1,53 |
| Meses sem contemplação | 0,0663 | 0,0531 | −0,0132 | 0,0226 | −0,58 |
| Wald conjunto, $J$ | | | | | 2,563 |

Fonte: `results/h2_teste.csv`. O valor-p de $J$ na qui-quadrado com dois graus de liberdade é 0,278.

Pela regra registrada, H2 não é rejeitada: $J$ = 2,563, abaixo de 5,99, e nenhuma razão individual passa do limiar de Bonferroni de 2,24. A regra secundária, só com o Spearman, também não rejeita (razão de 1,53, abaixo de 1,96), e o Spearman simulado tem o mesmo sinal do dado. As três partes da regra concordam.

O resultado tem leitura qualitativa clara. O modelo gera, sem que isso tenha sido imposto, uma relação positiva entre o tamanho dos grupos da administradora e a fração de contemplações por lance, pela mecânica descrita na seção 5.3: com um sorteio previsto por assembleia, o saldo que sobra para o lance cresce com a arrecadação, e a arrecadação cresce com o tamanho do grupo. O modelo exagera essa relação, com correlação de 0,5320 contra 0,3161. Na fração de meses sem contemplação, o modelo fica abaixo do dado, mas a diferença é pequena perto do erro.

## O que o teste consegue ver

Não rejeitar não confirma o modelo, e o teste tem pouco poder. A menor diferença no Spearman que ele detectaria com probabilidade de 80% é 0,3952, maior que o próprio valor observado da correlação; na fração sem contemplação, 0,0633, quase igual ao valor observado (`results/h2_teste.csv`). A maior parte da incerteza vem do dado: o erro-padrão do Spearman no bootstrap de administradoras é 0,1402, contra 0,0145 da incerteza dos parâmetros e 0,0069 da simulação. Com cerca de cinquenta administradoras e sete trimestres, uma correlação entre administradoras é medida com imprecisão grande, e nenhum modelo seria rejeitado por um erro de correlação menor que essa diferença detectável.

O teste é, portanto, capaz de rejeitar um modelo que inverta o sinal da relação ou que a anule com folga, e é isso que ele faz bem. Não é capaz de distinguir modelos que acertem o sinal e a ordem de grandeza.

## A versão de 16 de novembro

**Tabela 7.5 — Teste de H2 nas duas versões calibradas**

| | Modelo de 16/11 | Modelo revisado |
|---|---|---|
| Spearman simulado (dado: 0,3161) | 0,0212 | 0,5320 |
| Razão no Spearman | −1,78 | 1,53 |
| Meses sem contemplação simulado (dado: 0,0663) | 0,0398 | 0,0531 |
| Razão nos meses sem contemplação | −1,21 | −0,58 |
| $J$ | 4,671 | 2,563 |
| Valor-p | 0,0967 | 0,278 |

Fontes: `results/arquivo_2026-11-16/h2_teste.csv`, `results/h2_teste.csv`.

A versão de 16 de novembro também não era rejeitada pela regra formal. A não rejeição, porém, vinha da incerteza, e não da proximidade: o Spearman simulado de 0,0212 era quase nulo, e a razão de −1,78 ficava perto do limiar da regra secundária. O teste formal não rejeitava, mas o resultado dizia algo que o teste não captura, a saber, que o modelo não reproduzia a relação que se pretendia explicar pela mecânica do fundo. Foi esse resultado que levou à revisão descrita na seção 7.1.

## O peso da segunda rodada

Os dois testes não valem o mesmo. O primeiro é cego: a regra foi escrita antes, e o modelo não havia sido ajustado para os momentos de teste. O segundo não é: a revisão do modelo foi motivada pelos regulamentos, mas feita depois de visto o primeiro resultado, e não se pode descartar que a escolha entre as revisões possíveis tenha sido influenciada pelo que se sabia sobre o Spearman. Duas circunstâncias reduzem, sem eliminar, esse problema. A revisão mudou a regra de vagas e de restituição para a que os contratos descrevem, e não para uma forma escolhida pelo ajuste; e o Spearman do modelo revisado excede o dado, o que não seria o resultado de um ajuste dirigido ao momento. Ainda assim, o $J$ do modelo revisado deve ser lido como diagnóstico de adequação, e não como teste independente.

A fração de meses sem contemplação tem uma contaminação anterior, declarada na seção 5.4: a distância vista nesse número na primeira rodada do protótipo motivou parte das correções feitas antes da calibração. A regra secundária, só com o Spearman, existe por isso, e ela também não rejeita.

## Conclusão sobre H2

Pelo critério registrado, H2 não é rejeitada em nenhuma das duas versões. No modelo revisado, o resultado vem acompanhado de concordância qualitativa no sinal e na ordem de grandeza da relação entre tamanho e lance, que a versão anterior não tinha. O teste tem pouco poder e a segunda rodada não é cega; por isso, a afirmação que esta seção sustenta é limitada: o modelo revisado não é contraditado pelos momentos de teste disponíveis, e reproduz qualitativamente a relação estrutural que a calibração não usou. Isso basta para usá-lo na comparação entre mecanismos da seção 7.4, com a ressalva de que a validação é fraca.
