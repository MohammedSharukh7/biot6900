# BIOT 6900 · Module 3 Assignment
## Target Triage with Protein Language Models — Pancreatic Ductal Adenocarcinoma (PDAC)

**Student:** Mohammed Sharukh
**Date:** October 14, 2026
**Disease:** Pancreatic Ductal Adenocarcinoma (PDAC) — same disease as Module 2

## Data sources

**Module 2 input:** `targets_pdac.csv` (top 15 PDAC targets, ranked by multi-evidence score from
Module 2's RNA/protein/mutation integration).

**Module 3 data pack:** `BIOT6900_Module3_DataPack.zip`, provided via Canvas, unzipped into
`data/`. Contains:
- `panel.tsv` + `panel_emb_main.npy` / `panel_emb_baseline.npy` — ~1,200 labeled training
  proteins (Open Targets clinical precedence) with ESM C and ESM-2 embeddings
- `proteome.tsv` + `proteome_emb_main.npy` — every reviewed human protein, used to map Module 2
  targets to embeddings
- `anchor_variants.tsv` — pre-scored course anchor variants (APOE, TREM2, TP53)
- `variant_scores_TP53.tsv`, `variant_scores_APOE.tsv`, `variant_scores_TREM2.tsv` — full
  substitution landscapes for the anchor genes
- `manifest.json` — embedding model metadata (ESM C 300M used as main model)

Model used: **ESM C 300M** (per `manifest.json`), pre-computed — no model downloads were
required for this assignment.

## Pipeline summary

1. Loaded top 15 PDAC targets from Module 2, mapped to `proteome.tsv` by gene symbol —
   **15/15 mapped, 0 unmapped**.
2. Removed own targets from the training panel before fitting any model (leakage guard) —
   **1 target removed, 1,200 proteins remained for training**.
3. Validated the tractability prior with both random-split and family-split cross-validation —
   family-split AUROC 0.737, AP 0.541 (vs. random-split 0.845 / 0.726), confirming the expected
   homology-leakage gap.
4. Fit separate small-molecule (`sm_clinical`) and antibody (`ab_clinical`) priors, predicted
   both for all 15 targets.
5. Identified the 3 nearest known drugged proteins (by cosine similarity) for each target.
6. Reported score + within-protein percentile for the 4 required anchor variants: APOE R176C
   (ε2), APOE C130R (ε4), TREM2 R47H, and TP53 R175H (chosen hotspot).
7. Re-ranked targets combining Module 2 evidence (60% weight) with the best-modality
   tractability prior (40% weight), exported to `targets_pdac_w3.csv`.

## Files in this submission

- `BIOT6900_Module3_Assignment.ipynb` — notebook, runs cleanly top to bottom (Kernel → Restart &
  Run All)
- `targets_pdac_w3.csv` — re-ranked target table (15 targets), columns: gene, week2_score, p_sm,
  p_ab, nearest_drug_targets, final, rank
- `PDAC_Module3_Report.pdf` — written report (re-ranking justification, modality
  biology, validation interpretation, anchor variant interpretation, limitations), plus an addendum on
  disease/data choice and discordance/limitations
- `README_Module3.md` — this file

## What didn't work / notes

- The Module 3 data pack zip was not immediately visible in the Canvas Module 3 file list; it
  was found as a separate attachment (`BIOT6900_Module3_DataPack.zip`, 60.8 MB) linked within
  the Module 3 Assignment page itself, rather than alongside the lecture/notebook files.
- No other issues — all steps ran without modification beyond the required TODO completions.

## Report update (October 29, 2026)
Per the instructor's announcement, an addendum was appended to the report PDF covering **disease and data choice with biological interpretation** and **discordance and limitations**. The analysis is unchanged.
