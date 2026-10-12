# Data dictionary and target map

All counts refer to the included snapshots, not an unspecified live source. `CSV.gz` is ordinary gzip-compressed CSV readable by pandas. The manifest records provenance; the processing report records transformations, schemas, missingness and hashes. Generated inputs are separate from original downloaded research data.

## C1: An author résumé analysis release

| Table | Rows | Unit |
|---|---:|---|
| `data_gpt35_baseline.csv.gz` | 332,895 | Fictitious résumé analysis observations; one score missing |
| `data_gpt35_heter.csv.gz` | 332,895 | Observations with source heterogeneity indicators |
| `data_score_4models.csv.gz` | 332,257 | Released records and model-specific missing scores |
| `data_bootstrap_gpt35.csv.gz` | 3,000 | Stored regression/resampling estimates |
| `data_magnitude_gpt35.csv.gz` | 36 | Stored threshold-effect results |

These five tables live in `data/processed/01_an_resume/`. Raw Stata files preserve source nominal codes and embedded labels. `stata_dictionary.json` retains source variable/value mappings and decoding warnings. The approximate 361,000 generated-résumé headline differs from released analysis support.

| Fields | Role and interpretation |
|---|---|
| `record_id` | Added local row ID. No verified cross-file/base-profile pairing key. |
| `score_gpt35`, `score_gpt4o`, `score_gemini`, `score_claude`, `score_llama` | Historical model assessment outputs on 0–100. Missing remains missing. No automatic probability interpretation. |
| `igender`, `gender_cue` | Source 1=female,2=male and decoded assigned name cue. |
| `iethnicity`, `race_cue` | Source 1=black,2=white and decoded assigned name cue. |
| `audit_group` | Race-by-gender assigned intersection. These are not verified identities. |
| `iposition`, `occupation`, `istate`, `state`, `last_work_title` | Nominal occupation, state and prior work-title context, not continuous ranks. |
| `highest_degree`, `degree` | Source nominal degree category and decoded label. |
| `worknum`, `edunum`, `skillnum` | Author résumé entry counts for work, education and skills. |
| `avg_duration_work`, `duration_edu`, `num_high_level`, `avg_length_work_desc` | Author-derived controls; source definitions/units must be verified for new modelling. |
| `first_work_start`, `first_edu_start` | Stata dates serialized to ISO strings; encode deliberately for regressions. |
| `minority`, `median_female_bls`, `median_black_bls` | Author combined/heterogeneity indicators. Use explicit subgroup definitions in reports. |
| Bootstrap fields `SamplingRound`, `b`, `se`, `p`, `F`, `G` | Stored estimates and uncertainty plotting values. A row is an estimate. |
| Magnitude `cutoff`, `coeff`, `se`, `p`, `cilb`, `ciub` | Stored threshold-effect estimates and intervals. Inspect original `Code.do` for specifications. |

`selected=score≥80` is a derived hypothetical decision. No independently validated job-performance/qualification `y` is supplied. Do not calculate suitability error rates or manufacture pairs from row numbers.

## C2: disclosed matching simulation

`matching_variants.csv` has 144 rows: 18 base profiles ×4 institution tags ×2 arbitrary name tags. Three invented jobs each have six skill/experience profiles. Only three base profiles meet the constructed reference. Related variants are not independent people.

| Field | Meaning |
|---|---|
| `variant_id`, `base_pair_id`, `job_id` | Unique variant, repeated qualification-profile key and invented job. |
| `required_skills`, `resume_skills` | Raw lists of explicit tokens; processed semicolon-separated strings. |
| `skill_hits` | Cardinality of exact token-set intersection. |
| `required_years`, `experience_years` | Invented requirement 3 and profile experience 1 or5. |
| `institution_category` | Ivy League/HBCU/women's-college/other tag for controlled testing. Not actual quality or identity. |
| `name_cue` | Arbitrary A/B tag. No real demographic category is inferred. |
| `job_text`, `resume_text` | Invented readable templates; no personal applicant text. |
| `reference_match`, `y` | Constructed label: all three skills and at least three years. |
| `provenance` | Explicit generated-teaching status. |

Scores are computed in the notebook, not downloaded LLM outputs. Rubric score =`1+2×skill_hits+2×min(years/3,1)`. Proxy score adds disclosed arbitrary institution/name effects and clips to 1–10. The decision threshold is 8. The original Iso/Machamp source has private text pairs/match status and LLM scores1–10, but exact experiment records are not included.

## C3: attributed case facts and fictional boundary grid

`CASE_FACTS.json` is a source summary, not an applicant table. `applicant_grid.csv` has 36 generated rows: nine chosen ages, two reported rule categories and two constructed qualification states.

| Field | Meaning |
|---|---|
| `applicant_id` | Invented traceability key. |
| `age_years` | One of 30, 40,54,55,56,59,60,61,70, chosen for boundary tests. |
| `sex_rule_category` | Female/male categories described in the source allegation; no policy for other categories is supplied. |
| `work_sample` | Invented 50 or80 score. No connection to real employer data. |
| `teaching_eligible`, `y` | Invented work sample≥70 reference. |
| `age_band` | Under55,55–59,60+ bands derived for intersectional display. |
| `provenance` | Explicit generated-boundary status. |

The notebook's `veto` reconstructs the alleged age/sex rule. `decision_legacy=y AND NOT veto` includes our invented qualification step. `decision_revised=work_sample≥70` removes that veto in the scaffold. All calculated rates are conditional on the chosen fictional support. The source does not supply the real applicant denominator, full features or performance labels.

## C4: COMPAS public research cohort

The original CSV has 7,214 records. Documented conventional filters yield 6,172; the stated African-American/Caucasian comparison yields 5,278. All-group and two-group tables plus `filter_flow.csv` are retained under `04_compas/`.

| Field | Meaning and limitation |
|---|---|
| `record_id` | Original source record ID for traceability and splitting. |
| `race`, `sex` | Recorded source categories, retained for audit support. |
| `age`, `age_cat` | Source age/context. |
| `priors_count` | Recorded prior count, potentially influenced by institutional exposure. |
| `c_charge_degree` | Recorded charge-degree category, with measurement/context limits. |
| `decile_score` | Historical COMPAS ordinal score 1–10. Flag if≥5. Not a known probability. |
| `y` | Renamed raw `two_year_recid`, recorded 0/1 outcome. Does not observe all conduct. |

Positive decisions are adverse high-risk flags. Processed tables omit names, birth dates, case identifiers, detailed charge descriptions and future-outcome features. The new logistic teaching model uses age category, charge degree and prior count, optionally recorded audit columns for a methodological comparison. Its probabilities and calibrated probabilities are a different system from historical COMPAS.

Undefined metric denominators remain NaN. Max-minus-min gaps require all compared group rates to be defined. Rates are fractions in code and gaps become percentage points when multiplied by 100. A signed difference must name its reference.
