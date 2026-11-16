# Instruções do projeto — Consórcio: TCC + POO + IA + Seminário

*Colar no campo de instruções do Projeto Claude. Também vale como `CLAUDE.md` na raiz do repositório. Lido no início de todo chat.*

---

## 1. O que é este projeto

Um único domínio, o **mecanismo de contemplação do Sistema de Consórcios brasileiro** (sorteio e lance, Lei 11.795/2008 e Res. BCB 285/2023), atende a quatro entregas de Pedro Freitas Fassini na Escola Politécnica da USP:

| Entrega | Grupo | Prazo | Onde mora |
|---|---|---|---|
| **TCC** — avaliação computacional do mecanismo por simulação multiagente calibrada nos dados do Bacen. Orientador: Prof. Dr. Paulo Sergio Cugnasca | Pedro F. Fassini, Antônio F. Fassini, Pedro Paulo T. Silveira | semana de 30/11–04/12 (data a confirmar na EPUSP) | `tcc/` |
| **POO** — jogo educacional web "Consórcio: espera ou lance?", em Java, arquitetura hexagonal (Laboratório de POO) | Pedro e Antônio (exceção de 2 integrantes autorizada pelo professor) | entrega única 01/12/2026 | `poo-jogo/` |
| **Seminário de TAPOO** — Arquitetura Hexagonal, com o motor do jogo como caso real | Pedro e Antônio | inscrição até 10/11; apresentação entre 17/11 e 26/11, de 35 a 45 min | `seminario-tapoo/` |
| **IA (PCS3838, Prof. Jaime Sichman)** — classificação supervisionada de reclamações de consumidores sobre consórcio | trio do TCC | etapa 1 (dataset): data a confirmar no Moodle | `ia-reclamacoes/` |

**Como as quatro se ligam** (detalhe em `VISAO-INTEGRADA.md`):
- O TCC fornece o modelo, os parâmetros calibrados e os casos de verificação ao jogo.
- O jogo devolve ao TCC uma segunda implementação independente, para *docking* (seção 6.5).
- O seminário usa o motor do jogo como caso real.
- O projeto de IA alimenta a motivação e as implicações do TCC (caps. 1 e 8) e os eventos do jogo.

**Regra de prioridade:** o TCC é o caminho crítico e **nunca espera** pelos outros. Se algo apertar, o jogo usa os parâmetros do protótipo e o docking vira trabalho em andamento.

**Antes de qualquer coisa em toda sessão: leia `ESTADO.md`** (estado das quatro entregas, decisões, pendências) e o `PLANO.md` da entrega em que for trabalhar. Decisão registrada não se rediscute sem registrar a reabertura.

## 2. Onde mora cada coisa

Repositório `projetos-consorcio` (antes `tcc-consorcio`). Na raiz ficam só os arquivos comuns e uma pasta por entrega:

```
projetos-consorcio/
├── CLAUDE.md  ESTADO.md  VISAO-INTEGRADA.md  PROMPTS.md  .gitignore
├── tcc/              (TCC: Python, monografia, dados)
├── poo-jogo/         (jogo Java, Maven)
├── seminario-tapoo/  (slides e roteiro)
└── ia-reclamacoes/   (PCS3838)
```

**Comum**

| Caminho | Conteúdo |
|---|---|
| `ESTADO.md` | Estado, log de decisões (§4), pendências, achados, histórico — das quatro entregas |
| `VISAO-INTEGRADA.md` | Mapa das conexões, calendário combinado, riscos |
| `PROMPTS.md` | Prompts de abertura de cada chat |

**TCC (`tcc/`; caminhos abaixo relativos a essa pasta, e os comandos `make` e `python` rodam de dentro dela)**

| Caminho | Conteúdo |
|---|---|
| `CONTEXT.md` | Constituição do TCC: tese, pergunta, hipóteses, escopo excluído, notação canônica, fontes |
| `docs/PLANO.md`, `docs/GUIA-ABNT.md`, `docs/BIBLIOGRAFIA.md`, `docs/estrutura.tsv` | Plano, normas, controle bibliográfico, manifesto das 42 seções |
| `text/*.md` | Monografia, um arquivo por seção, com frontmatter |
| `refs/refs.bib`, `refs/pdfs/`, `refs/fichamentos/` | Referências verificadas, um PDF por chave, fichamentos |
| `data/raw/` (imutável), `data/processed/` (descartável) | Dados do Bacen e painéis |
| `results/` | **Única fonte de número para o texto do TCC** |
| `src/pipeline/`, `src/analysis/`, `src/sim/`, `tests/` | Pipeline, momentos, simulador (Python), testes |
| `scripts/audit.py`, `prompts/` | Auditoria de ancoragem; prompts P0 a P7 |

**Outras entregas**

| Caminho | Conteúdo |
|---|---|
| `poo-jogo/PLANO.md` | Plano do jogo; o código Maven fica em `poo-jogo/` |
| `seminario-tapoo/PLANO.md` | Roteiro do seminário, referências, slides |
| `ia-reclamacoes/PLANO.md` | Dataset, modelagem, entregas da PCS3838 |

## 3. Regras invioláveis

**Do TCC** (valem só para o que vai para a monografia):
1. **Nenhum número no texto sem célula correspondente em `results/`.** Números de fonte externa citada vão no campo `excecoes` do frontmatter.
2. **Nenhuma citação sem PDF em `refs/pdfs/`.** Nunca gerar referência de memória. Faltando a referência, escrever `[CITAR: descrição]`; faltando o resultado, `[RESULTADO PENDENTE: qual]`.
3. **Nenhuma seção escrita antes de o P0 dar `PRONTA`.**
4. **Nenhuma decisão de modelagem fora do log em `ESTADO.md` §4.**
5. **Nenhum experimento novo depois do congelamento** (fim de S5 no cronograma vigente).

**De todas as entregas:**
6. **Referência só depois de conferida na fonte primária.** Vale para slides, relatórios e o trabalho de IA. Candidata não conferida é marcada como tal.
7. **Cada entrega tem código e texto próprios.** O domínio é compartilhado; o código não. O TCC não importa código Java, e o jogo não importa código Python. A única ponte entre os dois é a CLI JSON do jogo, usada pelo teste de docking. Confirmar com cada professor que o reaproveitamento do domínio é aceito.
8. **Nada inventado em entrega.** Resultado não rodado não aparece como feito; protótipo é chamado de protótipo.

## 4. Como trabalhar

### Início de sessão
Ler `ESTADO.md` e o `PLANO.md` da entrega. Para escrita do TCC, ler também `CONTEXT.md`. Dizer em uma ou duas linhas onde a entrega está e o que se propõe fazer agora. Não recapitular o projeto.

### Durante
- Trabalhar direto nos arquivos da pasta; não produzir no chat conteúdo que deveria virar arquivo.
- Nunca escrever fora da pasta vinculada. Antes de editar um arquivo existente, ler o arquivo.
- **TCC:** rodar `python scripts/audit.py` depois de escrever ou alterar seção. Loop `prompts/P0` → `P4` → auditoria → `P5`, e só então `status: fechado`.
- **POO:** todo código com teste; `mvn test` verde antes de dar algo por pronto. O que for dito nos relatórios aponta classe ou trecho real.
- **Testes de qualquer entrega:** se o teste falhar, corrige-se o código, nunca o teste.
- O `Makefile` é protegido contra escrita remota: mudança nele é proposta ao Pedro, não feita.

### Registro no `ESTADO.md`
Registrar na hora, não no fim. Cada entrada indica a entrega (`[TCC]`, `[POO]`, `[SEM]`, `[IA]`).
- decisão de modelagem, escopo ou método → §4, com data, motivo e quem
- achado caro de redescobrir → §5
- seção ou artefato que muda de status → §2
- pendência que surge ou se resolve → §3
- gate ou marco atingido → §1

**Ao fim de toda sessão:** atualizar §1, §6, uma linha em §7 e a data no topo.

### Git
Repositório único `antonioffassini/projetos-consorcio` (antes `tcc-consorcio`; o GitHub redireciona o nome antigo), privado. Ao fim de cada passo concluído:
- **Se houver shell no computador:** `git add`, `git commit` com mensagem descritiva prefixada pela entrega (`[TCC]`, `[POO]` …) e `git push`, sem pedir.
- **Sem shell:** listar os arquivos alterados e pedir o commit ao Pedro, pelo GitHub Desktop.
- Nunca fazer commit de `tcc/data/processed/`, `.venv/`, `target/` nem segredos. Nunca fazer `force push`.

### Bibliografia
`docs/BIBLIOGRAFIA.md` controla a bibliografia do TCC. Status: `candidata` → `verificada` → `pdf baixado` → `fichada` → `citada`; só entra em `refs/refs.bib` a partir de `verificada`. As outras entregas mantêm a lista de referências no próprio `PLANO.md`, com o mesmo critério de verificação.

## 5. Quando usar o navegador

Para:
- baixar dados (Bacen, datasets de IA) e PDFs;
- buscar em BDTD, Teses USP, CAPES, SciELO, SPELL, working papers do BCB, ACL Anthology e Hugging Face;
- verificar dados bibliográficos e licenças contra a fonte primária;
- checar texto vigente de lei e de normativo.

Não para responder pergunta que já está nos documentos do projeto, nem para reconferir algo registrado em `ESTADO.md` §5. Arquivo baixado vai direto para o caminho certo e é registrado no `ESTADO.md`.

## 6. Como falar

- Português brasileiro. Direto, denso, sem preâmbulo.
- Profundidade de praticante: Pedro trabalha com crédito estruturado e private equity e estuda engenharia de computação; não explicar o básico de finanças nem de programação.
- Discordar quando houver motivo, e dizer o motivo. Não suavizar problema de método, escopo ou prazo, inclusive conflito de calendário entre as quatro entregas.
- Quando algo não for verificável, dizer que não é.
- Não narrar antes de fazer; fazer e relatar o que mudou nos arquivos e o que ficou pendente.
- Sem bajulação.

## 7. Voz dos textos

- **Monografia do TCC:** impessoal ("este trabalho propõe"), português formal, ABNT, sem primeira pessoa e sem adjetivo valorativo. A Introdução **não antecipa resultados** (exigência da EPUSP). Notação exclusivamente conforme `CONTEXT.md` §5; símbolo novo entra lá antes de aparecer no texto. Sem trejeitos típicos de IA: deve soar como texto de estudante com gosto pelo tema.
- **Relatórios de POO:** técnicos e concretos; toda afirmação aponta classe, método ou teste.
- **Slides do seminário:** pouco texto por slide, código real do projeto, referências no fim.
- **IA:** relatório técnico com métricas, sempre comparadas a um baseline.

## 8. O que não fazer

- Não reescrever seção do TCC com `status: fechado` sem pedido explícito.
- Não alterar `docs/estrutura.tsv` sem registrar a decisão no `ESTADO.md`.
- Não ampliar o escopo do TCC sem checar `CONTEXT.md` §4 e sinalizar que é ampliação. O docking na seção 6.5 é a única ampliação já aprovada.
- Não editar `data/raw/`.
- Não gerar `.docx` à mão; só por `make docx`.
- Não migrar o simulador do TCC para Java.
- Não criar documento de apoio novo sem necessidade clara; cada entrega tem um `PLANO.md`, e o estado de todas fica no `ESTADO.md`.
