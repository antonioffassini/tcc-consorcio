# ESTADO DO PROJETO

> **Documento vivo.** Atualizado ao longo de toda sessão de trabalho, não só no fim.
> Registra o que mudou: progresso, decisões, pendências.
> O que não muda (tese, notação, escopo) fica em `CONTEXT.md`.
> Bibliografia tem controle próprio em `tcc/docs/BIBLIOGRAFIA.md`.
> **Desde 09/11 este arquivo cobre as quatro entregas** (TCC, POO, seminário, IA). Caminhos sem prefixo nas seções sobre o TCC são relativos a `tcc/`.

**Última atualização:** 16/11/2026 — sessão Cowork [TCC]: passo 1 (heterogeneidade) e passo 2 (M1/M2); antes, [POO][SEM] 15/11: seminário passa a DDD; modelo de domínio do jogo

---

## 1. Onde estamos

| Item | Situação |
|---|---|
| Prazo | **12/10/2026 não foi cumprido.** Cronograma novo proposto em 16/10 (S1 19–23/10 a S7 30/11–04/12, em `docs/apresentacao-metodologia.pptx`, slide 14), **pendente de aprovação dos três autores e de confirmação da data final no calendário da EPUSP** |
| Fase | Etapas 1–4 feitas (4 em protótipo, só M0) e verificação (5a) feita. **[TCC] 15/11: passo 1 (heterogeneidade); 16/11: passo 2 (M1/M2).** Próximo: calibração SMM, H2, H3, interface de docking, texto dos caps. 4–7 |
| Escopo do Projeto Claude | Desde 09/11 o projeto abriga quatro entregas sobre o mesmo domínio: TCC, jogo educacional de POO (01/12), seminário de TAPOO (**Modelagem com DDD** desde 15/11; 17–26/11, data do grupo a confirmar) e trabalho de IA PCS3838 (classificação de reclamações). Uma pasta por entrega na raiz do repositório `projetos-consorcio` (§4, 09/11) |
| Gates | G0 cumprido. **G1 cumprido formalmente em 26/10** (`results/g1_identificacao.csv`: 94% da variância da fração de lance é entre administradoras). As datas antigas de G2–G4 caducaram; pelo cronograma proposto, congelamento dos experimentos ao fim de S5 (20/11) |
| Dados | 236 arquivos do Bacen (2017-03 a 2026-05) em `data/raw/bacen/`, commitados |
| Repositório | `github.com/antonioffassini/tcc-consorcio`, privado. Último commit em 16/10 17:42; pipeline, análise, simulador, testes, `results/` e este arquivo aguardam commit (09/11) |
| Código | `src/pipeline/` (16/10), `src/analysis/momentos.py` e `src/sim/` (protótipo, 26/10); **[TCC] 15/11: heterogeneidade por administradora, lance embutido, inadimplência/exclusão/recolocação e simulação no grão do painel (`src/sim/painel.py`); 16/11: M1 e M2 (`src/sim/regras.py`)**; 52 testes. Faltam calibração, comparação, docking |
| Orientador | Caps. 1–2 lidos pelo Prof. Cugnasca (09/10): texto confuso. Cap. 1 reescrito e apresentado na semana de 12/10 com boa recepção; a parte de metodologia (1.7) ficou confusa na fala, o que motivou `docs/apresentacao-metodologia.pptx` (16/10) |
| POO / seminário | [POO][SEM] Modelo de domínio em DDD em rascunho (`projetos/seminario-tapoo/MODELO-DOMINIO.md`, 15/11). Código Java ainda não começou (passos 2–5 do plano de 15/11); slides (passo 6) não começaram |
| Decisão pendente mais cara | Reformular H2 e os momentos-alvo para o grão administradora×trimestre (§3) |

## 2. O que está pronto

**Infraestrutura**
- Repositório com estrutura completa; no GitHub desde 29/09
- `scripts/audit.py` funcionando e testado contra caso quebrado proposital
- `Makefile` com os alvos painel, experimentos, resultados, auditoria e docx (os módulos de `src/` ainda não existem)
- `scripts/gen_skeleton.py`; 42 seções esqueletadas com frontmatter
- Biblioteca de 8 prompts em `prompts/` (P0 a P7)
- `docs/GIT.md`: guia operacional do git para o projeto (25/09)

**Pipeline** *(16/10, etapa 1)*
- `src/pipeline/` (`leitura.py`, `build_panel.py`, `README.md`); o alvo `make painel` existente roda sem mudança (o alvo `testes` não entrou: o Makefile é protegido contra escrita remota, ver §3)
- `data/processed/painel_a_grupo_mes.parquet` (grupo×mês, imóveis, ≥ 2024-07), `painel_b_adm_trimestre.parquet` (administradora×trimestre, imóveis, 2017-03 a 2026-03), `conciliacao.parquet`
- `results/qualidade_dados.csv`; `tests/` com 14 testes (somas, duplicatas, não negatividade, reagregação do bruto, conciliação com o consolidado)

**Fatos, momentos e simulador** *(26/10, etapas 2, 4 e 5a em protótipo)*
- `src/analysis/momentos.py` → `results/fatos_momentos.csv` (19 momentos, 5 fatos) e `results/g1_identificacao.csv`
- `src/sim/grupo.py`: motor mês a mês (arrecadação → sorteio com precedência → lance livre pay-as-bid sobre o saldo residual → exclusão por risco h constante; excluídos seguem no sorteio e são restituídos), política paramétrica `b = min(λ, max(0, φ0 + φ1·θ + φ2·restante))`; só M0, sem lance embutido, grupo fechado
- `tests/test_simulador.py`: 7 testes de verificação (conservação do dinheiro, saldo ≥ 0, espera média (T+1)/2 sem lance, todos contemplados sem exclusão, sorteio uniforme por qui-quadrado, monotonicidade do lance, semente fixa)
- `src/sim/primeira_rodada.py` → `results/sim_primeira_rodada.csv` e `_perfil.csv` (parâmetros de chute, sem calibração; §5 item 19)
- Apresentação de andamento de 26/10 (17 slides) e roteiro: `docs/apresentacao-andamento-2026-10-26.pptx`, `docs/roteiro-andamento-2026-10-26.md`

**Dados** *(25/09, baixados do site do Bacen, página "Consórcios — Banco de dados")*
- `data/raw/bacen/AAAAMMConsorcios.zip`: 111 arquivos mensais, 2017-03 a 2026-05 (segmentos consolidados + grupos de imóveis + grupos de móveis nos trimestres)
- `data/raw/bacen/AAAAMMConsorcios_UF.zip`: 37 trimestrais, 2017-03 a 2026-03 (lance/sorteio por administradora×segmento×UF)
- `data/raw/bacen/AAAAMMConsorcios_ADM.zip`: 88 contábeis, 2017-03 a 2024-12 (Docs 4010/4110 consolidados)
- Integridade conferida (todos os zips abrem; nomes e tamanhos batem com o pacote)

**Normativos em `refs/pdfs/`** *(25/09, texto oficial do BCB e do Planalto convertido em PDF; fora do git por causa do `.gitignore`)*
- `brasil2008lei11795.pdf`, `bcb2023res285.pdf`, `bcb2023res362.pdf`, `bcb2009circ3432.pdf`, `bcb2024in525.pdf`, `bcb2024res381.pdf`

**[TCC] Heterogeneidade e regra de vagas** *(15/11, passo 1; protótipo, sem calibração)*
- `src/sim/grupo.py` revisado: vagas de sorteio $\kappa$ por assembleia (não inteiro = arredondamento aleatório), lance embutido com teto (art. 13), inadimplência de 3 vencimentos antes da exclusão (art. 32, II; inadimplente conta como ativa e não concorre, art. 11, § 1º), risco de exclusão por faixa de idade, recolocação da vaga excluída, sorteio da sobra (opcional), horizonte de simulação. Com os valores padrão reproduz exatamente `results/sim_primeira_rodada*.csv`
- `src/sim/painel.py`: simulação no grão dos dados — 543 grupos amostrados do painel A (até 12 por administradora, semente fixa, pesos para a composição do painel), cada um com o próprio prazo, tamanho e idades observadas; momentos de calibração por mistura sobre a heterogeneidade contratual; momentos de teste só em `momentos_realizacao`, não chamados ainda
- `src/sim/rodada_heterogeneidade.py` → `results/parametros_fixos.csv` (h por faixa de idade, ρ, teto do embutido), `results/sim_heterogeneidade.csv` (efeito acumulado de cada revisão nos momentos de calibração), `results/sim_forma_heterogeneidade.csv` (momentos por nível nas duas formas candidatas)
- `tests/test_heterogeneidade.py`: 15 testes novos; os 21 anteriores seguem passando (36 no total; 1 pulado sem `data/raw` no ambiente)

**[TCC] Mecanismos M1 e M2** *(16/11, passo 2)*
- `src/sim/regras.py`: `Mecanismo` = regra de sorteio + regra de lance, trocável em `grupo.simula(..., mecanismo=)` e em `painel.simula_desenho(..., mecanismo=)`. M0 por mecanismo reproduz o padrão bit a bit
- `tests/test_mecanismos.py`: 16 testes — leilão único (M0 = primeiro preço, M2 = segundo preço), equivalência de receita com lances $(n-1)/n\cdot v$ contra verdade ($(n-1)/(n+1)$, $n=2,5$), lance de equilíbrio como melhor resposta, verdade dominante em M2, preço uniforme multiunidade, M2 contempla no máximo quanto M0 e os mesmos primeiros, divisão livre/embutido, frequência do sorteio de M1 segundo $\omega$, M1 não trivial no grupo fechado, conservação nos três. 52 testes no total (51 passam, 1 pulado sem `data/raw`)

**[TCC] Seção 4.3 em rascunho** *(16/11)*: `text/04-3-mecanismos.md` — elementos comuns, critério de admissibilidade, M0, M1, M2, Quadro 4.1. P0 PRONTA (insumos em disco, decisões no §4, símbolos no CONTEXT §5); auditoria: só os 3 marcadores [CITAR] (Vickrey e Krishna verificados e no `.bib`, sem PDF; regulamentos de administradoras). P5 não rodado

**POO e seminário** *(15/11)*
- [SEM] `projetos/seminario-tapoo/MODELO-DOMINIO.md`: linguagem ubíqua tirada da Lei 11.795/2008 e da Res. BCB 285/2023 (artigos reconferidos no PDF em 15/11), mapa de contextos, agregado `Grupo` com 8 invariantes, objetos de valor, State da cota, eventos de domínio, sequência da assembleia fiel a `src/sim/grupo.py`, M1/M2 provisórios. Rascunho
- [SEM] `projetos/seminario-tapoo/PLANO.md` reescrito para DDD (roteiro de 40 min, referências candidatas não conferidas)
- [POO] `projetos/poo-jogo/PLANO.md` e `projetos/VISAO-INTEGRADA.md` alinhados ao DDD

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
| ~~Pipeline, qualidade e `results/g1_identificacao.csv`~~ — resolvido (16/10 e 26/10) | — | — |
| Adicionar à mão no `Makefile` (protegido contra escrita remota): alvo `testes` (`$(PY) -m pytest -q tests`) e texto do `make ajuda` | Conveniência | quando der |
| **Confirmar com Antônio e Pedro Paulo a partição de momentos** aceita por Pedro em 09/11 (§4). *[TCC] 15/11: não confirmada até esta data; o trabalho segue com ela e todo resultado de H2 sai marcado "partição pendente de confirmação"* | Validade de H2 | antes de rodar a calibração |
| [TCC] Conferir em regulamentos de administradoras (contratos de adesão de grupos de imóveis) (i) o teto de lance embutido, hoje fixado em 0,25 por hipótese; (ii) se as vagas de sorteio previstas são número fixo ou proporcional ao grupo (forma adotada em §4, 15/11); (iii) se a sobra de recurso sem lance vai a sorteio | Justificativa da 4.2 e da 4.3 | antes do fechamento do cap. 4 |
| **Decidir o papel da H1 (RL)**: versão mínima ou trabalho futuro (proposta de 09/11) | Cap. 7, cronograma | S4 |
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
| Makefile chama `src.experiments` e `src.analysis`, que não existem (`src.pipeline` resolvido em 16/10) | `make all` | S2 em diante |
| Campo `responsavel` vazio nas 42 seções; adesão de Pedro Paulo às trilhas | Divisão do trabalho | qua 30/09 |
| `docs/monografia-esqueleto-completo.md` duplica `text/` | Fonte única de verdade | seg 05/10 |
| ~~Verificar mudança de leiaute após a IN BCB 525/2024~~ — resolvido 16/10, sem quebra (§5 item 14) | — | — |
| ~~[TCC][POO] **Especificar M1 e M2.** No grupo fechado do protótipo, todas as cotas não contempladas têm a mesma espera, então "sorteio ponderado pela espera" (M1) é idêntico ao uniforme. M1 só difere com adesão em andamento (Res. 285, art. 34) ou com outro peso. M2 (preço uniforme) precisa da regra de preço (k-ésima ou (k+1)-ésima oferta). Decisão de modelagem do TCC; o Java segue a provisória de `MODELO-DOMINIO.md` §8 até lá~~ *[TCC] resolvido em 16/11 (§4), pendente de aceite de Pedro; o Java deve seguir `src/sim/regras.py`*  | M1/M2 no jogo e no TCC; cap. 4.3 | antes do passo 3 do jogo |
| [POO][SEM] Aceitar ou não as decisões de 15/11 marcadas *pendente de aceite* (§4) | Passo 2 do jogo | antes do passo 2 |
| [SEM] Confirmar a data do seminário. Se cair em 17–19/11, os slides (passo 6) passam à frente do código, e o caso usa modelo + esqueleto | Ordem dos passos 2–6 | imediato |
| [POO][SEM] Confirmar com os professores de POO e TAPOO que usar o mesmo domínio nas duas disciplinas é aceito (regra 7 do `CLAUDE.md`) | Entregas | antes do seminário |
| **Reorganização do repositório não aplicada no disco.** O §4 de 09/11 diz que o TCC desceu para `tcc/` e que as entregas ficam na raiz; em 15/11 o disco tem o TCC na raiz e `projetos/{poo-jogo,seminario-tapoo,ia-reclamacoes}`. Os caminhos do `CLAUDE.md` não batem com o disco. Fazer o `git mv` (com shell) ou corrigir o `CLAUDE.md` | Caminhos de todos os prompts | antes do passo 2 do jogo |
| Divergência entre o fluxo trimestral do arquivo por UF e a soma mensal dos grupos em algumas administradoras (§5 item 17): entender antes de usar as duas fontes no mesmo momento | Momentos que combinam A e B | S1 |

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

- **2026-11-09 — Partição dos momentos (antes de qualquer ajuste)** — calibração: `frac_lance_media`, `frac_lance_dp` (entre administradoras), `taxa_contempl_q50`; teste de H2 (guardados): `spearman_lance_tamanho`, `frac_sem_contempl`. Motivo: a calibração usa nível e dispersão do canal e a taxa total; o teste usa uma relação estrutural e uma propriedade de cauda que o modelo não vê — Claude, aceito por Pedro *(pendente de confirmação dos coautores, §3)*
- **2026-11-09 — Centralizar no Projeto Claude e neste repositório quatro entregas sobre o mesmo domínio** — TCC (`tcc/`, regras inalteradas), jogo educacional de POO em Java (`poo-jogo/`, Pedro e Antônio, exceção de 2 integrantes autorizada pelo professor, entrega 01/12), seminário de TAPOO sobre Arquitetura Hexagonal (`seminario-tapoo/`, Pedro e Antônio, 17–26/11) e trabalho de IA PCS3838 de classificação de reclamações sobre consórcio (`ia-reclamacoes/`, trio). O TCC continua em Python e não espera pelo Java; o motor Java entra no TCC só como segunda implementação para *docking* (seção 6.5). Ampliação conforme `CONTEXT.md` §4 apenas nesse ponto (6.5); o resto é fora do escopo do TCC. Visão integrada em `VISAO-INTEGRADA.md`. **Estrutura:** o repositório passa a se chamar `projetos-consorcio`, com `CLAUDE.md`, `ESTADO.md`, `VISAO-INTEGRADA.md` e `PROMPTS.md` na raiz e uma pasta por entrega; o conteúdo do TCC desce para `tcc/` (movido com o histórico preservado) — Pedro
- **2026-11-09 — Git** — commits e push feitos pelo Claude quando houver shell no computador; senão, por Pedro via GitHub Desktop. VS Code deixa de ser necessário — Pedro
- **2026-11-15 — [SEM] Tema do seminário passa de Arquitetura Hexagonal para Modelagem com Domain-Driven Design** — a Arquitetura Hexagonal ficou com o grupo 3 na planilha. O caso real passa a ser o modelo de domínio do jogo; o roteiro foi refeito em `projetos/seminario-tapoo/PLANO.md`. Troca de slides com o grupo 3 com 48 h de antecedência — Pedro
- **2026-11-15 — [POO] Portas e adaptadores continuam como arquitetura interna do jogo** — o motivo (domínio sem framework, CLI JSON como única ponte com o TCC) independe do tema do seminário — Pedro
- **2026-11-15 — [POO][SEM] Modelo de domínio antes do código**, em `projetos/seminario-tapoo/MODELO-DOMINIO.md`, servindo ao jogo e ao seminário; o motor Python (`src/sim/grupo.py`) é a especificação e vence em caso de divergência — Pedro
- **2026-11-15 — [POO][SEM] Um contexto delimitado de núcleo (Contemplação), com Assembleia, Fundo e Cobrança/Exclusão como módulos, e não como contextos** — a contemplação só ocorre se o fundo cobrir o valor (Lei 11.795, art. 23) e muda cota e fundo juntos; separar exigiria consistência eventual e perderia a garantia; os três falam a mesma língua. Contextos de fato distintos: Partida (jogo) e Pesquisa (docking, linguagem publicada JSON com o TCC). Contraria o pedido inicial de Pedro (três contextos) — Claude, *pendente de aceite de Pedro*
- **2026-11-15 — [POO] Detalhes táticos do modelo** — (i) estados da cota renomeados para `NaoContemplada`, `Contemplada`, `Excluida`, `Restituida`, com `ativa()` no sentido do art. 21 da Lei (o `ATIVA` do Python é "não contemplada"); (ii) `RegraContemplacao` como composição de `RegraSorteio` e `RegraLance`, com a ordem sorteio → lance fixada no agregado (M1 muda o sorteio, M2 o lance); (iii) evento `CotaContemplada` com `finalidade` CREDITO/RESTITUICAO, porque a lei chama de contemplação também o sorteio do excluído (art. 22), mas o Bacen e o Python só contam ativas; (iv) contabilidade em `double` em fração de C, para reproduzir a aritmética do motor; (v) docking em distribuição, não bit a bit (PCG64 do numpy ≠ gerador Java) — Claude, *pendente de aceite de Pedro*
- **[TCC] 2026-11-15 — Heterogeneidade em três camadas** — (i) estrutural observada: cada grupo simulado tem o prazo, o tamanho (mediana de `ativas`) e as idades observadas de um grupo real do painel A; (ii) contratual latente por administradora: vagas de sorteio por assembleia $\kappa_g=\max(1, s_j N_g/T_g)$, com $s_j\sim\text{LogNormal}(\log m_s,\sigma_s)$; (iii) comportamental comum: $\phi$, $F_\theta$, $F_\lambda$. Motivo: 94% da variância da fração de lance é entre administradoras e quase nada dentro (`results/fatos_momentos.csv`), e o número de sorteios por assembleia é cláusula do contrato de adesão redigido pela administradora (Res. BCB 285, art. 2º, XII; art. 12, I). Efeito fixo por administradora (49 parâmetros) não é identificável com três momentos de calibração; distribuição populacional com dois parâmetros é — Claude, a confirmar por Pedro
- **[TCC] 2026-11-15 — Forma das vagas de sorteio: fração da capacidade, não número fixo** — alternativa descartada: $\kappa_j-1\sim$ Poisson, independente do tamanho do grupo. Com o desenho do painel e a política de chute, a forma de número fixo, no nível que dá a média observada da fração de lance (0,73), já produz desvio-padrão entre administradora×trimestre de 0,136, acima do observado (0,116), sem espaço para heterogeneidade; a forma proporcional dá 0,110 no mesmo nível (`results/sim_forma_heterogeneidade.csv`). Decidido só com momentos de calibração. Hipótese contratual a conferir (§3) — Claude, a confirmar por Pedro
- **[TCC] 2026-11-15 — Mistura em vez de sorteio dos níveis na função objetivo** — cada grupo é simulado para os 9 níveis de $s$ da grade e os momentos de calibração são ponderados pela massa da LogNormal em cada nível; a função objetivo fica contínua em $(m_s,\sigma_s)$ com números aleatórios comuns. Momentos de teste e intervalos usam realizações do nível por administradora — Claude
- **[TCC] 2026-11-15 — Exclusão, inadimplência e recolocação fixadas fora do SMM, no painel A** — risco de exclusão por faixa de idade (6 faixas de assembleia/prazo, razão de somas com truncagem no p99) e recolocação $\rho=1$ (reposição líquida de vagas no primeiro terço = 1,24 das exclusões, truncada em 1, porque o modelo não cria vaga nova): `results/parametros_fixos.csv`. Inadimplente por 3 vencimentos antes da exclusão (art. 32, II), contado entre as ativas e fora da disputa (art. 11, § 1º). Motivo: a taxa de exclusão cai de ~4% para ~0,1% ao mês ao longo da vida do grupo e o número de cotas ativas fica estável dentro do grupo (§5 item 20); são dados diretos, não precisam do simulador — Claude
- **[TCC] 2026-11-15 — Lance embutido: livre primeiro, embutido até o teto** — o participante cobre o lance desejado com liquidez própria até $\lambda_i$ e completa com embutido até $\bar b^{e}=0,25$ (hipótese, §3); vence o maior percentual total; contemplação exige $R_t\ge 1-b$; o vencedor recebe $1-$embutido. O lance amortiza as últimas parcelas (encurta o prazo da cota, parcela constante; art. 12, parágrafo único deixa a forma ao contrato) — Claude
- **[TCC] 2026-11-15 — Sobra sem lance fica no fundo** (caso base); sorteio da sobra só como sensibilidade. A Res. 285 prevê sorteios adicionais apenas com o fundo de reserva (art. 22, IV), que o modelo não tem — Claude
- **[TCC] 2026-11-15 — Parâmetros a calibrar por SMM: $\Theta=(\phi_0, m_s, \sigma_s)$**, três parâmetros para os três momentos de calibração; $\phi_1,\phi_2$, $F_\theta$, $F_\lambda$ e $\bar b^{e}$ fixos nos valores de `src/sim/grupo.py`, com sensibilidade em 7.5. A sobreidentificação vem só dos momentos de teste — Claude
- **[TCC] 2026-11-16 — M1: sorteio ponderado pela situação da cota** — peso 1 para a ativa não contemplada e $\omega$ para a excluída não restituída; lance pay-as-bid como em M0. Motivo: peso pela espera é idêntico ao uniforme no grupo fechado (§3, 15/11); a situação separa as elegíveis mesmo no grupo fechado sempre que há exclusão, não é manipulável (ser excluído custa a carta) e age onde o dado pesa: a maior parte dos sorteios vai a excluídos (§5 item 22). Troca prazo de restituição do excluído por prazo de carta da ativa — exatamente o conflito entre os critérios de bem-estar e de estabilidade. Alternativas descartadas: peso por lances perdidos (premia quem tem liquidez e é manipulável: lance perdido não custa nada) e peso inverso ao lance médio (pune quem oferta, incentivo contrário ao lance). Admissibilidade: as condições do sorteio são cláusula do contrato (Res. 285, art. 2º, XII); a Res. não fixa pesos — conferir no texto ao escrever 4.3. $\omega=0,5$ é referência; o passo 4 varre $\omega\in\{0; 0,25; 0,5; 0,75\}$. Opção $\beta$ de peso pela espera fica no código (só age em grupo aberto), fora da comparação principal — Claude; **aceito por Pedro em 16/11**
- **[TCC] 2026-11-16 — M2: preço uniforme no $(k+1)$-ésimo lance** — os $k$ maiores lances vencem e todos pagam o primeiro lance recusado (zero se não houver). Para demanda unitária, é a generalização do segundo preço em que ofertar o valor é dominante; a variante no $k$-ésimo lance não tem essa propriedade. Cada vencedor amortiza $p^u_t$, pagando livre até o que ofertou de livre e completando com embutido; saída líquida do fundo por vencedor $1-p^u_t$, logo $k$ é o maior inteiro com $R_t\ge k(1-p^u_t)$. Consequência verificada em teste: com os mesmos lances, M2 contempla no máximo tantas cotas quanto M0 — o preço menor custa vagas. Sorteio uniforme, como M0 — Claude; **aceito por Pedro em 16/11**
- **[TCC] 2026-11-16 — Política de lance fixa entre regras nesta etapa** — sob M2 a melhor resposta muda (verdade passa a ser dominante no leilão único); manter $\pi_\phi$ igual nas três regras é a limitação da crítica de Lucas, registrada para o passo 4 com [DECISÃO PENDENTE: papel do RL na comparação] — Claude
- **[TCC] 2026-11-16 — Critério de admissibilidade e $\omega=0$ fora dele** — admissível = altera só o que a norma delega ao contrato (forma do sorteio e regras do lance: Lei 11.795, art. 22, § 1º; Res. 285, art. 2º, XII) e preserva quem concorre (Lei, arts. 21 e 22, § 2º), a condição de recursos (Lei, art. 23), a precedência do sorteio (Res., art. 12, I) e o destino do lance (Res., arts. 12, parágrafo único, e 13, parágrafo único). Consequência: $\omega=0$ tira o excluído da disputa e contraria o art. 22, § 2º; vira só referência de limite. A grade do passo 4 passa a ser $\omega\in\{0,25;\ 0,5;\ 0,75\}$ admissíveis, mais $\omega=0$ como limite. Para M2, "valor do lance vencedor" (arts. 12 e 13) é lido como o montante que o contrato define como devido; a ata continua listando os percentuais ofertados (art. 48). Leitura dos textos, não interpretação do regulador — Claude, a pedido de Pedro

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
14. **Sem quebra de leiaute após a IN BCB 525/2024** (conferido no pipeline em 16/10). Os 111 arquivos mensais de grupos e os 37 por UF (2017-03 a 2026-05) têm o mesmo cabeçalho do dicionário vigente desde 2017-03; a continuidade dos grupos de um mês para o outro fica estável na faixa de 0,97–0,99 em 2024–2026, sem degrau no fim de 2024. Nenhuma linha descartada pelas regras de validade. Detalhe em `results/qualidade_dados.csv` (escopo `leiaute`).
15. **`Quantidade_de_cotas_excluídas` é estoque, não fluxo.** O fluxo mensal de exclusões só sai por diferença; a diferença é negativa em ~4% dos grupo×mês (recolocação de cota excluída), por isso o painel A traz `excluidas_var` (bruta) e `excluidas_mes` (truncada em zero). Os dois arquivos contam só cotas **ativas** contempladas; excluído contemplado (sorteio para restituição, §5 item 5) aparece apenas em `excluidos_contempl_trim` do arquivo por UF, sem canal.
16. **Lacunas de remessa.** Uma administradora (CNPJ 73516106) some de 2026-04 (145 → 1 → 148 grupos); outras quatro têm meses ausentes isolados em 2025. Não há arquivo mensal faltando. O RS em 2024 foi sinalizado no painel A por exposição da administradora (≥ 50% das cotas ativas no RS) e no painel B por trimestre, com fração de lance também calculada sem o RS.
17. **Arquivo por UF × soma dos grupos.** A soma das cotas contempladas no mês (grupos) bate exatamente com o consolidado por administradora em todos os administradora×mês, e os estoques por UF batem com o consolidado em ~98% dos administradora×trimestre. Já o **fluxo** trimestral do arquivo por UF (lance + sorteio) diverge da soma de três meses dos grupos em parte das administradoras: mediana da razão = 1,00, mas só ~60% dos administradora×trimestre ficam a ±5%, e há casos grandes nos dois sentidos (BB Consórcios com o UF muito acima; Bradesco abaixo). Razão agregada no regime pós-285 em `results/qualidade_dados.csv`. Hipóteses a verificar: critério de data de contemplação distinto entre remessas; grupos de imóveis reportados em outra remessa. Consequência: não combinar fluxos das duas fontes no mesmo momento sem tratar isso.

18. **Correlação fração de lance × tamanho = 0,32 no pipeline, contra ~0,56 na leitura exploratória (item 8).** O exploratório foi feito fora do pipeline, com outra medida de tamanho; vale o número de `results/fatos_momentos.csv` (tamanho = mediana de `cotas_total` dos grupos da administradora no trimestre). Prazo: −0,01. Sem o RS, a fração média de lance vai de 0,73 para 0,74.
19. **Primeira rodada do simulador (26/10, sem calibração).** Com parâmetros de chute (N = 600, T = 200, h = 0,005), a fração de lance (0,77 × 0,73) e a taxa mensal mediana (0,49% × 0,51%) já ficam próximas do dado: a estrutura da regra (uma vaga de sorteio, saldo para lance) explica boa parte do nível. Ficam longe a dispersão entre grupos (0,01 × 0,12 entre administradoras) e a fração de meses sem contemplação (18% × 6,6%). Consequência: o modelo precisa de parâmetros heterogêneos por administradora e de revisão da regra de vagas antes da calibração. Fonte: `results/sim_primeira_rodada.csv`.
20. **[TCC] Os meses sem contemplação concentram-se no fim da vida do grupo, e o grupo é aberto** (15/11, painel A pós-285). Na faixa 0,8–1,0 de assembleia/prazo, ~59% dos grupo×mês não têm contemplação (todos já contemplados); nas faixas até 0,67, entre 0,6% e 3%. Como o painel é concentrado em grupos jovens (mediana de assembleia 54 para prazo mediano 200), a fração de 18% da primeira rodada vinha de simular a vida inteira de grupos fechados. A taxa de exclusão cai com a idade (de ~3,8% ao mês no primeiro décimo do prazo para ~0,1% no último terço; `results/parametros_fixos.csv`), e a mediana da variação mensal de cotas ativas dentro do grupo é ~0: as vagas excluídas são recolocadas. O estoque de excluídos é da ordem das ativas, e no painel B os excluídos contemplados no trimestre (143 mil) superam os sorteios de ativas (52 mil): sorteio para restituição pesa no uso do fundo. Números exploratórios deste item, exceto os de `results/parametros_fixos.csv`, foram calculados fora de script; refazer em código antes de usar no texto.
21. **[TCC] Contaminação parcial de um momento de teste.** A revisão da regra de vagas e da exclusão (passo 1) foi motivada em parte pela distância em `frac_sem_contempl` vista na primeira rodada (26/10), antes de a partição ser fixada (09/11). O teste de H2 nesse momento é, portanto, mais fraco que o de `spearman_lance_tamanho`; isso entra em 7.2 e 8.3. No passo 1 nenhum momento de teste foi calculado no simulado.
22. **[TCC] Diagnóstico fora da partição:** fração dos sorteios que vai a excluídos. Dado 0,73 (painel B pós-285); protótipo 0,36; com inadimplência, exclusão por idade e recolocação, ~0,60 (`results/sim_heterogeneidade.csv`). Não entra em calibração nem em teste; serve para julgar a regra de sorteio único entre ativas e excluídos (§5 item 5).
23. **[TCC] Admissibilidade conferida nos PDFs (16/11).** Nem a Lei 11.795 nem a Res. 285 exigem sorteio equiprovável ou que o vencedor pague exatamente o lance ofertado: a forma do sorteio e as regras do lance são do contrato (Lei, art. 22, § 1º; Res., art. 2º, XII). Fixos pela norma: concorrem só ativos e excluídos, estes para restituição (Lei, arts. 21 e 22, § 2º); recursos suficientes (Lei, art. 23); lance só após os sorteios previstos (Res., art. 12, I); lance vencedor amortiza prestações vincendas (art. 12, parágrafo único) e o embutido é deduzido do crédito (art. 13, parágrafo único); a ata lista as cotas ofertantes e os percentuais oferecidos (art. 48). A Circular 3.432 foi revogada pela Res. 285 a partir de 01/07/2024 (nota do BCB no PDF).

## 6. Próximos passos acordados

**A partir de 15/11 — POO e seminário** (plano de 6 passos do chat [POO] de 15/11; parar e reportar a cada passo)
1. ~~Modelo de domínio em DDD~~ — rascunho feito em 15/11
2. Esqueleto Maven (Java 21) em `projetos/poo-jogo/`, domínio sem framework, README — depois do aceite das decisões de 15/11
3. Domínio Java fiel a `src/sim/grupo.py` (M0; M1/M2 com a especificação provisória até o TCC decidir, §3)
4. Testes JUnit 5 portados de `tests/test_simulador.py` + M1/M2; JaCoCo
5. Adaptador CLI JSON; teste de docking marcado como pendente
6. Slides de DDD, com referências conferidas na fonte primária. **Se o seminário cair em 17–19/11, este passo vem antes do 2**

**A partir de 09/11** (prompts em `PROMPTS.md`, um chat por entrega dentro do Projeto Claude)
1. Pedro: commit e push de tudo o que está pendente desde 16/10; registrar o tema Arquitetura Hexagonal na planilha de TAPOO até **10/11**
2. Coautores: confirmar a partição de momentos (§4, 09/11) e decidir a H1
3. TCC: ~~heterogeneidade por administradora~~ (15/11) → ~~M1/M2~~ (16/11) → calibração SMM → H2 → H3 → docking → caps. 4–7 em rascunho
4. POO: domínio Java e testes até ~16/11 (o seminário depende dele); CLI JSON para o docking
5. IA: verificar o ConsumerBR (segmento consórcio, rótulo, licença) e enviar o PDF da etapa 1

**Semana 1 (19–23/10)** — executada em 16/10 (etapa 1) e 26/10 (etapas 2, 4 e 5a em protótipo); a etapa 3 ficou só no código e nos slides

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
| 16/10/2026 | Cowork | Etapa 1: `src/pipeline/`, painéis A e B, `results/qualidade_dados.csv`, 14 testes; achados 14–17 |
| 26/10/2026 | Cowork | Etapas 2, 4 e 5a em protótipo: momentos, G1 formal, simulador M0 com 7 testes, primeira rodada; apresentação de andamento na reunião geral (números reais, simulador apresentado como protótipo) |
| 09/11/2026 | Cowork | Panorama e plano; partição de momentos aceita por Pedro; escopo integrado com POO, IA e seminário; repositório reorganizado em `projetos-consorcio/` com `tcc/`, `poo-jogo/`, `seminario-tapoo/`, `ia-reclamacoes/`; `CLAUDE.md` reescrito para o novo escopo |
| 15/11/2026 | Cowork [POO][SEM] | Seminário passa a DDD (PLANO e VISAO-INTEGRADA atualizados). Modelo de domínio em `projetos/seminario-tapoo/MODELO-DOMINIO.md`, com glossário reconferido nos PDFs da Lei 11.795 e da Res. 285. Achado: M1 é degenerado no grupo fechado (§3). Achado: reorganização de 09/11 não está no disco (§3). Sem shell: commit pendente com Pedro |
| 15/11/2026 | Cowork | [TCC] Passo 0: partição de 09/11 sem confirmação dos coautores (segue, com H2 marcada). Passo 1: heterogeneidade por administradora (vagas de sorteio proporcionais à capacidade, LogNormal entre administradoras), lance embutido, inadimplência/exclusão por idade/recolocação, simulador no grão do painel; 15 testes novos; achados 20–22 |
| 16/11/2026 | Cowork | [TCC] Passo 1 gravado na pasta (ESTADO mesclado com a sessão [POO][SEM] de 15/11). Passo 2: M1 (sorteio ponderado pela situação, $\omega$) e M2 (preço uniforme no $(k+1)$-ésimo lance) como estratégias trocáveis; 16 testes novos, incluindo leilão único e equivalência de receita. Sem shell: commits com Pedro |
| 16/11/2026 | Cowork | [TCC] Pedro aceita M1 e M2. Admissibilidade conferida na Lei e na Res. 285 (§5 item 23); $\omega=0$ fora do admissível (§4). Seção 4.3 em rascunho. Vickrey (1961) e Krishna (2010) verificados e no `.bib` |
