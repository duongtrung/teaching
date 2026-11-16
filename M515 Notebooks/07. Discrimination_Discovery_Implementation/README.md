# Discrimination discovery and implementation

This lab matches the 46-slide Gisma lesson. It uses 16 fictional applicants for an online assessment. The dataset is included, and no external data download is required.

| File | Purpose |
|---|---|
| `Discrimination_Discovery_Implementation_Lab.ipynb` | Companion notebook with explanations, saved outputs and exercises. The notebook embeds its own copy of the data. |
| `audit_lab.py` | Standalone version of the worked notebook code. It reads the bundled CSV, prints the audit and writes tables and a plot to `results/`. |
| `data/applicants_16.csv` | Source data used by the standalone script. |
| `requirements.txt` | Tested pandas and matplotlib versions. |

Extract the ZIP before running the code. Open a terminal in the extracted folder:

```bash
python -m pip install -r requirements.txt
python audit_lab.py
```

For the notebook, open it in JupyterLab, Jupyter Notebook or VS Code using a Python kernel with these same dependencies. If JupyterLab is not installed, run `python -m pip install jupyterlab` and then `jupyter lab`.

The original invitations should be 4/8 women and 6/8 men. Across the three policies (original, no car bonus at 70, no car bonus at 65), the numbers of missed qualified applicants should be 2, 4 and 0. The last policy also produces one false positive in this fictional cohort. The exercise illustrates how to audit a policy and does not support conclusions about a real population.
