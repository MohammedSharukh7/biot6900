# BIOT 6900 - AI-Powered Biotech Workflows (Fall 2026)

**Student:** Mohammed Sharukh
**Disease across all modules:** pancreatic ductal adenocarcinoma (PDAC)

## Repository index

| Module | What it is | README | Report |
|---|---|---|---|
| 1 | Environment setup and lab guide (Parts A-C) | this file | - |
| 2 | Independent multi-omics target discovery (CPTAC-PDAC) | this file (below) | `PDAC_Module2_Report.pdf` (also `REPORT.md`) |
| 3 | PDAC target triage with protein language models | `README_Module3.md` | `PDAC_Module3_Report.pdf` |
| 4 | Structural druggability of ERBB4 and CEL | `README_Module4.md` | `PDAC_Module4_Report.pdf` |
| 5 | Variant interpretation in CYP2C19 | `README_Module5.md` | `CYP2C19_Module5_Report.pdf` |
| Portfolio 1 | PDAC target package | `README_PD1.md` | `PD1_PDAC_Target_Package.pdf` |
| 6 | PRS portability on real data | `module6/README.md` | `module6/BIOT6900_Module6_Lab6_Report_MSharukh.pdf` |

---

# Module 2 - Assignment 2: Independent Multi-Omics Target Discovery (PDAC)

## What I did
I ran the course multi-omics pipeline independently on PDAC. Each of three CPTAC-PDAC data layers (RNA, protein, somatic mutation) was reduced to one row per gene (tumour-vs-normal log2 fold-change and Welch t-test p-value for RNA and protein; mutation frequency and a binomial enrichment p-value for mutations). The layers were joined on gene symbol (2,532 genes in all three), RNA-protein direction concordance was computed (1,650 / 2,532 concordant), and an equal-weight, rank-percentile multi-evidence score ranked the genes. The top hits recover known PDAC biology (MUC16/CA125, MUC5AC, MUC4, the desmoplastic-stroma genes COL11A1, FN1 and POSTN) plus less-studied candidates such as TNS4. The report interprets the top targets, the discordant gene ERBB4, and the limitations.

## Data sources
All data come from the CPTAC-PDAC cohort on the LinkedOmics portal:
https://www.linkedomics.org/data_download/CPTAC-PDAC/

**Access type:** open access - no application or data-use agreement required.

| Layer | File | Description | Samples |
|---|---|---|---|
| Transcriptomics | `mRNA_RSEM_UQ_log2_Tumor.cct` | RNA-seq, RSEM upper-quartile normalized, log2 | 140 tumour |
| Transcriptomics | `mRNA_RSEM_UQ_log2_Normal.cct` | same, normal tissue | 21 normal |
| Proteomics | `proteomics_gene_level_MD_abundance_tumor.cct` | gene-level proteomics, median-normalized abundance | 140 tumour |
| Proteomics | `proteomics_gene_level_MD_abundance_normal.cct` | same, normal tissue | 75 normal |
| Genomics | `Mutation_gene_level.cgt` | gene-level somatic mutation calls (variant type or "WT") | 140 tumour |

The tumours are sample-matched across all three layers; the normal comparators are not (21 RNA vs 75 protein). The analysis integrates at gene level, not patient level.

## Files
- `BIOT6900_Assignment2_PDAC.ipynb` - notebook, run top to bottom (Kernel > Restart & Run All)
- `targets_pdac.csv` - the full ranked table (2,532 genes, highest score first); the top 15 are discussed in the report
- `PDAC_Module2_Report.pdf` / `.docx` - written report (also as `REPORT.md`)

## What did not work / known issues
- **Genomic layer source.** The assignment suggests GWAS; I used CPTAC somatic mutations instead so all three layers come from the same tumours. Germline GWAS was not used.
- **Genes lost in reduction.** Some genes had too few non-missing normal values for a t-test (SciPy `SmallSampleWarning`); their p-values were NaN and they were dropped (RNA 28,057 -> 26,005 genes; protein 11,662 -> 11,630).
- **Inner join drops never-mutated genes.** Only genes mutated in at least one tumour survive the three-way join, so strongly changed but never-mutated genes cannot appear in the ranking.
- **Very small mutation p-values.** KRAS and TP53 enrichment p-values underflow; they were floored at 1e-300 before taking -log10.
- **Tissue composition.** Several top-ranked down-regulated genes (CEL, CPA1, PRSS1, PLA2G1B) are acinar enzymes; their drop mainly reflects normal pancreas in the comparator samples. This is discussed in the report rather than corrected.
- **Export scope.** `targets_pdac.csv` contains every ranked gene, not only the top 15.
