# BIOT 6900 · Module 10 · Computational Lab 10 — Medical Imaging AI: Build It, Then Break It

**Student:** Mohammed Sharukh · Fall 2026

This folder contains the graded Notebook 3 of Module 10. A transfer-learned DenseNet121 is fine-tuned on
PathMNIST tumour-vs-normal H&E tiles, then a self-designed confounder (a **burned-in microscope scale bar**) is injected
into the tumour class, the model is retrained, and a reliance battery with a clean control tests whether the
shortcut was learned. The pipeline (loader, preprocessing, DenseNet121, Grad-CAM settings, occlusion) is reused from
the course's Notebook 2, `BIOT6900_Module10_Real_Pathology`.

## Contents

| File | What it is |
|---|---|
| `BIOT6900_Module10_Graded.ipynb` | Graded notebook, Parts A–E, run top to bottom with Restart & Run All |
| `BIOT6900_Module10_Report.pdf` | 3–4 page written report (Part E) |
| `outputs/results.json` | Every number quoted in the report, written by the notebook |
| `outputs/figures/*.png` | Grad-CAM / occlusion panels, confounder examples, battery and dose-response plots |

## Pipeline

1. **Part A — clean model.** MONAI `DenseNet121(pretrained=True)` (ImageNet weights), 2-class head, Adam lr 1e-4,
   3 epochs, 128 px, ImageNet normalisation, seed 0. Reports validation and independent test accuracy.
2. **Part B — probe.** MONAI Grad-CAM at `class_layers.relu` (with the `minmax_keep_high` colour fix) and
   hand-built occlusion on 4 tumour + 4 normal test tiles, Grad-CAM for both target classes, and measured
   numbers for the five-point skeptic's checklist (heat on tissue and border, Grad-CAM/occlusion agreement,
   accuracy under a simulated scanner colour shift).
3. **Part C — confounder.** A scale-bar overlay (white label box, black bar, small text block) in the
   bottom-left corner, as stamped by microscope-camera or viewer export software. Added to tumour tiles only,
   in training **and** validation. `CONFOUNDER` can be switched to `"fold"` or `"color_cast"`.
4. **Part D — reliance battery.** Grad-CAM/occlusion on confounded tiles for both models, with the share of
   evidence on the artifact measured; tumour recall with vs without the artifact; flip rate when the artifact
   is added to normal tiles; the same tests on the clean model as a control; dose-response over overlay
   opacity 0–1.

## How to reproduce

Windows, Python 3.11, pip (no conda). From the repository root:

```powershell
python -m pip install "monai[pillow]" "medmnist>=3.0" torch scikit-learn scipy pandas matplotlib notebook
python -m notebook
```

Place `pathmnist_tumour_vs_normal_subset.npz` in a `data/` folder next to the notebook (or one level up), open the notebook
and run **Kernel → Restart & Run All**. CPU only, roughly 8–12 minutes. Seed = 0; small numeric differences between runs
are expected (as noted in the Notebook 2 lab guide). The first run downloads the ImageNet DenseNet121 weights.

To try an alternative confounder, set `CONFOUNDER = "fold"` or `"color_cast"` in the Part C cell.

## Notes

* Model weights are not saved or committed; they are retrained on every run.
* The dataset file is course-provided and is not redistributed here if it exceeds GitHub size limits.
