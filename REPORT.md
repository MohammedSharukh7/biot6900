# BIOT 6900 · Module 2 · Assignment 2 — Report

## Independent Multi-Omics Target Discovery in Pancreatic Ductal Adenocarcinoma (PDAC)

**Student:** Mohammed Sharukh  **Submitted:** September 24, 2026 (report sections completed October 29, 2026, per the instructor's announcement)
**Repository:** github.com/MohammedSharukh7/biot6900 · notebook `BIOT6900_Assignment2_PDAC.ipynb` · ranked table `targets_pdac.csv`

---

## 1. Disease and data choice

**Why PDAC.** Pancreatic ductal adenocarcinoma is one of the most lethal solid tumours: most patients are diagnosed late, the five-year survival is low, and very few molecularly targeted therapies exist. That combination makes it a disease where systematic target discovery is genuinely needed, and it is the disease I carry through every module of this course.

**Why these data.** I used the CPTAC-PDAC cohort, downloaded from the LinkedOmics portal (https://www.linkedomics.org/data_download/CPTAC-PDAC/). It is **open access** — no application or data-use agreement was required — and it is one of the few public PDAC resources that provides all three required layers from the same tumours:

| Layer | File | Samples | Genes loaded | Genes after reduction |
|---|---|---|---|---|
| Transcriptomics | `mRNA_RSEM_UQ_log2_Tumor/Normal.cct` | 140 tumour / 21 normal | 28,057 | 26,005 |
| Proteomics | `proteomics_gene_level_MD_abundance_tumor/normal.cct` | 140 tumour / 75 normal | 11,662 | 11,630 |
| Genomics | `Mutation_gene_level.cgt` (somatic) | 140 tumour | 4,424 | 4,424 |

**Matched or unmatched?** The *tumours* are sample-matched: the same 140 patients were profiled at RNA, protein and mutation level. The *normal* comparators are not matched across layers (21 normals for RNA versus 75 for protein). I did not use patient-level pairing: each layer was reduced to one row per gene — a tumour-versus-normal log2 fold-change and Welch t-test p-value for RNA and protein, and a mutation frequency with a binomial enrichment p-value (versus the cohort's mean mutation rate) for genomics. The integration is therefore **gene-level**, not patient-level, which limits what can be claimed (Section 4).

**Genomics choice.** The assignment suggests GWAS for the genomic layer. I used CPTAC somatic mutations instead, because they come from the same tumours as the RNA and protein data and capture the drivers that define PDAC (KRAS, TP53, CDKN2A, SMAD4). Germline GWAS loci describe inherited risk in different individuals and would have added a fourth, unmatched population.

**Weighting.** I kept equal weights (1/3 per layer). Mutation evidence could be argued to deserve more weight because mutations can be causal, but mutation frequency says nothing about functional impact, and RNA/protein changes reflect active tumour biology. Without a principled reason to favour one layer, equal weighting avoids building my assumptions into the ranking.

## 2. Top-ranked targets and what they mean

After harmonizing on gene symbol, **2,532 genes** were present in all three layers; **1,650 (65%)** moved in the same direction at RNA and protein. The 15 highest multi-evidence scores were:

| Rank | Gene | RNA log2FC | Protein log2FC | Concordant | Score |
|---|---|---|---|---|---|
| 1 | COL11A1 | +2.79 | +1.45 | yes | 0.984 |
| 2 | MUC5B | +2.07 | +1.22 | yes | 0.976 |
| 3 | TNS4 | +4.35 | +1.23 | yes | 0.975 |
| 4 | ERBB4 | −2.57 | +1.33 | **no** | 0.973 |
| 5 | PLIN4 | −3.07 | −1.20 | yes | 0.973 |
| 6 | MUC16 | +3.16 | +0.92 | yes | 0.971 |
| 7 | FN1 | +1.83 | +1.26 | yes | 0.971 |
| 8 | POSTN | +1.74 | +1.35 | yes | 0.971 |
| 9 | NOS1 | −1.92 | −1.25 | yes | 0.965 |
| 10 | MUC5AC | +3.75 | +0.82 | yes | 0.962 |
| 11 | CEL | −6.09 | −2.71 | yes | 0.954 |
| 12 | BRSK2 | −2.98 | −1.81 | yes | 0.948 |
| 13 | MAT1A | −2.83 | −1.97 | yes | 0.948 |
| 14 | KRT6A | +5.21 | +1.47 | yes | 0.948 |
| 15 | FRAS1 | −1.24 | −1.16 | yes | 0.945 |

**Known PDAC genes recovered.** The list is dominated by three recognizable groups of PDAC biology:

- **Mucins — the tumour's secretory phenotype.** MUC16 (rank 6) encodes CA125, a clinically used serum tumour marker; MUC5AC (10) and MUC5B (2) are gel-forming mucins aberrantly expressed in PDAC and its precursor lesions; MUC4 sits just outside the top 15 (rank 17). All are strongly up at both RNA and protein.
- **Desmoplastic stroma.** COL11A1 (1), FN1 (7) and POSTN (8) are extracellular-matrix genes produced largely by cancer-associated fibroblasts. PDAC is defined by a dense desmoplastic stroma, so recovering these at the top is expected — but it also means they partly describe the *stroma*, not the cancer cells (Section 4).
- **Ductal/epithelial identity.** KRT19 (rank 20), a ductal keratin, and the CEACAM5/6 tumour markers (ranks 159/189) are up at both levels.

**The classic drivers rank low — and that is informative.** KRAS (mutated in 96% of tumours), TP53 (75%), CDKN2A (21%) and SMAD4 (18%) top the mutation layer, but only CDKN2A reaches the top 50 (rank 36); KRAS ranks 279, SMAD4 458 and TP53 913. The score rewards the *size* of tumour-versus-normal expression change, and these genes are altered in sequence rather than in abundance (KRAS RNA +0.63, protein +0.20; TP53 RNA +0.03). Rank-percentile normalization also caps the advantage a single extreme layer can give. A target list built this way prioritizes *expression-level* targets and should be read alongside the mutation layer, not instead of it.

**Surprising hits worth a second look.**

- **TNS4 (rank 3)** — tensin 4 is up 4.4 log2 units at RNA and 1.2 at protein, among the largest concordant increases in the dataset, yet it is not a classic PDAC gene. It sits at focal adhesions and is linked to growth-factor receptor signalling and cell migration, which makes it a plausible, under-studied candidate for invasion biology.
- **KRT6A (rank 14)** — a keratin associated with the aggressive "basal-like" transcriptional subtype of PDAC (Moffitt et al., 2015). Its strong increase suggests a subset of these tumours carries basal-like features, which could be explored by stratifying patients.
- **ERBB4 (rank 4)** — a receptor tyrosine kinase that ranks highly only because RNA and protein move in *opposite* directions (Section 3).

## 3. Discordant gene: ERBB4

ERBB4 is the most prominent discordant gene: its mRNA is **lower** in tumours (log2FC −2.57) while its protein is **higher** (+1.33). Several mechanisms could produce this:

1. **Protein stability.** Reduced degradation (for example altered ubiquitination or receptor recycling) would let ERBB4 protein accumulate while transcription falls.
2. **Cellular composition.** The RNA and protein measurements come from bulk tissue with different normal comparators (21 vs 75 normals). If ERBB4 protein comes mainly from one cell population whose share differs between the RNA and protein normal sets, the two layers can disagree without any change inside the tumour cells.
3. **Technical factors.** Mass-spectrometry protein quantification relies on a limited set of peptides and can be affected by family members with shared sequence (ERBB1–4).

The decrease in ERBB4 mRNA agrees with earlier work reporting reduced ERBB4 expression in pancreatic cancer (Graber et al., 1999). The protein increase and the explanations above are my interpretations of this dataset, not established findings; resolving them would need matched immunohistochemistry or single-cell data. More broadly, 35% of the joined genes are discordant, a reminder that RNA is an imperfect proxy for protein.

## 4. Limitations: what these data let me claim — and not claim

**What I can claim.** Within the CPTAC-PDAC cohort, specific genes show consistent population-level differences between tumour and normal tissue at RNA and protein level, and the top-ranked genes reproduce well-known PDAC biology (mucins, stroma, ductal markers).

**What I cannot claim.**

- **Nothing about individual patients.** Differences are group means; integration was gene-level, so I cannot say any single patient shows these changes, or that RNA, protein and mutation co-occur within the same person.
- **Nothing causal.** A gene that differs between tumour and normal may be a consequence of the cancer rather than a driver of it.
- **Not tumour-cell specificity.** Bulk samples mix cancer cells, stroma and residual normal pancreas. Several top-ranked genes are digestive enzymes of the *acinar* pancreas that are strongly down in tumours — CEL (rank 11), and CPA1, PRSS1 and PLA2G1B (ranks 123–126). Their drop mostly reflects normal samples containing acinar tissue that tumours lack, not a change in tumour biology. Likewise the ECM genes partly measure stromal content.
- **Not an unbiased gene universe.** The three-way inner join keeps only genes mutated in at least one tumour, so the 2,532 survivors exclude thousands of protein-measured genes that were never mutated. Highly expressed but never-mutated targets cannot appear in this list.
- **Unbalanced comparators.** RNA has only 21 normal samples, so RNA fold-changes and p-values are less stable than protein ones.

**Next steps** would be to repeat the analysis with tumour-purity adjustment, use patient-level pairing of RNA and protein, include non-mutated genes (outer join with mutation frequency set to zero), and validate top candidates such as TNS4 in an independent cohort.

## References

1. Cao L, et al. Proteogenomic characterization of pancreatic ductal adenocarcinoma. *Cell* 184, 5031–5052 (2021). (CPTAC-PDAC cohort.)
2. LinkedOmics CPTAC-PDAC data portal. https://www.linkedomics.org/data_download/CPTAC-PDAC/ (open access).
3. Moffitt RA, et al. Virtual microdissection identifies distinct tumor- and stroma-specific subtypes of pancreatic ductal adenocarcinoma. *Nature Genetics* 47, 1168–1178 (2015).
4. Graber HU, et al. ErbB-4 mRNA expression is decreased in non-metastatic pancreatic cancer. *International Journal of Cancer* 84, 24–27 (1999).
5. Open Targets Platform. https://platform.opentargets.org
