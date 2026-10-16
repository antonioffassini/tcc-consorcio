# Plano Operacional do TCC — 13 dias

Documento de execução. Reescrito em 29/09/2026 sobre o plano de 30 dias de 12/09, cujo §1
(corte de escopo), §2 (spike vertical), §6, §8 e §9 continuam valendo. O que mudou e por quê
está no log de decisões, `ESTADO.md` §4.

**Entrega: segunda, 12/10/2026.** Mantida em 25/09. Não há reserva para escorregar.

---

## 0. Premissas

- **Horizonte:** 13 dias, de 29/09 a 12/10.
- **Produção no Claude Code** (código, testes, rascunhos); **autores** na decisão, revisão e
  orientador; **Cowork** na pesquisa, revisão adversarial e continuidade.
- **Formato final:** markdown em `text/` → pandoc → LaTeX abnTeX2 → PDF.
- **Dados em disco desde 25/09**; repositório no GitHub desde 29/09.

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
fecha* — só apareceria na véspera da entrega.

O plano novo é vertical. **Até 02/10 (G2) existe uma versão completa e feia de tudo:**
painel com uma data-base, modelo com dois agentes e um mecanismo alternativo, SMM com dois
momentos, uma tabela em `results/`, um PDF compilando. Feio, mas ponta a ponta. Só depois
disso é que cada camada engorda.

Regra prática que decorre disso: **nada é feito "direito" antes de existir na versão feia.**
Se você está refinando um componente e o `make all` ainda não roda do zero, você está no
lugar errado do plano.

---

## 3. Calendário — 13 dias (reescrito em 29/09)

O calendário de 30 dias (12/09) foi perdido na primeira quinzena: S1 não foi executada. A
entrega em 12/10 foi mantida (decisão de 25/09). Isso só fecha porque a produção passa para o
Claude Code: ele escreve o código e os rascunhos, e os autores decidem, revisam e atacam.
Qualquer dia que escorregar come a folga de domingo 11/10, e não a validação.

| Dia | Entrega | Onde | Gate |
|---|---|---|---|
| **Ter 29/09** | `src/pipeline/build_panel.py`: painel grupo×mês (imóveis) e administradora×UF×trimestre; `results/qualidade_dados.csv`, `results/fatos_fracao_lance.csv`, `results/g1_identificacao.csv`; testes | Claude Code | **G1 formal** |
| | `ESTADO.md` e este plano atualizados; normativos no git | Cowork / terminal | |
| **Qua 30/09** | Reformulação de H2 e partição dos momentos (calibração × teste), **antes de qualquer ajuste**; registro no `ESTADO.md` §4 | Autores + Cowork | |
| | Cap. 4 (4.1 a 4.5) em rascunho; notação do `CONTEXT.md` §5 congelada | Claude Code + revisão | |
| | Reunião com o orientador, se ele ainda não viu a troca de tema | Autores | |
| **Qui 01/10** | `src/sim`: ambiente do grupo sob M0 (sorteio com precedência → lance, vagas condicionadas ao fundo, excluídos no sorteio); testes de casos-limite analíticos | Claude Code | |
| **Sex 02/10** | Política de lance paramétrica (≤4 parâmetros); SMM com 2 momentos; M1 (sorteio ponderado por tempo de espera); primeira tabela em `results/`; `make all` roda do zero | Claude Code | **G2** |
| **Sáb 03/10** | M2; sobre-identificação nos momentos reservados | Claude Code + revisão | |
| **Dom 04/10** | Experimento de RL para H1 (uma configuração, seed fixa); varredura de robustez da ordenação; PDFs acadêmicos baixados (login USP) | Claude Code + autores | |
| **Seg 05/10** | **Congelamento**: `git tag G3-congelamento`; nada novo em `results/` depois disso | | **G3** |
| **Ter 06/10** | Caps. 5 (dados) e 6 (método), que já têm insumo em disco | Claude Code (P0→P4) + auditoria | |
| **Qua 07/10** | Caps. 3 (revisão) e 7 (resultados) | Claude Code + auditoria | |
| **Qui 08/10** | Caps. 8 e 9; 1.5 e 1.6; P7 (coerência global) | Claude Code + auditoria | |
| **Sex 09/10** | P5 (banca adversarial) nas 6 seções críticas: 3.6, 4.4, 5.5, 6.4, 7.5, 8.3; **reunião com o orientador com a versão completa** | Cowork (leitor independente) + autores | |
| **Sáb 10/10** | Pré-textuais, resumo e abstract, compilação abnTeX2, `audit.py --strict` zerado | Claude Code | **G4** |
| **Dom 11/10** | Folga para imprevistos | | |
| **Seg 12/10** | **Entrega** | | |

**Regra de corte, se algo atrasar:** sai primeiro o RL (H1 vira trabalho futuro), depois o
M2. A validação (casos-limite e sobre-identificação) e a robustez da ordenação nunca saem.

## 4. Gates

**G1 — ter 29/09. O painel identifica os parâmetros?**
Leitura exploratória de 25/09 (`ESTADO.md` §5, itens 7–8): lance e sorteio só aparecem separados
por administradora×UF×trimestre, e a variação da fração de lance é grande e quase toda **entre**
administradoras. Critério para passar: `results/g1_identificacao.csv` reproduz essa variação no
pipeline. *Falha:* calibração por alvos declarados, com H2 reescrita como consistência.

**G2 — sex 02/10.** `make all` roda do zero e produz uma tabela real.
*Falha:* cortar M2 e RL, nessa ordem.

**G3 — seg 05/10. Congelamento.** Tag no git. Nenhum experimento novo depois, sem exceção.

**G4 — sáb 10/10.** `python scripts/audit.py --strict` retorna zero, o PDF compila e todo
arquivo em `text/` está com `status: fechado`.

## 5. Divisão de trabalho

| Quem | Faz |
|---|---|
| **Claude Code** (VS Code, na pasta) | Código, testes, rascunho de seção (P0→P4), auditoria, commits |
| **Cowork** (claude.ai, projeto do TCC) | Busca e download de bibliografia e normativos; revisão adversarial (P5) como leitor independente; decisões de método; `ESTADO.md` |
| **Pedro e Antônio** | Decisões de modelagem e escopo; revisão de todo texto antes de `fechado`; orientador; PDFs atrás do login USP |
| **Pedro Paulo** | A definir; se entrar, fica com a trilha de dados (cap. 5) e com a revisão dos caps. 1–3 |

O que não se delega ao Claude: a partição dos momentos, os critérios de bem-estar e a decisão
de o que cortar. São as três escolhas que a banca vai perguntar quem fez e por quê.

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

- **Todo dia, ao parar:** auditoria (se tocou em `text/`), `ESTADO.md` atualizado, commit e push.
- **Toda decisão, na hora:** `ESTADO.md` §4.
- **Orientador:** esta semana, se ainda não viu o tema; sexta 09/10, com a versão completa. Sempre com arquivo em mãos.

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
| abnTeX2 não compila no dia 10 | Template só testado no fim | Template compilando com texto de teste até **seg 05/10** |
| TCC não fecha | Experimento rodando depois de 05/10 | G3, sem exceção |

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
