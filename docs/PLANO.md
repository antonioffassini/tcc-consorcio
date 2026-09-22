# Plano Operacional do TCC — 30 dias

Documento de execução. Substitui integralmente o plano de 14 semanas de 12/09/2026 (manhã).
O que mudou e por quê está no log de decisões, `ESTADO.md` §4.

**Entrega alvo: 12/10/2026.** Meta de ritmo, não contrato. Se escorregar, escorrega
para 26/10 — não para dezembro. A função do prazo curto é forçar as decisões de corte
agora, no dia 1, em vez de na sexta semana.

---

## 0. Premissas

- **Horizonte:** 30 dias corridos a partir de 12/09/2026.
- **Equipe:** três autores, todos com dedicação parcial (estágio e disciplinas em curso).
  Orçamento realista: **~36 pessoa-dia**. Escopo cortado para caber em ~44. A diferença
  é conhecida e sai das reservas do Bloco IV.
- **Aprovação do tema deixou de ser gate.** A conversa com o Prof. Cugnasca em
  **segunda, 14/09**, é apresentação de proposta com trabalho feito, não pedido de licença.
  O que ela pode produzir é ajuste de escopo, não bloqueio.
- **Formato final:** markdown em `text/` → pandoc → LaTeX abnTeX2 → PDF.
- **Ferramentas:** Claude Code local como camada de produção; Cowork/chat como camada de
  julgamento e pesquisa; Git obrigatório desde o dia 1.

---

## 1. O corte de escopo

Decidido em 12/09/2026. Reabrir qualquer linha desta tabela exige registro em `ESTADO.md` §4.

| Item | Desenho anterior | Desenho adotado | Por quê | Economia |
|---|---|---|---|---|
| Agentes na calibração | RL treinado dentro do loop de SMM | **Política de lance paramétrica** (3–4 parâmetros) | O loop aninhado — treinar até convergir a cada avaliação da função objetivo — é semanas de CPU em notebook e o único risco do projeto que não tem mitigação barata | ~10 p-d + o risco computacional inteiro |
| RL | Núcleo do método | **Experimento único** sobre o ambiente já calibrado, para testar H1 | H1 é sobre divergência entre agentes que aprendem e equilíbrio estático; isso se testa com um treinamento, não com mil | — |
| Cobertura empírica | Todos os segmentos, todos os regimes | **Imóveis, regime pós-Res. BCB 285/2023** | Um regime evita ter de modelar a quebra normativa de 01/01/2024 dentro do painel | ~5 p-d |
| Capítulo 3 | Revisão sistemática PRISMA | **Revisão narrativa com busca documentada e exaustiva** | A busca é barata e sustenta a afirmação de ineditismo em 3.6; o que custa é ler 25 artigos a fundo. 12 a fundo, ~15 instrumentais | ~6 p-d |
| Extensão | ~100 páginas | **~70 páginas** | Alvo por seção revisado no `docs/estrutura.tsv` | ~4 p-d |

**O que o corte não toca:** a validação (6.4, 6.5) e a robustez da ordenação entre
mecanismos (7.5). Cortar validação é cortar a tese — se atrasar, corta-se mecanismo
alternativo comparado no cap. 7, nunca validação.

**Consequência sobre as hipóteses.** H1 passa a ser testada por um experimento isolado e
declaradamente não calibrado por SMM; isso precisa estar dito em 6.2 e reconhecido em 8.3.
H2 e H3 ficam intactas — e são elas que sustentam a tese.

---

## 2. Arquitetura de execução: spike vertical

O plano anterior era horizontal: fechar dados, depois modelo, depois calibração, depois
resultados. Em 30 dias isso é suicídio, porque o risco fatal — *o pipeline inteiro não
fecha* — só apareceria no dia 25.

O plano novo é vertical. **Até o dia 15 existe uma versão completa e feia de tudo:**
painel com uma data-base, modelo com dois agentes e um mecanismo alternativo, SMM com dois
momentos, uma tabela em `results/`, um PDF compilando. Feio, mas ponta a ponta. Só depois
disso é que cada camada engorda.

Regra prática que decorre disso: **nada é feito "direito" antes de existir na versão feia.**
Se você está refinando um componente e o `make all` ainda não roda do zero, você está no
lugar errado do plano.

---

## 3. Calendário

### D0 — sáb 12/09 e dom 13/09: o pacote de segunda

Objetivo único: chegar na segunda com artefato, não com ideia. O que o orientador precisa
receber em mãos:

- [ ] **Proposta de TCC, 4–6 páginas**, em PDF: contextualização, problema, pergunta,
      hipóteses, objetivos, método em uma página, cronograma de 30 dias, e uma seção
      explícita sobre o abandono do tema anterior e o que dele foi reaproveitado.
- [ ] **`CONTEXT.md` fechado** — tese, pergunta, H1–H3, escopo excluído, notação canônica.
- [ ] **Capítulos 1 e 2 impressos** como estão (rascunho de ~25 páginas). É o que dá
      credibilidade: não é uma mudança de tema, é uma mudança de tema com dois capítulos escritos.
- [ ] **`docs/BIBLIOGRAFIA.md`** com as 22 referências e o status de cada uma.
- [ ] Este plano.

Nada de código é necessário para segunda. Não gaste o fim de semana em pipeline.

### S1 — 14 a 20/09: dados e formalização, em paralelo

| Dia | Trilha A (dados) | Trilha B (modelo) | Trilha C (infra + calibração) |
|---|---|---|---|
| Seg 14 | Apresentação ao Cugnasca (os três) | idem | idem |
| Seg 14 | Baixar todas as datas-base do Bacen para `data/raw/bacen/` | Ler Klonner 2003/2008 e Athey-Haile | Setup: Git, GitHub, venv, pandoc, abnTeX2, Claude Code |
| Ter 15 | `make painel` rodando com uma data-base | Rascunhar 4.1 e 4.2 à mão | `refs/abnt.csl`, template abnTeX2 compilando com texto de teste |
| Qua 16 | Painel completo, `results/qualidade_dados.csv` | 4.3 — espaço de mecanismos alternativos | Baixar os 22 PDFs para `refs/pdfs/`; `make auditoria` zerando nos caps. 1–2 |
| Qui 17 | **Fatos estilizados: fração lance/sorteio por tamanho, prazo e tempo** | 4.4 — critérios de avaliação | Esqueleto de `src/`: ambiente, agente, runner |
| Sex 18 | **G1** (ver §4) | 4.5 — escopo do modelo | Interface contratada: esquema do painel e assinatura do ambiente, por escrito no log |
| Sáb–dom | Momentos-alvo definidos e separados em calibração vs. teste | Cap. 4 completo em rascunho | Ambiente rodando com agentes aleatórios |

A separação entre momentos de calibração e momentos de teste é decidida **nesta semana,
antes de ver qualquer ajuste**. Decidir depois é ajuste disfarçado de validação, e a banca
pergunta.

### S2 — 21 a 27/09: o spike fecha

- Política de lance paramétrica implementada, com casos-limite analíticos como teste.
- SMM: função objetivo, matriz de pesos, otimizador. Dois momentos primeiro, o resto depois.
- Um mecanismo alternativo implementado, o mais simples (sugestão: sorteio ponderado por
  tempo de espera — barato de implementar, defensável, e já rompe a lógica atual).
- `results/` com a primeira tabela real.
- `make all` roda do zero.
- **G2 no domingo 27.**

### S3 — 28/09 a 04/10: enriquecimento e congelamento

- Demais mecanismos alternativos (alvo: 3 no total, incluindo o vigente).
- Sobre-identificação: ajuste nos momentos reservados. **Se o modelo falha aqui, isso é
  resultado e vai no texto** — não é motivo para mexer no modelo até passar.
- Experimento de RL para H1, uma configuração, seed fixa.
- Robustez: varredura do espaço de parâmetros, verificar se a ordenação entre mecanismos
  se mantém.
- **G3 sexta 02/10 à noite: congelamento.** Tudo em `results/` vira imutável.
- Sábado e domingo: redação dos capítulos 5 e 6, que já têm insumo em disco.

### S4 — 05 a 11/10: redação em massa e fechamento

- Seg a qua: capítulos 3, 7, 8 e 9. Com resultado congelado, é a fase rápida — foi para
  isso que a infraestrutura existe.
- Qui 08: P7 (coerência global) e P5 (adversarial) nas seis seções críticas: 3.6, 4.4,
  5.5, 6.4, 7.5, 8.3.
- Sex 09: pré-textuais, resumo em português e inglês, listas, sumário. Compilação abnTeX2 final.
- Sáb 10: **G4**. Auditoria estrita zerada, PDF compilando, checklist §9 completo.
- Dom 11: folga de contingência. Se estiver usando esse dia como planejado, algo deu certo.
- **Seg 12/10: entrega.**

---

## 4. Gates

Quatro, todos com critério objetivo e ação definida em caso de falha.

**G0 — dom 13/09.** Pacote de segunda pronto.
*Falha:* apresentar sem a proposta em PDF é o pior cenário possível para a credibilidade
da troca de tema. Não falhe este.

**G1 — sex 18/09. O painel identifica os parâmetros?**
Critério: existe variação observável na fração de contemplações por lance entre grupos de
tamanhos, prazos e datas distintas, no segmento imóveis, pós-2024.
*Falha:* não migrar de tema — não há prazo para isso. Migrar de **objeto**: passar de
estimação estrutural para **calibração por alvos declarados** (parâmetros fixados por
literatura e por dados agregados, sem SMM), e reescrever H2 como afirmação de consistência
e não de identificação. Custa um dia de reescrita e salva o cronograma.

**G2 — dom 27/09. `make all` roda do zero e produz uma tabela real.**
*Falha:* cortar o mecanismo alternativo mais caro e o experimento de RL, nessa ordem.
H1 vira trabalho futuro no cap. 9. Doloroso, não fatal.

**G3 — sex 02/10. Congelamento.**
Sem exceção. Todo experimento novo depois desta data é rejeitado, por melhor que pareça.
É a regra que faz o TCC fechar.

**G4 — sáb 10/10.** `python scripts/audit.py --strict` retorna zero, PDF compila,
todo arquivo em `text/` com `status: fechado`.

---

## 5. Trilhas

Mantida a divisão vertical do plano anterior — ela é o que evita dois autores ociosos —
com os limites redesenhados para o escopo cortado.

| Trilha | Escopo | Capítulos | Entregável próprio |
|---|---|---|---|
| **A — Dados** | Pipeline Bacen, painel, fatos estilizados, momentos-alvo, qualidade | 5 inteiro | `data/processed/painel.parquet` + `results/qualidade_dados.csv` |
| **B — Modelo** | Formalização, ambiente, agentes paramétricos, casos-limite, RL | 4 e 6.1–6.2, 6.4 | Ambiente com testes analíticos passando |
| **C — Calibração e resultados** | SMM, sobre-identificação, varredura, robustez, infra de build | 6.3, 6.5, 7 inteiro | `results/` completo + PDF compilando |

Capítulos 1, 2, 3, 8 e 9 são compartilhados, com responsável nomeado no frontmatter de
cada seção. **Preencher o campo `responsavel` de todas as 42 seções é tarefa da segunda-feira** —
seção sem dono não é escrita.

**As duas interfaces contratadas** (esquema do painel de A para C; assinatura do ambiente de
B para C) têm prazo: **sexta 18/09, por escrito, no log**. Sem isso, A e B trabalham uma
semana e não encaixam.

---

## 6. O loop de seção

Comprimido em relação ao plano anterior, porque 42 × 4 passos não cabe em 30 dias.

- **Seções comuns (36):** P0 → P4 → auditoria. Sem P5.
- **Seções críticas (6):** 3.6, 4.4, 5.5, 6.4, 7.5, 8.3 — ciclo completo, com P5.
  São as seis por onde a banca ataca.
- **Seções já em rascunho (9):** revisão de coerência com o `CONTEXT.md` fechado e
  promoção a `fechado`. Não reescrever.

Orçamento por seção: 30–45 min nas expositivas, 2–3 h nas críticas.

---

## 7. Cadência

Diária, não semanal — em 30 dias o ciclo semanal perde três oportunidades de correção.

- **Todo dia, 15 min, por escrito no grupo:** o que fechou, o que travou, o que precisa da
  outra trilha.
- **Todo dia, ao parar:** commit. Auditoria antes do commit se tocou em `text/`.
- **Toda decisão, na hora:** `ESTADO.md` §4. Decisão não registrada é decisão que será
  redecidida diferente daqui a dez dias, e aí os capítulos discordam entre si.
- **Orientador:** segunda 14/09 (proposta), sexta 25/09 (cap. 4 + fatos estilizados),
  sexta 09/10 (versão completa). Sempre com arquivo, nunca com "estamos avançando".

---

## 8. Modos de falha

| Falha | Sintoma precoce | Mitigação |
|---|---|---|
| Orientador rejeita o tema na segunda | — | Pacote D0 completo; e ter pronta a resposta sobre por que é Engenharia de Computação e não Economia: o objeto é o **mecanismo** e o método é **simulação multiagente e estimação computacional** |
| Dado do Bacen não identifica | Fatos estilizados sem variação | G1 na sexta da S1, com saída para calibração por alvos declarados |
| Spike não fecha | `make all` quebrado no dia 27 | G2, com corte de mecanismo e de RL |
| Dois autores desengajam | Trilha sem commit por três dias | Cadência diária; escalar na primeira semana |
| Referência alucinada | Citação sem PDF | `audit.py` no `make`, antes de todo commit |
| Número inventado | Número na prosa sem CSV declarado | Idem, mais o campo `excecoes` no frontmatter |
| Escopo infla | Ideia nova na S3 | §1 desta tabela e `CONTEXT.md` §4, lidos antes de aceitar |
| abnTeX2 não compila no dia 9 | Template só testado no fim | Template compilando com texto de teste na **terça 15/09**, não em outubro |
| TCC não fecha | Experimento rodando na S4 | G3, sem exceção |

---

## 9. Checklist de entrega

- [ ] `make all` roda do zero, com `data/processed` e `results` limpos, e reproduz tudo
- [ ] `python scripts/audit.py --strict` retorna zero
- [ ] Todo arquivo em `text/` com `status: fechado`
- [ ] Toda hipótese do 1.3 tem experimento correspondente no cap. 7
- [ ] Toda contribuição do 1.5 é entregue por uma seção nomeável
- [ ] Toda limitação do 8.3 é compatível com o que os capítulos anteriores afirmam
- [ ] Todo PDF citado está em `refs/pdfs/`
- [ ] Log de decisões completo e datado
- [ ] PDF abnTeX2 conforme `docs/GUIA-ABNT.md`, conferido contra a norma da unidade
- [ ] Repositório arquivado e referenciado na monografia

---

## 10. O que fazer agora, neste fim de semana

1. Renomear a pasta para `C:\Users\anton\Documents\tcc-consorcio` (sem acento, sem espaço,
   sem aninhamento duplicado).
2. Fechar o `CONTEXT.md`.
3. Montar a proposta de 4–6 páginas para segunda.
4. Instalar Git, GitHub CLI, Python, pandoc, abnTeX2 e Claude Code; primeiro commit e push.
5. Preencher `responsavel` nas 42 seções e mandar as trilhas para os outros dois **hoje**,
   não na segunda depois da reunião.
