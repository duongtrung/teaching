# Data meanings and ethical boundaries
## Constructed source records
There are 40 synthetic records:20 `Women`,20 `Men`. No real applicants are represented and no real gender/car-ownership relationship is claimed. The categories simplify arithmetic and do not exhaust possible identities. The deterministic generator is `src/prepare_data.py`.

| Raw field | Meaning |
|---|---|
| `record_id` | Stable W01–W20 and M01–M20 IDs. One application per person. |
| `group` | Two constructed audit categories. |
| `role` | Analyst, the same role for everyone. |
| `skill_score` | Constructed score 70–100. All meet the stated cutoff 70. Its validity is an explicit scenario assumption. |
| `certificate` | Optional 0/1 context, with ten records per group at each value. |
| `experience_years` | Constructed experience; ten per group below 3 years, ten at 3+. |
| `has_car` | A constructed ownership fact. The assessment is online, so the scenario supplies no travel need. |
| `application_complete` | Always 1 in the raw cohort. Completeness is separate from a later car filter. |

Four cells of five people per group use certificate 0/1 and experience under 3/3+. Women have denial counts 4,3,3,2 across those cells; men 1,1,1,1. Car ownership is constructed as the complement of those denials. This makes all calculations countable and reproducible.

## Derived fields
- `meets_minimum`: score≥70. All 40 satisfy this stated criterion.
- `experience_band`: `Under3` or `3plus`, used for a small context search.
- `ready_for_work`: a copy of `has_car`. This feature name overstates what the measured fact establishes.
- `invited`: meets_minimum AND ready_for_work. The benefit is assessment access, not a job offer.
- `denied`:1−invited. Original adverse allocation outcome.
- `report_included`: ready_for_work. This deliberately misleading sample is described by the fictional analyst as all complete applications, even though the raw completeness field includes everyone.
- `exclusion_reason`: included or car filter. Retained for traceability.
- `invited_revised`, `denied_revised`: separate outputs using the stated skill criterion and 40 assessment seats. Original outcomes remain unchanged.

## Counts that should reconcile
| Population / rule | Women invited | Men invited | Total |
|---|---:|---:|---:|
| Original full cohort |8/20|16/20|24/40|
| Misleading selected report |8/8|16/16|24/24|
| Reviewed rule, full cohort |20/20|20/20|40/40|

The selected report omits 12 women and 4 men. Changing the reporting sample changes a description; changing the rule gives those 16 people access. Intent is stipulated in the scenario. In real data, this pattern can arise deliberately or accidentally, and counts alone cannot reveal motive.

## Uncertainty examples
The Wilson calculations use 12/20 and 4/20. They illustrate an independent-binomial sampling model for a stable wider process. This manually constructed cohort is not an empirical random sample, and its observed cohort rates are already known exactly.

The hypothetical 120/200 count illustrates sample-size effects, not an additional 200-person dataset. The 20-person fair-lottery table is a separate example, with 8/10 versus 2/10 denials. Its two-sided Fisher p≈.023014 is conditional on the observed margins. It is not a probability of discrimination or a probability that the null is true.

The independent-test curve uses all nulls true, independence and exact size.05 per test. The model does not establish those assumptions for the overlapping context rules or for discrete Fisher tests. The normal-test simulation is explicitly an ideal calibrated model.

## What remains ethically unresolved
A feature can be recorded accurately but lack a defensible relationship to the opportunity. A positive name does not validate a construct. A relevant skill measure still needs validity, accessibility and accommodation review. A justified population restriction needs a clear purpose and exclusion log. Group parity alone does not settle the entire hiring process, job offers or other groups. Keep the denominator, decision process, capacity assumptions and affected people visible.
