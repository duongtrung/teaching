# Teaching guide:150 minutes
## Route
| Minutes | Material | Teaching focus |
|---|---|---|
|0–10|Slides 1–8|One story, a defined opportunity, all 40 applicants and two linked practicals.|
|10–35|Slides 9–20|Counts, support/confidence, extended lift, a five-context search.|
|35–50|Lab 1, Notebook 01|Run count/metric/search cells. Each pair explains one denominator.|
|50–75|Slides 21–29|Wilson meaning, normal percentile, full calculation, coverage and size.|
|75–85|Break|Pause after the interval examples.|
|85–110|Slides 30–38|Fair lottery, a true null, level, two/twenty tests, dependencies and Bonferroni.|
|110–130|Slides 39–50|Car feature, selected sample, excluded people and actual access remedy.|
|130–145|Lab 2, Notebook 02|Trace IDs, compare reports and rerun the separate reviewed policy.|
|145–150|Slides 51–59|Brief exit check and project choice. Reading/rubric slides are take-home reference.|

Slide 60 is an optional derivation of the lottery p-value. It is not required to understand the false-alarm formula. Install packages and distribute the extracted pack before class. Use saved outputs if setup blocks a student. Students should not type every helper function live.

## Scenario clarity
All three opening questions concern the same 40 applicants. Practical 1 counts the decisions and finds a small contextual pattern. Practical 2 investigates the car feature and the selected report, then changes one explicit rule. The fair-lottery and hypothetical 120/200 examples are separately labeled statistical illustrations.

The opportunity is an invitation to an online skills assessment. There are 40 seats and all 40 meet the stated score cutoff. Inviting everyone after removing the car barrier is therefore feasible here. It does not imply everyone receives a job offer, nor that an unlimited-capacity remedy works in every hiring setting.

## Hand calculations and expected answers
- Women:12/20=.60 denied. Men:4/20=.20. Context:16/40=.40.
- Support 12/40=.30. Confidence 12/20=.60. Lift.60/.40=1.50. Comparator risk ratio.60/.20=3. Gap.40. Favorable invitation ratio.40/.80=.50.
- Certificate 0:7/10 women and 2/10 men denied. Context 9/20=.45. Lift.70/.45≈1.556. Gap.50. Support 7/40=.175.
- There are five declared contexts, all reported. Contexts share records; their tests are not independent.

## Wilson: how to explain it
First distinguish the known rate in this exact cohort from an unknown wider-process rate. The constructed records illustrate a binomial model; they do not validate population inference. A real application needs independent comparable observations, a suitable sampling design and a stable probability.

For 95% two-sided confidence, α=.05. Each normal-reference tail has.025 area. The upper cumulative probability is.975, so z=Φ⁻¹(.975)≈1.959964. **A percentile locates a value in a distribution. A percentage describes a fraction.** It is not the 97.5th percentile of applicant outcomes.

With x=12,n=20,p̂=.60, D=1+z²/n≈1.192073. The adjusted center is.583887 and half-width.197306. Bounds [.386582,.781193]. For men 4/20, bounds [.080658,.416017]. Code uses the full z, while slide arithmetic rounds.

Interpretation: the nominal 95% procedure targets about 95% coverage over repeated suitable samples. The fixed true parameter is not assigned a 95% probability by this frequentist calculation. Actual Wilson coverage varies with n and p because outcomes are discrete. This interval is not a range covering 95% of applicants, not a per-person prediction interval and not proof of discrimination. Overlap of two separate rate intervals does not directly test their difference.

At 90%,95%,99%, upper normal percentiles are 95th,97.5th,99.5th; z values 1.645,1.960,2.576. Corresponding 12/20 bounds [.419,.758], [.387,.781], [.329,.821]. With hypothetical 120/200, the 95% bounds are [.531,.665]. Higher confidence widens bounds; more independent relevant data narrows them. Neither repairs biased selection.

## Independent true-null tests: how to explain it
The separate lottery really ignores group membership, so H₀ of equal group probabilities is true by construction. It can still produce an unusual sample. The 8/10 versus 2/10 denial table has two-sided Fisher p=.023014. A predeclared.05 test flags this rare example even though the generating process is fair. A p-value does not give P(H₀ true) or P(discrimination).

A valid level-.05 test has false-alarm probability at most.05 under its null. Discrete tests can be conservative. For the simple repeated-test calculation, explicitly assume exact.05 size, independence and all nulls true. One test avoids a false alarm with probability.95. Two avoid both with.95×.95=.9025, so at least one false alarm has probability.0975. Twenty give 1−.95²⁰=.641514. The result is a family event probability, not the probability that a particular finding is false.

Do not apply that exact formula to overlapping subgroups or a Fisher pipeline without establishing actual sizes and independence. Bonferroni uses.05/m per test, or adjusted p=min(1,m×p), and controls family false alarms with valid tests despite dependence. It can be conservative. Keep the whole declared family, including inconvenient results.

Optional slide 60: with 10 total denials among 20 people, all C(20,10)=184756 assignments are equally likely under the conditional null. Counts 0/10,1/9 and 2/8 women denied contribute 2,200 and 4050 assignments. Their sum 4252 gives p=4252/184756≈.023014. This matches the symmetric two-sided Fisher example. No combinatorics derivation is required during the main route.

## Lab instructions
**Lab 1,15 minutes:** run the dataset inspection, metrics and five-context search cells. Each pair submits one supported rule with its counts and comparison definition. As a follow-up during the statistics discussion, run the z/Wilson and family-risk cells. The long Monte Carlo and project sections are self-study if time is short.

**Lab 2,15 minutes:** run the feature/policy derivation; print complete versus selected invitation rates; print the 16 excluded IDs; rerun the reviewed skill-only rule; write a short claim/action paragraph. Students must explain why 8/8 and 16/16 do not establish fair access among the original 40.

## Feature and selection ethics
In this fictional story, the analyst knowingly calls only car owners “complete” despite all raw applications being complete. Bad intent is provided, not inferred from numbers. A real bias could come from accidental ETL errors or deliberate manipulation; look for code, definitions, policies and exclusion logs.

Car ownership is a factual field. “Work readiness” is a claimed construct. Accurate recording does not make the construct valid for an online opportunity. Removing the group field leaves the car rule intact. The remedy changes actual access from 24 to 40, granting it to 12 women and 4 men while retaining original outcomes. It establishes one improvement in this specified process, with assumed skill validity and 40 seats.

Ask what happens if there are 12 seats: a different allocation process is needed. This is a project extension, not an instruction to invite everyone under an unstated capacity constraint. Ask how a skill test itself might introduce barriers, how appeals/accommodations work and how the reviewed process should be monitored on new cohorts.

## Project assessment
Two paths: counts/uncertainty or feature/selection. Both notebooks contain a complete lesson and guided TODOs. Require a substantive extension, data meanings, a declared comparison, sensitivity or suitable independent evidence, a process-based ethical argument and reproducible artifacts. Rubric: provenance 15%, method 25%, validation/sensitivity 25%, ethics 20%, reproducibility 15%. In an oral check, recompute one rate and trace one excluded record.
