# Git no TCC — guia de uso

Guia operacional para o repositório `tcc-consorcio`. Premissa atual: só Pedro e o Claude
mexem no repositório; os coautores entram depois (seção 7).

---

## 1. O modelo mental em cinco peças

| Peça | O que é | No TCC |
|---|---|---|
| **Working tree** | Os arquivos como estão na pasta agora | `C:\Users\anton\Documents\tcc-consorcio` |
| **Staging (índice)** | O que vai entrar no próximo commit | Você escolhe: "só o `text/04-1-ambiente.md` e o `ESTADO.md`" |
| **Commit** | Uma fotografia datada e assinada do projeto, com mensagem | "texto(4.1): rascunho do ambiente" |
| **Remote (`origin`)** | A cópia no GitHub | `github.com/<seu-usuario>/tcc-consorcio`, privado |
| **Tag** | Um nome fixo para um commit | `G3-congelamento` marca o estado de `results/` na sexta 02/10 |

O ciclo é sempre: **editar → `git add` → `git commit` → `git push`**. Commit é local e barato;
push é o que salva no GitHub. Até dar push, o trabalho só existe no notebook.

---

## 2. Configuração inicial (uma vez só)

### 2.1 Conferir o que já existe

O repositório já foi iniciado em 22/09 (`git init` + um commit inicial), mas **sem remote** e com
a identidade do Antônio. No terminal do VS Code, dentro da pasta:

```powershell
git --version            # deve responder 2.5x
git status               # mostra o que mudou desde o commit inicial
git log --oneline        # mostra o commit inicial
git remote -v            # vazio = ainda não tem GitHub
```

### 2.2 Identidade

Este notebook está logado como Antônio, e o `git config` do repositório está com o nome dele.
Se quem vai assinar os commits daqui em diante é você, configure **só neste repositório**
(sem `--global`, para não mexer no git do Antônio em outros projetos):

```powershell
git config user.name  "Pedro Freitas Fassini"
git config user.email "p2fassini@gmail.com"
```

Autoria importa: a banca pode pedir o histórico, e ele mostra quem fez o quê.

### 2.3 GitHub CLI e login

```powershell
winget install --id GitHub.cli
# feche e reabra o terminal
gh auth login        # GitHub.com → HTTPS → Login with a web browser
gh auth status       # confirma que está logado na SUA conta
```

Se o `gh` já estiver logado com a conta do Antônio, rode `gh auth logout` antes e entre com a sua.

### 2.4 Criar o repositório privado e subir

```powershell
gh repo create tcc-consorcio --private --source . --remote origin --push
```

Isso cria o repositório **privado** na sua conta, liga a pasta a ele e envia o histórico.
Confira em `https://github.com/<seu-usuario>/tcc-consorcio`.

### 2.5 Como o Claude acessa

O Claude não precisa de conta no GitHub. O **Claude Code** roda na sua máquina e usa o seu
login do `gh` e do git; ele executa `git add`, `commit` e `push` como você, e você aprova cada
comando. A sessão do Cowork (esta) lê e escreve na pasta, mas **não roda git**: o que ela
altera fica como mudança pendente até uma sessão do Claude Code (ou você) fazer o commit.

---

## 3. O dia a dia

### 3.1 Início de sessão

```powershell
git pull             # traz o que estiver no GitHub (vira essencial quando os coautores entrarem)
git status           # vê se ficou algo pendente da sessão anterior (inclusive do Cowork)
```

### 3.2 Durante: commits pequenos e temáticos

Um commit = uma coisa com sentido. Exemplos reais deste projeto:

```powershell
# Dados baixados pelo Cowork
git add data/raw/bacen ESTADO.md
git commit -m "dados: 237 arquivos do Bacen (consolidados, UF, contábeis), 2017-03 a 2026-05"

# Pipeline do painel
git add src/pipeline tests/test_pipeline.py
git commit -m "pipeline: build_panel lê Bens_Imoveis_Grupos e gera painel.parquet"

# Seção do texto, depois da auditoria passar
python scripts/audit.py
git add text/04-1-ambiente.md
git commit -m "texto(4.1): rascunho do ambiente; notação conforme CONTEXT §5"

# Decisão de modelagem: vai sempre junto com o ESTADO.md
git add ESTADO.md CONTEXT.md
git commit -m "decisao: momentos de teste = fração lance/sorteio por quartil de prazo"
```

Prefixos usados: `dados:`, `pipeline:`, `sim:`, `calib:`, `results:`, `texto(N.N):`,
`refs:`, `decisao:`, `infra:`, `estado:`. Assim o `git log --oneline` vira um diário legível.

**Nunca use `git add .` às cegas.** Rode `git status` antes e adicione pelo nome. É assim que
um `.docx` de rascunho, um CSV de teste ou um arquivo com senha não entram por acidente.

### 3.3 Fim de sessão (obrigatório)

```powershell
python scripts/audit.py                 # se mexeu em text/
git add ESTADO.md <o que mais mudou>
git commit -m "estado: fim de sessão 26/09 — painel rodando, G1 decidido"
git push
```

Commit sem push não conta: se o notebook morrer, perdeu.

---

## 4. Tags: como o congelamento vira regra técnica

Os gates do plano viram tags. A tag é o que torna "congelado" verificável.

```powershell
git tag -a G2-spike -m "make all roda do zero; primeira tabela real"
git tag -a G3-congelamento -m "results/ congelado; nenhum experimento novo"
git push --tags
```

Depois de `G3-congelamento`, para provar que `results/` não mudou:

```powershell
git diff G3-congelamento -- results/     # tem que sair vazio
```

Se sair qualquer coisa, alguém rodou experimento depois do congelamento. A regra 5 do
projeto passa a ter teste automático.

---

## 5. Desfazer coisas

| Situação | Comando |
|---|---|
| Estraguei um arquivo e quero a versão do último commit | `git restore text/04-1-ambiente.md` |
| Adicionei ao staging por engano | `git restore --staged arquivo` |
| Quero ver o que mudou antes de commitar | `git diff` (não staged) / `git diff --staged` |
| Commitei algo errado e **já dei push** | `git revert <hash>` (cria commit que desfaz; não reescreve histórico) |
| Quero ver como a seção 2.2 estava em 12/09 | `git log --oneline -- text/02-2-contemplacao.md` e `git show <hash>:text/02-2-contemplacao.md` |
| Commitei, **não** dei push, e quero só corrigir a mensagem | `git commit --amend -m "mensagem nova"` |

Evite `git reset --hard` e `git push --force`. Com push feito, a regra é `revert`.

---

## 6. Branches: quando usar (pouco)

Com uma pessoa só, trabalhe direto na `main`. Branch só para experimento arriscado que você
talvez jogue fora:

```powershell
git switch -c exp/sorteio-ponderado     # cria e entra no branch
# ... Claude Code implementa M1, você testa ...
git switch main
git merge exp/sorteio-ponderado          # se deu certo
git branch -d exp/sorteio-ponderado      # se não deu, apaga e segue: git branch -D ...
```

---

## 7. Quando os coautores entrarem

```powershell
gh repo edit --visibility private        # confirma que continua privado
gh api repos/<seu-usuario>/tcc-consorcio/collaborators/<usuario-do-antonio> -X PUT -f permission=push
```

(ou GitHub → Settings → Collaborators → Add people.)

A partir daí, três regras:

1. **`git pull` antes de começar, sempre.**
2. **Cada trilha mexe nos seus arquivos.** Trilha A em `src/pipeline` e `text/05-*`, trilha B em
   `src/sim` e `text/04-*`, e assim por diante. Assim o git não tem conflito para resolver.
3. **`ESTADO.md` é o arquivo que todo mundo edita**, e portanto o que mais vai conflitar. Edite
   pouco por vez, commite logo e dê push logo.

Se aparecer conflito (`CONFLICT (content)`), o git marca o trecho no arquivo com `<<<<<<<`,
`=======`, `>>>>>>>`. Peça ao Claude Code para resolver mostrando as duas versões; confira e
commite.

---

## 8. O que fica fora do git (`.gitignore`)

- `refs/pdfs/*.pdf` — por licença. Consequência: coautor que clonar não tem os PDFs e a
  auditoria dele falha. Com repositório privado de três pessoas, dá para rever essa regra;
  se revisar, registrar em `ESTADO.md` §4.
- `data/processed/*` — é gerado por `make painel`; qualquer um regenera.
- `.venv/`, `__pycache__/`, `build/*.pdf` e intermediários do LaTeX.

`data/raw/` **entra** no git: é pequeno, é imutável e é a base da reprodutibilidade.
