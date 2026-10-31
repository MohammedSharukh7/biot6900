# BIOT 6900 · Module 7 — Knowledge Graph for PDAC (Neo4j)

**Name:** Mohammed Sharukh
**Disease:** Pancreatic ductal adenocarcinoma (PDAC)
**Course:** BIOT 6900 AI-Powered Biotech Workflows, Computational Lab 7, Fall 2026

## What this is
A Neo4j AuraDB knowledge graph for PDAC. It joins my Module 2 multi-omics targets (`targets_pdac.csv`, CPTAC-PDAC), the Module 5/6 PGS000725 GWAS variants, HPO phenotypes, Reactome pathways, drugs, and two related diseases (cholangiocarcinoma and chronic pancreatitis). The graph is used to answer "which drugs act on PDAC genes", to run a shared-symptom repurposing query, to rank candidate biomarkers (PageRank fused with evidence), and to find communities.

**Final graph:** 64 nodes (29 genes, 11 pathways, 11 drugs, 5 phenotypes, 5 variants, 3 diseases) and 77 relationships (30 ASSOCIATED_WITH, 20 PARTICIPATES_IN, 12 TARGETS, 10 HAS_PHENOTYPE, 5 OCCURS_IN).

## Files (`module7/`)
| File | What it is |
|---|---|
| `BIOT6900_Module7_PDAC.ipynb` | Completed starter notebook (Kernel → Restart & Run All) |
| `targets_pdac.csv` | Module 2 input (copied here so the notebook runs from this folder) |
| `my_knowledge_graph.png` | Graph figure, coloured by node kind |
| `nodes.csv`, `edges.csv` | Node and edge tables; every edge has `source` and `confidence` |
| `biomarkers_ranked.csv` | PageRank + evidence fused ranking (29 genes) |
| `PDAC_Module7_Report.pdf` / `.docx` | Part F written report |

## How to run
1. Create an AuraDB Free instance and download its credentials file.
2. Save it in this folder as `neo4j_credentials.txt`. It is git-ignored and must never be committed.
3. `pip install neo4j networkx matplotlib pandas requests`
4. Open the notebook and run **Kernel → Restart & Run All**.

## Changes from the starter
- Credentials are read from `neo4j_credentials.txt` instead of being typed into a cell.
- `RELATED` is a list, so there are two related diseases.
- Every edge carries `source` and `confidence`.
- There is a harmonization cell that checks symbol → Ensembl ID (one ID per gene), Reactome IDs, and GWAS rsIDs against the PGS000725 file.
- The fused biomarker score uses undirected PageRank. Directed PageRank gives nearly identical values to all genes because gene edges point outward.
- The graph is drawn with a Kamada–Kawai layout (deterministic) and a legend.

## What didn't work / known issues
- **Optional patient layer not built.** The 1000 Genomes samples from Module 6 have no real PDAC phenotype, so a patient stratification query would have been circular.
- **No true GWAS p for the Module 2 genes.** Module 2 used CPTAC somatic mutations, not GWAS, so `gwas_p` is filled only for the five GWAS genes. The somatic enrichment p is in `mut_p`.
- **Druggability is a tier derived from the drug layer** (1.0 / 0.8 / 0.5 / 0.2), not the Module 3 tractability values. This makes the fused score partly circular (discussed in the report).
- **Variant → gene edges use the reported/nearest gene** and are marked `confidence = low`.
- The Ensembl/Reactome checks need internet. If they fail, the notebook prints a warning and continues with `ensembl` blank.
