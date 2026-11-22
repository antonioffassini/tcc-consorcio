---
secao: 6.6
titulo: Protocolo experimental e reprodutibilidade
status: rascunho
responsavel:
insumos:
  - Makefile
  - requirements.txt
  - ESTADO.md §4 (registro de decisões e critérios antes dos resultados)
fontes:
  - results/calibracao_config.csv
  - results/h3_config_sobra.csv
excecoes:
  - 20261116
paginas_alvo: 2
---

# Protocolo experimental e reprodutibilidade

Um resultado de simulação só vale se outra pessoa consegue reproduzi-lo a partir dos mesmos dados. Esta seção descreve o que garante isso no trabalho e em que ordem os passos foram executados.

## Ordem dos passos e registro prévio

O trabalho seguiu uma ordem fixa, e cada etapa só começou depois de registrada no log do projeto a decisão que a governa:

1. construção dos painéis a partir dos dados brutos (seção 5.2);
2. cálculo dos fatos estilizados e partição dos momentos em calibração e teste, registrada antes da calibração (seção 5.4);
3. especificação do modelo e dos mecanismos, com os testes da seção 6.4;
4. calibração (seção 6.3);
5. registro da regra de rejeição de H2, depois teste de H2 (seção 6.5);
6. registro dos critérios e da regra de decisão de H3, depois comparação entre mecanismos (seção 7.4);
7. congelamento: nenhum experimento novo depois dele.

O log é um arquivo versionado no repositório, e cada entrada tem data, motivo e autor. Os pontos em que a ordem não foi cega — a revisão do modelo depois de conhecido o primeiro teste de H2 e a contaminação parcial de um momento de teste — estão registrados ali e são declarados nas seções 7.2 e 8.3.

## Sementes

Toda aleatoriedade do trabalho parte de sementes fixas e registradas. O bootstrap de administradoras usa a semente 20261116; os desenhos de grupos, as sementes 0, 1 e 2; cada grupo do desenho guarda a própria semente (seção 6.1). Os arquivos de configuração gravados junto com cada resultado trazem as sementes, o número de reamostragens, as grades e os parâmetros fixos usados (`results/calibracao_config.csv`; `results/h3_config_sobra.csv`). Com os mesmos dados brutos, o mesmo código e as mesmas versões das bibliotecas, a execução reproduz os mesmos arquivos de resultado.

## Versões e ambiente

O código está num repositório Git privado, e cada resultado do texto corresponde a um estado registrado do repositório. As bibliotecas estão listadas em `requirements.txt` (NumPy, pandas, SciPy, entre outras). [RESULTADO PENDENTE: fixar as versões exatas das bibliotecas e a versão do Python no requirements.txt e registrar o commit de cada resultado em results/] Os dados brutos do Bacen estão versionados no mesmo repositório e nunca são alterados; os painéis derivados podem ser apagados e regenerados.

## Do dado ao texto

A cadeia completa tem quatro elos. O pipeline gera os painéis; os scripts de análise geram os arquivos de `results/`; o texto cita apenas números presentes nesses arquivos; e um script de auditoria confere, em cada seção, que todo número da prosa tem correspondente num dos arquivos declarados no cabeçalho da seção e que toda citação tem entrada na base bibliográfica e o documento correspondente arquivado. A monografia é gerada a partir dos arquivos de texto por uma única ferramenta de conversão, sem edição manual do documento final.

Os comandos de cada etapa são executados a partir da raiz do repositório:

```
python -m src.pipeline.build_panel --raw data/raw --out data/processed
python -m src.analysis.momentos
python -m src.sim.rodada_heterogeneidade
python -m src.analysis.calibracao identificacao --forma fracao
python -m src.analysis.calibracao calibra --forma sobra
python -m src.analysis.calibracao h2 --forma sobra
python -m src.analysis.comparacao --forma sobra
python -m src.analysis.comparacao --forma fracao
python -m src.analysis.tabelas_texto
python -m src.sim.tabela_parametros
python -m pytest -q tests
python scripts/audit.py
```

[RESULTADO PENDENTE: comando único que encadeie todas as etapas; o alvo atual do Makefile ainda aponta para módulos do plano inicial e precisa ser atualizado]
