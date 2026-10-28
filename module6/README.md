# Module 6 â€” PRS Portability on Real Data

BIOT 6900 Â· AI-Powered Biotech Workflows Â· Fall 2026 Â· Computational Lab 6 Â· Mohammed Sharukh

## What this is
This module applies a published polygenic risk score (PRS) to real 1000 Genomes phase 3 genotypes for 2,336 people in five ancestry groups (EUR, AFR, EAS, SAS, AMR). It measures how the score's distribution, a single top-10% cutoff, discrimination (AUC) and calibration change across ancestries.

> **The phenotype is simulated.** 1000 Genomes has no disease labels. The PRS and its distribution come from real genotypes and published weights. AUC, calibration and the age comparison use a simulated case label and are illustrative only.

## Contents
| File | Description |
|---|---|
| `BIOT6900_Module6_Part3_Graded.ipynb` | **Graded run.** Alzheimer's score PGS000334 on the Canvas data pack |
| `BIOT6900_Module6_Part3_PDAC_Extension.ipynb` | Same workflow on my Part I disease (PDAC), score PGS000725; real-data sections only |
| `build_pdac_data.py` | Builds `data_pdac/` from 1000 Genomes via the Ensembl REST API |
| `figures/` | PRS distribution, AUC and calibration plots (graded run); PDAC PRS distribution |
| `BIOT6900_Module6_Lab6_Report_MSharukh.pdf` | Written report |

`data/` (Canvas data pack) and `data_pdac/` are not committed.

## Graded run: proof of data
```
source      : REAL
people      : 2336
score size  : 22 variants
by ancestry : {'AFR': 500, 'EAS': 500, 'EUR': 500, 'SAS': 489, 'AMR': 347}
  genotypes.csv: sha256 9cf41a1f
  variants.csv: sha256 f7a87d3f
  score.csv: sha256 7f80e8ff
  meta.csv: sha256 6cc55b6e
```

## Key results (graded run)
| | EUR | AFR | EAS | SAS | AMR |
|---|---|---|---|---|---|
| % above pooled top-10% cutoff | 7.8 | 27.8 | 2.2 | 4.3 | 6.3 |
| AUC (simulated phenotype) | 0.672 | 0.493 | 0.575 | 0.611 | 0.555 |
| Predicted âˆ’ observed risk (EUR-fitted) | +0.000 | +0.044 | âˆ’0.034 | +0.017 | +0.028 |

Harmonization: 22/22 variants found, 13 flipped, 0 dropped. Cross-validated AUC: age 0.562; age + PRS 0.618 (+0.056).

## PDAC extension (Part I disease)
The Canvas panel contains only Alzheimer's loci, so I built a matching PDAC dataset. The score is PGS000725 (PRS_Pancreas; Jia et al., *JNCI Cancer Spectr* 2020; 22 variants, European-derived). Genotypes for the same 2,336 samples come from 1000 Genomes phase 3 via Ensembl. ALT is the non-REF allele actually observed in 1000 Genomes. 21/22 variants were retrieved; rs16986825 was not retrieved because of server errors. EUR effect-allele frequencies match the PGS-reported frequencies within Â±0.035. No AUC or calibration was computed, because no PDAC labels exist and simulating one from the same score would be circular.

## Reproduce
Requires Python 3.11 with numpy, pandas, scipy, matplotlib and scikit-learn.
```powershell
python build_pdac_data.py      # needs data/meta.csv and data_pdac/PGS000725.txt.gz
python -m notebook             # Kernel > Restart & Run All on each Part3 notebook (USE_DEMO = False)
```
