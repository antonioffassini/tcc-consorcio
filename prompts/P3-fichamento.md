# P3 — Fichamento de artigo (um PDF por vez)

Segue o PDF. Produza `refs/fichamentos/<chave>.md` neste formato:

```
---
chave: <sobrenomeAAAA>
status: fichado
---
- Referência ABNT completa, extraída do próprio PDF
- Pergunta de pesquisa do artigo
- Método
- Resultado principal
- Relação com esta tese: sustenta / contradiz / é ferramenta / é contexto
- O que dá para reaproveitar diretamente (e onde, qual seção)
- Limitação que me afeta
```

Depois emita a entrada BibTeX para `refs/refs.bib`.

Use exclusivamente o conteúdo do PDF. Campo ausente no documento → "não consta".
Nunca complete metadado de memória.

**Contrato de saída:** um fichamento + uma entrada BibTeX, ambos verificáveis contra o PDF.
