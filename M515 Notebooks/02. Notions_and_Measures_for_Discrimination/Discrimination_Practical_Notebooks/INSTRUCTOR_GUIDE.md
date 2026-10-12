# Instructor guide: 150 minutes and four matched case studies

The deck and notebooks use the same C1–C4 IDs. There are exactly four notebooks. This guide prioritizes **60 minutes of theory, 80 minutes of practical work/discussion and a 10-minute break**. Complete one core case per team during class. The longer guided/self-study sections and Part 2 support later final projects.

Instructor / institution / course / date: ____________________

## Session plan

| Time | Activity | What students produce |
|---|---|---|
| 0–10 | Case map and output/reference vocabulary | One harm and the meaning of a positive decision |
| 10–30 | Confusion-matrix tutorial, slides 5–18 | Row classification, denominator and hand-calculation checkpoint |
| 30–40 | Three audit lenses, slides 19–24 | Evidence needed for treatment, impact and errors |
| 40–50 | C1–C4 source, feature and target maps | Distinguish original data from reconstructions |
| 50–60 | Labels, proxies and practical responses | One ethical question per case |
| 60–70 | Break | Case-team assignments confirmed |
| 70–80 | Open the matched notebook and inspect inputs | Source/unit/feature/target card |
| 80–115 | Team core practical | One figure, one complete calculation, one recognized problem |
| 115–135 | Exchange audit records across cases | A denominator or assumption challenged by peers |
| 135–145 | Refine the response and select an extension | Evidence-limited recommendation and project question |
| 145–150 | Individual exit response | Problem, calculation, action and missing evidence |

The 63-slide deck includes a 14-slide calculation tutorial, case reference tables and practical prompts. Keep the tutorial within 20 minutes by treating steps 9–10 (FDR/NPV/FOR) as a visible reference if needed. Reserve two minutes for the student checkpoint. All essential tutorial examples, formulas, substituted counts and worked answers appear on the slides. Speaker notes retain facilitation and source information.

Use only the dataset/target maps during the 10-minute case overview. Teams use their assigned case's detailed tables and calculation slides during practice. The full case references and notebook extensions support self-study. The deck is not a script to read every slide sequentially during the theory block.

## Shared arithmetic foundation, slides 5–18

The fictional support example has TP=3, FP=1, FN=2, TN=2 and n=8. Students follow one record into one cell before calculating a rate. The denominators are n=8, reference positives=5, reference negatives=3, decisions positive=4 and decisions negative=4. Recall/FNR use reference positives; FPR/specificity use reference negatives; precision/FDR use positive decisions; NPV/FOR use negative decisions.

The second fictional group shows equal selection (50%) and accuracy (62.5%) with different FPRs: 1/3 versus 2/5. The signed A-minus-B gap is −6.67 percentage points and the A/B ratio is 0.8333. Small invented counts illustrate arithmetic only.

Checkpoint counts TP=4, FP=2, FN=1, TN=3 produce n=10, FPR=40%, FNR=20%, PPV=66.67%, selection=60% and accuracy=70%. Students write the fractions first, then inspect the next slide's answer. Zero denominators produce undefined rates. Missing reference labels prevent a confusion-matrix error audit. This foundation does not add another notebook.

## C1: An résumé scores, slides 25–31

Core notebook headings: dataset/schema and raw loader; support/score visualization; descriptive gap; threshold decision; practical response/diagnosis. Other-model missingness, equal-occupation summaries and stored author results can be self-study.

Students should identify **332,895 baseline rows, one missing score, 332,894 complete scores**, four assigned cue intersections and a 0–100 score scale. The release's 3,000 bootstrap rows and 36 magnitude rows are stored estimates, not more applicants. `record_id` is table-local and cannot establish cross-file pairs.

Worked selection checkpoint at threshold 80:

| Assigned cue | Selected | Valid scores | Rate |
|---|---:|---:|---:|
| black / female | 29,984 | 83,159 | 36.056% |
| black / male | 27,470 | 83,381 | 32.945% |
| white / female | 29,611 | 83,173 | 35.602% |
| white / male | 28,555 | 83,181 | 34.329% |

Black/male minus white/male = **−1.383599 percentage points**. Score means instead give approximately −0.301 **score points**. These are descriptive recomputations, not the original adjusted coefficients. TPR/FPR for job suitability are unavailable because the data lack an independent job-performance/qualification target.

Teacher prompts: What happens near rounded score thresholds? Which occupation mixture does your average describe? What counts as a failed response? What evidence could validate a job rubric? Why would dropping demographic columns leave cues in the original résumé text?

Expected recommendation: a broader, version-specific controlled audit; documented failure handling; independently validated, accessible job criteria. Do not accept “the whole model is fair” from one mean or ratio.

## C2: Iso matching/proxies, slides 32–37

Core headings: original versus accessible data; engineering; visible scorer mechanism; paired comparisons; before/after response. The simulation has **18 base profiles ×8 variants =144 rows**. Keep all variants of a base pair together. Its exact-token overlap and three-year requirement are artificial assumptions.

Original study design: 40 occupational groups, 400 base pairs (five matched/five unmatched per group), 80 variants per pair and 12 model snapshots. That gives 32,000 distinct variants and 384,000 related model evaluations. **No original Machamp microdata or original LLM scores are included.** The notebook does not substitute JobFair as if it were Iso's data.

Worked mechanism: three skill hits plus one year yields `1 +2×3 +2×(1/3) =7.667`. Averaging the arbitrary ±0.2 name variants cancels that term. The planted +0.8 institution bonus yields **8.467**, crossing threshold 8 even though the constructed reference says the experience requirement is unmet.

The correction removes known planted terms and succeeds against the constructed reference by design. This result demonstrates a mechanism, not a claim about actual LLMs or school quality. The simulation's group rates and deterministic paired effects are not estimates of the labour market. A label's annotation criteria still need justification.

Teacher prompts: Can education be job-relevant? Which feature does this job actually require? Why does a college not determine a person's identity? How would you compensate annotators and preserve disagreement? What would a permitted new empirical audit need?

## C3: iTutorGroup, slides 38–43

Core headings: official facts and unknowns; dataset/target map; boundary tests; direct comparisons; correction and safeguards. The 36-row grid contains **9 ages ×2 reported rule categories ×2 invented eligibility states**. Its qualification step is a teaching assumption, not the actual employer's full rubric.

The source reports allegations resolved through settlement: women aged ≥55 and men aged ≥60 faced an automatic rejection rule, more than 200 qualified applicants were affected, and the settlement provided $365,000 plus preventive relief. The described mechanism was programmed logic. Do not describe it as a proven LLM failure or a trial verdict.

Boundary answer for otherwise identical eligible profiles:

| Age | Female rule category | Male rule category |
|---:|---|---|
| 54 | advance | advance |
| 55 | reject | advance |
| 59 | reject | advance |
| 60 | reject | reject |

Grid-only FNR =6/9 (66.7%) for female-category profiles and 3/9 (33.3%) for male-category profiles. Removing the reconstructed veto recovers **nine eligible fictional profiles**. These are not empirical employer rates or real affected counts. Three of 18 paired final decisions flip; veto differences need not change an ineligible profile's final outcome.

Teacher prompts: Why is a denominator for the real employer missing? What if a model learns legacy rejection as its target? Which birth-date/age fields are necessary for operations versus restricted auditing? How should unsupported categories or missing inputs be handled without inventing a source rule?

Expected response: remove unjustified conditions, validate job-related accessible requirements, inspect remaining proxies, minimize personal data, and assign review/appeal ownership.

## C4: COMPAS, slides 44–52

Class core: source/filter flow, direct historical-score audit, denominator calculations, ordinal-score interpretation and ethical diagnosis. Optional worked self-study: fit the separate scikit-learn model, validation-fitted threshold experiment and probability-calibration demonstration.

Data flow: **7,214 raw →6,172 conventionally filtered →5,278 in the stated two-group comparison**. Positive decision means an **adverse high-risk flag** at historical decile score ≥5. The target is the recorded two-year outcome; it does not observe all conduct or remove justice-process measurement bias.

| Recorded group | TP | FP | FN | TN | n |
|---|---:|---:|---:|---:|---:|
| African-American | 1,188 | 641 | 473 | 873 | 3,175 |
| Caucasian | 414 | 282 | 408 | 999 | 2,103 |

FPR =641/1,514 =42.338% versus 282/1,281 =22.014%, a **20.324125 pp** signed gap. FNR =473/1,661 =28.477% versus 408/822 =49.635%. PPV =1,188/1,829 =64.954% versus 414/696 =59.483%. Check which people belong in each denominator.

At ordinal score 7, recorded positives are 209/343 (60.933%) and 68/113 (60.177%). The score does not automatically mean 70% probability. Similar values in one bin do not establish overall calibration. The notebook's later isotonic experiment calibrates a **different teaching model** on validation data and inspects reserved test records.

The separate logistic teaching experiment has a useful negative result: the held-out FPR gap increases from **9.8821 pp to 15.5103 pp** under the validation-fitted group threshold policy. Keep it. Ask why a validation objective may fail to generalize and what new evidence would support revision. Do not repeatedly tune on the test set. Group-specific thresholds are a methodological example requiring contextual ethical/legal assessment, not a deployment recommendation.

Zafar supplies disparate-mistreatment theory; Hardt supplies equal-opportunity/equalized-odds objectives; Chouldechova supplies calibration/base-rate tradeoffs. They share this dataset notebook. Students need not reproduce the original constrained optimizer to understand the audit, and must not claim the classroom model is COMPAS.

## Facilitating final projects

Each Part 2 has a question scaffold, TODO work packages, validation/uncertainty guidance, self-study links, a disabled extension function and submission rubric. A project must extend the worked baseline. Suitable additions include a new justified policy, an expanded controlled audit, measurement/coverage sensitivity or independently evaluated calibration. More plots alone are insufficient.

Require a protocol before results: decision/population, stakeholders, independent unit, target, primary criterion, reference, practical threshold, validation/resampling plan, proposed response and permissions. Preserve raw inputs. Report support/exclusions and any negative result. Explain which uncertainty comes from sampling versus arbitrary assumptions in a finite simulation.

Human labeling plans should state tasks, accessible instructions, disagreement, time, compensation and opt-out. AI-use statements should identify assistance and explain verification. In the oral defence, ask for one hand calculation, one unsupported claim the student avoided and one assumption whose change would alter the recommendation.

The rubric is 15% question/objective, 20% data/ethics, 25% implementation, 25% extension/uncertainty and 15% communication. The templates provide a reproducible report structure.
