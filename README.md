# BIOT 6900 · Module 2 · Assignment 2 — Independent Multi-Omics Target Discovery

**Student:** Mohammed Sharukh
**Disease:** Pancreatic Ductal Adenocarcinoma (PDAC)

## Data sources

All data sourced from the CPTAC-PDAC cohort via the LinkedOmics data download portal:
https://www.linkedomics.org/data\_download/CPTAC-PDAC/

**Access type:** Open access — no data-use agreement or application required.

|Layer|File|Description|Samples|
|-|-|-|-|
|Transcriptomics (RNA)|`mRNA\_RSEM\_UQ\_log2\_Tumor.cct`|RNA-seq, RSEM upper-quartile normalized, log2, tumor|140|
|Transcriptomics (RNA)|`mRNA\_RSEM\_UQ\_log2\_Normal.cct`|Same, normal tissue|21|
|Proteomics (protein)|`proteomics\_gene\_level\_MD\_abundance\_tumor.cct`|Gene-level proteomics, median-normalized abundance, tumor|140|
|Proteomics (protein)|`proteomics\_gene\_level\_MD\_abundance\_normal.cct`|Same, normal tissue|75|
|Genomics (variants)|`Mutation\_gene\_level.cgt`|Gene-level somatic mutation calls (categorical: variant type or "WT")|140|

**Note:** the underlying CPTAC-PDAC cohort is sample-matched (same 140 tumors profiled across
all three layers). This analysis reduces each layer to a gene-level tumor-vs-normal summary
statistic (log2 fold-change + p-value for RNA/protein; mutation frequency + enrichment p-value
for genomics) to match the pipeline's gene-level schema, rather than using per-patient pairing
directly. See the report for discussion of what this does and doesn't let us claim.

## Files in this submission

* `BIOT6900\_Assignment2\_PDAC.ipynb` — notebook, runs cleanly top to bottom (Kernel → Restart \& Run All)
* `targets\_pdac.csv` — ranked target table (top 15 genes by multi-evidence score)
* `README.md` — this file
* `report.pdf` (or `.docx`) — 3–4 page written report (disease/data justification, biological
interpretation of top targets, discordant-gene discussion, limitations)

## Pipeline summary

Harmonize gene symbols → join RNA + protein + mutation tables on `gene` → compute sign-agreement
concordance (RNA vs. protein direction) → compute multi-evidence score (equal-weighted,
rank-percentile normalized across the three layers) → rank → export top 15 to `targets\_pdac.csv`.

