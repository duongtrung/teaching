# Notions and Measures for Discrimination: four matched case practicals

This revision pairs **exactly four case studies with exactly four Jupyter notebooks**. The accompanying 150-minute deck uses the same C1–C4 identifiers. Method papers support the case analyses rather than creating additional unmatched notebooks.

| Case | Slides | Notebook | Included evidence |
|---|---|---|---|
| C1 LLM résumé evaluation, An et al. (2025) | 25–31, plus lens example 21 | `01_an_resume_evaluation.ipynb` | Complete public author analysis release: five Stata tables, source code and ReadMe |
| C2 Matching and educational proxies, Iso et al. (2025) | 32–37 | `02_iso_matching_proxies.ipynb` | A disclosed 18-profile/144-variant teaching simulation; original Machamp microdata unavailable in the paper |
| C3 iTutorGroup rule audit, EEOC (2023) | 38–43, plus lens example 20 | `03_itutorgroup_rule_audit.ipynb` | Official source facts and a disclosed 36-row fictional boundary grid; no applicant microdata in the supplied release |
| C4 COMPAS error disparities | 44–52, plus lens example 22 | `04_compas_error_disparities.ipynb` | Original public benchmark, direct historical-score audit, and a separate teaching-model experiment |

Zafar (2017), Hardt et al. (2016) and Chouldechova (2017) supply C4's error/fairness theory. Kusner et al. (2017) supplies further reading on C2's causal assumptions. They do not create extra case notebooks. Every notebook has **Part 1: guided theory, engineering, visualizations, ethical diagnosis and practical responses** and **Part 2: research guidance, TODOs, substantive extensions and self-study**.

## Calculation tutorial in the slides

Slides **5–18** explain the reference label and decision, classify eight fictional records, build a confusion matrix, choose denominators, and compute every binary rate reported by the notebook helpers. They also show group gaps/ratios and a student checkpoint with its worked answer. The visible computations continue in C1 (slide 29), C2 (35), C3 (41) and C4 (46–49). The tutorial is a small arithmetic example, not a fifth case or notebook.

## Setup and use

Extract the **entire** ZIP, preserving its folders. Use Python 3.12 or a compatible environment. These numerical package versions were used for verification; the exact execution environment is recorded in `reports/ENVIRONMENT.json`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

On Windows, activate with `.venv\Scripts\activate` instead. Open a notebook from `notebooks/` and run from the top. The dataloader finds the package root whether Jupyter starts there or in the notebooks folder. No API key, live model or paid call is required. Source data and processed tables are already included.

For class, teams complete one case and exchange findings. Full notebook durations are self-study estimates, not four sequential activities inside 150 minutes. Read `INSTRUCTOR_GUIDE.md` for core sections, timings, hand-calculation checkpoints and teacher hints.

## Data organization and provenance

- `data/raw/01_an_resume/`: unchanged downloaded author release, including all five `.dta` files and the embedded coding.
- `data/raw/02_iso_matching/`: explicitly generated JSONL profiles and a source/scope card. These are **not** Machamp records or queried LLM outputs.
- `data/raw/03_itutorgroup/`: attributed case facts and explicitly generated applicant grid. These are **not** actual rejected applicants.
- `data/raw/04_compas/`: unchanged downloaded public research CSV.
- `data/processed/`: ten analysis tables and a Stata dictionary, with filtering/engineering documentation.
- `data/DATA_MANIFEST.json`: original download URLs, versions, timestamps, hashes and generated-data status.
- `data/processed/PROCESSING_REPORT.json`: transformations, fields, row counts, missingness and output hashes.

Public source availability does not establish a blanket license, consent or fitness for a new purpose. `THIRD_PARTY_NOTICES.md` records source/reuse limits. Classroom outputs use minimized processed COMPAS fields. The preserved raw public-record file contains identifying fields; avoid displaying or submitting them in student reports.

## Rebuild and verify

```bash
python scripts/download_data.py --verify-only
python scripts/process_data.py
python scripts/validate_bundle.py
```

If a downloaded research asset is missing, run `python scripts/download_data.py` to retrieve its recorded immutable version. The script does not overwrite changed local raw data silently. There is no download endpoint for the unavailable original C2/C3 microdata.

The disclosed synthetic inputs can be rebuilt with:

```bash
python scripts/generate_teaching_data.py
python scripts/process_data.py
```

The generator is deterministic and its outputs should match the manifest. For a project extension, keep your modified generator/data in the appropriate `reports/` case folder instead of altering the immutable classroom inputs.

## Evidence boundaries

C1's approximate 361,000-résumé paper headline differs from the released baseline's 332,895 rows (332,894 valid scores). No independent performance target or verified cross-file pairing key is supplied. The class recomputes descriptive summaries, not the paper's complete adjusted/clustered inference.

C2's original study has source matching status and LLM output scores, but exact data are private. Our known arithmetic scorer and constructed skill/experience label teach a mechanism. Its deliberately planted category effects do not estimate any real institution's quality or an actual LLM's bias.

C3's source reports alleged age/sex vetoes and a settlement. Its reconstructed rule grid has an invented work-sample target. All selection/error rates on that grid describe the design, not the employer's real applicant population.

C4's reference is a recorded justice outcome with measurement limits. The historical vendor score and newly fitted logistic teaching model are different systems. Group-specific thresholds are an experiment, not a deployment recommendation. A validation-fitted policy worsens a held-out FPR gap in the included example; preserve and interpret that result.

## Verification and final projects

All guided source cells and assertions were executed, with rich tables and 12 inline figures captured. This hosted environment prevents the socket binding required to start a normal Jupyter kernel. Verification therefore used fresh in-process IPython shells with unchanged source cells, one fresh process per notebook. Calculations and figures were checked; a normal Jupyter server/kernel startup was not verified here. The report documents that limitation. Student extension functions were defined but deliberately not executed or completed.

Part 2 requires students to choose a question, complete a protocol, implement a substantive extension and evaluate assumptions/uncertainty. Use `project_templates/` and save outputs under `reports/`. The assessment rubric is in every notebook. Merely rerunning Part 1 does not complete a final project.
