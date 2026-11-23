---
secao: 9
titulo: Conclusão e trabalhos futuros
status: rascunho
responsavel:
insumos:
  - caps. 7 e 8
fontes:
  - results/agentes/h5_relativas_B_s1.csv
  - results/h5_politica/h5_robustez_resumo.csv
  - results/agentes/h5_relativas_B.csv
  - results/sens_forma_relativas.csv
  - results/m3_relativas_B.csv
  - results/agentes/h4_relativas.csv
  - results/h2_teste.csv
  - results/texto_2211_apresentacao.csv
excecoes:
  - 11.795
  - 285
  - 0,05
paginas_alvo: 3
---

# Conclusão e trabalhos futuros

Este trabalho avaliou o mecanismo de contemplação do Sistema de Consórcios brasileiro, sorteio e lance, contra desenhos alternativos admissíveis sob a Lei n. 11.795/2008 e a Resolução BCB n. 285/2023. A avaliação foi feita num simulador de grupos de consórcio calibrado nos dados públicos do Banco Central, com quatro hipóteses e regras de decisão fixadas antes de cada resultado, e uma quinta hipótese, exploratória, formulada depois da quarta.

## O que se pode afirmar

**O modelo não é contraditado pelos dados disponíveis (H2).** Calibrado em quatro momentos agregados, ele reproduz o sinal e a ordem de grandeza da relação entre o tamanho dos grupos de uma administradora e a fração de contemplações por lance, que a calibração não usou. O teste tem pouco poder, e a validação é, por isso, fraca; mas é a validação que o dado público permite.

**A teoria estática de leilões não descreve o lance de quem otimiza no consórcio (H1).** Agentes que aprendem por tentativa e erro sob a regra vigente ofertam, em média, perto da previsão estática no início do grupo e longe dela depois, com os participantes mais urgentes ofertando menos do que a teoria prevê. A avaliação de regras alternativas exige, portanto, simulação.

**Com o comportamento mantido, existe um desenho admissível que domina o vigente (H3).** O lance de preço uniforme, com lance mínimo de 0,05 do crédito e sorteio obrigatório da sobra, melhora o bem-estar e a estabilidade do fundo sem piorar a dispersão da espera nem o tempo de restituição, em amostras não usadas na sua escolha e na maior parte da incerteza de calibração. A dominância, porém, depende da forma da distribuição de urgência: sob duas formas alternativas, a dispersão da espera passa a piorar. O ganho vem principalmente do preço uniforme, o único dos três instrumentos que o mercado não pratica; os outros dois são o que o torna aceitável.

**Com o comportamento adaptado, nenhum desenho testado domina o vigente (H4).** Quando os agentes aprendem a ofertar sob cada regra, o ganho de bem-estar do preço uniforme se mantém e aumenta, mas a dispersão da espera passa a piorar. O padrão é o mesmo da sensibilidade à forma da urgência, e a recomendação que sobrevive a ambas é mais estreita que a de H3: o preço uniforme aumenta o bem-estar médio dos participantes e reduz a instabilidade do fundo, à custa de alguma igualdade na espera.

**A busca por um desenho robusto ao aprendizado encontrou uma direção, e não um desenho definitivo (H5).** A busca, formulada depois de H4 e guiada pelo seu diagnóstico, partiu de uma observação: os atenuantes que dependiam de o participante deixar saldo foram desfeitos pelo aprendizado. O desenho escolhido, $M_4$, mantém o preço uniforme com lance mínimo e sorteio da sobra e pondera o sorteio das cotas ativas pela espera já cumprida, algo que o participante não controla. Escolhido num conjunto de grupos e testado em outro, ele domina o vigente com o lance aprendido, com a política calibrada, sob outra forma da urgência e em nove de dez sorteios dos parâmetros; pela regra registrada, H5 não é rejeitada. Uma segunda semente de treino dos agentes, porém, desfaz a dominância, e com peso mais forte da espera nenhum critério piora, mas o ganho de bem-estar desaparece. O que fica é uma fronteira entre bem-estar e igualdade na espera, e o instrumento que a desloca. O caminho até ela é a principal lição de método do trabalho: foi a simulação com agentes que aprendem que mostrou por que o primeiro desenho falhava, onde procurar o segundo e quão frágil é cada conclusão diante do comportamento.

## O que o trabalho deixa

Além dos resultados, o trabalho deixa três contribuições de método. A primeira é a forma de calibrar um mecanismo de alocação sem observar os lances individuais, usando só agregados publicados por administradora e trimestre. A segunda é a separação entre comparação com comportamento fixo e com comportamento aprendido, que mostrou que a conclusão muda de uma para a outra, e em que ponto muda. A terceira é o registro, antes de cada resultado, das regras de decisão, da família de desenhos e das amostras de escolha e de avaliação, que permite ao leitor separar o que foi testado do que foi procurado.

## Trabalhos futuros

Quatro extensões seguem diretamente das limitações discutidas na seção 8.3. A primeira é calibrar os agentes aos dados, e não apenas a política paramétrica, para que o comportamento aprendido seja também o observado. A segunda é refazer a busca na família $M_3$ sob cada forma da distribuição de urgência, na versão completa da calibração, e estender a análise à forma da distribuição de liquidez e à cláusula da sobra das administradoras cujo regulamento não foi lido. A terceira é mapear a fronteira entre bem-estar e igualdade na espera em função da intensidade do peso da espera, com várias sementes de treino e com agentes calibrados aos dados, para saber se existe uma intensidade em que os dois ganhos coexistem de forma robusta. A quarta é avaliar desenhos hoje inadmissíveis, como o dividendo do lance vencedor aos que perderam a disputa, praticado nas associações rotativas de lance, para medir quanto a restrição normativa custa aos participantes.
