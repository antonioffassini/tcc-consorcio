---
secao: 7.4
titulo: Comparação entre mecanismos
status: rascunho
responsavel:
insumos:
  - results/
  - ESTADO.md §4, 2026-11-19 (critérios e regra de H3) e 2026-11-22 (família M3, regra de escolha, conjuntos A e B, diagnóstico de decomposição), todos escritos antes de rodar; §5 item 34
  - src/analysis/comparacao.py, src/analysis/bloco_2211.py, src/analysis/tabelas_2211.py
fontes:
  - results/m3_decomposicao_B.csv
  - results/texto_2211_apresentacao.csv
  - results/h3_metricas_sobra_reg.csv
  - results/h3_relativas_sobra_reg.csv
  - results/h3_config_sobra_reg.csv
  - results/m3_rodada1_A.csv
  - results/m3_relativas_B.csv
  - results/h3_metricas_sobra_reg_m3B.csv
excecoes:
  - 0,05
  - 0,10
  - 0,15
  - 0,20
  - 0,25
  - 0,5
  - 1.629
paginas_alvo: 6
---

# Comparação entre mecanismos

Esta seção compara o mecanismo vigente $M_0$ com os desenhos $M_1$, $M_2$ e com a família $M_3$, no modelo calibrado na seção 7.1. Os critérios são os da seção 4.4. A regra de decisão de H3 foi registrada no log do projeto em 19 de novembro; a família $M_3$, a regra de escolha dentro dela e a separação entre amostra de escolha e amostra de avaliação foram registradas em 22 de novembro, antes de qualquer variante rodar.

## Desenho do experimento

Cada um dos 1.629 grupos do desenho calibrado (três réplicas de 543 grupos do painel) foi simulado do início ao encerramento sob cada mecanismo, com os mesmos números aleatórios: os mesmos participantes, com os mesmos tipos, e os mesmos choques de inadimplência. O destino da sobra de cada administradora vem do regulamento, quando lido, ou de um sorteio com probabilidade $\eta_0$, mantido entre mecanismos. A política de lance $\pi_\phi$ é a mesma em todos os desenhos: esta seção mede o efeito da regra com o comportamento fixo, e a seção 7.6 refaz a comparação com o lance aprendido sob cada regra.

As diferenças contra $M_0$ são pareadas por grupo e agregadas com o peso de cada grupo no painel; os intervalos de 95% vêm de um bootstrap de administradoras com 500 reamostragens. Um desenho domina $M_0$ se melhora ao menos um critério com o intervalo inteiro do lado favorável e não piora nenhum com o intervalo inteiro do lado desfavorável.

## Níveis sob o mecanismo vigente

Sob $M_0$, o bem-estar médio é 0,4901 crédito por cota; o desvio-padrão da espera, 47,28 meses, para uma espera média de 53,03 meses; o sorteio previsto falha por falta de saldo em 0,91% das assembleias; e o excluído espera, em média, 115,28 meses pela restituição (`results/h3_metricas_sobra_reg.csv`). A fração de contemplações por lance na vida inteira dos grupos é 0,7003. O nível do bem-estar é maior que o da versão anterior do modelo porque a urgência passou a ter escala financeira plausível (seção 4.2): a espera pesa menos, e a utilidade de uma contemplação tardia fica mais perto da de uma imediata.

## $M_1$ e $M_2$

**Tabela 7.7 — $M_1$ e $M_2$ contra $M_0$, em % do nível de $M_0$ (IC de 95%)**

| Desenho | Bem-estar $\mathcal{W}$ | Dispersão $\mathcal{E}$ | Instabilidade $\mathcal{S}$ | Tempo de restituição $\mathcal{R}$ | Domina? |
|---|---|---|---|---|---|
| $M_1$, $\beta=0{,}5$ | −1,10 (−1,41; −0,85) | −2,27 (−2,83; −1,70) | 0,66 (−0,36; 1,84) | −0,05 (−0,17; 0,04) | não |
| $M_1$, $\beta=1$ | −1,71 (−2,11; −1,46) | −3,77 (−4,62; −3,05) | 0,95 (0,21; 2,04) | −0,18 (−0,32; −0,06) | não |
| $M_1$, $\beta=2$ | −2,67 (−3,23; −2,11) | −5,56 (−6,84; −4,53) | 1,43 (0,55; 2,98) | −0,15 (−0,23; −0,06) | não |
| $M_2$ | 1,19 (0,96; 1,49) | 0,81 (0,71; 0,96) | −2,63 (−6,56; −0,70) | −0,06 (−0,17; 0,06) | não |

Fonte: elaborado pelos autores (`results/h3_relativas_sobra_reg.csv`). Menor é melhor em todos os critérios, exceto no bem-estar.

**$M_1$ troca bem-estar por igualdade.** O peso pela espera reduz o desvio-padrão da espera de 2,27% a 5,56%, conforme $\beta$, e reduz o bem-estar de 1,10% a 2,67%, com o intervalo inteiro do lado desfavorável. O mecanismo da perda é direto: o sorteio passa a favorecer quem entrou antes, e não quem tem mais urgência, e a vez tirada dos recém-chegados urgentes custa mais utilidade do que a dada aos antigos. O resultado é coerente com a comparação clássica entre os dois tipos de ROSCA: com participantes idênticos, o sorteio basta, e é a diferença de preferências que dá valor a um canal que ordena pela disposição a pagar [@besley1993economics].

**$M_2$ melhora bem-estar e instabilidade, mas aumenta a dispersão.** O lance de preço uniforme aumenta o bem-estar em 1,19% e reduz em 2,63% a instabilidade do fundo, ambos com o intervalo inteiro do lado favorável; mas aumenta o desvio-padrão da espera em 0,81%, com o intervalo inteiro do lado desfavorável. Pela regra registrada, não domina. A espera média cresce 1,56%: com os mesmos lances, o preço uniforme cobra menos de cada vencedor, entra menos dinheiro no fundo e menos cotas são contempladas adiante.

## Família $M_3$

A família $M_3$ parte do lance de preço uniforme e ataca o custo identificado em $M_2$: o saldo que fica parado quando o preço cai. As onze variantes combinam três instrumentos: um preço de reserva $p$ (lance mínimo), o sorteio obrigatório da sobra e um peso pequeno pela espera no sorteio (seção 4.3).

**Escolha (conjunto A).** As onze variantes foram simuladas em uma amostra de grupos e de sementes, o conjunto A. A regra registrada escolhe, entre as que dominam $M_0$, a de maior ganho de bem-estar.

**Tabela 7.8 — Família $M_3$ no conjunto A, em % do nível de $M_0$**

| Variante | $\mathcal{W}$ | $\mathcal{E}$ | $\mathcal{S}$ | $\mathcal{R}$ | Domina? |
|---|---|---|---|---|---|
| $M_3^{r}$, $p=0{,}05$ | −1,94 | 10,60 | −2,23 | −0,69 | não |
| $M_3^{r}$, $p=0{,}10$ | −8,81 | 11,78 | −4,98 | −1,05 | não |
| $M_3^{r}$, $p=0{,}15$ | −14,14 | 8,37 | −6,82 | −1,23 | não |
| $M_3^{r}$, $p=0{,}20$ | −16,96 | 5,37 | −11,37 | −1,15 | não |
| $M_3^{s}$ | 1,42 | −0,52 | −2,28 | −0,10 | sim |
| $M_3^{rs}$, $p=0{,}05$ | 1,49 | −0,90 | −2,23 | −0,14 | sim |
| $M_3^{rs}$, $p=0{,}10$ | 0,28 | −3,85 | −4,98 | 0,00 | sim |
| $M_3^{rs}$, $p=0{,}15$ | −1,10 | −5,77 | −6,82 | −0,27 | não |
| $M_3^{rs}$, $p=0{,}20$ | −1,96 | −6,76 | −11,37 | −0,20 | não |
| $M_3^{e}$, $\beta=0{,}1$ | 0,99 | 0,42 | −3,69 | −0,12 | não |
| $M_3^{e}$, $\beta=0{,}25$ | 0,53 | −0,39 | −2,81 | −0,19 | sim |

Fonte: elaborado pelos autores (`results/m3_rodada1_A.csv`). "Domina?" segue a regra do intervalo; a tabela mostra só as estimativas pontuais.

Dois padrões aparecem. O preço de reserva sozinho piora tudo o que importa ao participante: com lance mínimo e sem destino para o saldo que sobra, o dinheiro fica parado no fundo, a espera cresce e a dispersão dispara. O mesmo preço de reserva, combinado com o sorteio obrigatório da sobra, passa a ajudar, porque o saldo que o leilão não usa vai a sorteio na mesma assembleia. Quatro variantes dominam $M_0$; a regra escolhe $M_3^{rs}(0{,}05)$, com o maior ganho de bem-estar entre elas.

**Avaliação (conjunto B).** A variante escolhida foi avaliada em três amostras novas de grupos e de sementes, nunca usadas na escolha.

**Tabela 7.9 — $M_2$ e $M_3^{rs}(0{,}05)$ contra $M_0$ no conjunto B, em % do nível de $M_0$ (IC de 95%)**

| Desenho | $\mathcal{W}$ | $\mathcal{E}$ | $\mathcal{S}$ | $\mathcal{R}$ | Domina? |
|---|---|---|---|---|---|
| $M_2$ | 1,17 (0,98; 1,31) | 0,80 (0,60; 1,01) | −3,24 (−8,02; −1,20) | −0,16 (−0,39; 0,12) | não |
| $M_3^{rs}(0{,}05)$ | 1,28 (1,15; 1,39) | −0,08 (−0,56; 0,23) | −3,30 (−8,08; −1,24) | −0,14 (−0,35; 0,11) | **sim** |

Fonte: elaborado pelos autores (`results/m3_relativas_B.csv`).

Em amostras independentes, $M_3^{rs}(0{,}05)$ melhora o bem-estar em 1,28% e a instabilidade em 3,30%, ambos com o intervalo inteiro do lado favorável, e não piora a dispersão nem o tempo de restituição: domina $M_0$ pela regra registrada. $M_2$ repete o padrão do conjunto A.

**O que o ganho custa fora dos critérios.** Dois efeitos não entram na regra e precisam ser ditos. A espera média sobe 1,85% (`results/m3_relativas_B.csv`): o desenho troca um pouco de espera média por mais bem-estar, porque contempla mais cedo quem tem mais urgência. E a fração das contemplações feitas por lance cai de 0,6895 para 0,4378 (`results/h3_metricas_sobra_reg_m3B.csv`): com o lance mínimo, parte dos ofertantes de lance baixo sai do leilão, e o saldo correspondente vai ao sorteio da sobra. Um regulador que acompanhe a fração de lance como indicador de funcionamento do mercado veria uma mudança grande nesse número, sem que ela signifique pior alocação.

## De onde vem o ganho

Dois dos três instrumentos de $M_3^{rs}(0{,}05)$ já existem no mercado: o lance mínimo e o sorteio da sobra. Para saber se o ganho vem deles ou do preço uniforme, que nenhum contrato lido adota, dois desenhos de diagnóstico foram simulados no conjunto B, com o lance pago pelo próprio valor de $M_0$: $D_1$, que acrescenta a $M_0$ o sorteio obrigatório da sobra, e $D_2$, que acrescenta também o lance mínimo de 0,05. Os dois foram registrados antes de rodar, fora da família e sem papel na escolha.

**Tabela 7.10 — Decomposição do ganho de $M_3^{rs}(0{,}05)$, conjunto B, em % do nível de $M_0$ (IC de 95%)**

| Desenho | Preço do lance | Lance mínimo | Sobra obrigatória | $\mathcal{W}$ | $\mathcal{E}$ | $\mathcal{S}$ | Domina? |
|---|---|---|---|---|---|---|---|
| $D_1$ | próprio lance | não | sim | 0,07 (0,03; 0,13) | −0,50 (−0,91; −0,21) | 0,00 | não |
| $D_2$ | próprio lance | sim | sim | 0,26 (0,17; 0,33) | −1,00 (−1,46; −0,69) | −0,22 (−0,75; −0,04) | sim |
| $M_2$ | uniforme | não | não | 1,17 (0,98; 1,31) | 0,80 (0,60; 1,01) | −3,24 (−8,02; −1,20) | não |
| $M_3^{rs}(0{,}05)$ | uniforme | sim | sim | 1,28 (1,15; 1,39) | −0,08 (−0,56; 0,23) | −3,30 (−8,08; −1,24) | sim |

Fonte: elaborado pelos autores (`results/m3_decomposicao_B.csv`). $D_1$ não domina porque aumenta o tempo de restituição em 0,01%, com o intervalo inteiro do lado desfavorável.

Generalizar as práticas de mercado já ajuda: $D_2$ domina $M_0$. O que ele entrega, porém, é sobretudo menos dispersão da espera; o ganho de bem-estar é de 0,26%, e o de estabilidade, de 0,22%. O preço uniforme responde pela maior parte do ganho de $M_3^{rs}(0{,}05)$: cerca de um ponto percentual dos 1,28 de bem-estar e quase toda a redução da instabilidade. Sozinho, porém, ele não domina, porque aumenta a dispersão. Os dois instrumentos já praticados no mercado são o que torna o preço uniforme aceitável pela regra: com eles, a piora na dispersão desaparece. A contribuição do desenho está na combinação, e o seu componente novo é o preço uniforme.

A comparação desta seção mantém a política de lance fixa. Sob preço uniforme, a melhor resposta de cada participante muda, e o ganho de $M_2$ e de $M_3$ vem em parte de cobrar menos pelo mesmo lance; a seção 7.6 verifica se a ordenação sobrevive quando o lance se adapta.
