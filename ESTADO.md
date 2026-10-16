# ESTADO DO PROJETO

> **Documento vivo.** Atualizado ao longo de toda sessão de trabalho, não só no fim.
> Registra o que mudou: progresso, decisões, pendências.
> O que não muda (tese, notação, escopo) fica em `CONTEXT.md`.
> Bibliografia tem controle próprio em `docs/BIBLIOGRAFIA.md`.

**Última atualização:** 16/10/2026 — sessão Cowork (diagnóstico pós-prazo; apresentação da metodologia com cronograma proposto; prompt das etapas 1–3)

---

## 1. Onde estamos

| Item | Situação |
|---|---|
| Prazo | **12/10/2026 não foi cumprido.** Cronograma novo proposto em 16/10 (S1 19–23/10 a S7 30/11–04/12, em `docs/apresentacao-metodologia.pptx`, slide 14), **pendente de aprovação dos três autores e de confirmação da data final no calendário da EPUSP** |
| Fase | Início da parte técnica. Meta da semana 1 (19–23/10): pipeline e painéis (etapa 1), fatos e momentos (etapa 2), especificação do modelo / rascunho do cap. 4 (etapa 3) |
| Gates | G0 cumprido. G1 com leitura exploratória positiva no nível da administradora (§5, itens 7–8), ainda não formalizado em `results/`. As datas antigas de G2–G4 caducaram; pelo cronograma proposto, congelamento dos experimentos ao fim de S5 (20/11) |
| Dados | 236 arquivos do Bacen (2017-03 a 2026-05) em `data/raw/bacen/`, commitados |
| Repositório | `github.com/antonioffassini/tcc-consorcio`, privado, 2 commits (29/09) |
| Código | `src/` vazio; `make painel` não roda. Confirmado por Pedro em 16/10: não existe pipeline feito pelo Claude Code em outro computador |
| Orientador | Caps. 1–2 lidos pelo Prof. Cugnasca (09/10): texto confuso. Cap. 1 reescrito e apresentado na semana de 12/10 com boa recepção; a parte de metodologia (1.7) ficou confusa na fala, o que motivou `docs/apresentacao-metodologia.pptx` (16/10) |
| Decisão pendente mais cara | Reformular H2 e os momentos-alvo para o grão administradora×trimestre (§3) |

## 2. O que está pronto

**Infraestrutura**
- Repositório com estrutura completa; no GitHub desde 29/09
- `scripts/audit.py` funcionando e testado contra caso quebrado proposital
- `Makefile` com os alvos painel, experimentos, resultados, auditoria e docx (os módulos de `src/` ainda não existem)
- `scripts/gen_skeleton.py`; 42 seções esqueletadas com frontmatter
- Biblioteca de 8 prompts em `prompts/` (P0 a P7)
- `docs/GIT.md`: guia operacional do git para o projeto (25/09)

**Dados** *(25/09, baixados do site do Bacen, página "Consórcios — Banco de dados")*
- `data/raw/bacen/AAAAMMConsorcios.zip`: 111 arquivos mensais, 2017-03 a 2026-05 (segmentos consolidados + grupos de imóveis + grupos de móveis nos trimestres)
- `data/raw/bacen/AAAAMMConsorcios_UF.zip`: 37 trimestrais, 2017-03 a 2026-03 (lance/sorteio por administradora×segmento×UF)
- `data/raw/bacen/AAAAMMConsorcios_ADM.zip`: 88 contábeis, 2017-03 a 2024-12 (Docs 4010/4110 consolidados)
- Integridade conferida (todos os zips abrem; nomes e tamanhos batem com o pacote)

**Normativos em `refs/pdfs/`** *(25/09, texto oficial do BCB e do Planalto convertido em PDF; fora do git por causa do `.gitignore`)*
- `brasil2008lei11795.pdf`, `bcb2023res285.pdf`, `bcb2023res362.pdf`, `bcb2009circ3432.pdf`, `bcb2024in525.pdf`, `bcb2024res381.pdf`

**Texto escrito (status: rascunho)**
- 1.1 a 1.9 (reescritos em 09/10, nova estrutura); 2.1 a 2.5

**Documentos de apoio**
- `docs/PLANO.md`: calendário de 13 dias *(reescrito em 29/09)*
- `docs/proposta-2026-09-14.md` + `build/proposta-tcc-consorcios.pdf`
- `docs/pitch-orientador.md`: roteiro de fala *(calendário desatualizado; usar o do PLANO)*
- `docs/apresentacao-projeto.pptx`: visão geral do projeto em slides (29/09)
- `docs/apresentacao-cap1.pptx` (21 slides, falas nas notas) e `docs/colinha-cap1.md`: apresentação do cap. 1 ao orientador (09/10)
- `docs/apresentacao-metodologia.pptx` (15 slides: as 7 etapas, onde entra a IA, ferramentas, andamento, cronograma) e `docs/colinha-metodologia.md` (16/10)
- `build/monografia-caps1-2-preliminar.docx`: regerado em 09/10 com o novo cap. 1
- `docs/GUIA-ABNT.md`, `docs/BIBLIOGRAFIA.md`, `docs/estrutura.tsv`, `refs/refs.bib`

## 3. O que está travado

| Pendência | Bloqueia | Prazo |
|---|---|---|
| **Aprovar o cronograma novo** (slide 14 de `docs/apresentacao-metodologia.pptx`) e confirmar a data final da EPUSP; registrar no §4 | Todo o planejamento | seg 19/10 |
| Confirmar as escolhas propostas de ferramenta: `multiprocessing` para paralelizar e Q-learning (código próprio) para a etapa 7 | Etapas 5–7 | antes de S2 |
| **Reformular H2 e os momentos-alvo** para o grão administradora×trimestre (fração de lance) + grupo×mês (taxa total de contemplação). Proposta em §5 itens 7–9; decisão de Pedro/Antônio, depois `CONTEXT.md` §3 e §4 do log | Cap. 4, SMM, cap. 7 | qua 30/09 |
| Separar os momentos de calibração dos de teste **antes** de ver qualquer ajuste: o chat das etapas 1–3 propõe, os autores decidem | Validade de H2 | S1 (19–23/10) |
| `src/pipeline/build_panel.py` + `results/qualidade_dados.csv` + `results/g1_identificacao.csv` | G1 formal, cap. 5 | ter 29/09 |
| Apagar as seções antigas do cap. 1 (`text/01-2-problema.md`, `01-3-hipoteses.md`, `01-4-objetivos.md`, `01-5-contribuicoes.md`, `01-6-organizacao.md`); enquanto existirem, o pandoc monta o cap. 1 duplicado | `make docx` | imediato |
| PDF do anuário ABAC 2026 para os números da 1.1 (5,16 mi cotas; R$ 500 bi; 12,74 mi participantes), hoje em `excecoes` | Auditoria da 1.1 | antes de 12/10 |
| Alinhar o texto de 1.2, 1.3 e 1.5 à lógica da apresentação de 09/10: (i) raiz do problema = regras alternativas sem dado → exige modelo; (ii) as duas faltas atribuídas a literaturas distintas (econometria de leilões × teoria de leilões); (iii) Q1→Q2→Q3 como passos dependentes, com consequência de falha por hipótese; (iv) cota, lógica do lance e matriz urgência×liquidez no efeito distributivo | Coerência texto × apresentação | antes de 12/10 |
| Apresentação do cap. 2 (regras de contemplação, granular) | Reunião com o orientador | a combinar |
| Corrigir a data da Res. 285 na proposta de 14/09 (`refs/refs.bib` e seções 2.2–2.4 já corrigidas em 01/10) | Coerência do texto | qua 30/09 |
| Seção 2.4 afirma "entendimento consolidado na jurisprudência" sobre o momento da restituição, sem fonte | Fechamento da 2.4 | antes de 05/10 |
| Incluir os 6 PDFs de normativo no git (`git add -f refs/pdfs/*.pdf`) | Coautores sem os PDFs | ter 29/09 |
| ~16 PDFs de artigos acadêmicos (atrás de paywall; precisa do login USP) | Auditoria dos caps. 1–3 | dom 04/10 |
| Confirmar as 3 referências de SMM (Gouriéroux-Monfort-Renault; McFadden; Duffie-Singleton) | Cap. 6.3 | sex 02/10 |
| Esgotar BDTD, Teses USP, CAPES, SciELO, SPELL e WPs do BCB | Ineditismo em 3.6 | dom 04/10 |
| Template abnTeX2 inexistente (o `refs/abnt.csl` e o `build/template-abnt.docx` para o caminho .docx foram criados em 01/10) | Compilação final | seg 05/10 |
| Makefile chama `src.pipeline`, `src.experiments`, `src.analysis`, que não existem | `make all` | sex 02/10 |
| Campo `responsavel` vazio nas 42 seções; adesão de Pedro Paulo às trilhas | Divisão do trabalho | qua 30/09 |
| `docs/monografia-esqueleto-completo.md` duplica `text/` | Fonte única de verdade | seg 05/10 |
| Verificar mudança de leiaute após a IN BCB 525/2024 (§5 item 10) | Pipeline | ter 29/09 |

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
- **2026-09-25 — Manter a entrega em 12/10/2026, idealmente antes** — Pedro recusou o adiamento para 26/10; a diferença de capacidade é coberta usando Claude Code como camada de produção (código e rascunho) e os autores como revisão e decisão — Pedro
- **2026-09-25 — Baixar o banco de dados do Bacen desde 2017-03** — é quando começa o leiaute de campos atual (código vigente desde mar/2017); séries anteriores não entram — Claude, aceito por Pedro
- **2026-09-29 — Repositório privado no GitHub em `antonioffassini/tcc-consorcio`** — backup e canal com os coautores; Pedro entra como colaborador — Antônio
- **2026-09-29 — Calendário comprimido para 13 dias (ver `docs/PLANO.md` §3)** — G2 em 02/10, congelamento (G3) em 05/10, G4 em 10/10 — Claude, aceito por Pedro e Antônio
- **2026-10-09 — Cap. 1 reestruturado em 9 seções** (1.1 Contexto, 1.2 Motivação, 1.3 Problema e pergunta, 1.4 Proposição central, 1.5 Hipóteses, 1.6 Objetivos, 1.7 Metodologia, 1.8 Escopo e contribuições, 1.9 Organização) — o orientador achou o cap. 1 confuso e sem resposta objetiva a objetivos, motivação e metodologia; a nova ordem separa cada conceito e o Quadro 3 amarra a cadeia. `docs/estrutura.tsv` atualizado. Cap. 2 mantido — Pedro


## 5. Achados que mudam o modelo

Registrados aqui porque são caros de redescobrir e afetam o Capítulo 4.

1. **Número de contemplações por lance é endógeno ao fundo.** A contemplação está condicionada à existência de recursos suficientes no grupo (art. 23 da Lei 11.795/2008). O prêmio disputado não é fixo: é um número estocástico de vagas.
2. **Precedência do sorteio sobre o lance.** Sob a Circular 3.432/2009 (art. 8º), a contemplação por lance só ocorre após a por sorteio, ou se esta não se realizar por insuficiência de recursos. O lance disputa recurso residual. **Confirmado em 25/09 no art. 12, I, da Res. BCB 285/2023.** O parágrafo único do mesmo artigo (incluído pela Res. BCB 362/2023) destina o lance vencedor à quitação ou amortização de prestações vincendas.
3. **Lance embutido** (art. 9º da Circular 3.432/2009; **mantido no art. 13 da Res. BCB 285/2023**, conferido em 25/09) — oferta contra parte do próprio crédito a ser distribuído. Existem duas tecnologias de lance com custos de oportunidade distintos; a restrição de liquidez não é absoluta.
4. **Critério de desempate percentual.** Em grupos com créditos diferenciados (mínimo de 50% do maior; **mantido no art. 7º da Res. BCB 285/2023**), o desempate pode se dar pelo maior percentual do próprio crédito. A ação natural do agente é percentual, não valor em reais.
5. **Excluídos continuam nos sorteios.** A restituição ao excluído ocorre mediante contemplação em sorteio ou no encerramento do grupo. O conjunto que disputa o sorteio não coincide com o que pode receber crédito — e ambos consomem o mesmo fundo.
6. **Quebra de regime em 01/07/2024, não em 01/01/2024.** A Res. BCB 285, de 19/01/2023, revogou integralmente a Circular 3.432/2009 (art. 58). A vigência original era 01/01/2024, mas o art. 59 foi alterado pela Res. BCB 362, de 14/12/2023, para **01/07/2024**. Conferido no texto oficial do BCB em 25/09. Consequência: o regime pós-285 no painel começa na data-base **2024-07**, o que dá 23 meses no painel por grupo (até 2026-05) e 7 trimestres no painel por UF (2024-09 a 2026-03). A data 20/12/2023 na proposta de 14/09 está errada, e as notas de `bcb2023res285` e `bcb2009circ3432` em `refs/refs.bib` dizem 01/01/2024: corrigir.
7. **Lance e sorteio só aparecem separados no arquivo por UF.** O arquivo por grupo (`AAAAMMBens_Imoveis_Grupos.csv`, mensal) traz o total de cotas contempladas no mês, sem separar o canal. A separação lance/sorteio existe só em `AAAAMMConsorcios_UF.csv` (trimestral), no grão **administradora × segmento × UF**. Levantado em 25/09.
8. **Teste de identificação (G1), primeira leitura em 25/09 — passa, mas no nível da administradora.** Nos dados, segmento imóveis, a fração de contemplações por lance sobe de ~0,70 (2017) para ~0,80 (2026). No regime pós-285, entre as 53 administradoras com pelo menos 30 contemplações no trimestre, a fração de lance vai de 0,12 a 0,97 (média 0,73, desvio-padrão 0,12). A variância é quase toda **entre** administradoras (0,0135 no total contra 0,0008 dentro de cada uma). Correlação de Spearman da fração de lance com o tamanho mediano dos grupos da administradora: 0,56; com o prazo mediano: ~0. A análise é exploratória e foi feita fora do pipeline: **refazer em `src/pipeline` antes de usar qualquer número no texto.**
9. **Painel por grupo, regime pós-285:** 3.470 grupos, 76 administradoras, 57.086 observações grupo×mês. A taxa mensal de contemplação por grupo tem mediana de ~0,5% das cotas ativas, e em ~7% dos grupo×mês não há contemplação nenhuma. O número de vagas por assembleia é observável por grupo; o canal (lance ou sorteio), não.
10. **Normativos correlatos.** A IN BCB 525/2024 (19/09/2024) mudou a remessa para o Documento 2080, mensal, o que pode alterar o leiaute a partir do fim de 2024: verificar no pipeline. A Res. BCB 381/2024 criou medidas temporárias para consorciados afetados pelas enchentes do RS, válidas até 31/12/2024. Avaliar excluir o RS de 2024 ou tratá-lo como sensibilidade.
11. **Art. 30 da Lei 11.795/2008:** caput vigente; §§ 1º a 3º vetados. Conferido no Planalto em 25/09.
12. **Arquivos contábeis (`*_ADM.zip`, Docs 4010/4110)** trazem saldos consolidados de todo o sistema, e não por administradora. A série publicada termina em 2024-12. Uso limitado a contexto.
13. **Contemplado excluído no regime atual.** Sob a Circ. 3.432/2009, a assembleia podia cancelar a contemplação de quem ficasse inadimplente antes de usar o crédito. Na Res. BCB 285/2023, o contemplado excluído **mantém a contemplação**, com crédito parcial igual ao percentual amortizado do bem, deduzidas as obrigações pendentes (art. 33). A exclusão por inadimplência ocorre após três vencimentos (art. 32, II, na redação da Res. 362/2023, que retirou "consecutivos"). Conferido no texto oficial em 01/10. Afeta a dinâmica de vagas e de restituição no cap. 4.

## 6. Próximos passos acordados

**Semana 1 (19–23/10)** — executado em chat Cowork separado, com o prompt de 16/10:
1. Etapa 1: `src/pipeline/`, painéis A (grupo×mês) e B (administradora×trimestre), `results/qualidade_dados.csv`, testes em `tests/`
2. Etapa 2: `results/fatos_momentos.csv` e `results/g1_identificacao.csv`; proposta de partição calibração × teste para decisão dos autores
3. Etapa 3: especificação do modelo em `text/04-*.md` (rascunho)
4. Autores: apagar as 5 seções antigas do cap. 1, commit e push pelo GitHub Desktop; aprovar o cronograma

*(Itens abaixo são anteriores; mantidos para referência.)*

**A partir de 09/10**
1. Apagar as 5 seções antigas do cap. 1 (§3) e commitar o novo cap. 1
2. Apresentar o cap. 1 ao orientador com `docs/apresentacao-cap1.pptx`; registrar o retorno no §4
3. Apresentação granular do cap. 2
4. Rodar `scripts/audit.py` sobre as 1.x e baixar o anuário ABAC

*(Itens abaixo são de 29/09; conferir o que já foi feito.)*

**Hoje, ter 29/09**
1. Claude Code: `src/pipeline/build_panel.py`, painéis grupo×mês e administradora×UF×trimestre, `results/qualidade_dados.csv`, `results/fatos_fracao_lance.csv`, `results/g1_identificacao.csv`, testes, commit e push
2. `git add -f refs/pdfs/*.pdf`, commit e push
3. Confirmar o estado da conversa com o orientador

**Qua 30/09**
4. Decidir a reformulação de H2 e a partição dos momentos (calibração × teste), e registrar no §4
5. Rascunho do cap. 4 (4.1 a 4.5); congelar a notação do `CONTEXT.md` §5

Daí em diante: calendário em `docs/PLANO.md` §3.

## 7. Histórico de sessões

| Data | Superfície | O que aconteceu |
|---|---|---|
| 12/09/2026 | Chat | Troca de tema; catálogo de 4 temas; plano de remontagem; plano operacional de 14 semanas; repositório montado; guia ABNT; seções 1.1-1.4 e capítulo 2 escritos; bibliografia verificada; decisão de migrar para Cowork |
| 12/09/2026 | Cowork | Pasta vinculada e repositório auditado. Meta de 30 dias fixada; aprovação do orientador deixa de ser gate; corte de escopo em cinco linhas; RL sai do loop de SMM; abnTeX2 escolhido como formato final. `docs/PLANO.md` reescrito de 14 semanas para 30 dias em spike vertical. Levantados os buracos de infraestrutura: `refs/pdfs/` e `data/raw/` vazias, `refs/abnt.csl` e template inexistentes, `.git` ausente |
| 24/09/2026 | Cowork | Diagnóstico: nada de S1 executado (12 dias de atraso); G0 cumprido; repo sem remote. `docs/pitch-orientador.md` criado (roteiro de fala, com calendário proposto até 26/10, pendente de decisão). Achado não verificado: página do Bacen lista "Bens Imóveis – Grupos" com contemplações — abrir o CSV é o teste de G1 |
| 25/09/2026 | Cowork | Download pelo navegador embutido de 236 arquivos do Bacen (2017-03 a 2026-05) e de 6 normativos. Verificados no texto oficial: vigência da Res. 285 = 01/07/2024 (Res. 362/2023); precedência sorteio→lance (art. 12), lance embutido (art. 13) e piso de 50% (art. 7º) mantidos; art. 30 da Lei 11.795 com §§ vetados. G1 exploratório: lance/sorteio só por administradora×UF×trimestre; variação quase toda entre administradoras. Pedro decide manter 12/10. `docs/GIT.md` escrito |
| 29/09/2026 | Cowork + terminal | Dados e normativos extraídos na pasta (243 arquivos conferidos). Repositório privado criado em `antonioffassini/tcc-consorcio`, commit 957ef8b. `ESTADO.md` e `docs/PLANO.md` reescritos para 13 dias. Apresentação do projeto em `docs/apresentacao-projeto.pptx` |
| 01/10/2026 | Cowork | Briefing do orientador reescrito (`docs/pitch-orientador.md`). Caps. 1–2 gerados por pandoc em `build/monografia-caps1-2-preliminar.docx` (ABNT: Times 12, 1,5, margens 3/2), com `refs/abnt.csl` (CSL oficial do repositório citation-style-language) e `build/template-abnt.docx`. Seções 2.2, 2.3 e 2.4 atualizadas com o texto conferido da Res. 285 (vigência 01/07/2024, precedência, lance embutido, 50%, art. 33); pendência da 2.2 resolvida; `refs/refs.bib` com a vigência corrigida. Erro de login do Claude Code no VS Code (trava `.oauth_refresh.lock`) diagnosticado |
| 09/10/2026 | Cowork | Retorno do orientador sobre os caps. 1–2 (confusos; tese, problema, hipóteses e objetivos misturados). Cap. 1 reescrito em 9 seções (`text/01-1` a `01-9`), `docs/estrutura.tsv` atualizado, `.docx` regerado. Apresentação do cap. 1 (`docs/apresentacao-cap1.pptx`, 21 slides com slide-resumo inicial e fluxo do dinheiro do grupo) e colinha (`docs/colinha-cap1.md`) |
| 16/10/2026 | Cowork | Diagnóstico: prazo de 12/10 vencido; `src/` vazio e sem pipeline em outro computador. `docs/apresentacao-metodologia.pptx` + `docs/colinha-metodologia.md` (7 etapas explicadas, IA restrita à etapa 7, ferramentas, andamento, cronograma S0–S7 proposto). Prompt das etapas 1–3 entregue para execução em chat separado. Git: adotado GitHub Desktop (ou `git pull` no terminal do VS Code) |
