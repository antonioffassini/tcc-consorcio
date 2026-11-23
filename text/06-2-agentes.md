---
secao: 6.2
titulo: Agentes de aprendizado por reforço
status: rascunho
responsavel:
insumos:
  - ESTADO.md §4, 2026-11-22 (protocolo dos agentes, emenda, tentativas 1 e 2, critério endurecido), escritos antes de rodar
  - src/sim/agentes.py, src/analysis/agentes_rl.py, src/sim/grupo.py
fontes:
  - results/agentes/treino_M3rs_p0.05_s0_t2.csv
  - results/agentes/treino_M2_s0_t2.csv
  - results/agentes/treino_M0_s1_t2.csv
  - results/agentes/treino_M0_s0_t2.csv
  - results/agentes/treino_M0_s0.csv
  - results/agentes/treino_M0_s1.csv
excecoes:
  - 240
  - 285
  - 0,05
  - 0,50
  - 0,3
  - 0,02
  - 0,1
  - 0,95
  - 4.000
  - 7.500
  - 15.000
  - 20.000
  - 2022
  - 2020
paginas_alvo: 4
---

# Agentes de aprendizado por reforço

A política paramétrica $\pi_\phi$ da seção 4.1 serve à calibração, mas impõe uma forma ao comportamento e não muda quando a regra muda. Para as hipóteses H1 e H4, o comportamento de lance é substituído por agentes que aprendem por tentativa e erro dentro do ambiente simulado, sem regra de lance imposta. Esta seção descreve o algoritmo, a representação do estado, a recompensa, o treinamento e o critério de convergência, todos registrados no log do projeto antes do primeiro treino.

## Algoritmo

O algoritmo é o Q-learning tabular, a forma mais simples de aprendizado por reforço com tabela de valores [@calvano2020artificial; @banchio2022artificial]. Para cada estado $s$ e cada ação $a$, o agente mantém uma estimativa $\mathcal{Q}(s,a)$ da utilidade que obtém ao escolher $a$ em $s$ e seguir, depois, a política atual. Na maior parte das vezes escolhe a ação de maior valor estimado; com probabilidade $\varepsilon$, escolhe uma ação ao acaso, para continuar experimentando.

Duas escolhas adaptam o algoritmo ao consórcio. A primeira é a tabela compartilhada: um grupo tem centenas de cotas, e manter uma tabela por cota exigiria uma experiência que nenhuma cota acumula na vida de um grupo. Todas as cotas consultam e atualizam a mesma tabela; a diferença entre elas está no estado, que inclui o tipo de cada uma. O resultado se aproxima do aprendizado de uma população de participantes semelhantes, e não da interação estratégica entre poucos agentes independentes estudada nos trabalhos de leilão com algoritmos. A segunda escolha é a atualização por Monte Carlo: a recompensa só é conhecida na contemplação, às vezes dezenas de assembleias depois do lance, e cada par $(s,a)$ visitado por uma cota é atualizado com a utilidade que essa cota realizou ao final.

## Estado, ação e recompensa

O estado combina quatro informações, cada uma discretizada em faixas: o quintil da urgência $\theta_i$ na população, a faixa da liquidez $\lambda_i$ (três faixas), a faixa do prazo restante do grupo (quatro faixas) e a faixa do menor lance vencedor da assembleia anterior (quatro faixas), num total de 240 estados. A última informação é pública, porque a ata da assembleia relaciona os percentuais ofertados (Resolução BCB n. 285/2023, art. 48) [@bcb2023res285]. Ela é também a informação que, em leilões de primeiro preço repetidos entre algoritmos de Q-learning, impede a convergência para lances coordenados abaixo do valor [@banchio2022artificial].

A ação é o lance total, entre 0 e 0,50 do crédito em passos de 0,05. Lances acima da liquidez mais o teto do embutido não estão disponíveis para a cota. O lance é coberto primeiro com recursos próprios e o restante com embutido, como na política paramétrica.

A recompensa é a utilidade realizada $U_i$ da seção 4.4, a mesma usada no critério de bem-estar, recebida na contemplação, por lance ou por sorteio. A cota excluída não gera atualização, porque a exclusão é exógena no modelo e não decorre do lance. O agente aprende, portanto, a maximizar o mesmo objetivo pelo qual os desenhos são avaliados.

## Treinamento

O treinamento usa os parâmetros calibrados na seção 6.3. Cada episódio é a vida inteira de um grupo, de trinta grupos do desenho calibrado percorridos em ciclo, com prazo, tamanho e cláusula da sobra próprios. A tabela começa com valores otimistas, acima de qualquer utilidade possível, o que força a experimentação de todas as ações no início do treino [@banchio2022artificial].

Foram feitas duas tentativas, ambas registradas antes de rodar. Na primeira, a atualização usou passo constante de 0,1, com $\varepsilon$ caindo de 0,3 a 0,02 e até 4.000 episódios. Na segunda, a estimativa de cada par $(s,a)$ passou a ser a média de todas as utilidades observadas, com $\varepsilon$ caindo de 0,3 a 0,02 ao longo de 15.000 episódios e até 20.000 episódios. Sob os desenhos alternativos, o treino parte da tabela aprendida sob $M_0$, com exploração menor, e dura ao menos 7.500 episódios: os participantes chegam à regra nova com o comportamento que tinham sob a vigente e se ajustam a partir dele.

## Convergência

O critério de convergência é o mesmo nas duas tentativas: a ação de maior valor não pode mudar, entre duas verificações seguidas, em pelo menos 0,95 da massa de estados visitados. Na segunda tentativa, o critério foi atingido cedo, ainda com exploração alta; como uma tabela estável enquanto um quarto das ações é aleatório descreve a resposta a uma população que ainda experimenta, a convergência passou a ser verificada só depois de $\varepsilon$ chegar ao piso. A mudança endurece o critério e foi registrada antes de o resultado ser conhecido.

Na primeira tentativa, os agentes não convergiram: a ação de maior valor ficou estável em cerca de três quartos da massa de estados, nas duas sementes (`results/agentes/treino_M0_s0.csv`, `results/agentes/treino_M0_s1.csv`), embora o lance médio aprendido já fosse estável. O passo constante, com recompensas muito variáveis de uma cota para outra, fazia a escolha alternar entre lances de valor quase igual. Na segunda tentativa, os agentes convergiram sob $M_0$ nas duas sementes, com a ação de maior valor estável em mais de 0,999 da massa de estados depois de a exploração chegar ao piso, e sob $M_2$ e $M_3^{rs}(0{,}05)$, treinados a partir da tabela de $M_0$ com uma semente (`results/agentes/treino_M0_s0_t2.csv`, `results/agentes/treino_M0_s1_t2.csv`, `results/agentes/treino_M2_s0_t2.csv`, `results/agentes/treino_M3rs_p0.05_s0_t2.csv`). Na busca exploratória de H5 (seção 7.6), o mesmo procedimento de treino, aquecido a partir da tabela de $M_0$, foi repetido sob cada uma das oito variantes registradas.

## O que os agentes não são

Os agentes não são calibrados aos dados: a calibração usa a política paramétrica, e os agentes treinam sobre o ambiente já calibrado. O comportamento que aprendem é o que maximiza a utilidade do modelo, e não necessariamente o dos participantes reais. Por isso, o papel deles é responder a duas perguntas condicionais, não estimar o comportamento observado: se uma regra estática descreveria o lance de quem otimiza nesse ambiente (H1) e se a ordenação entre desenhos sobrevive quando o lance se adapta à regra (H4).
