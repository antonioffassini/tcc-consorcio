# ESTADO DO PROJETO

> **Documento vivo.** Atualizado ao longo de toda sessão de trabalho, não só no fim.
> Registra o que mudou: progresso, decisões, pendências.
> O que não muda (tese, notação, escopo) fica em `CONTEXT.md`.
> Bibliografia tem controle próprio em `docs/BIBLIOGRAFIA.md`.

**Última atualização:** 12/09/2026 — sessão Cowork (replanejamento para 30 dias)

---

## 1. Onde estamos

| Item | Situação |
|---|---|
| Prazo alvo | **12/10/2026** — 30 dias |
| Fase do plano | D0 — pacote de apresentação ao orientador |
| Marco imediato | **Segunda, 14/09**: apresentar a troca de tema ao Prof. Cugnasca, com proposta escrita em mãos |
| Gate pendente | **G0** (dom 13/09) — proposta em PDF, `CONTEXT.md` fechado, caps. 1–2 impressos |
| Tema | Tema 4 (consórcios), escolhido e assumido |
| Bloqueio principal | `CONTEXT.md` ainda em `PREENCHER`; ambiente local não configurado |
| Risco mais próximo | G1 (sex 18/09) — o painel do Bacen identifica os parâmetros? |

## 2. O que está pronto

**Infraestrutura**
- Repositório montado, 81 arquivos, estrutura completa
- `scripts/audit.py` funcionando e testado contra caso quebrado proposital
- `Makefile` com alvos: painel, experimentos, resultados, auditoria, docx
- `scripts/gen_skeleton.py` regenera `text/` a partir de `docs/estrutura.tsv`
- 42 seções esqueletadas com frontmatter (status, insumos, fontes, exceções)
- Biblioteca de 8 prompts em `prompts/` (P0 a P7), cada um com contrato de saída

**Texto escrito (status: rascunho)**
- 1.1 Contexto e relevância econômica
- 1.2 Problema de pesquisa
- 1.3 Hipóteses
- 1.4 Objetivos
- 2.1 Mecânica do grupo
- 2.2 Contemplação por sorteio e por lance
- 2.3 Arcabouço regulatório
- 2.4 Inadimplência, desistência e efeitos sobre o grupo
- 2.5 O consórcio como jogo dinâmico de alocação

**Documentos de apoio**
- `docs/PLANO.md` — plano operacional de 30 dias, spike vertical, 4 gates *(reescrito em 12/09)*
- `docs/GUIA-ABNT.md` — normas ABNT/EPUSP consolidadas
- `docs/BIBLIOGRAFIA.md` — 17 referências verificadas, 8 candidatas
- `docs/estrutura.tsv` — manifesto das seções
- `refs/refs.bib` — 22 entradas

## 3. O que está travado

| Pendência | Bloqueia | Prazo |
|---|---|---|
| `CONTEXT.md` inteiro em `PREENCHER` — tese, pergunta, hipóteses, notação canônica | G0; P0 de qualquer seção nova; coerência dos caps. 1–2 já escritos | dom 13/09 |
| Proposta de 4–6 páginas para o orientador | G0 | dom 13/09 |
| Pasta com acento, espaço e aninhamento duplicado (`TCC - Consórcio/tcc-consórcio`) | Scripts bash, `pandoc text/*.md`, caminho LaTeX | sáb 12/09 |
| Ambiente local: Git, GitHub, Python, pandoc, abnTeX2, Claude Code | Tudo a partir da segunda | seg 14/09 |
| `refs/abnt.csl` e template abnTeX2 inexistentes — `make docx` falha hoje | Compilação da monografia | ter 15/09 |
| 22 PDFs faltando em `refs/pdfs/` (a pasta está vazia) | Auditoria zerar; caps. 1–2 fecharem | qua 16/09 |
| CSVs do Bacen não baixados; `data/raw/` vazia | G1, cap. 5, todo o cap. 7 | seg 14/09 |
| Campo `responsavel` vazio nas 42 seções | Divisão em trilhas | seg 14/09 |
| Adesão dos dois coautores ao tema e às trilhas | Execução em paralelo | sáb 12/09 |
| `docs/monografia-esqueleto-completo.md` duplica `text/` e vai divergir | Fonte única de verdade | S1 |
| Confirmar se Res. BCB 285/2023 preservou precedência sorteio→lance e lance embutido | Formalização do cap. 4 | qua 16/09 |
| Confirmar situação do art. 30 da Lei 11.795 (veto parcial, discussão com CDC) | Modelagem da restituição | S1 |
| Confirmar as 3 referências de SMM (Gouriéroux-Monfort-Renault; McFadden; Duffie-Singleton) | Cap. 6.3 | S2 |
| Esgotar BDTD, Teses USP, CAPES, SciELO, SPELL e working papers do BCB | Afirmação de ineditismo em 3.6 | S1 |

## 4. Log de decisões

Formato: `data — decisão — motivo — quem`

- **2026-09-12 — Abandonar o tema estufa inteligente** — a disciplina de Laboratório de Sistemas Embarcados usa protótipos didáticos simples, então a otimização de reaproveitamento não se justificava; o orientador já questionava profundidade e escopo — Pedro
- **2026-09-12 — Reaproveitar a parte física da estufa (~15-20%) na disciplina de embarcados** — o trabalho feito não se perde, muda de destino — Pedro
- **2026-09-12 — Escolher o Tema 4 (desenho de mecanismo em consórcios)** — entre os quatro do catálogo; dado do Bacen melhor que o previsto, originalidade alta — Pedro
- **2026-09-12 — Escrever a monografia em markdown com geração por pandoc** — preserva diff, versionamento e reprodutibilidade; Word direto perde as três coisas — Claude, aceito por Pedro
- **2026-09-12 — Adotar auditoria de ancoragem como condição de entrega** — nenhum número sem célula em `results/`, nenhuma citação sem PDF em `refs/pdfs/` — Claude, aceito por Pedro
- **2026-09-12 — Dividir o trabalho em trilhas verticais (Dados / Modelo / Calibração)** — evita dois coautores ociosos esperando o terceiro — Claude, aceito por Pedro *(pendente de acordo com os coautores)*
- **2026-09-12 — Migrar de chat para projeto Claude em modo Cowork com pasta local vinculada** — elimina o ciclo de zip e download; o repositório passa a ser editado no lugar — Pedro
- **2026-09-12 — Prazo alvo de 30 dias (entrega 12/10/2026)** — meta de ritmo, não contrato; a função é forçar as decisões de corte no dia 1 em vez de na sexta semana — Pedro
- **2026-09-12 — A aprovação do tema pelo orientador deixa de ser gate** — a reunião de segunda 14/09 é apresentação de proposta com trabalho feito, não pedido de licença; o que ela pode produzir é ajuste de escopo, não bloqueio — Pedro
- **2026-09-12 — Corte de escopo agressivo, em cinco linhas** — o orçamento realista da equipe é ~36 pessoa-dia contra ~65 de escopo integral; sem corte a meta é ficção. As cinco linhas estão em `docs/PLANO.md` §1 — Claude, aceito por Pedro
- **2026-09-12 — Agentes paramétricos na calibração; RL fora do loop de SMM** — o loop aninhado (treinar até convergir a cada avaliação da função objetivo) é o único risco do projeto sem mitigação barata; RL passa a ser um experimento único sobre o ambiente calibrado, destinado a H1 — Claude, aceito por Pedro
- **2026-09-12 — Restringir a um segmento (imóveis) e um regime (pós-Res. BCB 285/2023)** — evita modelar a quebra normativa de 01/01/2024 dentro do painel — Claude, aceito por Pedro
- **2026-09-12 — Capítulo 3 vira revisão narrativa com busca documentada, não PRISMA** — a busca exaustiva é barata e sustenta o ineditismo em 3.6; o custo está em ler 25 artigos a fundo — Claude, aceito por Pedro
- **2026-09-12 — Alvo de extensão reduzido de ~100 para ~70 páginas** — `docs/estrutura.tsv` precisa ser revisado de acordo — Pedro
- **2026-09-12 — Formato final por pandoc → LaTeX abnTeX2** — fidelidade ABNT máxima e resolve os pré-textuais, ao custo de instalar TeX nas três máquinas; o template precisa compilar já na terça 15/09, não em outubro — Pedro
- **2026-09-12 — Plano de execução em spike vertical** — versão completa e feia de ponta a ponta até 27/09, e só depois enriquecimento; em 30 dias o plano horizontal só revelaria o risco fatal no dia 25 — Claude, aceito por Pedro

## 5. Achados que mudam o modelo

Registrados aqui porque são caros de redescobrir e afetam o Capítulo 4.

1. **Número de contemplações por lance é endógeno ao fundo.** A contemplação está condicionada à existência de recursos suficientes no grupo (art. 23 da Lei 11.795/2008). O prêmio disputado não é fixo: é um número estocástico de vagas.
2. **Precedência do sorteio sobre o lance.** Sob a Circular 3.432/2009 (art. 8º), a contemplação por lance só ocorre após a por sorteio, ou se esta não se realizar por insuficiência de recursos. O lance disputa recurso residual. *Verificar na Res. 285/2023.*
3. **Lance embutido** (art. 9º da Circular 3.432/2009) — oferta contra parte do próprio crédito a ser distribuído. Existem duas tecnologias de lance com custos de oportunidade distintos; a restrição de liquidez não é absoluta.
4. **Critério de desempate percentual.** Em grupos com créditos diferenciados (mínimo de 50% do maior), o desempate pode se dar pelo maior percentual do próprio crédito. A ação natural do agente é percentual, não valor em reais.
5. **Excluídos continuam nos sorteios.** A restituição ao excluído ocorre mediante contemplação em sorteio ou no encerramento do grupo. O conjunto que disputa o sorteio não coincide com o que pode receber crédito — e ambos consomem o mesmo fundo.
6. **Quebra de regime em 01/01/2024.** A Res. BCB 285/2023 revogou integralmente a Circular 3.432/2009. O painel atravessa ao menos três regimes normativos. *Contornado pela decisão de 12/09 de restringir ao regime pós-2024.*

## 6. Próximos passos acordados

Fim de semana (12–13/09), na ordem:

1. Renomear a pasta para `C:\Users\anton\Documents\tcc-consorcio`
2. Fechar o `CONTEXT.md` — tese, pergunta, H1–H3, escopo excluído, notação canônica
3. Montar a proposta de 4–6 páginas em PDF para a reunião de segunda
4. Instalar Git, GitHub CLI, Python, pandoc, abnTeX2 e Claude Code; `git init` e primeiro push
5. Preencher `responsavel` nas 42 seções e enviar as trilhas aos dois coautores
6. Revisar `docs/estrutura.tsv` para o alvo de ~70 páginas

Segunda-feira (14/09) em diante: cronograma em `docs/PLANO.md` §3.

## 7. Histórico de sessões

| Data | Superfície | O que aconteceu |
|---|---|---|
| 12/09/2026 | Chat | Troca de tema; catálogo de 4 temas; plano de remontagem; plano operacional de 14 semanas; repositório montado; guia ABNT; seções 1.1-1.4 e capítulo 2 escritos; bibliografia verificada; decisão de migrar para Cowork |
| 12/09/2026 | Cowork | Pasta vinculada e repositório auditado. Meta de 30 dias fixada; aprovação do orientador deixa de ser gate; corte de escopo em cinco linhas; RL sai do loop de SMM; abnTeX2 escolhido como formato final. `docs/PLANO.md` reescrito de 14 semanas para 30 dias em spike vertical. Levantados os buracos de infraestrutura: `refs/pdfs/` e `data/raw/` vazias, `refs/abnt.csl` e template inexistentes, `.git` ausente |
