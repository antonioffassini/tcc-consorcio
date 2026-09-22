# TCC — Context Pack

> Constituição do projeto: o que raramente muda.
> Progresso, decisões e pendências vivem em `ESTADO.md` — não duplique aqui.
> Lido automaticamente no Cowork e no Claude Code; mantenha-o na raiz.
> Última atualização: 12/09/2026

---

## 1. Identificação

| Campo | Valor |
|---|---|
| Título provisório | Avaliação computacional do mecanismo de contemplação no Sistema de Consórcios brasileiro: um modelo multiagente calibrado em dados regulatórios |
| Autores | Antônio Freitas Fassini; Pedro Freitas Fassini; Pedro Paulo Teles Silveira |
| Orientador | Prof. Dr. Paulo Sergio Cugnasca |
| Instituição | Escola Politécnica da Universidade de São Paulo |
| Área de concentração | Engenharia de Computação e Sistemas Digitais |
| Data de entrega | 12/10/2026 (alvo interno; ver `docs/PLANO.md`) |
| Data da defesa | PREENCHER |

## 2. Tese em uma frase

O mecanismo de contemplação vigente no Sistema de Consórcios brasileiro — sorteio e lance,
fixados por regulação e nunca submetidos a avaliação comparativa — é dominado, sob critérios
explícitos de bem-estar dos participantes e de estabilidade financeira do grupo, por ao menos
um desenho alternativo admissível sob a mesma restrição regulatória; e essa dominância é
verificável por simulação multiagente calibrada exclusivamente em dados agregados públicos,
sem observação de lances individuais.

Duas afirmações compõem a tese, e é útil mantê-las separadas: a **afirmação substantiva** é a
dominância; a **afirmação metodológica** é que ela pode ser estabelecida a partir de observação
agregada. A segunda é o que faz o trabalho ser de engenharia, e não de economia aplicada.

## 3. Pergunta de pesquisa e hipóteses

**Pergunta.** Em que medida o mecanismo de contemplação vigente no Sistema de Consórcios
brasileiro é eficiente, sob critérios de bem-estar dos participantes e de estabilidade
financeira do grupo, quando comparado a desenhos alternativos de alocação admissíveis sob a
mesma restrição regulatória?

Desdobra-se em três questões subordinadas — Q1, Q2 e Q3 —, enunciadas em `text/01-2-problema.md`.

**H1 — Divergência comportamental.** O comportamento de lance que emerge de participantes que
aprendem por interação repetida sob as regras vigentes difere sistematicamente da previsão de
equilíbrio dos modelos estáticos de leilão de valor privado, e essa divergência é atribuível à
restrição de liquidez, ao caráter repetido da disputa e à externalidade que cada contemplação
impõe aos demais. → **Testada na seção 7.3.**

**H2 — Adequação empírica.** É possível calibrar o modelo de comportamento por método de
momentos simulados, usando exclusivamente os agregados publicados pelo regulador, de modo que
ele reproduza momentos não empregados na calibração — em particular a variação da fração de
contemplações por lance entre grupos de tamanhos, prazos e segmentos distintos.
→ **Testada nas seções 7.1 e 7.2.**

**H3 — Dominância de desenho alternativo.** Existe ao menos um desenho alternativo de
contemplação, admissível sob as restrições da regulação vigente, que domina o desenho atual em
pelo menos um critério sem deteriorar os demais; e essa ordenação é robusta à incerteza de
calibração compatível com os dados observados. → **Testada nas seções 7.4 e 7.5.**

**Dependência entre hipóteses.** A rejeição de H2 invalida o uso do modelo para fins
prescritivos e retira sustentação a H3 — razão pela qual a validação antecede a comparação
entre desenhos no desenvolvimento. H1 é independente das outras duas: sua rejeição não
compromete a tese, apenas reduz a contribuição metodológica.

**Estatuto de H1 após o corte de 12/09.** H1 passa a ser testada por um experimento único de
aprendizado por reforço sobre o ambiente já calibrado, e não por agentes que aprendem dentro do
laço de calibração. Isso precisa estar dito em 6.2 e reconhecido como limitação em 8.3.

## 4. O que este trabalho NÃO é

Seção mais importante do arquivo. Toda vez que alguém — você ou a IA — propuser ampliar escopo,
confira aqui primeiro.

- NÃO é um estudo jurídico da Lei 11.795/2008. A norma entra como restrição do espaço de
  desenhos admissíveis, não como objeto de interpretação.
- NÃO é uma proposta de reforma regulatória com redação normativa.
- NÃO reivindica estimar a distribuição individual de lances — dado não observável nas bases
  públicas. Reivindica identificar parâmetros comportamentais a partir de agregados.
- NÃO é um sistema de software para administradoras.
- NÃO modela o mercado secundário de cotas.
- NÃO modela a concorrência entre administradoras nem a formação de grupos.
- NÃO trata a taxa de administração nem o fundo de reserva como variáveis de escolha.
- NÃO cobre todos os segmentos: restringe-se a **imóveis**, no regime **posterior à
  Res. BCB 285/2023**. Demais segmentos e regimes, se entrarem, entram como sensibilidade.
- NÃO produz recomendação de investimento nem avaliação de administradora específica.

## 5. Notação canônica

Versão inicial, derivada de `text/02-5-formalizacao.md`. **Congela ao fim da Semana 1**
(sex 18/09). Até lá, alterar aqui é barato; depois, exige registro em `ESTADO.md` §4.
Nenhum símbolo aparece em qualquer capítulo sem estar nesta tabela.

### Grupo, tempo e cota

| Símbolo | Significado | Domínio/unidade |
|---|---|---|
| $N$ | Número de cotas do grupo | $\mathbb{N}$, cotas |
| $T$ | Prazo do grupo | $\mathbb{N}$, assembleias (meses) |
| $t$ | Índice da assembleia | $\{1,\dots,T\}$ |
| $i$ | Índice do participante | $\{1,\dots,N\}$ |
| $C$ | Valor do crédito da cota | R$, normalizado a $1$ no modelo |
| $p$ | Parcela mensal | fração de $C$ |
| $\tau_a$ | Taxa de administração | fração de $C$ |
| $\tau_r$ | Fundo de reserva | fração de $C$ |

### Tipos (informação privada)

| Símbolo | Significado | Domínio/unidade |
|---|---|---|
| $\theta_i$ | Urgência do participante $i$ na antecipação do crédito | $\mathbb{R}_{>0}$ |
| $\delta_i$ | Fator de desconto implícito, $\delta_i = e^{-\theta_i}$ | $(0,1)$ |
| $\lambda_{i,t}$ | Liquidez disponível de $i$ em $t$ para antecipar parcelas | fração de $C$ |
| $F_\theta,\ F_\lambda$ | Distribuições dos tipos na população do grupo | — |

### Estado

| Símbolo | Significado | Domínio/unidade |
|---|---|---|
| $R_t$ | Saldo do fundo comum no início da assembleia $t$ | fração de $C$ |
| $A_t$ | Conjunto de cotas ativas e adimplentes em $t$ | $\subseteq\{1,\dots,N\}$ |
| $n_t$ | Cardinalidade de $A_t$ | $\mathbb{N}$ |
| $K_t$ | Cotas já contempladas até $t$ | $\mathbb{N}$ |
| $X_t$ | Cotas excluídas aguardando restituição | $\mathbb{N}$ |
| $s_t$ | Estado agregado, $s_t=(R_t,n_t,K_t,X_t,t)$ | — |
| $z_{i,t}$ | Estado individual de $i$ (contemplação, parcelas pagas, liquidez) | — |

### Ações e mecanismo

| Símbolo | Significado | Domínio/unidade |
|---|---|---|
| $b_{i,t}$ | Lance ofertado por $i$ em $t$ | $[0,\bar b_{i,t}]$, **percentual do próprio crédito** |
| $\bar b_{i,t}$ | Lance máximo viável dada a liquidez | fração de $C$ |
| $m_{i,t}$ | Modalidade do lance | $\{\text{livre},\text{embutido}\}$ |
| $g_t$ | Número de vagas de contemplação em $t$ (endógeno a $R_t$) | $\mathbb{N}_0$ |
| $g^s_t,\ g^b_t$ | Vagas por sorteio e por lance, $g^s_t+g^b_t=g_t$ | $\mathbb{N}_0$ |
| $M$ | Mecanismo de contemplação: regra $(s_t,\{b_{i,t}\})\mapsto$ conjunto de contemplados | — |
| $M_0$ | Mecanismo vigente (sorteio com precedência, seguido de lance) | — |
| $M_1,M_2,\dots$ | Desenhos alternativos avaliados no Capítulo 7 | — |

### Comportamento e calibração

| Símbolo | Significado | Domínio/unidade |
|---|---|---|
| $\pi_\phi$ | Política de lance paramétrica | $\pi_\phi:(z_{i,t},s_t)\mapsto b_{i,t}$ |
| $\phi$ | Vetor de parâmetros comportamentais | $\mathbb{R}^{d_\phi}$, $d_\phi\le 4$ |
| $\Theta$ | Vetor de parâmetros estruturais a calibrar, $\Theta=(\phi,F_\theta,F_\lambda)$ | — |
| $\hat{\mu}$ | Vetor de momentos empíricos (dados do Bacen) | $\mathbb{R}^{d_\mu}$ |
| $\tilde{\mu}(\Theta)$ | Vetor de momentos simulados | $\mathbb{R}^{d_\mu}$ |
| $\Omega$ | Matriz de pesos do SMM | $\mathbb{R}^{d_\mu\times d_\mu}$, p.s.d. |
| $Q(\Theta)$ | Função objetivo, $(\hat\mu-\tilde\mu)^\top\Omega(\hat\mu-\tilde\mu)$ | $\mathbb{R}_{\ge0}$ |
| $\mu^{\text{cal}},\ \mu^{\text{tes}}$ | Partição dos momentos: calibração e teste (definida antes de ver ajuste) | — |

### Critérios de avaliação

| Símbolo | Significado | Domínio/unidade |
|---|---|---|
| $U_i$ | Utilidade realizada do participante $i$ | unidades de $C$ |
| $\mathcal{W}(M)$ | Bem-estar agregado dos participantes sob o mecanismo $M$ | unidades de $C$ |
| $\mathcal{E}(M)$ | Dispersão do tempo de espera até a contemplação | assembleias |
| $\mathcal{S}(M)$ | Estabilidade financeira do grupo | ver definição em 4.4 |
| $w_i$ | Tempo de espera de $i$ até a contemplação | assembleias |

**Convenções.** Índice $i$ sempre participante, $t$ sempre assembleia. Valores monetários
sempre em fração do crédito $C$, nunca em reais, exceto em tabelas descritivas do Capítulo 5.
Lance sempre em percentual do próprio crédito — decorre do critério de desempate percentual
registrado em `ESTADO.md` §5.

## 6. Fontes de dados

| Fonte | Conteúdo | Periodicidade | Caminho local |
|---|---|---|---|
| Bacen — Banco de dados de consórcios | Doc. 4010/2080 (grupos, por administradora), Doc. 4110 (recursos por grupo), Dados por UF (contemplados por lance/sorteio) | Mensal e trimestral, desde 1997 | `data/raw/bacen/` |
| ABAC | Estatísticas agregadas do setor | Mensal | `data/raw/abac/` |

**Recorte adotado.** Segmento imóveis; período a partir de 01/01/2024 (vigência da
Res. BCB 285/2023). Séries anteriores são carregadas no painel mas marcadas por regime, e não
entram na calibração.

## 7. Convenções de escrita

- Norma: ABNT, conforme diretrizes da POLI-USP. Detalhe em `docs/GUIA-ABNT.md`.
- Cadeia de produção: markdown em `text/` → pandoc → LaTeX abnTeX2 → PDF.
- Idioma: português brasileiro. Resumo também em inglês.
- Voz: impessoal ("este trabalho propõe"), nunca primeira pessoa. Sem adjetivo valorativo.
- A Introdução **não antecipa resultados** — exigência expressa da EPUSP.
- Citação: sintaxe pandoc `[@chave2020]`, resolvida por `refs/refs.bib` e `refs/abnt.csl`.
- Matemática em LaTeX inline (`$x$`) e display (`$$`), compatível com pandoc.
- Figuras e tabelas: legenda acima em tabelas, abaixo em figuras; toda figura referenciada no
  texto antes de aparecer.
- Um arquivo `.md` por seção em `text/`, nomeado `NN-nome.md`, com frontmatter completo.

## 8. Instruções permanentes para a IA

1. **Nunca inventar referência bibliográfica.** Se a chave não existe em `refs/refs.bib` com PDF
   correspondente em `refs/pdfs/`, não cite. Se precisar de uma referência que não existe,
   escreva `[CITAR: descrição do que falta]`.
2. **Nunca inventar número de resultado.** Todo número no texto vem de um arquivo em `results/`.
   Se o resultado não existe ainda, escreva `[RESULTADO PENDENTE: qual]`.
3. **Usar exclusivamente a notação da seção 5.** Símbolo novo entra na tabela antes de aparecer
   no texto. Depois de 18/09, entrar na tabela exige decisão registrada.
4. **Respeitar o log de decisões** em `ESTADO.md` §4. Decisão registrada não se rediscute sem
   registrar a reabertura.
5. **Sinalizar mudança de escopo explicitamente.** Se a sugestão viola a seção 4 deste arquivo
   ou o corte de escopo em `docs/PLANO.md` §1, dizer isso antes de qualquer outra coisa.
6. **Checar insumos antes de escrever.** Se a seção depende de material que não está em disco,
   devolver a lista do que falta em vez do texto.
7. Preferir dizer "não sei" a produzir texto plausível sem lastro.
8. **Voz da monografia é distinta da voz da conversa.** No texto, impessoal e formal; e sem
   trejeitos de texto gerado — nada de "é importante notar", "vale destacar", listas de três
   adjetivos, ou parágrafo que abre anunciando o que o parágrafo vai dizer.
