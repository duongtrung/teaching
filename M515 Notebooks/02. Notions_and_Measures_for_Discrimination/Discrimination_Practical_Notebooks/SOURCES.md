# Primary sources and case mapping

## C1: original author analysis release

An, J., Huang, D., Lin, C. & Tai, M. (2025). Measuring gender and racial biases in large language models: Intersectional evidence from automated resume evaluation. *PNAS Nexus*, 4(3), pgaf089. https://doi.org/10.1093/pnasnexus/pgaf089

Author data/code: https://osf.io/4dahv/. The included five Stata tables, ReadMe and Code.do are the public analysis release. Their exact original URLs/versions and hashes are in the manifest. The notebook's pooled descriptive summaries and threshold rates are independently recomputed from this release.

## C2: original design, separate teaching simulation

Iso, H., Pezeshkpour, P., Bhutani, N. & Hruschka, E. (2025). Evaluating Bias in LLMs for Job-Resume Matching: Gender, Race, and Education. *NAACL Industry*, 672–683. https://aclanthology.org/2025.naacl-industry.55/

Original method/data-access statement: https://arxiv.org/html/2503.19182v1. The source describes proprietary Machamp pairs and unshared exact experiment records. Generated classroom data/scorer are separate original teaching material, not the paper's microdata, coefficients or LLM scores. Institution categories do not identify an individual's race or gender.

## C3: official enforcement case, separate rule reconstruction

EEOC (11 September 2023). iTutorGroup to Pay $365,000 to Settle EEOC Discriminatory Hiring Suit. https://www.eeoc.gov/newsroom/itutorgroup-pay-365000-settle-eeoc-discriminatory-hiring-suit

The source describes allegations resolved through settlement, an age/sex rejection mechanism and preventive relief. It does not provide an applicant-level dataset or establish an LLM mechanism. Case-fact summaries retain attribution. Boundary records, qualification labels and scaffold outcomes are explicitly fictional.

## C4: public benchmark and supporting methods

Original public research data/code: https://github.com/propublica/compas-analysis. The included CSV is pinned to a commit in the manifest. The classroom filters and threshold are documented; displayed counts are recomputed descriptive results for that cohort.

Zafar, M.B., Valera, I., Gomez Rodriguez, M. & Gummadi, K.P. (2017). Fairness Beyond Disparate Treatment & Disparate Impact: Learning Classification without Disparate Mistreatment. https://arxiv.org/abs/1610.08452

Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. https://arxiv.org/abs/1610.02413

Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. https://arxiv.org/abs/1703.00056

The notebook audits historical scores and fits a separate teaching classifier. It does not reproduce the vendor model or Zafar's constrained optimizer. Theory papers support this one case notebook, rather than adding independent cases or data families.

## Further reading and documentation

- Kusner et al. (2017), Counterfactual Fairness: https://arxiv.org/abs/1703.06856. C2 reading for the distinction between controlled cue edits and full causal counterfactual fairness.
- Fairlearn common metrics: https://fairlearn.org/main/user_guide/assessment/common_fairness_metrics.html
- scikit-learn LogisticRegression: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
- scikit-learn GroupShuffleSplit: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html
- scikit-learn isotonic calibration: https://scikit-learn.org/stable/modules/calibration.html
- AGG §3: https://www.gesetze-im-internet.de/agg/__3.html
- Official AI Act text: https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
- Current European Commission AI Act guidance: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

Research snapshots remain historical. Policy/technical documentation was checked for lesson preparation on 12 October 2026. The deck does not assert an operational compliance deadline or treat computational metrics as legal verdicts.
