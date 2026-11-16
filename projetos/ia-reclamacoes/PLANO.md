# Projeto de IA (PCS3838): classificação de reclamações sobre consórcio

**Disciplina:** Inteligência Artificial, PCS3838 (Prof. Jaime Sichman) · **Grupo:** o mesmo trio do TCC (até 3 integrantes) · **Etapa 1 (escolha do dataset):** data a confirmar no Moodle; as etapas seguintes ainda não foram divulgadas

## O que vamos fazer

Classificação supervisionada de textos: dada a reclamação de um consumidor contra uma administradora de consórcio, prever o tipo de problema. Exemplos: restituição de valores pagos, contemplação ou sorteio, lance, cobrança indevida, cancelamento, informação na venda.

## Dataset

**Candidato principal: ConsumerBR** (PROPOR 2026), com mais de 3,1 milhões de interações do Consumidor.gov.br entre 2021 e 2025. Traz o texto anonimizado e metadados de desfecho e satisfação. **Ainda falta verificar:**
1. se o segmento "administradoras de consórcio" está no corpus e com quantas amostras; o tamanho tem de ser "adequado", nem pequeno nem enorme;
2. qual campo serve de rótulo (provavelmente o assunto ou o problema do Consumidor.gov.br) e quantas classes ele tem;
3. a licença e o link de download.

**Plano B**, se o consórcio sozinho for pequeno: usar o segmento financeiro mais amplo (bancos, cartões, consórcios), mantendo o consórcio como recorte de análise.

**Plano C:** os dados abertos do Consumidor.gov.br, se trouxerem o texto do relato.

**Entrega da etapa 1:** PDF `PCS3838_Escolha_dataset_NUSP1_NUSP2_NUSP3.pdf` com nomes e números USP, nome e link do dataset, número de amostras, idioma (português) e classes. Todos os integrantes enviam o mesmo arquivo.

## Como vamos fazer (proposta, a ajustar às etapas que o professor divulgar)

- **Modelagem do dataset:**
  - filtro do segmento, limpeza e deduplicação;
  - análise do desbalanceamento das classes;
  - divisão treino, validação e teste estratificada e por tempo, para o modelo não "ver o futuro".
- **Modelos:** baseline TF-IDF com regressão logística ou SVM linear; depois um modelo de linguagem em português (como o BERTimbau) ajustado; comparação por F1-macro e matriz de confusão.
- **Análise:** erros por classe e quais termos e trechos sustentam cada classe.

## O que este projeto recebe e devolve

- **Para o TCC:** a frequência dos tipos de problema, a evidência qualitativa de onde o mecanismo dói, os caps. 1 e 8.
- **Para o jogo de POO:** eventos e dicas baseados nos problemas reais mais comuns.
- **Recebe do TCC:** o domínio. Saber o que é restituição, lance embutido e contemplação ajuda a definir as classes e a ler os erros do modelo.

**Referência do dataset:** [ConsumerBR: A Large-Scale Corpus of Consumer Complaints in Brazilian Portuguese](https://preview.aclanthology.org/anlp-naacl/2026.propor-1.66/)
