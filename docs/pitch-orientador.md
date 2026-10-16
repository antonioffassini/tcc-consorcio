# Reunião com o Prof. Cugnasca — o que levar na cabeça

*Briefing para apresentar o trabalho já feito. A troca de tema está aceita; esta conversa é
sobre conteúdo, método e o que vem até 12/10. Material de apoio para mostrar:
`docs/apresentacao-projeto.pptx` (21 slides) e `build/monografia-caps1-2-preliminar.docx`.
Atualizado em 01/10/2026.*

---

## 0. Como usar este documento

### A conversa em três frases

1. O consórcio brasileiro decide quem recebe o crédito a cada mês por sorteio e por lance,
   com regras fixadas por lei e por norma do Banco Central que nunca foram comparadas com
   desenhos alternativos.
2. Este trabalho modela o grupo de consórcio como um jogo dinâmico entre participantes
   heterogêneos, implementa o jogo como simulação multiagente, calibra o comportamento contra
   os dados públicos do Bacen e compara o desenho vigente com alternativas.
3. A dificuldade técnica central é de identificação: o Bacen não publica lances individuais,
   só contagens agregadas. O trabalho mostra o que dá para inferir mesmo assim.

Se a conversa tiver só cinco minutos: essas três frases e o slide 19 (variação entre
administradoras).

### Roteiro sugerido da conversa

O documento segue a ordem em que vale explicar: primeiro **o que é** o consórcio, depois
**o que perguntamos**, depois **como vamos responder**, depois **onde estamos** e, por fim,
**o que precisamos dele**.

| Parte | Seções | Slides | Tempo |
|---|---|---|---|
| A. O objeto: como o consórcio funciona | 1 | 3–5 | 5 min |
| B. A pergunta: problema, tese, hipóteses e escopo | 2–4 | 6–10 | 5 min |
| C. O método e a parte de computação | 5–7 | 11–16 | 10 min |
| D. Onde estamos: dados, achado e calendário | 8–9 | 17–20 | 5 min |
| E. O que pedir a ele | 10 | — | 5 min |

As seções 11 (perguntas prováveis) e 12 (glossário) são para consulta, não para apresentar.

---

# PARTE A — O OBJETO

## 1. O consórcio em cinco minutos

### 1.1 Como um grupo funciona

Um grupo tem N cotas e prazo T (em meses; em imóveis, tipicamente de 150 a 240). Todo mês, cada
cota ativa paga uma parcela ao **fundo comum**. A cada assembleia acontecem, nesta ordem:

1. **Apuração de vagas.** A administradora verifica o saldo do fundo e calcula quantos créditos
   ele comporta. A contemplação está condicionada a recursos suficientes (Lei 11.795/2008,
   art. 23). Por isso o número de contemplados no mês, gₜ, **não é fixo**: depende do saldo, que
   depende da adimplência de todos.
2. **Sorteio.** Concorrem as cotas ativas em dia (pelo crédito) e as excluídas ainda não
   contempladas (pela restituição). Ver 1.2.
3. **Lance.** Só depois do sorteio, com o que sobrou do fundo (Res. BCB 285/2023, art. 12, I).
   Vence o maior lance, em percentual do crédito. Ver 1.3.
4. **Transição.** O contemplado sai da disputa. Na assembleia seguinte há menos concorrentes, e
   o perfil de quem resta é outro.

### 1.2 O sorteio: quem concorre

Dois grupos diferentes concorrem no mesmo sorteio, cada um por um prêmio diferente (Lei
11.795, art. 22, § 2º; Res. 285, art. 11, § 1º).

| Situação da cota | Quem é | Concorre no sorteio? | Ganha o quê |
|---|---|---|---|
| Ativa em dia | Participante normal | Sim | O **crédito** |
| Ativa em atraso | Ainda é membro, mas deve parcelas | **Não**, até regularizar | — |
| Excluída | Desistiu, ou atrasou 3 parcelas (Res. 285, art. 32, II) | Sim | A **restituição** do que pagou |

"Adimplente" é exigência para quem ainda é ativo. O excluído saiu do plano e concorre só para
receber o dinheiro de volta. Os dois grupos consomem **o mesmo fundo**: cada excluído sorteado
é dinheiro que não vira crédito para um ativo.

### 1.3 O lance: o segundo caminho

O lance é um **segundo caminho** para a contemplação, independente do sorteio. Quem é sorteado
não passa pelo lance.

| | Sorteio | Lance |
|---|---|---|
| Quem participa | Toda cota ativa em dia, automaticamente | Só quem faz oferta |
| Como se ganha | Sorte | Maior oferta (em % do crédito) |
| Custo | Nenhum além das parcelas | O valor ofertado, pago na hora |
| Ordem | Primeiro | Depois, com o que sobrou |

O lance é **pagar adiantado parte do que ainda se deve**. Exemplo: com uma carta de R$ 300 mil
e um lance de 30%, você paga R$ 90 mil agora e recebe a carta. Os R$ 90 mil quitam parcelas
futuras (Res. 285, art. 12, parágrafo único); não são taxa e não se perdem. Quem não ganha
recebe o lance de volta. O custo real é de oportunidade: imobilizar dinheiro para ter o
crédito antes.

**Dois detalhes que mudam o modelo:**

- **Lance embutido** (Res. 285, art. 13). Em vez de pagar com dinheiro próprio (lance livre),
  o participante pode ofertar parte da própria carta: ganha, recebe R$ 210 mil, e os R$ 90 mil
  abatem a dívida. A falta de liquidez não impede o lance; muda o custo dele. Há duas
  "tecnologias" de lance, e escolher entre elas faz parte da estratégia.
- **Lance em percentual** (Res. 285, art. 7º). Num mesmo grupo podem coexistir créditos de
  valores diferentes, desde que o menor seja pelo menos 50% do maior. Por isso o desempate
  usual é pelo percentual do crédito, e a ação do agente no modelo é b ∈ [0, b̄], em fração do
  crédito, e não em reais.

**Que tipo de leilão é:** de primeiro preço (cada vencedor paga o que ofertou), de múltiplas
unidades e repetido todo mês. Nos dados de imóveis, cerca de 80% das contemplações saem por
lance: na prática, o consórcio de imóveis funciona principalmente como um leilão de
antecipação.

### 1.4 Como o fundo se reparte e por que pode sobrar

A norma não fixa quanto vai para cada canal. Ela define a ordem:

1. **Sorteio:** o número é o "previsto" no contrato (Res. 285, art. 12, I). Se faltar recurso,
   o fundo de reserva cobre (art. 22, I, a), e ele pode pagar sorteios adicionais (art. 22, IV).
2. **Restituição:** não é uma fatia separada. Sai do sorteio: se o sorteado é excluído, paga-se
   só a restituição dele, que custa menos que um crédito cheio.
3. **Lance:** usa o residual, do maior para o menor lance, até o dinheiro acabar. Só vale depois
   que o lance é pago (art. 12, II).

**Exemplo:** fundo de R$ 600 mil, crédito de R$ 300 mil, 1 sorteio previsto. O sorteio leva R$
300 mil e sobram R$ 300 mil. Há lances de 50%, 40% e 30%. O de 50% paga R$ 150 mil, e o fundo
libera R$ 300 mil (custo líquido de R$ 150 mil, sobram R$ 150 mil). O de 40% precisaria de R$
180 mil e não cabe. Resultado do mês: 1 por sorteio, 1 por lance, e R$ 150 mil ficam no fundo.

**Pode sobrar dinheiro, e é normal.** A Res. 285 (art. 25-B) fala do "saldo remanescente do
fundo comum não utilizado nas contemplações do período", que rende e é corrigido. Sobra porque
o crédito é indivisível, porque pode não haver lance que caiba no residual, e porque pode faltar
dinheiro até para o sorteio (em cerca de 7% dos grupo×mês não houve contemplação). Se a
administradora é obrigada a usar todo o residual em lances é regra do contrato, a confirmar.

**Por que isso importa no modelo:** o saldo Rₜ é variável de estado. O que sobra num mês muda
as vagas do seguinte, e isso encadeia as decisões no tempo.

**Atenção (inferência a confirmar em regulamentos):** se o custo para o fundo for de fato
"crédito − lance", o número de vagas por lance depende do tamanho dos lances, e não só do saldo.
Isso mudaria a formalização do cap. 4 (`ESTADO.md` §5, item 14).

### 1.5 O que a norma garante

Tudo abaixo foi lido no texto oficial (Planalto e Bacen) em 25/09 e 01/10, e os PDFs estão em
`refs/pdfs/`.

| Norma | Ponto | Uso no modelo |
|---|---|---|
| Lei 11.795/2008, art. 22 §1º | Contemplação por sorteio ou por lance | Os dois canais são obrigatórios: os desenhos alternativos mudam a parametrização, não a existência dos canais |
| Lei 11.795/2008, art. 23 | Contemplação condicionada a recursos suficientes | Vagas gₜ endógenas ao saldo Rₜ |
| Lei 11.795/2008, art. 30 | Restituição ao excluído; §§ 1º–3º vetados | Excluídos no sorteio consomem o mesmo fundo |
| Res. BCB 285/2023, art. 12, I | Lance só depois do sorteio | Precedência no mecanismo M₀ |
| Res. BCB 285/2023, art. 13 | Lance embutido | Duas modalidades de lance |
| Res. BCB 285/2023, art. 7º | Menor crédito ≥ 50% do maior | Ação em percentual |
| Res. BCB 285/2023, art. 33 | O contemplado excluído mantém a contemplação, com crédito parcial | Mudança em relação à Circ. 3.432, que permitia cancelar |
| Res. BCB 285/2023, arts. 58–59 | Revoga a Circ. 3.432/2009; **vigência em 01/07/2024** (redação da Res. 362/2023) | O recorte do trabalho começa na data-base 2024-07 |

**Correção a fazer em voz alta:** a proposta de 14/09 dizia que a Res. 285 era de 20/12/2023 e
valia desde 01/01/2024. As datas certas são **19/01/2023** e **01/07/2024**. O documento dos
caps. 1–2 já está corrigido.

### 1.6 O parente informal: ROSCA

*Rotating Savings and Credit Association*, o "avô informal" do consórcio: *tanda* (México),
*chit fund* (Índia), *partner* (Jamaica), *hui* (China), *tontine* (África francófona). Um grupo
de conhecidos põe um valor fixo por mês, e a cada mês um deles leva o pote; em N meses todos
levaram. Quem leva cedo recebeu um empréstimo sem juros; quem leva por último fez uma poupança
forçada. A ordem sai por **sorteio** (ROSCA aleatória) ou por **lance**, em que quem quer levar
antes aceita um desconto que é repartido entre os demais.

| | ROSCA | Consórcio brasileiro |
|---|---|---|
| Quem faz a regra | O próprio grupo | Lei e Banco Central |
| Quem participa | Gente que se conhece | Milhões de desconhecidos |
| Quem garante o pagamento | Pressão social, reputação | Contrato, administradora, supervisão do Bacen |
| Prêmio por rodada | Um pote fixo | Número variável de vagas |
| Lance | Desconto no pote | Antecipação de parcelas, livre ou embutida |

**Para fechar a Parte A:** o consórcio é uma ROSCA regulada e em escala industrial, sem as
simplificações que tornam a ROSCA tratável no papel. A ROSCA tem uma literatura acadêmica rica
(§7); o consórcio, não.

---

# PARTE B — A PERGUNTA

## 2. Problema, pergunta e tese

**Problema.** A regra de contemplação é uma escolha regulatória. Toda regra de alocação de
recurso escasso admite a pergunta sobre sua eficiência relativa, e para o consórcio brasileiro
ninguém respondeu. A literatura nacional olha a solvência do grupo pela ótica da
administradora. A internacional estuda ROSCAs: arranjos informais, com regra escolhida pelo
próprio grupo e um prêmio por rodada (1.6).

**Pergunta.** Em que medida o mecanismo vigente é eficiente, sob critérios de bem-estar dos
participantes e de estabilidade financeira do grupo, quando comparado a desenhos alternativos
admissíveis sob a mesma regulação?

**Tese, em duas partes.** Convém dizer as duas separadas, porque a segunda é o que faz disto
Engenharia de Computação:

- *Substantiva:* o desenho vigente é dominado por pelo menos um desenho alternativo
  admissível, sob critérios explícitos.
- *Metodológica:* essa dominância pode ser verificada por simulação calibrada apenas em dados
  agregados públicos, sem observar lances individuais.

---

## 3. Hipóteses

| | Enunciado curto | Como se testa |
|---|---|---|
| **H1** | Agentes que aprendem jogando lançam diferente do que prevê a teoria estática de leilões | Um experimento de aprendizado por reforço sobre o modelo calibrado |
| **H2** | O modelo calibrado só com agregados reproduz momentos que não foram usados na calibração | Calibração por momentos simulados + teste fora da amostra |
| **H3** | Algum desenho alternativo melhora pelo menos um critério sem piorar os outros, de forma robusta | Comparação M₀ × M₁ × M₂ + varredura de parâmetros |

### Em linguagem simples

- **H1 — Como as pessoas dão lance.** A teoria clássica trata o leilão como evento único
  ("oferte (n−1)/n do seu valor"). No consórcio há repetição, falta de dinheiro e saída de
  concorrentes. Teste: agentes que aprendem por tentativa e erro, sem fórmula imposta, jogam
  milhares de rodadas; compara-se o lance aprendido com o previsto. Precedente: Banchio e
  Skrzypacz (2022). Se confirmar, avaliar regras com as fórmulas clássicas daria resposta
  errada.
- **H2 — O simulador é confiável.** Os "botões" de comportamento são ajustados para reproduzir
  alguns números reais; depois se verifica se o simulador acerta **outros** números que ele
  nunca viu, como treino e teste em aprendizado de máquina. A escolha de quais números são de
  teste é feita **antes** de ajustar; decidir depois seria ajuste disfarçado de validação.
- **H3 — Existe regra melhor.** Uma regra domina a atual se melhora pelo menos um entre
  bem-estar, equidade e estabilidade sem piorar os outros, e isso vale em toda a faixa de
  parâmetros que os dados permitem. Afirma-se **qual** é melhor, nunca **quanto**.

**Dependência:** H3 é uma conclusão tirada do simulador, então só vale se H2 passar; por isso
a validação vem antes da comparação. H1 é um experimento à parte: se cair, a tese continua de
pé, só que com menos contribuição metodológica.

**Frase para o professor:** "H2 garante que o simulador é confiável, H3 usa o simulador para
comparar regras, e H1 testa se a forma de modelar o comportamento faz diferença."

---

## 4. Escopo: o que o trabalho não é

- Não é estudo jurídico nem proposta de redação normativa: a lei entra como restrição.
- Não estima a distribuição individual de lances, que não é observável.
- Não modela mercado secundário de cotas, concorrência entre administradoras nem formação de
  grupos.
- Não trata taxa de administração nem fundo de reserva como variáveis de escolha.
- Cobre só imóveis, no regime posterior a 01/07/2024. O resto entra, se entrar, como
  sensibilidade.

---

# PARTE C — COMO VAMOS RESPONDER

## 5. O método

### 5.1 Por que simular em vez de resolver

"Forma fechada" é ter uma **fórmula** para o comportamento dos jogadores. A teoria tem fórmula
para o caso com um prêmio por rodada, uma característica privada por participante, população
fixa e sem realimentação. O consórcio tem as quatro coisas ao contrário. Cada uma, sozinha, já
complica a conta; juntas, impedem a fórmula:

| Característica | O que complica |
|---|---|
| Vagas aleatórias | O participante não sabe quantas vagas haverá; a incerteza sobre as vagas se soma à incerteza sobre os rivais |
| Liquidez com duas formas de lance | Cada participante passa a ter duas dimensões (quanto valoriza, quanto dinheiro tem) e uma escolha a mais (como pagar) |
| População que diminui e muda de perfil | Os apressados saem primeiro; o jogo do mês 50 é outro, e o participante raciocina sobre quem sobrou; vira uma sequência de leilões encadeados |
| Realimentação por exclusão | A exclusão tira um concorrente (bom) e aumenta a restituição e reduz a arrecadação (ruim); o efeito depende do estado, que depende das decisões |

Os modelos analíticos de ROSCA (Besley-Coate-Loury; Klonner) chegam a fórmulas removendo pelo
menos duas dessas características.

**Frase para defender:** "Manter as características e simular é preferível a removê-las para ter
fórmula, porque a conclusão sobre a regra poderia vir justamente do que foi removido. O preço é
provar que a simulação está certa, e é para isso que existem os casos-limite (5.4)."

### 5.2 O modelo

- **Participantes** i = 1…N, com dois atributos privados: **urgência θᵢ** (quanto vale
  receber antes) e **liquidez λᵢ,ₜ** (quanto podem ofertar com dinheiro próprio).
- **Estado do grupo** sₜ = (Rₜ, nₜ, Kₜ, Xₜ, t): saldo do fundo, cotas ativas adimplentes,
  contempladas e excluídas, e o mês.
- **Ação** bᵢ,ₜ: lance em percentual do crédito, mais a modalidade (livre ou embutido).
- **Mecanismo** M: a regra que transforma estado + lances no conjunto de contemplados. M₀ é o
  vigente.
- **Política de lance** π(φ): uma função simples, com 3 ou 4 parâmetros φ, que diz quanto cada
  tipo de participante oferta em cada situação.

### 5.3 Calibração por momentos simulados (SMM)

Em termos de identificação de sistemas: escolhe-se Θ (os parâmetros de comportamento e as
distribuições de urgência e liquidez), simula-se o sistema, calculam-se estatísticas resumo
("momentos") da simulação e comparam-se com as mesmas estatísticas nos dados reais. Ajusta-se Θ
até a distância ser mínima:

  Q(Θ) = (μ̂ − μ̃(Θ))ᵀ Ω (μ̂ − μ̃(Θ))

onde μ̂ são os momentos observados, μ̃(Θ) os simulados e Ω uma matriz de pesos.

O teste de H2 está em **separar os momentos em dois grupos antes de ver qualquer ajuste**: um
grupo calibra, o outro só testa.

**Por que o RL não está dentro da calibração:** treinar agentes de aprendizado por reforço até
convergirem a cada avaliação de Q(Θ) multiplicaria o custo computacional por milhares, e seria
inviável num notebook. Por isso a política é paramétrica dentro da calibração, e o RL roda
**uma vez**, sobre o modelo já calibrado, só para testar H1.

### 5.4 Validação

1. **Casos-limite.** Para algumas versões simplificadas do problema, a teoria já tem a resposta
   exata: num leilão de uma rodada, com valores sorteados de uma distribuição conhecida, ela diz
   quanto cada um deve ofertar; numa ROSCA com prêmio único, também. Configura-se o simulador
   nessas versões e confere-se se ele chega no mesmo número. É como testar um circuito com uma
   entrada cuja saída já se conhece antes de usá-lo no sistema real. Se não reproduzir, isso é
   um resultado e entra no texto; não se mexe no modelo até passar.
2. **Teste fora da amostra** (H2).
3. **Robustez da ordenação:** varrer o espaço de parâmetros compatível com os dados e ver se a
   ordem entre M₀, M₁ e M₂ se mantém. O trabalho afirma a **ordenação**, nunca o tamanho do
   ganho.

### 5.5 Critérios de comparação

| Símbolo | Critério | Ideia |
|---|---|---|
| 𝒲(M) | Bem-estar agregado | Soma do valor que cada participante tira do crédito, descontada a espera e o lance pago |
| ℰ(M) | Equidade temporal | Dispersão do tempo de espera até a contemplação |
| 𝒮(M) | Estabilidade do fundo | Suficiência de recursos e resiliência à inadimplência |

**Ponto a levar ao professor:** somar utilidades de pessoas com urgências diferentes embute um
juízo de valor. Como agregar e como ponderar os três critérios é a escolha mais consequente do
trabalho, e queremos fechá-la com ele.

### 5.6 Desenhos alternativos (candidatos)

- **M₁ — sorteio ponderado pelo tempo de espera:** quem espera há mais tempo tem mais chance no
  sorteio. O lance não muda.
- **M₂ — regra de preço do lance:** todos os vencedores pagam o menor lance vencedor (preço
  uniforme), em vez de cada um pagar o próprio. É a distinção clássica entre leilão
  discriminatório e uniforme de múltiplas unidades.

Os dois mantêm sorteio e lance. A admissibilidade de cada um frente à Res. 285 ainda precisa ser
confirmada; vale perguntar a opinião dele.

---

## 6. Onde está a Engenharia de Computação

Para responder com segurança à pergunta "o que tem de computação nisso?". Resposta curta: **o
trabalho é a construção e a validação de um sistema computacional que reproduz um mercado real e
serve para testar regras que não dá para testar no mundo real.** A economia diz *o que*
simular; a computação diz *como* construir, calibrar e provar que a simulação está certa.

### 6.1 A ideia em linguagem de leigo

Pense num **videogame do consórcio**. Cada jogador é um participante virtual, com mais ou menos
pressa para receber o crédito e mais ou menos dinheiro para dar lance. Todo mês o jogo arrecada
as parcelas, faz o sorteio, abre o lance e anda o relógio. Rodando o jogo milhares de vezes,
vemos o que acontece em média: quanto tempo cada um espera, quanto paga de lance, se o fundo
aguenta.

Três problemas de engenharia aparecem:

1. **Construir o jogo direito.** As regras têm de ser exatamente as da lei, e o código não pode
   ter erro: testes automáticos e casos-limite (5.4).
2. **Fazer os jogadores virtuais se comportarem como os reais.** Não sabemos como cada pessoa dá
   lance, porque o Bacen não publica isso. Sabemos o resultado agregado (por exemplo, que cerca
   de 80% das contemplações em imóveis saem por lance). Então "giramos os botões" dos jogadores
   virtuais até o jogo produzir os mesmos números que a realidade: a **calibração** (5.3).
3. **Trocar a regra e comparar.** Com o jogo calibrado, troca-se a regra e mede-se quem ganha e
   quem perde (5.5–5.6).

A analogia mais próxima dentro da Engenharia de Computação é a **identificação de sistemas**:
uma "caixa-preta" (o mercado de consórcios) da qual só se medem as saídas agregadas, e um modelo
cujos parâmetros internos precisam fazer as saídas coincidirem. A diferença é que aqui a
caixa-preta é um sistema de agentes que decidem estrategicamente.

### 6.2 Os componentes do sistema e as tecnologias

| Componente | O que faz | Como é feito | Em linguagem simples |
|---|---|---|---|
| **1. Pipeline de dados** | Lê os 236 arquivos do Bacen, padroniza, junta e gera painéis prontos para análise | Python, pandas, Parquet; leitura direto dos `.zip`; relatório automático de qualidade | Transforma uma pilha de planilhas mensais numa tabela única e limpa |
| **2. Simulador do grupo** | Reproduz, mês a mês, a vida de um grupo: arrecadação, apuração de vagas, sorteio, lance, exclusão, restituição | Simulação de eventos discretos com agentes, em Python/NumPy; interface no padrão Gymnasium; sementes aleatórias fixas | O "videogame do consórcio" |
| **3. Agentes paramétricos** | Decidem o lance de cada participante a partir da urgência, da liquidez e do estado do grupo | Função com 3 ou 4 parâmetros (π(φ)) | A "personalidade" dos jogadores, ajustável por botões |
| **4. Calibração (SMM)** | Encontra os parâmetros que fazem a simulação reproduzir os dados reais | Otimização numérica sem derivadas (a função objetivo é ruidosa, porque vem de simulação), com o SciPy; mesmas sementes em cada avaliação | Girar os botões até o jogo "bater" com a realidade |
| **5. Validação** | Verifica que o simulador está certo e que a calibração não é sorte | Testes automatizados (pytest); casos-limite; teste em momentos reservados | Provar que o jogo não tem bug e que o ajuste vale fora da amostra |
| **6. Comparação de mecanismos** | Troca a regra de contemplação e mede bem-estar, espera e estabilidade | Simulação de Monte Carlo (milhares de rodadas por cenário) e varredura de parâmetros | Testar regras novas sem mexer na vida de ninguém |
| **7. Agentes que aprendem (RL)** | Testa se jogadores que aprendem sozinhos chegam ao comportamento previsto pela teoria | Aprendizado por reforço (Q-learning ou PPO, via Stable-Baselines3; escolha em aberto) | Jogadores que aprendem por tentativa e erro |
| **8. Reprodutibilidade e controle** | Garante que qualquer número do texto pode ser regenerado do zero | Git/GitHub; `make all`; auditoria que impede número sem origem e citação sem PDF; Markdown → Pandoc → LaTeX/Word | Ninguém precisa "confiar"; dá para rodar de novo e conferir |

**Por que é difícil do ponto de vista computacional:**
- **Não existe fórmula pronta** (5.1): a única saída é simular, e por isso o trabalho tem de
  demonstrar que a simulação está correta.
- **A calibração é um problema de otimização caro e ruidoso:** cada avaliação da função objetivo
  é uma bateria de simulações.
- **A identificação é um problema inverso:** inferir comportamento individual a partir de dados
  agregados, como reconstruir um sinal a partir de medições indiretas.

### 6.3 Como dizer isso em 30 segundos

"O trabalho é construir um simulador multiagente do grupo de consórcio, calibrá-lo contra os
dados públicos do Banco Central e usá-lo para comparar regras de contemplação. A parte de
computação está em três lugares: na construção e verificação do simulador, que não tem solução
analítica; na calibração, que é um problema de otimização ruidosa com observação só agregada,
parecido com identificação de sistemas; e na infraestrutura de reprodutibilidade, que garante
que cada número do texto sai de código versionado. Os dados e a infraestrutura já estão prontos,
e o pipeline está sendo implementado agora."

---

## 7. Bibliografia: o que cada referência faz no trabalho

São 22 referências verificadas contra a fonte primária e 8 candidatas em verificação. As
centrais:

| Referência | O que mostra | Por que importa aqui |
|---|---|---|
| Besley, Coate e Loury (1993), *AER* | Comparam alocação aleatória e por lance em ROSCAs; a aleatória é preferível quando os participantes têm gostos idênticos | É a versão teórica de H3: o resultado deles cai com heterogeneidade, que é exatamente o que nosso modelo introduz |
| Kovsted e Lyk-Jensen (1999), *J. Dev. Econ.* | A escolha entre sorteio e lance em ROSCAs | Precedente direto da pergunta |
| Klonner (2003, 2008) | ROSCA como sequência de leilões; estimação estrutural com dados de ROSCAs indianas | O precedente metodológico mais próximo |
| Guerre, Perrigne e Vuong (2000), *Econometrica* | Como estimar valorações quando se observam **todos** os lances | O contraste: o que **não** dá para fazer com o dado do Bacen |
| Athey e Haile (2002), *Econometrica* | Condições para identificar modelos de leilão observando **só parte** da informação | A base para dizer que identificar por agregados é possível em princípio |
| Banchio e Skrzypacz (2022), *ACM EC* | Agentes de Q-learning em leilões repetidos se afastam do equilíbrio estático, e o afastamento depende do formato do leilão | A âncora de H1 |
| Calvano et al. (2020), *AER* | Algoritmos de aprendizado chegam a preços acima do competitivo sem comunicação | Legitima usar agentes que aprendem como instrumento de análise econômica |

**A lacuna:** não se achou trabalho que trate um mecanismo de alocação **regulado**, de adesão
massiva, com número de vagas aleatório e sem observação de lances. A busca formal em BDTD,
CAPES, SciELO, SPELL e working papers do BCB ainda está em andamento. Não afirmar ineditismo
como certo antes de terminá-la.

**Pendentes de verificação:** as referências clássicas de momentos simulados (Gouriéroux,
Monfort e Renault, 1993; McFadden, 1989; Duffie e Singleton, 1993). Ainda não entram no texto.

---

# PARTE D — ONDE ESTAMOS

## 8. Os dados e o primeiro achado

**O que temos:** 236 arquivos do banco de dados de consórcios do Bacen, de 2017-03 a 2026-05,
já no repositório:

- **Por grupo, mensal:** cotas ativas, inadimplentes, contempladas no mês, excluídas, prazo,
  valor do bem, taxa de administração. No regime da Res. 285: cerca de 3.470 grupos de imóveis
  e 76 administradoras.
- **Por administradora × UF, trimestral:** contemplados **por lance** e **por sorteio**.
- **Contábil, consolidado do sistema**, até 2024-12.

**O achado que muda o desenho (o mais importante da reunião):**

- O arquivo por grupo informa **quantos** foram contemplados, mas **não por qual canal**. A
  separação lance × sorteio só existe por **administradora × trimestre**.
- No agregado, a fração de contemplações por lance em imóveis subiu de cerca de 70% (2017) para
  cerca de 80% (2026).
- Entre administradoras, no regime atual, essa fração varia de 0,12 a 0,97. **Cerca de 94% da
  variação está entre administradoras**, e quase nada dentro de cada uma ao longo do tempo. Ela
  se correlaciona com o tamanho dos grupos (ρ de Spearman ≈ 0,56) e não com o prazo.

**O que isso implica:** a identificação é possível, mas num grão diferente do previsto. H2
falava em "variação entre grupos de tamanhos e prazos distintos"; os dados sustentam calibrar
em **dois grãos**: a taxa total de contemplação por grupo × mês (vagas) e a fração de lance por
administradora × trimestre (canal). É uma reformulação a apresentar e discutir com ele.

**Cautela obrigatória:** esses números vêm de uma análise exploratória feita em 25/09, fora do
pipeline oficial. Estão sendo reproduzidos no código do projeto e só entram na monografia
depois disso. Dizer isso explicitamente se ele pedir números.

---

## 9. O que já está feito e o que vem

| Componente | Situação |
|---|---|
| Tese, pergunta, hipóteses, notação, escopo | Fechados |
| Capítulo 1 (1.1–1.4) e capítulo 2 (2.1–2.5) | Rascunho, em .docx ABNT para leitura |
| Normativos e dados do Bacen (236 arquivos, 2017–2026) | Obtidos, conferidos e versionados |
| Conferência do leiaute: cabeçalhos iguais em toda a série | Pronto |
| Leitura exploratória da variação entre administradoras | Pronto, a reproduzir no pipeline |
| Repositório Git/GitHub e auditoria automática do texto | Pronto |
| Geração da monografia: Markdown → Pandoc → Word/LaTeX ABNT | Pronto para .docx; abnTeX2 em configuração |
| Pipeline do painel e teste formal de identificação | Em desenvolvimento (plano aprovado em 01/10) |
| Formalização (cap. 4), simulador, agentes, calibração, comparação, RL | A fazer |

| Quando | Entrega | O que ela prova |
|---|---|---|
| 01–02/10 | Pipeline do painel + teste formal de identificação (G1) | Que os dados têm variação suficiente para calibrar |
| 02/10 | Simulador do mecanismo vigente (M₀), com testes e casos-limite | Que o "videogame" reproduz as regras e a teoria onde ela existe |
| 02–03/10 | Agentes paramétricos + calibração SMM com dois momentos + primeira tabela | Que o sistema fecha de ponta a ponta |
| 03–04/10 | M₁ e M₂; teste fora da amostra; RL; varredura de robustez | H2, H3 e H1, nessa ordem de prioridade |
| 05/10 | Congelamento dos resultados | Que o texto descreve exatamente o que foi rodado |
| 06–08/10 | Redação dos capítulos restantes | |
| 09/10 | Revisão adversarial + reunião com a versão completa | |
| 10/10 | Compilação final e auditoria zerada | |

**Regra de corte:** se apertar, sai primeiro o RL (H1 vira trabalho futuro), depois o M₂. A
validação não sai.

---

# PARTE E — O QUE PRECISAMOS DELE

## 10. O que pedir a ele

1. **Critérios de bem-estar:** como agregar utilidades heterogêneas e como ponderar 𝒲, ℰ e 𝒮
   (5.5).
2. **Reformulação de H2** para os dois grãos do §8: ele concorda?
3. **Admissibilidade de M₁ e M₂:** algum dos dois lhe parece fora do que a norma permite?
4. **Formato e prazo da unidade:** data real de entrega e defesa, e o padrão de formatação
   esperado.
5. **Próximo encontro:** a proposta é por volta de 09/10, com a versão completa.

---

# CONSULTA

## 11. Perguntas prováveis e respostas curtas

**"Se não observam os lances, como estimam o comportamento?"**
Pelos efeitos agregados. A política de lance tem poucos parâmetros, e eles são escolhidos para
que o modelo reproduza o que se observa: quantas contemplações saem por lance em cada
administradora e quantas vagas o fundo gera por grupo. Athey e Haile (2002) mapeiam quando esse
tipo de identificação parcial funciona. E a validade é testada em momentos reservados, não só
afirmada.

**"Política paramétrica não é assumir a resposta?"**
Ela restringe a *forma* do comportamento, não a ordenação entre mecanismos. O teste fora da
amostra verifica se a forma é adequada, e o experimento de RL verifica se agentes sem forma
imposta se comportam de maneira muito diferente.

**"Como sabem que o simulador está certo?"**
Pelos casos-limite com solução conhecida (5.4). É condição para seguir, e se falhar é
reportado.

**"O que tem de computação nisso?"**
Ver §6.3. Em uma linha: um sistema de alocação distribuída sem solução analítica, que exige
simulação, otimização numérica e validação do procedimento; e a contribuição metodológica
(inferir parâmetros de agentes a partir de observação agregada) vale para qualquer sistema só
instrumentado no agregado.

**"Dá tempo?"**
O escopo foi cortado para caber: um segmento, um regime, política paramétrica, RL como
experimento único, cerca de 70 páginas. Os dados e a infraestrutura já existem. O risco
principal é o calendário da modelagem, e a regra de corte já está definida.

---

## 12. Glossário rápido

- **Contemplação:** atribuição do crédito a uma cota.
- **Fundo comum:** caixa do grupo formado pelas parcelas.
- **Lance livre / embutido:** oferta com recursos próprios / com parte do próprio crédito.
- **Excluído:** consorciado desligado; recebe restituição quando sorteado ou no encerramento.
- **ROSCA:** *rotating savings and credit association*, a versão informal do consórcio (1.6).
- **Rₜ, gₜ:** saldo do fundo e número de vagas na assembleia t.
- **Momento:** estatística resumo dos dados (média, fração, correlação) usada na calibração.
- **SMM:** método de momentos simulados; calibra parâmetros fazendo a simulação reproduzir
  momentos dos dados.
- **Fora da amostra / sobre-identificação:** testar o modelo em momentos que não foram usados
  para calibrá-lo.
- **Caso-limite:** configuração simplificada em que a resposta analítica é conhecida.
- **Q-learning / RL:** algoritmo em que o agente aprende por tentativa e erro qual ação rende
  mais.
