# Fairness in recommender systems: internship board lab

This fictional example uses four learners and four internship listings. The ZIP includes the notebook, all three input CSVs, and a standalone script. The calculations use only the Python standard library.

- **Notebook:** Open `notebooks/Fairness_in_Recommender_Systems_Lab.ipynb` in Jupyter or VS Code after extracting the ZIP, with a Python kernel running from the lab folder or its notebooks folder. Run the cells in order. Saved outputs are provided.
- **Terminal:** From the extracted lab folder, run `python src/audit.py`. It prints the comparison and creates `results/policy_comparison.csv`.
- **Data:** `listings.csv` defines listings and employer groups. `learners.csv` holds the learner segments and baseline orders. `relevance.csv` has the separate fit judgments (0 poor, 1 plausible, 2 strong) for all 16 pairs. All listings are eligible for everyone in the main case.
- **Metrics:** NDCG@3 uses gain `2**grade - 1` with log discounts. The separate illustrative exposure weights are 1, 0.5, 0.25. Neither the weights nor the results describe a real platform.

The baseline gives small employers 14.3% of modeled exposure. Promoting to rank 2 changes that to 28.6%, with new and returning learners scoring 0.907 and 0.951 NDCG@3. The notebook separates the worked example from home and project tasks.
