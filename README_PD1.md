# BIOT 6900 · Portfolio Deliverable 1 — Multi-Omics Target Discovery Package

**Student:** Mohammed Sharukh  **Disease:** Pancreatic ductal adenocarcinoma (PDAC)  **Due:** Oct 29, 2026, 6:00 pm

This package synthesizes Labs 2–4 (no new analysis). It takes CPTAC-PDAC multi-omics evidence through
protein-language-model triage and AlphaFold structure assessment to a ranked, structurally characterized shortlist.

## Final shortlist

| # | Target | Decision | Modality |
|---|--------|----------|----------|
| 1 | ERBB4 (Q15303) | Advance, with a validation gate on the RNA/protein discordance | Small molecule (ATP pocket; PDB 2R4B) |
| 2 | POSTN (Q15063) | Advance; structure not yet assessed | Antibody (secreted, stromal) |
| 3 | TNS4 | Hold; strong biology, weak tractability | Degrader or PPI |
| 4 | CEL (P19835) | Deprioritize as a target; keep as pipeline positive control | n/a (acinar enzyme) |

## Files

| File | From | What it is |
|------|------|-----------|
| `PD1_PDAC_Target_Package.pdf` | this deliverable | 5–6 page package submitted on Canvas |
| `pd1/make_pd1_figures.py` | this deliverable | Regenerates Fig 1 (integration) and Fig 2 (Venn) from `targets_pdac.csv`; writes `pd1/pd1_numbers.txt` |
| `pd1/fig1_integration.png`, `pd1/fig2_venn.png` | generated | Required figures |
| `BIOT6900_Assignment2_PDAC.ipynb`, `targets_pdac.csv` | Lab 2 | Multi-omics integration and ranked table |
| `BIOT6900_Module3_Assignment.ipynb`, `targets_pdac_w3.csv` | Lab 3 | ESM C tractability priors and re-ranked table |
| `module4/BIOT6900_Module4_Assignment.ipynb` + outputs | Lab 4 | AlphaFold pLDDT/PAE, RMSD vs 2R4B/1F6W, fpocket |

**Note on file names:** the assignment template refers to `targets_ad.csv`. This project's equivalent is
`targets_pdac.csv`, because the disease is PDAC.

## Reproduce the figures

```powershell
cd C:\Users\USER\biot6900
python pd1\make_pd1_figures.py
```

The script needs only pandas, numpy and matplotlib. It prints the columns it detected; if a column is picked
wrongly, set it in the `COLS` dictionary at the top of the script. Venn thresholds are: RNA |log2FC| ≥ 1 and
p < 0.05; protein |log2FC| ≥ 0.5 and p < 0.05; mutation enrichment p < 0.05.

## Data sources

- CPTAC-PDAC via LinkedOmics (open access): https://www.linkedomics.org/data_download/CPTAC-PDAC/
- AlphaFold Protein Structure Database: AF-Q15303-F1, AF-P19835-F1
- RCSB PDB: 2R4B (ERBB4 kinase and covalent thienopyrimidine), 1F6W (CEL catalytic domain)
- Module 3 data pack (ESM C 300M embeddings, Open Targets clinical-precedence labels), via Canvas

## Known gaps (stated in the report)

- POSTN and TNS4 were triaged in Lab 3 but not modeled in Lab 4.
- fpocket ran on the Northeastern Explorer cluster, because it is not available through pip on Windows.
- All integration is at the group level, not patient-paired.
