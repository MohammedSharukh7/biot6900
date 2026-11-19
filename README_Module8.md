# BIOT 6900 — Module 8: Single-Cell & Spatial Omics

**Name:** Mohammed Sharukh
**Target gene:** ERBB2 (HER2)
**Files:** `BIOT6900_Module8_Assignment_Starter.ipynb` (completed notebook), `BIOT6900_Module8_Report.pdf` (report)

I followed ERBB2 through breast-cancer single-cell data (CELLxGENE Census, 10 donors) and the provided 10x Visium section. ERBB2 is expressed by epithelial/tumor cells, at levels that differ strongly between patients, and in the tissue it is concentrated in the tumor-nest cores rather than at the invasive margin or in the stroma. scVI was chosen over Harmony (better cell-type preservation with comparable donor mixing). All TODO cells ran.

## What did not run as written, and what I changed
- **Explorer session:** JupyterLab only starts with the Working Directory field left blank. A non-existent folder made the session exit at launch.
- **PyTorch:** `scvi-tools` pulled in a CUDA 13 build of PyTorch, which the P100 node's driver (CUDA 12.3) cannot run. I pinned `torch==2.14.1+cu126`.
- **Census download:** reading from S3 timed out because compute nodes reach the internet through an HTTP proxy. I passed the proxy to TileDB via `tiledb_config` and pinned `census_version="2025-11-08"`.
- **Batch-aware HVGs:** `seurat_v3` failed for one donor, so I used `span=0.5` and filtered genes to ≥10 cells. I also made the QC cell safe to re-run from raw counts.
- **Library versions:** I added two small compatibility patches near the top of the notebook (scanpy 1.11 with newer scipy and umap-learn 0.6).
- **Cell labels:** the starter's broad-label mapping sent 8,526 "malignant cell" to T (substring "t cell"), which I corrected in a cell after the Census pull.
- The 1.3 interpretation (unintegrated UMAP) was entered as a comment in a code cell rather than in the markdown answer cell.
