# Protein Inhibitor QSAR Demo

Can a model trained on molecular structures estimate inhibitor potency for compounds with scaffolds it has not seen during training?

This portfolio demo uses ChEMBL activity data for human acetylcholinesterase (CHEMBL220). It demonstrates molecular data cleaning, RDKit Morgan fingerprints, and evaluation on held-out Bemis–Murcko scaffolds. The notebook compares a random forest with a baseline that predicts the mean training potency.

## Run locally

Use Python 3.11 or 3.12. From the repository root, run:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS or Linux
# source .venv/bin/activate
python -m pip install -r requirements.txt
python fetch_data.py
python -m jupyterlab
```

Open `qsar_demo.ipynb` and choose **Restart Kernel and Run All Cells**. Internet access is required to install dependencies and fetch the public data.

## Data and evaluation

The [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data/target/CHEMBL220.json) supplies up to 1,000 activity records ordered by activity ID. The query selects exact IC50 measurements in nM from binding assays. It excludes records with a validity comment and converts concentrations to pIC50 as `9 - log10(IC50 in nM)`. Repeated canonical structures are represented by median pIC50. Live API results can change over time.

The notebook uses one scaffold-grouped split with fixed model settings and reports test MAE and RMSE in pIC50 units. The split estimates performance on unseen scaffold groups within this dataset. Assay conditions can vary, and a single split provides a limited estimate of generalisation. Predictions are computational estimates and require experimental confirmation.

## Files

- `fetch_data.py` downloads and converts the activity records.
- `qsar_demo.ipynb` prepares molecules, trains the models, and plots observed versus predicted activity.
- `requirements.txt` lists dependencies.
- `data/README.md` describes the generated input file.
