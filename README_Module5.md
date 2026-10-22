# BIOT 6900 — Module 5: Variant Interpretation in CYP2C19

**Name:** Mohammed Sharukh
**Gene:** CYP2C19 (self-selected — no allocation was available on Canvas)
**AlphaGenome Atlas:** run live (70 variants scored, 0 failures)

## Files

- `BIOT6900_Module5_Part3_Assignment.ipynb` — the full analysis, Q1–Q6
- `pgx_classified_CYP2C19.csv` — the 33 VUS rows exported in Q5
- `CYP2C19_Module5_Report.pdf` — the written report

The `data/` folder (cached MyVariant.info downloads) is excluded via `.gitignore`.
The AlphaGenome API key is held in the `ALPHA_GENOME_API_KEY` environment
variable and does not appear anywhere in the notebook.

## Results in brief

- 80 ClinVar variants fetched; both anchor star alleles present
  (CYP2C19*2 / rs4244285 and CYP2C19*17 / rs12248560).
- Coverage: CADD 85.0%, REVEL 67.5%, AlphaMissense 67.5%. Seven consequence
  classes had no REVEL score at all.
- Frequency filter MAX_AF = 0.50 removed 2 of 80 variants and no functional
  alleles. A 0.001 rare-disease filter would have removed 19, including both
  star alleles.
- **Calibration was not possible for this gene.** After filtering, CYP2C19 has
  0 P/LP and 0 B/LB labelled variants (37 of 78 are annotated "drug response",
  33 "Uncertain significance", 7 benign-side). Every CADD band returned
  LR+ = NaN. Taking the documented route, I report that calibration is not
  possible rather than pooling a second gene.
- Consequently all 33 VUS remain VUS; none moved toward pathogenic or benign.
- Atlas: rs72558186 (splice donor, unscored by every other tool) scored
  AVI 25.51 with MERGED_SPLICING; rs4244285 (*2) scored AVI 22.33 with
  MERGED_SPLICING despite a CADD of 5.686.

## What didn't work

- **No gene allocation found on Canvas**, so CYP2C19 was chosen; disclosed here
  as the assignment permits.
- **`clinvar_label()` does not capture this gene's labels.** Seven variants carry
  ClinVar "Benign" or "Likely benign" annotations but all 78 rows return
  `label = "none"`. Even with that parsing corrected the P/LP side remains zero,
  so the calibration conclusion is unchanged.
- **AlphaGenome needed a fresh terminal.** `setx` only affects new processes, so
  the first Atlas run failed with "No API key in your environment"; relaunching
  Jupyter from a new PowerShell window fixed it.
- A `tqdm`/`ipywidgets` IProgress warning appears during the Atlas query. It is
  cosmetic and does not affect results.
