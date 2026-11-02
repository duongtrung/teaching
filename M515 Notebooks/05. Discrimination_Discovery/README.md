# Discrimination Discovery: two linked practicals
This edition matches the revised 60-slide lecture. It replaces the former matched-neighbor and validation/re-audit practicals with **one simpler feature-and-selection case**. There are two active notebooks. Both use the same 40 fictional applicants.

## Start
Use Python 3.12. From the extracted pack folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

On Windows, activate with `.venv\Scripts\activate`. Keep the folder structure and open the notebooks inside it. All input data are bundled. The exercises run offline after packages are installed. Saved outputs are included.

| Notebook | Slides | Main student output |
|---|---|---|
| `01_counts_uncertainty_and_false_alarms.ipynb` | 9–38, optional appendix 60 | Counts, a five-context rule table, Wilson calculation and false-alarm interpretation |
| `02_feature_engineering_and_selection_bias.ipynb` | 39–52 | Feature trace, complete/selected reports, excluded IDs and a justified revised rule |

Each notebook contains a complete **Part 1** lesson and guided **Part 2** project extensions. TODO cells are runnable scaffolds, not completed research projects. A full explanation is available for self-study; only the highlighted tasks in `TEACHING_GUIDE.md` are required during the short classroom labs.

## One hiring story
Forty people submit complete applications for an online Analyst assessment. All meet the stated skill cutoff of 70. There are 40 assessment seats. The original car-ownership filter invites 8/20 women and 16/20 men, leaving 12 and 4 denied. A misleading reporting definition excludes those 16 people and shows 100% invitation rates within the selected 24. A reviewed skill-only rule invites all 40 while preserving original outcomes.

The fair-lottery example is a **separate statistics demonstration**, not an alternative description of these 40 decisions. The normal-test simulation is an ideal calibrated probability model. The exact family formula requires all nulls true, independence and actual size exactly.05. Fisher's discrete test need not have exactly that size.

## Files and reproducibility
- `data/raw/applicants_40.csv`: constructed source facts, all applications complete.
- `data/raw/policy_and_scenario.json`: opportunity, capacity, policy and the explicitly stated misleading intent.
- `data/processed/`: derived fields, full/selected reports, excluded IDs, original/revised outputs, rules and uncertainty results.
- `src/prepare_data.py`: deterministic generation and documented feature derivation.
- `src/audit.py`: inspectable counts, rule metrics, Wilson intervals and probability calculations.
- `figures/`: seven computed notebook figures.
- `DATA_GUIDE.md`, `TEACHING_GUIDE.md`, `SOURCES.md`: meanings, teaching prompts and references.

Run `python src/prepare_data.py`, then **Restart Kernel and Run All Cells** in notebooks 01 and 02. Original decisions are retained alongside separate revised outputs. The raw cohort is constructed, not an empirical sample supporting population or demographic claims. Wilson intervals illustrate a binomial model; a real application must justify its sampling assumptions.

The new pack has two notebooks. Keep this edition with the corresponding revised slides to avoid mixing it with the earlier three-notebook version.
