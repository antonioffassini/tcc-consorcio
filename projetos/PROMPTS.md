# Prompts de abertura dos chats

Cada chat é aberto dentro do Projeto Claude, com a pasta `C:\Users\anton\Documents\projetos-consorcio` vinculada. Copie o bloco inteiro.

---

## 1. TCC: calibração, comparação e caps. 4 a 7

```
[TCC] Leia ESTADO.md (raiz), tcc/CONTEXT.md, tcc/docs/estrutura.tsv, tcc/src/pipeline/README.md, tcc/src/sim/grupo.py e tcc/src/analysis/momentos.py, e siga o CLAUDE.md. Caminhos do TCC abaixo são relativos a tcc/. Regras: número só com arquivo em results/; data/raw é imutável; decisão registrada no ESTADO.md na hora, com prefixo [TCC]; commit e push ao fim de cada passo, se houver shell (senão, me liste os arquivos para eu commitar).

Meta: fechar o núcleo técnico em protótipo, com resultados em results/, e o rascunho dos caps. 4 a 7. Pare e me reporte ao fim de cada passo.

0. Confira no ESTADO §3 se os coautores já confirmaram a partição de momentos de 09/11. Se não, siga com ela mesmo assim, mas marque todo resultado de H2 como "partição pendente de confirmação".

1. Heterogeneidade: parâmetros por administradora (ou por cluster de administradoras) no simulador, com a forma justificada; incorpore o lance embutido (ESTADO §5) e revise a regra de vagas de sorteio, pelo achado 19. Os testes existentes continuam passando; acrescente os novos.

2. Regras M1 (sorteio ponderado; num grupo fechado, defina uma ponderação que não seja trivial e justifique) e M2 (lance de preço uniforme), como estratégias trocáveis, com teste de verificação. Inclua o caso do leilão único, (n−1)/n × valor.

3. Calibração SMM (SciPy) só sobre os momentos de calibração do §4, com matriz de pesos declarada, semente fixa e erro-padrão por bootstrap → results/calibracao_*.csv. Depois, e só depois, defina por escrito o critério de rejeição da H2 e abra os momentos de teste → results/h2_teste.csv.

4. Comparação M0 × M1 × M2 com o θ calibrado: bem-estar, dispersão do tempo de espera e estabilidade do fundo, com intervalos por replicação → results/h3_*.csv. Política de lance fixa entre regras = limitação explícita (crítica de Lucas), com [DECISÃO PENDENTE: papel do RL na comparação].

5. Prepare em src/sim/ uma interface de docking: um script que lê um JSON de parâmetros e sementes, roda o motor Python e grava os momentos em JSON, para comparar depois com a CLI do jogo Java. Por enquanto, só o lado Python.

6. Texto: rascunho de text/04-*, 05-*, 06-* e 07-*, com P0 antes de cada seção e scripts/audit.py depois; voz da monografia; [CITAR: …] onde não houver PDF; status: rascunho. Símbolo novo entra antes no CONTEXT.md §5, e você me avisa.

AO FINAL: ESTADO.md §1, §2, §3, §5, §6 e uma linha em §7; lista curta do que mudou em cada pasta e do que ficou pendente.
```

---

## 2. POO + seminário: jogo "Consórcio: espera ou lance?" e Arquitetura Hexagonal

```
[POO] Leia ESTADO.md, VISAO-INTEGRADA.md, poo-jogo/PLANO.md, seminario-tapoo/PLANO.md e tcc/src/sim/grupo.py (o motor Python do TCC, que é a especificação do domínio), e siga o CLAUDE.md. Registre decisões no ESTADO.md com prefixo [POO] ou [SEM]. Commit e push ao fim de cada passo, se houver shell (senão, me liste os arquivos). Não altere nada fora de poo-jogo/ e seminario-tapoo/, exceto o ESTADO.md.

Contexto: jogo educacional web em Java sobre o mecanismo de contemplação do consórcio, para o Laboratório de POO (Pedro e Antônio, entrega única em 01/12, com código, aplicação no ar, documentação, UML de classes e de casos de uso e quatro relatórios: boas práticas, padrões com trade-offs, testes, conceitos de POO). O seminário de TAPOO (Arquitetura Hexagonal, 35 a 45 min, entre 17/11 e 26/11) usa este motor como caso real, então o domínio precisa estar de pé até ~16/11.

Pare e me reporte ao fim de cada passo.

1. Esqueleto Maven (Java 21) em poo-jogo/ com os pacotes da arquitetura hexagonal (domínio sem framework, portas, adaptadores) e um README de como rodar.

2. Domínio: Grupo, Cota, Assembleia, Fundo, Agente; RegraContemplacao (Strategy: M0, depois M1 e M2); PoliticaLance (Strategy: paramétrica para os bots, decisão do jogador); SituacaoCota (State). Porte a dinâmica de tcc/src/sim/grupo.py com fidelidade: mesma ordem mensal e mesma contabilidade.

3. Testes JUnit 5 do domínio: porte os casos de tcc/tests/test_simulador.py (conservação, saldo ≥ 0, espera média (T+1)/2, sorteio uniforme, todos contemplados sem exclusão, semente fixa) e acrescente os de M1 e M2. Configure o JaCoCo.

4. Adaptador CLI JSON (parâmetros e sementes de entrada, momentos de saída) para o docking com o TCC. Escreva o teste de docking como pendente até o lado Python existir.

5. Seminário: rascunho dos slides em seminario-tapoo/, seguindo o roteiro do PLANO, com trechos reais do código. Referências candidatas conferidas na fonte primária antes de entrar.

Depois (próximos chats): casos de uso e API Spring, persistência, frontend jogável, modo regulador, deploy, UML e os quatro relatórios.

AO FINAL: ESTADO.md (§1, §2, §3, §6 e §7) e uma lista curta do que mudou e do que ficou pendente.
```

---

## 3. IA (PCS3838): classificação de reclamações sobre consórcio

```
[IA] Leia ESTADO.md, VISAO-INTEGRADA.md e ia-reclamacoes/PLANO.md, e siga o CLAUDE.md. Registre decisões no ESTADO.md com prefixo [IA]. Commit e push ao fim de cada passo, se houver shell (senão, me liste os arquivos). Trabalhe só em ia-reclamacoes/, exceto o ESTADO.md.

Contexto: trabalho de PCS3838 (Prof. Jaime Sichman), grupo de até 3 (o trio do TCC). Etapa 1: escolher um conjunto de dados textuais rotulados para classificação supervisionada, de tamanho adequado (nem pequeno nem excessivo), e entregar um PDF com nomes e NUSPs, nome do dataset, link, número de amostras, idioma e classes, com o nome PCS3838_Escolha_dataset_NUSP1_NUSP2_NUSP3.pdf. As etapas seguintes ainda não foram divulgadas.

Pare e me reporte ao fim de cada passo.

1. Verifique na fonte primária (artigo, repositório e licença) o ConsumerBR (PROPOR 2026): se há o segmento de administradoras de consórcio e com quantas amostras; qual campo serve de rótulo e quantas classes tem, com a distribuição; licença e link de download. Não afirme nada sem ter conferido.

2. Se o consórcio sozinho for pequeno ou mal rotulado, avalie os planos B (segmento financeiro mais amplo) e C (dados abertos do Consumidor.gov.br, se tiverem o texto do relato) com os mesmos critérios. Recomende um dataset em uma tabela comparativa e espere a minha escolha.

3. Com a escolha feita: baixe para ia-reclamacoes/data/raw/ (fora do git pelo .gitignore), escreva um script de perfil (amostras, classes, tamanho dos textos, duplicatas) e gere o PDF da etapa 1. Os nomes e NUSPs ficam como campos a preencher, se eu não os tiver passado.

4. Proposta (não implementação) da modelagem para as próximas etapas: divisão estratificada e temporal, baseline TF-IDF com modelo linear, modelo de linguagem em português, métricas (F1-macro, matriz de confusão).

AO FINAL: ESTADO.md (§1, §2, §3, §6 e §7) e uma lista curta do que mudou e do que ficou pendente.
```
