# Seminário de TAPOO: Modelagem com Domain-Driven Design (DDD)

**Disciplina:** Tópicos Avançados de POO · **Grupo:** Pedro F. Fassini e Antônio F. Fassini · **Tema na planilha:** Modelagem com DDD (a Arquitetura Hexagonal, tema original, ficou com o grupo 3; mudança registrada no `ESTADO.md` §4 em 15/11) · **Apresentação:** entre 17/11 e 26/11, 35 a 45 minutos, os dois falando · **Data do grupo:** a confirmar

## O que vamos fazer

Uma apresentação sobre DDD que cobre o conteúdo pedido pelo enunciado e usa como caso real o modelo de domínio do nosso jogo de consórcio (`MODELO-DOMINIO.md`, nesta pasta). O caso tem o que um exemplo de livro não tem: linguagem tirada de lei (Lei 11.795/2008 e Res. BCB 285/2023), uma invariante legal que decide o tamanho do agregado (art. 23: só contempla se houver recursos), um conflito real de linguagem no código antigo (`ATIVA` no motor Python) e uma segunda implementação em outra linguagem ligada por linguagem publicada (o docking com o TCC).

## Roteiro (40 min)

| Bloco | Min | Quem | Conteúdo |
|---|---|---|---|
| 1. Definição e contexto | 5 | Pedro | O que é DDD; origem (Evans); o problema que ataca: complexidade do domínio, não da tecnologia; quando o domínio é o núcleo do sistema |
| 2. Conceitos estratégicos | 8 | Pedro | Linguagem ubíqua; domínio, subdomínio (núcleo, de suporte, genérico); contexto delimitado; mapa de contextos (cliente/fornecedor, conformista, camada anticorrupção, linguagem publicada, núcleo compartilhado) |
| 3. Conceitos táticos | 8 | Antônio | Entidade, objeto de valor, agregado e raiz, invariante, evento de domínio, serviço de domínio, repositório, fábrica, módulo |
| 4. Relação com POO e arquitetura | 5 | Antônio | Encapsulamento e invariantes no agregado; VO imutável; Strategy e State como políticas de domínio; modelo anêmico × rico; DDD e arquiteturas que isolam o domínio (camadas, portas e adaptadores, *clean*), sem repetir o seminário do grupo 3 |
| 5. Caso real: o consórcio | 9 | Ambos | Glossário da lei → nomes no código; por que Fundo **não** é contexto próprio; o agregado `Grupo` e suas invariantes; ciclo de vida da cota (State); eventos `CotaContemplada`/`CotaExcluida`; contextos Partida e Pesquisa; trechos reais do código Java |
| 6. Ferramentas | 2 | Antônio | Event Storming; diagramas de contexto; ArchUnit e jMolecules para verificar a modelagem no código (a confirmar nas fontes) |
| 7. Vantagens e limites | 2 | Pedro | Ganho em domínio complexo e vida longa; custo em CRUD; risco de cerimônia (todo conceito vira classe); exige acesso a quem conhece o domínio |
| 8. Tendências e fechamento | 1 | Pedro | DDD e microsserviços (contexto delimitado como fronteira de serviço); monólito modular; perguntas |

Os tempos somam 40; a margem até 45 é para perguntas.

## Como vamos fazer

- **Slides:** design sóbrio, pouco texto por slide, código real do projeto (não exemplo genérico). Cada conceito tático aparece com a classe correspondente do jogo.
- **Diagramas:** os de `MODELO-DOMINIO.md` (mapa de contextos, classes do agregado, estados da cota, sequência da assembleia), redesenhados para slide.
- **Dependência:** o bloco 5 precisa de código Java compilando (passos 2 a 4 do jogo). Se a data cair em 17–19/11, o bloco 5 usa o modelo e o esqueleto, e o código entra como "em construção", dito assim.
- **Referências candidatas** (conferir cada uma na fonte primária antes de usar; nenhuma entra de memória):
  - Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (Addison-Wesley);
  - Eric Evans, *Domain-Driven Design Reference* (resumo dos padrões publicado pelo autor);
  - Vaughn Vernon, *Implementing Domain-Driven Design* (Addison-Wesley);
  - Vaughn Vernon, *Domain-Driven Design Distilled* (Addison-Wesley);
  - Vlad Khononov, *Learning Domain-Driven Design* (O'Reilly);
  - Alberto Brandolini, material sobre Event Storming;
  - Martin Fowler, verbetes do bliki sobre contexto delimitado e modelo anêmico;
  - Alistair Cockburn, texto original sobre arquitetura hexagonal (só para o bloco 4);
  - documentação do ArchUnit e do jMolecules.

  Ano, editora e ISBN entram só depois de conferidos. Status de cada uma é atualizado aqui (`candidata` → `verificada`).
- **Ensaio:** pelo menos uma vez com cronômetro, e revisão cruzada dos slides entre os dois.
- **Grupos com tema vizinho:** o grupo 3 apresenta Arquitetura Hexagonal. Trocar slides com 48 h de antecedência, como recomenda o enunciado, para o bloco 4 não repetir o deles.

## O que este projeto recebe dos outros

- **Do POO:** o modelo de domínio e o código de exemplo. A ordem importa: o domínio Java tem de estar de pé antes da apresentação.
- **Para o POO:** a pesquisa do seminário vira parte do relatório de padrões (Strategy, State, Repository, eventos) e do relatório de conceitos de POO (encapsulamento e invariantes no agregado).
