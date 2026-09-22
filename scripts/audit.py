#!/usr/bin/env python3
"""
Auditoria de ancoragem da monografia.

Verifica tres invariantes antes de qualquer entrega ao orientador:

  1. CITACOES   - toda chave [@chave] citada no texto existe em refs/refs.bib
                  E tem PDF correspondente em refs/pdfs/<chave>.pdf
  2. NUMEROS    - todo numero na prosa aparece em algum CSV listado no
                  frontmatter 'fontes' da secao, ou consta em 'excecoes'
  3. MARCADORES - nenhum [CITAR: ...] ou [RESULTADO PENDENTE: ...] sobrou

Uso:   python scripts/audit.py [--strict]
Saida: relatorio por secao; exit code 1 com --strict se houver falha.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "text"
BIB = ROOT / "refs" / "refs.bib"
PDFS = ROOT / "refs" / "pdfs"

NUM_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:\.\d{3})+|\d+,\d+|\d+\.\d+|\d{3,})(?![\w])")
CITE_RE = re.compile(r"\[@([A-Za-z0-9_\-:]+)")
PEND_RE = re.compile(r"\[(?:CITAR|RESULTADO PENDENTE):[^\]]*\]")
YEAR_RE = re.compile(r"^(?:19|20)\d{2}$")
TOL = 0.005


def parse_frontmatter(raw):
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    head, body = raw[3:end], raw[end + 4:]
    meta, key = {}, None
    for line in head.splitlines():
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and key:
            meta.setdefault(key, [])
            if isinstance(meta[key], list):
                meta[key].append(line.lstrip()[2:].strip())
        elif ":" in line:
            k, v = line.split(":", 1)
            key, v = k.strip(), v.strip()
            meta[key] = v if v else []
    return meta, body


# remissoes internas ("secao 7.3", "Capitulo 5", "Tabela 4.1") nao sao
# afirmacoes numericas e nao precisam de lastro em results/
XREF_RE = re.compile(
    r"(?:se[cç][aã]o|se[cç][oõ]es|cap[ií]tulo|cap[ií]tulos|figura|figuras|"
    r"tabela|tabelas|quadro|quadros|item|itens|ap[eê]ndice|anexo|equa[cç][aã]o)"
    r"\s+(?:\d+(?:\.\d+)*)(?:\s*(?:e|a|,)\s*\d+(?:\.\d+)*)*",
    re.IGNORECASE)


def strip_code(body):
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = re.sub(r"`[^`]*`", " ", body)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    return XREF_RE.sub(" ", body)


def to_float(tok):
    if tok is None:
        return None
    tok = str(tok).strip()
    t = tok.replace(".", "") if re.match(r"^\d{1,3}(\.\d{3})+$", tok) else tok
    t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def csv_values(path):
    out = set()
    if not path.exists():
        return out, False
    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        for row in csv.reader(fh):
            for cell in row:
                v = to_float(cell)
                if v is not None:
                    out.add(v)
    return out, True


def close(v, pool):
    return any(abs(v - p) <= max(TOL * abs(p), 1e-9) for p in pool)


def bib_keys():
    if not BIB.exists():
        return set()
    txt = BIB.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"@\w+\{([^,]+),", txt))


def aslist(x):
    if not x:
        return []
    return [x] if isinstance(x, str) else x


def main():
    strict = "--strict" in sys.argv
    keys = bib_keys()
    files = sorted(TEXT.glob("*.md"))
    if not files:
        print("Nenhum arquivo em text/. Nada a auditar.")
        return 0

    total = 0
    for f in files:
        meta, body = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        if str(meta.get("status", "")).lower() in ("esqueleto", "vazio"):
            print(f"[pulado] {f.name} (status: esqueleto)")
            continue
        body = strip_code(body)
        problems = []

        for m in PEND_RE.finditer(body):
            problems.append("marcador pendente: " + m.group(0))

        for k in sorted(set(CITE_RE.findall(body))):
            if k not in keys:
                problems.append("citacao sem entrada no refs.bib: @" + k)
            elif not (PDFS / (k + ".pdf")).exists():
                problems.append("citacao sem PDF em refs/pdfs/: @" + k)

        pool = set()
        for rel in aslist(meta.get("fontes")):
            vals, ok = csv_values(ROOT / rel)
            if ok:
                pool |= vals
            else:
                problems.append("fonte declarada nao existe: " + rel)

        exc = {to_float(e) for e in aslist(meta.get("excecoes"))}
        exc.discard(None)

        for tok in sorted(set(NUM_RE.findall(body))):
            if YEAR_RE.match(tok):
                continue
            v = to_float(tok)
            if v is None or v in exc:
                continue
            if not close(v, pool):
                problems.append("numero sem lastro em results/: " + tok)

        if problems:
            total += len(problems)
            print("\n[FALHA] " + f.name)
            for p in sorted(set(problems)):
                print("   - " + p)
        else:
            print("[ok]     " + f.name)

    print("\n" + "-" * 52)
    print("Total de problemas: %d" % total)
    return 1 if (total and strict) else 0


if __name__ == "__main__":
    sys.exit(main())
