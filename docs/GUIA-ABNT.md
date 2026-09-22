# Guia normativo — ABNT / EPUSP

Referência de formatação para a monografia. Consolidado das normas ABNT aplicáveis
e das diretrizes da Escola Politécnica da USP.

> **Confirmar com o orientador e com a biblioteca da Poli antes da entrega final.**
> Diretrizes de graduação variam entre departamentos e são revisadas periodicamente.
> Este guia reflete o padrão geral EPUSP/USP; divergência local sempre prevalece.

---

## 1. Normas ABNT aplicáveis

| Norma | Objeto |
|---|---|
| NBR 14724 | Estrutura e apresentação de trabalhos acadêmicos |
| NBR 6023 | Elaboração de referências |
| NBR 10520 | Citações em documentos |
| NBR 6024 | Numeração progressiva das seções |
| NBR 6027 | Sumário |
| NBR 6028 | Resumo |
| NBR 6034 | Índice |
| NBR 12225 | Lombada |

---

## 2. Apresentação gráfica

| Item | Padrão |
|---|---|
| Papel | A4 (21 × 29,7 cm), branco ou reciclado |
| Cor | Preto; outras cores apenas em ilustrações |
| Fonte | Times New Roman 12 (padrão EPUSP para trabalhos finais de graduação) |
| Fonte reduzida (10 ou 11) | Citações com mais de 3 linhas, notas de rodapé, paginação, ficha catalográfica, legendas e fontes de ilustrações e tabelas |
| Espaçamento | 1,5 entre linhas no corpo do texto |
| Espaçamento simples | Citações longas, notas de rodapé, referências (separadas entre si por uma linha em branco simples) |
| Margens | Esquerda e superior: 3 cm. Direita e inferior: 2 cm |
| Parágrafo | Recuo de primeira linha; padronizar e não misturar com espaçamento entre parágrafos |
| Citação longa | Recuo de 4 cm da margem esquerda, fonte menor, espaçamento simples, sem aspas |

**Títulos.** Títulos de capítulo em MAIÚSCULAS; subdivisões em minúsculas (apenas
inicial maiúscula). Ambos alinhados à esquerda, numerados em algarismos arábicos.

**Paginação.** Contada a partir da folha de rosto, mas impressa apenas a partir da
primeira folha textual (Introdução), no canto superior direito.

---

## 3. Estrutura do trabalho

### Pré-textuais
1. Capa (obrigatório)
2. Folha de rosto (obrigatório) — verso traz a ficha catalográfica, gerada pela biblioteca da Poli
3. Errata (opcional)
4. Folha de aprovação (obrigatório)
5. Dedicatória (opcional)
6. Agradecimentos (opcional)
7. Epígrafe (opcional)
8. Resumo em português (obrigatório) — parágrafo único, verbo na voz ativa e terceira pessoa, seguido de palavras-chave
9. Resumo em língua estrangeira (obrigatório)
10. Lista de ilustrações (obrigatório se houver)
11. Lista de tabelas (obrigatório se houver)
12. Lista de abreviaturas e siglas (obrigatório se houver)
13. Lista de símbolos (obrigatório se houver)
14. Sumário (obrigatório)

### Textuais
15. Introdução
16. Desenvolvimento
17. Conclusão

### Pós-textuais
18. Referências (obrigatório)
19. Glossário (opcional)
20. Apêndices — material elaborado pelo autor (opcional)
21. Anexos — material de terceiros (opcional)
22. Índice (opcional)

Elementos pré-textuais iniciam no anverso da folha; a ficha catalográfica é a
exceção, ficando no verso da folha de rosto.

---

## 4. Citações (NBR 10520)

Dois sistemas admitidos; escolher um e **nunca misturar**:

- **Autor-data (ABNT):** `Barbosa (1995) demonstrou...` ou `(BARBOSA, 1995)`.
- **Numérico (IEEE):** `[1]`, na ordem de chamada. Comum em engenharia.

Regras que mais geram erro em banca:

- Dois autores: `Melcher e Coutinho (1966)`; entre parênteses: `(MELCHER; COUTINHO, 1966)`.
- Três ou mais: `Amaral et al. (1967)`; entre parênteses: `(AMARAL et al., 1967)`.
- Citação direta exige indicação de página: `(BARBOSA, 1995, p. 42)`.
- Citação de citação (`apud`) só quando o original for comprovadamente inacessível.
  A referência completa é a da obra **consultada**, não a do original.
- Toda obra citada no texto tem de constar nas Referências, e vice-versa.

## 5. Referências (NBR 6023)

Ordem alfabética por sobrenome do autor. Prenome abreviado ou por extenso, mas
padronizado em toda a lista.

```
GOMES, L. G. F. F. Novela e sociedade no Brasil. 2. ed. Niterói: EdUFF, 1998.

MOSS, D. W.; HENDERSON, A. R. Clinical enzymology. In: BURTIS, C. A.;
ASHWOOD, E. R. (Ed.). Tietz textbook of clinical chemistry. 3rd ed.
Philadelphia: Saunders, 1999. p. 617-721.

BRASIL. Lei nº 11.795, de 8 de outubro de 2008. Dispõe sobre o Sistema de
Consórcio. Diário Oficial da União, Brasília, DF, 9 out. 2008.
```

---

## 6. Regras de conteúdo que a EPUSP cobra

Duas merecem destaque porque são cobradas e frequentemente violadas:

**A Introdução não antecipa resultados.** A diretriz da EPUSP é explícita: antecipar
os resultados na Introdução anula o interesse pela leitura integral do texto. A
Introdução estabelece contexto, problema, hipóteses e objetivos — e o ponto de vista
sob o qual o assunto será tratado. Nada além disso.

**O resumo é de no máximo ~20 linhas, em parágrafo único.** Contém objetivo, método,
resultado e conclusão, nesta ordem, sem citações e sem enumerações.

---

## 7. Configuração operacional neste repositório

A formatação não é feita à mão. O texto vive em markdown em `text/` e o `.docx`
final é gerado por `make docx`, que usa:

- `build/template-abnt.docx` — documento de referência do pandoc, com os estilos
  ABNT já configurados (margens, fontes, espaçamento, estilos de título).
  **Este arquivo você monta uma vez, no Word, e nunca mais toca.**
- `refs/abnt.csl` — estilo de citação ABNT para o citeproc. Baixar do repositório
  público de estilos CSL.
- `refs/refs.bib` — base BibTeX.

Para criar o template: abra um `.docx` gerado pelo pandoc, ajuste os estilos
`Title`, `Heading 1..4`, `Body Text`, `Block Text` (citação longa) e as margens
conforme a seção 2 deste guia, e salve como `build/template-abnt.docx`.
