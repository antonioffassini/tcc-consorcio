"""Rodada 1 do bloco de 22/11 (ESTADO §4): invariância da escala da urgência no modelo de 19/11.

Reconstrói o desenho calibrado de 19/11 (forma "sobra", sementes de desenho 0–2) a partir de
results/calibracao_theta.csv e results/calibracao_bootstrap.csv, sem a superfície em disco, e roda a
comparação H3 duas vezes:
  - conferência: base de 19/11 (deve reproduzir results/h3_diferencas_sobra.csv);
  - invariante: F_theta = LogNormal(log 0,2; 0,5) e phi1 = 0,5 — mesmo comportamento, só W muda.

Uso (da raiz):  python -m src.analysis.bloco_2211 invariante
Saídas: results/sens_invariante/h3_{metricas,diferencas,robustez}_sobra.csv, h3_conferencia_sobra.csv
"""
from __future__ import annotations

import argparse
import os
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from src.analysis import comparacao as cp
from src.analysis.calibracao import SEMENTE, _carrega, base_parametros
from src.sim import painel

ESCALA = 0.2


def invariante(args):
    out = Path("results") / "sens_invariante"
    out.mkdir(parents=True, exist_ok=True)
    a, b, fixos = _carrega(args.proc)
    th = pd.read_csv(Path("results") / "calibracao_theta.csv").set_index("parametro")["valor"]
    th_b = pd.read_csv(Path("results") / "calibracao_bootstrap.csv")
    des = [painel.monta_desenho(a, b, 12, seed=r) for r in range(3)]
    base = base_parametros(fixos, "sobra")
    ts = dict(phi0=float(th["phi0"]), teto_restituicao=float(th["teto_restituicao"]))
    wn = painel.pesos("sobra", (float(th["pi"]),), painel.niveis_de("sobra"))
    cp.CONJUNTO = "h3"
    # conferência contra a rodada de 19/11
    df0 = cp.roda_comparacao(des, base, ts, wn, "sobra", processos=args.processos, log=print)
    _, d0 = cp.resume(df0, args.B, SEMENTE)
    ant = pd.read_csv(Path("results") / "h3_diferencas_sobra.csv")
    conf = d0[["mecanismo", "W", "E", "S", "Rst"]].merge(ant[["mecanismo", "W", "E", "S", "Rst"]], on="mecanismo",
                                                         suffixes=("_agora", "_1911"))
    conf.round(6).to_csv(out / "h3_conferencia_sobra.csv", index=False)
    print(conf.round(5).to_string(index=False), flush=True)
    # invariante
    base_i = replace(base, mu_theta=base.mu_theta + np.log(ESCALA), phi1=base.phi1 / ESCALA)
    df = cp.roda_comparacao(des, base_i, ts, wn, "sobra", processos=args.processos, log=print)
    niveis, difs = cp.resume(df, args.B, SEMENTE)
    niveis.round(6).to_csv(out / "h3_metricas_sobra.csv", index=False)
    difs.round(6).to_csv(out / "h3_diferencas_sobra.csv", index=False)
    print(difs.round(4).to_string(index=False), flush=True)
    rng = np.random.default_rng(SEMENTE + 7)
    escolha = rng.choice(len(th_b), size=min(args.n_theta, len(th_b)), replace=False)
    nivel_m0 = niveis.set_index("mecanismo").loc["M0"].to_dict()
    dfs = []
    for k, i in enumerate(escolha):
        r = th_b.iloc[i]
        tsk = dict(phi0=float(r["phi0"]), teto_restituicao=float(r["teto_restituicao"]))
        wk = painel.pesos("sobra", (float(r["pi"]),), painel.niveis_de("sobra"))
        dfs.append(cp.roda_comparacao(des[:1], base_i, tsk, wk, "sobra", processos=args.processos,
                                      rep_seeds=[SEMENTE + 1000 + k], log=lambda s: None))
    rob = cp.robustez(dfs, nivel_m0)
    rob.round(6).to_csv(out / "h3_robustez_sobra.csv", index=False)
    res = rob.groupby("mecanismo")["domina_pontual"].agg(["sum", "count"]).reset_index()
    res["robusta"] = res["sum"] >= 0.8 * res["count"]
    print(res.to_string(index=False))


# ---------------------------------------------------------------- escolha do M3 (ESTADO §4, 22/11)

def tabela_relativa(dif: pd.DataFrame, niv: pd.DataFrame) -> pd.DataFrame:
    """Diferenças contra M0 em % do nível de M0 e piora máxima relativa por variante."""
    n0 = niv.set_index("mecanismo").loc["M0"]
    L = []
    for _, r in dif.iterrows():
        if r["mecanismo"] == "M0":
            continue
        lin = dict(mecanismo=r["mecanismo"], domina_M0=str(r["domina_M0"]).strip().lower() in ("true", "1", "1.0"),
                   melhora=r.get("melhora", ""), piora=r.get("piora", ""))
        pioras = []
        for c, sgn in cp.CRITERIOS.items():
            pct = 100 * r[c] / abs(n0[c]) if n0[c] else np.nan
            lin[f"pct_{c}"] = pct
            pioras.append(max(0.0, -sgn * pct))
        lin["piora_max_pct"] = max(pioras)
        L.append(lin)
    return pd.DataFrame(L)


def escolhe(rel: pd.DataFrame) -> str:
    """Regra registrada: entre as que dominam, maior W relativo; senão, menor piora máxima entre as que melhoram W."""
    dom = rel[rel["domina_M0"]]
    if len(dom):
        return dom.sort_values("pct_W", ascending=False)["mecanismo"].iloc[0]
    cand = rel[(rel["pct_W"] > 0) & rel["mecanismo"].str.startswith("M3")]
    if not len(cand):
        return ""
    return cand.sort_values(["piora_max_pct", "pct_W"], ascending=[True, False])["mecanismo"].iloc[0]


def grade_rodada2(escolhida: str, rel: pd.DataFrame) -> list[str]:
    """Busca coordenada em torno da escolhida e combinação reserva + espera (ESTADO §4, 22/11)."""
    sobra = 1 if escolhida.startswith(("M3s", "M3rs")) else 0
    ps = [round(x, 3) for x in np.arange(0.0, 0.4001, 0.025)]
    bs = [round(x, 2) for x in np.arange(0.0, 0.5001, 0.05)]
    m3e = rel[rel["mecanismo"].str.startswith("M3e")]
    b_best = float(m3e.sort_values(["piora_max_pct", "pct_W"], ascending=[True, False])["mecanismo"].iloc[0]
                   .split("beta")[1]) if len(m3e) else 0.1
    m3r = rel[rel["mecanismo"].str.startswith(("M3r_", "M3rs_"))]
    p_best = float(m3r.sort_values(["piora_max_pct", "pct_W"], ascending=[True, False])["mecanismo"].iloc[0]
                   .split("_p")[1]) if len(m3r) else 0.1
    if escolhida.startswith("M3e"):
        nomes = [f"M3x_p0_b{b:g}_s0" for b in bs] + [f"M3x_p{p_best:g}_b{b:g}_s0" for b in bs]   # + combinação
    else:
        nomes = [f"M3x_p{p:g}_b0_s{sobra}" for p in ps] + [f"M3x_p{p:g}_b{b_best:g}_s{sobra}" for p in ps]
    return nomes, sobra, b_best


def m3(args):
    out = Path(os.environ.get("TCC_RESULTS", "results"))
    rodada = args.rodada
    if rodada == 1:
        dif = pd.read_csv(out / "h3_diferencas_sobra_reg_m3A.csv"); niv = pd.read_csv(out / "h3_metricas_sobra_reg_m3A.csv")
        rel = tabela_relativa(dif, niv)
        rel.round(4).to_csv(out / "m3_rodada1_A.csv", index=False)
        e = escolhe(rel)
        dom = bool(rel.set_index("mecanismo").loc[e, "domina_M0"]) if e else False
        print(rel.round(3).to_string(index=False)); print("escolhida:", e, "domina:", dom)
        if dom or not e:
            print("PROXIMO: avaliar", e, "em B")
            Path(out / "m3_escolha.txt").write_text(f"rodada=1\nescolhida={e}\ndomina_A={dom}\n")
        else:
            nomes, sobra, b_best = grade_rodada2(e, rel)
            Path(out / "m3_rodada2_lista.txt").write_text(",".join(nomes))
            Path(out / "m3_escolha.txt").write_text(f"rodada=1\nescolhida={e}\ndomina_A=False\nb_best={b_best}\nsobra={sobra}\n")
            print("PROXIMO: rodada 2 com", len(nomes), "variantes")
    else:
        dif = pd.read_csv(out / "h3_diferencas_sobra_reg_m3A2.csv"); niv = pd.read_csv(out / "h3_metricas_sobra_reg_m3A2.csv")
        rel = tabela_relativa(dif, niv)
        info = dict(l.split("=") for l in Path(out / "m3_escolha.txt").read_text().split())
        melhor = rel.sort_values(["domina_M0", "piora_max_pct", "pct_W"], ascending=[False, True, False]).iloc[0]["mecanismo"]
        rel.round(4).to_csv(out / "m3_rodada2_A.csv", index=False)
        print(rel.round(3).to_string(index=False)); print("melhor da grade:", melhor)
        Path(out / "m3_rodada2_melhor.txt").write_text(melhor)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("comando", choices=["invariante", "m3"])
    ap.add_argument("--rodada", default=1, type=int)
    ap.add_argument("--proc", default="data/processed", type=Path)
    ap.add_argument("--B", default=500, type=int)
    ap.add_argument("--n-theta", default=10, type=int)
    ap.add_argument("--processos", default=2, type=int)
    a = ap.parse_args(argv)
    {"invariante": invariante, "m3": m3}[a.comando](a)



if __name__ == "__main__":
    main()
