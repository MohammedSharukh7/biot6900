# BIOT 6900 · Module 2 · Assignment 2 — Report

## Independent Multi-Omics Target Discovery — Pancreatic Ductal Adenocarcinoma (PDAC)

**Student:** Mohammed Sharukh
**Date:** 09.24.2026

\---

## 1\. Disease \& Data Choice

Pancreatic ductal adenocarcinoma (PDAC) was chosen for this analysis because it is one of the
most aggressive cancers with a very low survival rate, making target discovery especially
meaningful, and because the CPTAC-PDAC dataset was readily accessible and provided all three
required omics layers. Data was sourced from LinkedOmics
(https://www.linkedomics.org/data\_download/CPTAC-PDAC/), which is open access and required no
data-use agreement. The underlying cohort is sample-matched -- the same 140 patients were
measured at the RNA, protein, and mutation level -- but this analysis did not use that
patient-level matching directly. Instead, each layer was reduced to gene-level tumor-versus-normal
summary statistics (mean differences and p-values). This distinction matters: without stating it
clearly, a reader might assume the analysis preserved patient-level relationships between RNA,
protein, and mutation status, when in fact it did not -- which limits what can be claimed about
individual patients or about relationships between molecular layers within the same person (see
Limitations).

## 2\. Weighting

Equal weighting (1/3 each for transcriptomic, proteomic, and genomic evidence) was used in this
analysis. A case could be made for weighting mutation evidence more heavily, since mutations are
permanent DNA-level changes that can act as upstream drivers of cancer. However, a mutation does
not guarantee a functional consequence, so mutation frequency alone does not necessarily reflect
biological importance. Conversely, RNA and protein changes reflect active biology within the
tumor -- a gene can be mutated without significantly affecting expression or protein activity,
while a strong RNA or protein change indicates that something is genuinely changing at the
functional level. Given the absence of a strong disease-specific or statistical reason to
prioritize any single layer, equal weighting was retained to avoid arbitrarily favoring one
evidence type over the others while still allowing all three to contribute to the final score.

## 3\. Top Targets

**Mutation frequency layer:**

|Gene|Mutation frequency|-log10(p)|
|-|-|-|
|KRAS|96.4%|260.76|
|TP53|75.0%|176.57|
|CDKN2A|20.7%|28.40|
|SMAD4|17.9%|22.90|

**Top 10 of combined multi-evidence score:**

|Gene|RNA log2FC|Protein log2FC|-log10(p) mutation|Concordant|Score|
|-|-|-|-|-|-|
|COL11A1|2.787|1.448|1.263|True|0.984|
|MUC5B|2.071|1.224|2.499|True|0.976|
|TNS4|4.351|1.234|0.771|True|0.975|
|ERBB4|-2.565|1.329|0.771|False|0.973|
|PLIN4|-3.068|-1.197|0.771|True|0.973|
|MUC16|3.162|0.922|6.636|True|0.971|
|FN1|1.826|1.263|1.263|True|0.971|
|POSTN|1.743|1.353|1.263|True|0.971|
|NOS1|-1.916|-1.252|0.771|True|0.965|
|MUC5AC|3.751|0.815|3.220|True|0.962|

KRAS, TP53, CDKN2A, and SMAD4 were the most frequently mutated genes in this cohort (up to 96%
for KRAS), but none of them ranked in the top 15 by combined score. This is because the combined
score rewards the size of the RNA and protein changes, while mutation frequency measures how
often the DNA is altered in the tumors. A gene can be mutated in nearly every patient without
necessarily showing a large expression or protein swing between tumor and normal -- so a gene can
top the mutation-frequency list without topping the combined-score list.

One clear pattern in the top-ranked genes was that several were related to mucin production or
the extracellular matrix. Mucin genes such as MUC5B, MUC16, and MUC5AC make sense because PDAC
tumors can have abnormal mucus production, while ECM-related genes such as COL11A1, FN1, and
POSTN also make sense because PDAC is associated with dense desmoplastic stroma.

## 4\. Discordant Gene

ERBB4 showed a discordant pattern, with its RNA level decreasing in tumors (log2FC = -2.565)
while its protein level increased (log2FC = +1.329). A possible explanation is that ERBB4 protein
degradation is reduced, allowing the protein to accumulate even though less ERBB4 mRNA is being
produced. The decrease in ERBB4 mRNA is supported by previous research reporting reduced ERBB4
mRNA expression in pancreatic cancer (Graber et al., 1999, *International Journal of Cancer*),
while the increased protein level and the degradation explanation are interpretations of our data
rather than established findings.

## 5\. Limitations

This analysis integrated data at the group level rather than the patient level: differential
expression was computed as the mean across all tumor samples versus the mean across all normal
samples, without pairing any individual patient's RNA, protein, and mutation values together. As
a result, this analysis can claim that certain genes show population-level differences in RNA,
protein, or mutation patterns between PDAC tumor and normal samples in this cohort. It cannot
claim that these changes occur in every individual patient, since group averages do not guarantee
that any single patient follows the overall pattern. It also cannot claim that these genes cause
PDAC, since an association between a gene and tumor status is consistent with the gene being a
downstream consequence of the cancer, not necessarily a driver of it -- establishing causality
would require additional experiments beyond this correlational, gene-level analysis.

