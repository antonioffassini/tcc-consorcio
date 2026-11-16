# Projeto de POO: jogo educacional "Consórcio: espera ou lance?"

**Disciplina:** Laboratório de POO · **Grupo:** Pedro F. Fassini e Antônio F. Fassini (exceção de 2 integrantes autorizada pelo professor) · **Entrega única:** 01/12/2026 · **Onde:** `poo-jogo/` no repositório `projetos-consorcio` (projeto Maven independente; para a entrega, dar acesso ao professor ou exportar a pasta para um repositório próprio)

## O que vamos fazer

Um **jogo educacional web** sobre educação financeira. O jogador é um cotista num grupo de consórcio de imóvel, com centenas de outros cotistas simulados. A cada assembleia mensal ele vê o saldo do fundo, o histórico de lances e o próprio caixa, e decide se dá lance e de quanto.

- **Objetivo do jogador:** conseguir o crédito antes que a sua "urgência" vença (o aluguel sobe, a família cresce) sem comprometer o caixa.
- **O que a mecânica ensina** (a exigência do enunciado é que a mecânica ensine o tema, não que seja só um verniz temático):
  - lance é antecipar parcelas, não pagar a mais;
  - esperar tem custo, e quem tem liquidez fura a fila;
  - todo mundo em dia acaba contemplado, então o que está em jogo é o *quando*;
  - a exclusão por atraso tem consequência real.
- **Modo "regulador" (fase final):** o jogador troca a regra (M0, M1 ou M2) e vê quem ganha e quem perde. É o mesmo experimento da H3 do TCC, só que jogável.
- **Problema socioeconômico:** educação financeira e inclusão de crédito. O consórcio atende a um público que muitas vezes não acessa financiamento bancário e decide sem entender o mecanismo.

## Como vamos fazer

**Stack:** Java 21, Spring Boot (REST e servidor web), frontend simples (HTML, CSS e JavaScript, ou Thymeleaf), persistência com Spring Data JPA e PostgreSQL (partidas, ranking, histórico), JUnit 5, JaCoCo, Maven e Docker. O deploy fica num serviço com plano gratuito que aceite Docker, como Render ou Railway; a escolha fica para quando chegar a hora, depois de conferir os limites do plano.

**Modelo de domínio em DDD** (desenho completo em `../seminario-tapoo/MODELO-DOMINIO.md`, que também é o caso do seminário de DDD) com **portas e adaptadores** por dentro, para manter o domínio livre de framework:

```
domínio (Java puro, sem framework)
  Grupo (raiz do agregado), Cota, Fundo; objetos de valor Valor, Lance, Parcela, Credito, SaldoDevedor, Perfil
  RegraContemplacao  ← Strategy por composição: RegraSorteio (SorteioUniforme, SorteioPonderado)
                       + RegraLance (LancePayAsBid, LancePrecoUniforme); M0, M1, M2
  PoliticaLance      ← Strategy: PoliticaParametrica (bots), DecisaoJogador
  PoliticaExclusao   ← Strategy: RiscoConstante
  SituacaoCota       ← State: NaoContemplada, Contemplada, Excluida, Restituida
  eventos: CotaContemplada, CotaExcluida, CotaRestituida, AssembleiaRealizada, GrupoEncerrado
portas (interfaces)
  entrada:  JogarAssembleia, IniciarPartida, TrocarRegra, SimularGrupo (CLI)
  saída:    RepositorioPartida, GeradorAleatorio, PublicadorEventos
adaptadores
  web (Spring MVC/REST) · JPA/Postgres · CLI JSON (para o docking com o TCC) · testes
```

**Padrões candidatos ao catálogo** (só entram os que forem de fato usados):

| Padrão | Uso |
|---|---|
| Strategy | Regra de contemplação e política de lance |
| State | Situação da cota |
| Factory | Criação dos agentes a partir dos parâmetros calibrados |
| Observer | Eventos da assembleia para a interface e o log |
| Repository | Porta de persistência |
| Builder | Configuração do grupo |

**Testes:**
- unitários no domínio: os mesmos casos de resposta conhecida do TCC (espera média (T+1)/2, sorteio uniforme, conservação do dinheiro, todos contemplados sem inadimplência, leilão (n−1)/n);
- integração: API e repositório;
- aceitação: uma partida inteira;
- docking contra o Python do TCC.

**Pacote de entrega (01/12):**
- código e aplicação no ar;
- documentação;
- UML de classes, gerado a partir do código;
- UML de casos de uso;
- relatório de boas práticas, com a classe ou o trecho de cada prática;
- catálogo de padrões no modelo Padrão / Problema / Alternativa / Trade-off;
- relatório de testes, com o relatório do JaCoCo;
- relatório de conceitos de POO, inclusive onde *não* se usou herança e por quê (o Strategy por composição no lugar de subclasses de `Grupo`).

## Cronograma (proposta)

| Quando | O quê |
|---|---|
| 10–14/11 | Domínio e testes unitários (porte do motor Python); CLI JSON; primeiro docking |
| 15–21/11 | Casos de uso, API, persistência, frontend mínimo jogável |
| 22–26/11 | Modo regulador, deploy, UML |
| 27–30/11 | Quatro relatórios, revisão e congelamento |
| 01/12 | Entrega |

## O que este projeto recebe dos outros

- **Do TCC:** o modelo e os parâmetros calibrados. Enquanto a calibração não sai, o jogo roda com os parâmetros do protótipo.
- **Do seminário (DDD):** o modelo de domínio, a linguagem ubíqua e a justificativa do agregado; o relatório de padrões e o seminário compartilham pesquisa.
- **Do projeto de IA:** os tipos de problema mais frequentes nas reclamações reais viram eventos e dicas no jogo ("restituição demora", "lance embutido reduz o crédito").
