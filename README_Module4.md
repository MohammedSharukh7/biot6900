# BIOT 6900 — Module 4: Structure-Based Druggability Assessment

**Name:** Mohammed Sharukh
**Disease:** Pancreatic ductal adenocarcinoma (PDAC)

## Targets

| Gene | UniProt | Module 2 rank | Experimental structure | Druggability call |
|---|---|---|---|---|
| ERBB4 | Q15303 | 4 | 2R4B, chain A (2.40 Å, thienopyrimidine inhibitor bound) | Structure supports a small-molecule pocket |
| CEL | P19835 | 11 | 1F6W, chain A (2.30 Å, no bound ligand) | Possible but uncertain |

ERBB4 was chosen as a receptor tyrosine kinase with a strong small-molecule
tractability prior in Module 3 (p_sm = 0.70) and a known ATP-binding kinase
pocket. CEL was chosen as a pancreatic lipase with one of the highest Module 3
small-molecule scores (p_sm = 0.72) — a catalytic enzyme, and so a clean test of
whether sequence-based tractability predicts a real structural pocket.

## Files

- `BIOT6900_Module4_Assignment.ipynb` — the full analysis, Steps 1–7
- `structure_assessment_pdac.csv` — summary table exported in Step 7
- `PDAC_Module4_Report.pdf` — the written report
- `targets_pdac.csv` — Module 2 ranked target list (input)

The `structures/` folder (AlphaFold models, PAE files and downloaded PDB
structures) is excluded from the repository via `.gitignore`.

## What didn't work

- **fpocket on Windows.** fpocket is not available through pip and Homebrew does
  not carry it, so Step 6 could not be run locally. The notebook was run on the
  Northeastern Explorer cluster instead, using a conda environment
  (`conda create -n biot6900 -c conda-forge python=3.11 numpy pandas matplotlib
  fpocket ipykernel`) registered as a Jupyter kernel. Steps 1–5 ran locally on
  Windows without issue.
- **No ligand in 1F6W.** The CEL reference structure has no bound small-molecule
  ligand, so the Step 6 ligand-site check could only be run for ERBB4. CEL's
  pockets were instead compared against the catalytic triad (Ser214, Asp340,
  His455 in UniProt numbering).
- **Numbering offsets.** 1F6W uses mature-protein numbering and carries two
  crystallization mutations (N186D, A298D), which appear as mismatches in the
  sequence alignment. All residue numbers in the report and notebook use UniProt
  numbering.
- **MUC5B dropped.** Originally considered from the Module 2 list, but at 5,762
  residues it exceeds the 2,700-residue AlphaFold fragmentation cutoff.

## Main findings

ERBB4's top-ranked pocket (score 0.894, mean pLDDT 80.9, PAE within 5.4 Å)
covers 68% of the residues contacting the GW7 inhibitor in 2R4B. CEL's
highest-scoring pocket (0.925) does not correspond to its catalytic site; the
pocket containing Ser214 and His455 ranks 4th with a druggability score of only
0.135, illustrating that fpocket scores can underrate open, solvent-exposed
catalytic sites.
