"""
BIOT 6900 - Portfolio Deliverable 1 (PDAC)
Regenerates the two required Lab 2 figures from the merged Module 2 table
and prints every number the report needs.

  Figure 1  fig1_integration.png  RNA vs protein log2FC (concordance) + top-15 scores
  Figure 2  fig2_venn.png         cross-layer evidence overlap (RNA / protein / mutation)
  Numbers   pd1_numbers.txt       surviving-gene count, concordance, Venn region counts

Run from C:\\Users\\USER\\biot6900 :   python pd1\\make_pd1_figures.py
Needs only pandas + numpy + matplotlib (no matplotlib-venn).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ---------------------------------------------------------------- settings
INPUT = Path("targets_pdac.csv")          # merged Module 2 table (one row per gene)
OUTDIR = Path("pd1")
TOP_N = 15

# Evidence thresholds used to call a gene "supported" in each layer (state these in the caption)
RNA_LFC, RNA_P = 1.0, 0.05                # |log2FC| >= 1 and p < 0.05
PROT_LFC, PROT_P = 0.5, 0.05              # |log2FC| >= 0.5 and p < 0.05 (proteomic FCs are compressed)
MUT_NEGLOG10P = -np.log10(0.05)           # mutation enrichment p < 0.05

# Set these by hand ONLY if auto-detection picks the wrong column (look at the printed column list)
COLS = {"gene": None, "rna_lfc": None, "rna_p": None, "prot_lfc": None,
        "prot_p": None, "mut": "neglog10p", "concordant": None, "score": None}
# ---------------------------------------------------------------------------


def find(df, key, *must, avoid=()):
    if COLS[key]:
        return COLS[key]
    for c in df.columns:
        lc = c.lower()
        if all(m in lc for m in must) and not any(a in lc for a in avoid):
            return c
    return None


def neglog10(series):
    """Accept either raw p-values or -log10(p); return -log10(p)."""
    s = pd.to_numeric(series, errors="coerce")
    if s.dropna().between(0, 1).all():
        return -np.log10(s.clip(lower=1e-300))
    return s


def main():
    if not INPUT.exists():
        sys.exit(f"Cannot find {INPUT.resolve()} - run this from the repo root.")
    OUTDIR.mkdir(exist_ok=True)
    df = pd.read_csv(INPUT)
    print("Columns found:", list(df.columns))

    g = find(df, "gene", "gene") or df.columns[0]
    rl = find(df, "rna_lfc", "rna", "fc") or find(df, "rna_lfc", "rna", "log")
    rp = find(df, "rna_p", "rna", "p", avoid=("fc", "log2"))
    pl = find(df, "prot_lfc", "prot", "fc") or find(df, "prot_lfc", "prot", "log")
    pp = find(df, "prot_p", "prot", "p", avoid=("fc", "log2"))
    mu = find(df, "mut", "mut")
    co = find(df, "concordant", "concord")
    sc = find(df, "score", "score") or find(df, "score", "final")
    print(f"Using: gene={g} rna_lfc={rl} rna_p={rp} prot_lfc={pl} prot_p={pp} "
          f"mut={mu} concordant={co} score={sc}")
    for name, col in [("rna_lfc", rl), ("prot_lfc", pl), ("mut", mu), ("score", sc)]:
        if col is None:
            sys.exit(f"Could not detect the {name} column. Set COLS['{name}'] at the top of the script.")

    d = pd.DataFrame({
        "gene": df[g].astype(str),
        "rna": pd.to_numeric(df[rl], errors="coerce"),
        "prot": pd.to_numeric(df[pl], errors="coerce"),
        "mut": neglog10(df[mu]),
        "score": pd.to_numeric(df[sc], errors="coerce"),
    })
    d["rna_nlp"] = neglog10(df[rp]) if rp else np.nan
    d["prot_nlp"] = neglog10(df[pp]) if pp else np.nan
    d["concordant"] = (df[co].astype(str).str.lower().isin(["true", "1", "yes"])
                       if co else np.sign(d["rna"]) == np.sign(d["prot"]))
    d = d.dropna(subset=["rna", "prot", "score"]).drop_duplicates("gene")

    n = len(d)
    conc = d["concordant"].mean() * 100
    top = d.sort_values("score", ascending=False).head(TOP_N)
    conc_top = top["concordant"].mean() * 100

    # ---- layer calls for the Venn
    rna_ok = d["rna"].abs() >= RNA_LFC
    if rp:
        rna_ok &= d["rna_nlp"] > -np.log10(RNA_P)
    prot_ok = d["prot"].abs() >= PROT_LFC
    if pp:
        prot_ok &= d["prot_nlp"] > -np.log10(PROT_P)
    mut_ok = d["mut"] > MUT_NEGLOG10P
    R, P, M = set(d.gene[rna_ok]), set(d.gene[prot_ok]), set(d.gene[mut_ok])
    regions = {
        "RNA only": len(R - P - M), "Protein only": len(P - R - M), "Mutation only": len(M - R - P),
        "RNA+Protein": len((R & P) - M), "RNA+Mutation": len((R & M) - P),
        "Protein+Mutation": len((P & M) - R), "All three": len(R & P & M),
    }
    all3 = sorted(R & P & M)
    rp_conc = d[d.gene.isin(R & P)]["concordant"].mean() * 100 if (R & P) else float("nan")

    # ---- Figure 1: integration
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1.15, 1]})
    a.scatter(d.loc[d.concordant, "rna"], d.loc[d.concordant, "prot"], s=8, c="#4C72B0",
              alpha=0.45, label=f"concordant ({d.concordant.sum()})")
    a.scatter(d.loc[~d.concordant, "rna"], d.loc[~d.concordant, "prot"], s=8, c="#DD8452",
              alpha=0.45, label=f"discordant ({(~d.concordant).sum()})")
    for _, r in top.iterrows():
        a.scatter(r.rna, r.prot, s=40, facecolors="none", edgecolors="k", lw=0.9)
        a.annotate(r.gene, (r.rna, r.prot), xytext=(3, 3), textcoords="offset points", fontsize=7)
    a.axhline(0, c="grey", lw=0.6); a.axvline(0, c="grey", lw=0.6)
    a.set_xlabel("RNA log2FC (tumor vs normal)"); a.set_ylabel("Protein log2FC (tumor vs normal)")
    a.set_title(f"A. RNA-protein agreement, {n:,} genes ({conc:.1f}% concordant)", fontsize=10)
    a.legend(fontsize=8, loc="lower right")

    t = top.iloc[::-1]
    b.barh(t.gene, t.score, color=np.where(t.concordant, "#4C72B0", "#DD8452"))
    b.set_xlim(t.score.min() - 0.02, 1.0)
    b.set_xlabel("Multi-evidence score (equal-weight rank percentile)")
    b.set_title(f"B. Top {TOP_N} by combined score (blue = concordant)", fontsize=10)
    b.tick_params(axis="y", labelsize=8)
    fig.suptitle("Figure 1. Multi-omics integration, CPTAC-PDAC (140 tumors)", fontsize=11, y=1.01)
    fig.tight_layout()
    fig.savefig(OUTDIR / "fig1_integration.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # ---- Figure 2: hand-drawn 3-set Venn (no extra package needed)
    fig, ax = plt.subplots(figsize=(6, 5.4))
    centers = {"R": (-0.6, 0.35), "P": (0.6, 0.35), "M": (0.0, -0.65)}
    colors = {"R": "#4C72B0", "P": "#55A868", "M": "#C44E52"}
    labels = {"R": f"Transcriptomic\n(n={len(R):,})", "P": f"Proteomic\n(n={len(P):,})",
              "M": f"Genomic / mutation\n(n={len(M):,})"}
    for k, (x, y) in centers.items():
        ax.add_patch(Circle((x, y), 1.1, color=colors[k], alpha=0.25, lw=1.5, ec=colors[k]))
    ax.text(-1.55, 1.55, labels["R"], ha="center", fontsize=9, color=colors["R"], weight="bold")
    ax.text(1.55, 1.55, labels["P"], ha="center", fontsize=9, color=colors["P"], weight="bold")
    ax.text(0, -2.05, labels["M"], ha="center", fontsize=9, color=colors["M"], weight="bold")
    pos = {"RNA only": (-1.05, 0.6), "Protein only": (1.05, 0.6), "Mutation only": (0, -1.15),
           "RNA+Protein": (0, 0.85), "RNA+Mutation": (-0.62, -0.35),
           "Protein+Mutation": (0.62, -0.35), "All three": (0, 0.0)}
    for k, (x, y) in pos.items():
        ax.text(x, y, f"{regions[k]:,}", ha="center", va="center", fontsize=11,
                weight="bold" if k == "All three" else "normal")
    ax.set_xlim(-2.3, 2.3); ax.set_ylim(-2.3, 2.1); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Figure 2. Cross-layer evidence overlap", fontsize=11)
    cap = (f"RNA: |log2FC|>={RNA_LFC}{' & p<'+str(RNA_P) if rp else ''};  "
           f"protein: |log2FC|>={PROT_LFC}{' & p<'+str(PROT_P) if pp else ''};  "
           "mutation enrichment p<0.05")
    fig.text(0.5, 0.01, cap, ha="center", fontsize=7.5)
    fig.savefig(OUTDIR / "fig2_venn.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # ---- numbers for the report
    lines = [
        f"Genes surviving the 3-layer join (rows with RNA, protein and mutation stats): {n:,}",
        f"RNA-protein sign concordance, all genes: {conc:.1f}%  "
        f"({d.concordant.sum():,} concordant / {(~d.concordant).sum():,} discordant)",
        f"Concordance among genes significant in BOTH RNA and protein: {rp_conc:.1f}% (n={len(R & P):,})",
        f"Concordance in top {TOP_N}: {conc_top:.0f}%  "
        f"(discordant: {', '.join(top.gene[~top.concordant]) or 'none'})",
        f"Layer sizes: RNA={len(R):,}  protein={len(P):,}  mutation={len(M):,}",
        "Venn regions: " + "; ".join(f"{k}={v:,}" for k, v in regions.items()),
        f"Genes supported in all three layers: {', '.join(all3[:30]) or 'none'}"
        + (" ..." if len(all3) > 30 else ""),
        f"p-value columns used: RNA={'yes' if rp else 'NO (FC only)'}, protein={'yes' if pp else 'NO (FC only)'}",
    ]
    for gene in ["KRAS", "TP53", "CDKN2A", "SMAD4", "ERBB4", "CEL", "POSTN", "TNS4", "MUC16"]:
        r = d[d.gene == gene]
        if len(r):
            r = r.iloc[0]
            rank = int((d.score > r.score).sum()) + 1
            lines.append(f"{gene:7s} rank={rank:5d}  RNA={r.rna:+.3f}  prot={r.prot:+.3f}  "
                         f"mut -log10p={r.mut:.2f}  concordant={bool(r.concordant)}  score={r.score:.3f}")
        else:
            lines.append(f"{gene:7s} not in merged table")
    txt = "\n".join(lines)
    (OUTDIR / "pd1_numbers.txt").write_text(txt)
    print("\n" + txt + f"\n\nSaved: {OUTDIR/'fig1_integration.png'}, {OUTDIR/'fig2_venn.png'}, "
          f"{OUTDIR/'pd1_numbers.txt'}")


if __name__ == "__main__":
    main()
