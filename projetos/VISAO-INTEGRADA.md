# Visão integrada: um domínio, quatro entregas

Planos de cada entrega: [`ESTADO.md`](ESTADO.md) (estado e decisões das quatro entregas) · [`poo-jogo/PLANO.md`](poo-jogo/PLANO.md) · [`seminario-tapoo/PLANO.md`](seminario-tapoo/PLANO.md) · [`ia-reclamacoes/PLANO.md`](ia-reclamacoes/PLANO.md)

**O núcleo:** o mecanismo de contemplação do consórcio (sorteio e lance). Os quatro projetos olham para o mesmo objeto por ângulos diferentes, e cada um produz algo que outro consome.

```
                 ┌────────────────────────────┐
                 │   TCC (Python, pesquisa)   │
                 │ dados Bacen → modelo →     │
                 │ calibração → H2 → H3       │
                 └───────┬───────────▲────────┘
     parâmetros calibrados│           │docking (seção 6.5):
     + casos de verificação│           │mesmas sementes, mesmas
                          ▼           │distribuições?
                 ┌────────────────────┴───────┐        ┌───────────────────────┐
                 │ POO: jogo "espera ou lance"│◄──────►│ Seminário TAPOO:      │
                 │ Java, DDD + portas, web    │ caso   │ Modelagem com DDD     │
                 └────────────▲───────────────┘ real / └───────────────────────┘
                              │ eventos do jogo  pesquisa
                 ┌────────────┴───────────────┐
                 │ IA: reclamações sobre      │──► TCC caps. 1 e 8
                 │ consórcio (classificação)  │    (onde o mecanismo dói)
                 └────────────────────────────┘
```

## As conexões, uma a uma

| De → Para | O que passa | Por que vale |
|---|---|---|
| TCC → POO | Modelo, parâmetros calibrados, casos de teste de resposta conhecida | O jogo nasce validado; os testes do TCC viram testes JUnit |
| POO → TCC | Segunda implementação independente, comparada por docking | Validação cruzada na seção 6.5; mostra que o resultado não depende de bug de uma implementação |
| POO ↔ Seminário | O modelo de domínio do jogo (`seminario-tapoo/MODELO-DOMINIO.md`) é o caso real do seminário de DDD; a pesquisa do seminário justifica o agregado, os objetos de valor e os eventos | A mesma pesquisa serve ao seminário e aos relatórios de padrões e de conceitos de POO |
| IA → TCC | Tipos de problema mais frequentes nas reclamações reais | Motivação (cap. 1) e implicações (cap. 8) com evidência, não só argumento |
| IA → POO | Problemas reais viram eventos e dicas no jogo | Reforça o propósito pedagógico exigido no enunciado de POO |

## Calendário combinado

| Data | Marco |
|---|---|
| **10/11** | Inscrição do tema do seminário. Arquitetura Hexagonal ficou com o grupo 3; tema registrado: **Modelagem com DDD** |
| 09–13/11 | TCC: calibração, H2, H3 em protótipo · POO: domínio Java e testes · IA: verificar o dataset e enviar a etapa 1 |
| 15/11 | Modelo de domínio em DDD (`seminario-tapoo/MODELO-DOMINIO.md`), antes do código |
| ~16–18/11 | Domínio Java de pé (o bloco de caso do seminário depende dele) · primeiro docking |
| 17–26/11 | Seminário de DDD (data do grupo a definir; trocar slides com o grupo 3, de hexagonal, 48 h antes) · POO: API, frontend, deploy · TCC: caps. 4 a 7 |
| 27–30/11 | POO: relatórios · TCC: caps. 3, 8 e 9 e revisão |
| **01/12** | Entrega de POO |
| 30/11–04/12 | Entrega do TCC (data a confirmar) |

## Riscos e regras de convivência

- **O caminho crítico é o TCC.** Se algo apertar, o jogo usa os parâmetros do protótipo e o docking vira "trabalho em andamento". O TCC não espera pelo Java.
- **Um repositório (`projetos-consorcio`), uma pasta por entrega.** `tcc/` (Python, com as regras de sempre), `poo-jogo/` (Maven), `seminario-tapoo/` e `ia-reclamacoes/`. Nenhuma pasta importa código de outra; o docking passa só pela CLI JSON do jogo, chamada a partir do TCC.
- **Reaproveitamento entre disciplinas:** confirmar com cada professor que usar o mesmo domínio é aceito. Cada entrega tem de ter o seu código e o seu texto próprios.
- **Carga:** são quatro entregas entre 10/11 e ~04/12, em paralelo às outras disciplinas. Cortes já previstos: a H1 (aprendizado por reforço) do TCC fica mínima; o modo regulador do jogo é o último item a entrar.
