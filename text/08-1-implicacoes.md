---
secao: 8.1
titulo: Implicações para o desenho regulatório
status: rascunho
responsavel:
insumos:
  - cap. 7
  - ESTADO.md §5 itens 34 e 35
fontes:
  - results/h5_politica/h5_robustez_resumo.csv
  - results/agentes/h5_relativas_B_s1.csv
  - results/agentes/h5_relativas_B.csv
  - results/sens_forma_relativas.csv
  - results/m3_decomposicao_B.csv
  - results/texto_2211_apresentacao.csv
  - results/m3_relativas_B.csv
  - results/h3_metricas_sobra_reg_m3B.csv
excecoes:
  - 14.5
  - 9.1
  - 0,05
  - 11.795
  - 285
  - 9.1.7.3
  - 14.5.8
  - 35.8
paginas_alvo: 3
---

# Implicações para o desenho regulatório

Esta seção traduz os resultados do Capítulo 7 em implicações para quem regula ou redige contratos de consórcio. Não propõe texto normativo: indica o que os resultados sugerem, sob quais condições e com que grau de confiança.

## O que a regulação vigente já permite

O primeiro ponto é de leitura. Todos os desenhos comparados neste trabalho foram construídos para serem admissíveis sob a Lei n. 11.795/2008 e a Resolução BCB n. 285/2023, mexendo apenas no que a norma deixa ao contrato: a forma do sorteio e as regras do lance (seção 4.3). Nenhuma das melhorias encontradas exige mudança de lei ou de resolução. Elas exigem cláusulas de contrato diferentes das hoje praticadas, que uma administradora poderia adotar por conta própria e que o regulador poderia, se quisesse, recomendar.

## O desenho proposto

No modelo calibrado e com o comportamento de lance mantido, o desenho $M_3^{rs}(0{,}05)$ domina o vigente: lance de preço uniforme, em que todos os vencedores pagam a maior oferta recusada; lance mínimo de 5% do crédito; e sorteio obrigatório do saldo que o leilão não usar. Em amostras não usadas na sua escolha, aumenta o bem-estar em 1,28% e reduz a instabilidade do fundo em 3,30%, sem piorar a dispersão da espera nem o tempo de restituição (`results/m3_relativas_B.csv`).

A lógica do desenho é mais importante que o número. O preço uniforme cobra menos de cada vencedor do que o lance pago pelo próprio valor e, com isso, aproxima o lance do consórcio do leilão que a teoria recomenda para vagas múltiplas [@vickrey1961counterspeculation] e que as associações rotativas de lance praticam informalmente [@klonner2008private]. Cobrar menos, porém, deixa saldo no fundo. O lance mínimo e o sorteio obrigatório da sobra fecham esse circuito: o primeiro evita que o preço caia a quase nada, e o segundo garante que o dinheiro que o leilão não usou seja entregue na mesma assembleia. A comparação mostra que os instrumentos não funcionam isolados: o lance mínimo sem sorteio da sobra piora o bem-estar, porque o saldo fica parado (seção 7.4).

Dois dos três instrumentos já existem no mercado. Uma das administradoras lidas exige lance mínimo de 10% do valor da cota [@santander2026regulamento, cl. 9.1.7.3], e três sorteiam a sobra quando os lances não bastam [@portoseguro2025regulamento, art. 35.8; @itau2024condicoes, cl. 14.5.8; @sicredi2026regulamento]. O que nenhum contrato lido adota é o preço uniforme. A decomposição da seção 7.4 separa os efeitos. Estender a todo o sistema as duas práticas já existentes, mantendo o lance pago pelo próprio valor, também domina o desenho vigente, mas com ganho de bem-estar de 0,26%, concentrado na redução da dispersão da espera. O preço uniforme responde pela maior parte do ganho de bem-estar e de estabilidade do desenho proposto, e as duas práticas de mercado são o que o torna aceitável, ao neutralizar o aumento da dispersão que ele causaria sozinho (`results/m3_decomposicao_B.csv`). Para o regulador, isso ordena as opções: generalizar o que o mercado já faz é um ganho pequeno e seguro; adotar também o preço uniforme é o ganho maior, que depende das outras duas peças. A presença dos outros dois instrumentos no mercado tem um valor prático: mostra que são operáveis, auditáveis e compatíveis com a forma como as assembleias são conduzidas hoje.

## O que não se pode afirmar

Quatro limites qualificam a implicação. O primeiro é a magnitude: o ganho de bem-estar é da ordem de 1%, medido numa utilidade estilizada, e o trabalho afirma a ordenação entre desenhos, e não o tamanho do ganho. O segundo é a dependência do comportamento: quando o lance se adapta à regra, $M_3^{rs}(0{,}05)$ deixa de dominar o vigente (seção 7.6); o ganho de bem-estar se mantém, e até cresce, mas a dispersão da espera passa a piorar. O terceiro é a forma da distribuição de urgência: sob uma Gamma, que os dados não rejeitam, o desenho também deixa de dominar, pelo mesmo motivo (seção 7.5). O quarto é a fração de lance: sob o desenho proposto, a parcela das contemplações feitas por lance cai de 0,6895 para 0,4378 (`results/h3_metricas_sobra_reg_m3B.csv`). Um indicador que hoje se lê como sinal de funcionamento do mercado mudaria de nível sem que isso significasse pior alocação, e um regulador que adotasse o desenho precisaria rever o que acompanha.

O segundo e o terceiro limites têm resposta parcial na busca exploratória de H5 (seção 7.6). O desenho $M_4$ mantém o preço uniforme, o lance mínimo e o sorteio da sobra, e acrescenta ao sorteio das cotas ativas um peso pela espera já cumprida. Com a política calibrada, ele domina o vigente em nove de dez sorteios dos parâmetros e sob a forma Gamma da urgência; com o lance aprendido, domina com a semente de treino registrada, mas não com uma segunda. Com peso mais forte, nenhum critério piora em relação ao vigente nas duas sementes, mas o ganho de bem-estar desaparece. A implicação para o regulador tem, assim, duas partes de força diferente. A primeira é firme: o preço uniforme no lance melhora o bem-estar dos participantes e a estabilidade do fundo em todos os testes. A segunda é uma direção, e não uma prescrição: ponderar o sorteio pela espera é o instrumento que este trabalho encontrou para conter o custo do preço uniforme em igualdade na espera, por atuar num canal que o lance não alcança, e a intensidade certa desse peso depende do comportamento que os participantes desenvolverem sob a nova regra.

O resultado sobre o peso pela espera também tem uma leitura regulatória. Favorecer no sorteio quem espera há mais tempo reduz a dispersão da espera, mas custa bem-estar, porque tira a vez de quem tem mais urgência. Uma regra que pareça mais justa por igualar a espera pode, portanto, piorar a situação média dos participantes.

## Um desenho que a regulação exclui

Nas associações rotativas de lance, o lance vencedor é distribuído como dividendo entre os que perderam a disputa daquela rodada [@klonner2008private]. É uma alternativa natural de desenho, que transfere diretamente a quem espera o que o vencedor paga para antecipar. No consórcio brasileiro, ela é inadmissível: a Resolução destina o lance vencedor à amortização das prestações do próprio vencedor (art. 12, parágrafo único) [@bcb2023res285]. O trabalho não a simulou. Avaliar se essa restrição custa bem-estar aos participantes é uma pergunta que só uma mudança normativa permitiria responder na prática, e que o modelo deste trabalho permitiria explorar em simulação.
