# Recommender systems: foundations, ethical audit and final projects

Companion to the 84-slide Gisma-template lecture. Two sessions of 150 minutes, each including a 10-minute break. Prerequisites: basic Python, arrays, means and train/test separation. Read `TEACHING_GUIDE.md` for the schedule and slide-to-notebook map.

## What is included

- `notebooks/01_recommender_foundations.ipynb`: guided theory, exact course-rating calculations, data engineering, three fitted models, evaluation, local recommendation inspection, and final-project TODOs.
- `notebooks/02_recommender_ethical_audit.ipynb`: six matched ethical cases, actual discovery and user-quality audits, MMR, synthetic provider/privacy/feedback exercises, a current policy case, and project guidance.
- `src/recsys_lab.py`: readable implementations of data loading, validation, popularity, item CF, observed-only biased matrix factorization, metrics, MMR and audits.
- `src/download_data.py`: original-host download with a disclosed public-mirror fallback.
- `data/raw/synthetic/`: complete fictional teaching datasets, safe to use for the exercises.
- `data/processed/summary.json`: aggregate results and exact slide-calculation values.
- `figures/`: aggregate figures produced by executing the notebooks.
- `execution_report.json`: code-cell execution counts; neither notebook had an execution error.

**One notebook per session.** The six ethical cases are sections within Notebook 02, not six additional hidden notebooks. Papers are conceptual readings unless a section explicitly says it reproduces an experiment. These labs are teaching adaptations, not claimed reproductions of all cited papers.

## Set up

Use Python 3.11 or later (tested with Python 3.12). Unzip the package and open a terminal in its root folder.

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m jupyterlab
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open Notebook 01 and run cells in order. The first download needs internet access; subsequent runs use local files. Notebook 02 can also fit its reference model if Notebook 01 has not generated a cache. The notebooks contain saved aggregate outputs for reading before setup. The source-derived user-history display is intentionally omitted from the distributed output; rerun that cell locally.

## Data acquisition and usage conditions

MovieLens 100K is a historical benchmark from GroupLens, University of Minnesota: <https://grouplens.org/datasets/movielens/100k/>. Read the downloaded `data/raw/movielens-100k/README`. Its conditions include acknowledgment, restrictions on redistribution, and permission requirements for commercial/revenue-bearing use. This package does not grant additional data rights.

The source records, movie metadata, individual processed splits, per-user outputs and model caches are **not bundled**. The downloader places source files in `data/raw/movielens-100k/`; running a notebook creates train/validation/test and movie tables in `data/processed/`. This preserves the requested raw/processed separation locally. The supplied `.gitignore` excludes these records and caches from a public repository. Check data rights before distributing any additional dataset.

During preparation the original host returned HTTP 503. The executed analysis retrieved the seven essential files from `https://raw.githubusercontent.com/chiang9/Medium_blog/main/data/ml-100k/`. Counts, ranges, unique user-item pairs, metadata joins and split chronology were checked; an official byte-level checksum was not independently verified. `download_manifest.json` records the preparation file hashes and retrieval origin. The notebook-generated `local_manifest.json` records local acquisition. The synthetic datasets are original fictional teaching values, not annotations of MovieLens users or providers.

## Read the results honestly

The strict global time split produces 166 test users, of whom 153 have positive test ratings, and 76 cold test users. A simple popularity ranking beats the supplied ItemKNN ranking on this protocol. The cold slice scores better than warm slices in this run. These are diagnostic results, not evidence that personalization is always inferior or that having less history causally improves quality.

MMR increases genre diversity, while the paired NDCG change is small and its bootstrap interval includes zero. Exposure uses an assumed position discount; it is not actual impression data. MovieLens cannot demonstrate present-day provider discrimination, well-being effects or legal noncompliance. Every ethical claim must identify the affected person, mechanism and evidence needed.

## Reproducibility

- Fit period: first 90% after demonstrating an 80/10/10 global chronological split.
- Hyperparameters: predeclared teaching settings, not tuned on test. Projects must tune on validation.
- Candidates: fitted catalog minus already-rated items; stable item-ID ties.
- Relevance: future test stars ≥4; cold relevant items remain in recall denominators.
- Ranking means exclude users with no positive test ratings; rating errors use all test ratings.
- Item CF: user-mean-adjusted common-rater cosine; ≥3 common ratings; positive similarities; overlap shrinkage n/(n+20); per-target top 40.
- MF: 12 factors; λ=10; seed 7; observed-only squared error plus bias/vector L2 penalty; L-BFGS-B maximum 1,000 iterations, ftol 1e-6. The supplied run converged.
- MMR: top 10 from 50 candidates; λ=.75; pool-score min-max normalization; genre cosine.
- Bootstrap: 1,000 user resamples, seed 7; pair user differences for policy comparisons.

The full environment versions are in `environment_tested.json`. Small numerical differences can occur across numerical-library versions. Do not adjust results merely to match rounded slide numbers.
