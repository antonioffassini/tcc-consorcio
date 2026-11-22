---
secao: 5.1
titulo: Fontes de dados
status: rascunho
responsavel:
insumos:
  - data/raw
  - src/pipeline/README.md
  - ESTADO.md §5 itens 6, 7, 10, 12, 14 e 15
fontes:
  - results/qualidade_dados.csv
  - results/fatos_momentos.csv
excecoes:
  - 285
  - 362
  - 381
  - 525
  - 4010
  - 4110
  - 2080
  - 3.432
paginas_alvo: 3
---

# Fontes de dados

Todos os dados do trabalho são públicos e vêm do banco de dados de consórcios que o Banco Central do Brasil mantém a partir das remessas obrigatórias das administradoras [CITAR: bcb2026consorcios — página do banco de dados; PDF ou captura datada pendente]. Não se usaram dados de administradoras, de associações setoriais nem de consorciados. Esta seção descreve o que cada arquivo contém, o recorte adotado e o que fica disponível para a calibração.

## Os arquivos do Bacen

O banco de dados é distribuído em três famílias de arquivos compactados, com leiaute único desde março de 2017.

**Arquivo mensal por grupo.** Para cada grupo de cada administradora, no segmento de imóveis, o arquivo `AAAAMMBens_Imoveis_Grupos.csv` traz, na data-base, o prazo do grupo, o número de assembleias realizadas, o valor médio do bem de referência e a contagem de cotas por situação: ativas em dia, ativas inadimplentes (contempladas ou não), excluídas e quitadas, além do número de cotas contempladas no mês. É a única fonte com grão de grupo, e dela sai o painel por grupo e mês (painel A). Duas propriedades limitam o uso: a contagem de contempladas não separa sorteio de lance, e o número de excluídas é um estoque, de modo que o fluxo mensal de exclusões só se obtém por diferença entre meses consecutivos do mesmo grupo.

**Arquivo trimestral por unidade da federação.** O arquivo `AAAAMMConsorcios_UF.csv` traz, por administradora, segmento e UF, as cotas ativas contempladas no trimestre por lance e por sorteio, separadamente, e o número de excluídos contemplados no trimestre, sem separação de canal. É a única fonte que distingue o canal da contemplação. Somadas as UFs, dela sai o painel por administradora e trimestre (painel B).

**Arquivos consolidados.** O arquivo `AAAAMMSegmentos_Consolidados.csv` traz os totais mensais por administradora e segmento e serve apenas para conciliar as somas dos grupos (seção 5.2). Os arquivos contábeis (Documentos 4010 e 4110) trazem saldos consolidados de todo o sistema, e não por administradora, e a série publicada termina em dezembro de 2024; não são usados.

A Instrução Normativa BCB n. 525/2024 mudou a remessa para o Documento 2080, mensal, a partir do fim de 2024. O pipeline confere o cabeçalho de cada arquivo contra o dicionário de dados e não encontrou nenhuma divergência em todo o período (`results/qualidade_dados.csv`, escopo `leiaute`).

As estatísticas da associação das administradoras, previstas no plano inicial, não entram no trabalho. São agregados do setor, sem grão de administradora ou de grupo, e não acrescentam nada que os arquivos do Bacen não tragam com mais detalhe.

## Recorte

O trabalho restringe-se ao segmento de imóveis e ao regime da Resolução BCB n. 285/2023. A Resolução revogou a Circular n. 3.432/2009 e entrou em vigor em 1º de julho de 2024, data fixada pela Resolução BCB n. 362/2023, que alterou a vigência original [@bcb2023res285; @bcb2009circ3432]. O painel por grupo começa, por isso, na data-base de julho de 2024, e o painel por trimestre, no primeiro trimestre inteiro sob o novo regime, encerrado em setembro de 2024. Os dados anteriores são carregados e marcados por regime, mas não entram na calibração nem nos testes.

Um evento dentro do recorte exige tratamento próprio: as medidas temporárias da Resolução BCB n. 381/2024 para consorciados atingidos pelas enchentes do Rio Grande do Sul, válidas até o fim de 2024. As observações afetadas são sinalizadas, e não excluídas (seção 5.2).

## O que fica disponível

O painel por grupo, no regime posterior à Resolução, tem 57.086 observações de grupo e mês, cobrindo 3.470 grupos de 76 administradoras em 23 datas-base, de julho de 2024 a maio de 2026 (`results/qualidade_dados.csv`). O painel por administradora e trimestre cobre de março de 2017 a março de 2026, com 2.572 observações de 91 administradoras; no regime posterior à Resolução e com ao menos 30 contemplações de ativas no trimestre, restam $305$ observações de administradora e trimestre, que são a base dos momentos sobre o canal de contemplação (`results/fatos_momentos.csv`).

O desenho dos dados tem uma consequência que atravessa todo o trabalho. O canal da contemplação — a variável que interessa para avaliar o lance — só é observado no grão de administradora e trimestre, enquanto a dinâmica do grupo — saldo, prazo, idade, exclusões — só é observada no grão de grupo e mês, sem o canal. Nenhum arquivo liga um lance a um participante, nem traz o percentual ofertado. O modelo precisa, portanto, reproduzir ao mesmo tempo agregados de dois grãos diferentes, e o comportamento de lance é inferido, e não medido. A seção 5.5 trata do que isso impede de afirmar.
