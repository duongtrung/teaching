# Teaching route and case mapping

## Session A — 150 minutes

| Minutes | Slides | Focus | Student action |
|---|---|---|---|
| 0–10 | 1–6 | Task, stakeholders, pipeline | Name one recommendation encountered today |
| 10–45 | 7–17 | Concrete data, missingness, content profiles | Compute a profile and two cosines |
| 45–75 | 18–25 | User and item collaborative filtering | Reproduce 4.497 and explain centering |
| 75–85 | — | Break | — |
| 85–110 | 26–35 | Factorization, implicit feedback, evaluation | Calculate RMSE and NDCG |
| 110–145 | 36–39 | Notebook 01 guided lab | Models, metrics, one inspected user |
| 145–150 | 40 | Checkpoint | Explain a mechanism without copying code |

## Session B — 150 minutes

| Minutes | Slides | Focus | Student action |
|---|---|---|---|
| 0–10 | 41–44 | Ethical evidence and audit procedure | Separate pattern, harm hypothesis and causal claim |
| 10–35 | 45–52 | Discovery, exposure and MMR | Compute position share and an MMR choice |
| 35–55 | 53–58 | Provider opportunity, fairness choices, user access | Defend a principle and its tradeoff |
| 55–65 | — | Break | — |
| 65–85 | 59–65 | Slices, privacy and feedback mechanism | Explain averages and synthetic linkage |
| 85–105 | 66–72 | Feedback simulation, agency, current policy | Propose evidence and an effective control |
| 105–145 | 73–78 | Notebook 02 guided lab and memo | Audit, intervene, recheck, decide |
| 145–150 | 79–80 | Transfer and exit | Apply the method to a different setting |

Slides 81–82 contain references; 83–84 are optional propensity-weighting extensions outside the timed core. The speaker notes contain prompts, model answers, caveats, timings and primary-source URLs. Equations and worked values appear directly on slides.

## Exact ethical-case match

| Case | Slides | Notebook 02 section | Data / evidence | What students produce |
|---|---|---|---|---|
| 1. Discovery and popularity | 45–52 | §§2–4 | Real MovieLens model outputs; assumed attention weights | Before/after discovery and quality table, uncertainty |
| 2. Provider opportunity | 53–57 | §5 | Complete synthetic provider CSV | Exposure calculation, graded NDCG cost, chosen principle |
| 3. User service quality | 58–61, 75 | §6 | Real history slices; separate four-user synthetic illustration | Slice table, uncertainty, diagnosis and proposed response |
| 4. Privacy and linkage | 62–64 | §7 | Historical Netflix research + fictional three-row CSV | Threat model, safe linkage calculation, protection plan |
| 5. Feedback | 65–68 | §8 | Fully specified expected-value simulation | Recurrence plot, sensitivity questions, causal limits |
| 6. Engagement and agency | 69–72 | §9 | Dated EU primary documents; no private platform dataset | Audit design and effective-control test |

## Facilitation and assessment

Ask students to predict a number before running a cell. Require each pair to explain one line of reasoning, not simply submit a notebook that runs. For the weak item-CF result, inspect overlap and the mismatch between star prediction and top-k ranking rather than changing the story. A finding that an expected disadvantage is not supported is an acceptable outcome.

The 400–600-word audit memo must name a stakeholder, lost benefit, mechanism, evidence, intervention, alternative, tradeoff and next recheck. Final-project Part 2 adds validation experiments, two alternatives, uncertainty and a reproducible report. The rubric is in both notebooks. LLM assistance should be disclosed; each student should orally explain one failed recommendation and solve a fresh arithmetic variation.
