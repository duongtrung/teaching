"""Validate case/data mapping, raw integrity, engineering support and worked calculations."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
import pandas as pd
import nbformat
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from fairness_lab import load_table,rates,rate_gaps,audit_table,matching_scores,alleged_age_veto
checks=[]
def check(name,condition):
    if not condition:raise AssertionError(name)
    checks.append(name)

manifest=json.loads((ROOT/'data/DATA_MANIFEST.json').read_text())
for item in manifest['raw_assets']+manifest['generated_assets']:
    path=ROOT/item['path']
    check('raw hash: '+item['path'],hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'])
report=json.loads((ROOT/'data/processed/PROCESSING_REPORT.json').read_text())
for item in report['outputs']:
    path=ROOT/item['path'];df=pd.read_csv(path)
    check('processed hash: '+item['path'],hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'])
    check('processed support/schema: '+item['path'],len(df)==item['rows'] and list(df)==item['columns'])
check('exactly ten processed tables',len(report['outputs'])==10)

expected={m['notebook'] for m in manifest['case_mapping']}
actual={p.name for p in (ROOT/'notebooks').glob('*.ipynb')}
check('exactly four matched notebooks',expected==actual and len(actual)==4)
for entry in manifest['case_mapping']:
    nb=nbformat.read(ROOT/'notebooks'/entry['notebook'],as_version=4);nbformat.validate(nb)
    text='\n'.join(c.source for c in nb.cells)
    check(entry['case_id']+' notebook case identifier',nb.metadata.get('case_id')==entry['case_id'])
    check(entry['case_id']+' two-part structure','## Part 1' in text and '## Part 2' in text)
    check(entry['case_id']+' project TODO scaffold','TODO' in text and 'RUN_STUDENT_PROJECT=False' in text.replace(' = ','='))
    check(entry['case_id']+' guided code execution',all(c.execution_count is not None for c in nb.cells if c.cell_type=='code'))
    check(entry['case_id']+' no recorded code errors',not any(o.output_type=='error' for c in nb.cells for o in c.get('outputs',[])))
    check(entry['case_id']+' inline figures',any('image/png' in o.get('data',{}) for c in nb.cells for o in c.get('outputs',[])))

# C1 valid-response denominators, not headline population or source estimate rows.
an=load_table('01_an_resume','data_gpt35_baseline.csv.gz',root=ROOT)
check('C1 baseline support',len(an)==332895 and an.score_gpt35.isna().sum()==1)
valid=an.dropna(subset=['score_gpt35']).assign(selected=lambda d:d.score_gpt35.ge(80))
s=valid.groupby('audit_group').selected.agg(n='size',selected='sum',rate='mean')
check('C1 hand fractions',s.loc['black / male','selected']==27470 and s.loc['black / male','n']==83381 and
      s.loc['white / male','selected']==28555 and s.loc['white / male','n']==83181)
check('C1 signed gap',np.isclose(100*(s.loc['black / male','rate']-s.loc['white / male','rate']),-1.383599,atol=1e-6))
check('C1 no manufactured qualification y','y' not in an)

# C2 independent units and planted effect, with no claim to observed LLM scores.
iso=load_table('02_iso_matching','matching_variants.csv',root=ROOT)
check('C2 repeated support',len(iso)==144 and iso.base_pair_id.nunique()==18 and iso.groupby('base_pair_id').size().eq(8).all())
check('C2 no raw model outputs','score_proxy' not in iso and 'score_rubric' not in iso)
score=matching_scores(iso,True)
example=iso[(iso.job_id=='data_analyst')&(iso.skill_hits==3)&(iso.experience_years==1)]
check('C2 7.667 rubric arithmetic',np.allclose(matching_scores(example,False),23/3))
check('C2 8.467 proxy arithmetic',np.isclose(matching_scores(example[example.institution_category=='Ivy League'],True).mean(),23/3+.8))

# C3 direct boundary condition and known fictional qualification scope.
it=load_table('03_itutorgroup','applicant_grid.csv',root=ROOT)
veto=alleged_age_veto(it);legacy=it.y.eq(1)&~veto
check('C3 grid support',len(it)==36 and it.applicant_id.is_unique)
check('C3 source boundaries',not veto[(it.age_years==54)&it.sex_rule_category.eq('female')].any() and
      veto[(it.age_years==55)&it.sex_rule_category.eq('female')].all() and
      not veto[(it.age_years==59)&it.sex_rule_category.eq('male')].any() and
      veto[(it.age_years==60)&it.sex_rule_category.eq('male')].all())
check('C3 recovered fictional profiles',int((it.y.eq(1)&~legacy).sum())==9)

# C4 historical score counts, target direction and privacy minimization.
compas=load_table('04_compas','black_white.csv.gz',root=ROOT)
check('C4 filtered cohort',len(compas)==5278)
check('C4 minimized display fields',not {'name','dob','first','last','r_offense_date'}.intersection(compas))
table=audit_table(compas.assign(decision=compas.decile_score.ge(5).astype(int)),group='race')
check('C4 confusion counts',np.allclose(table.loc['African-American',['TP','FP','FN','TN']],[1188,641,473,873]) and
      np.allclose(table.loc['Caucasian',['TP','FP','FN','TN']],[414,282,408,999]))
check('C4 FPR denominators',np.isclose(table.loc['African-American','FPR'],641/1514) and
      np.isclose(table.loc['Caucasian','FPR'],282/1281))
check('undefined rates stay undefined',np.isnan(rates({'TP':0,'FP':0,'FN':0,'TN':3})['TPR']))
check('undefined gap stays undefined',np.isnan(rate_gaps(pd.DataFrame({'FPR':[.2,np.nan]}),metrics=['FPR'])['FPR']))
check('single-group gap stays undefined',np.isnan(rate_gaps(pd.DataFrame({'FPR':[.2]}),metrics=['FPR'])['FPR']))

execution=json.loads((ROOT/'reports/EXECUTION_REPORT.json').read_text())
check('four guided execution results',len(execution['notebooks'])==4 and all(x['status']=='passed' for x in execution['notebooks']))
result={'status':'passed','checks':checks,'check_count':len(checks),
        'claim_boundary':'Input integrity, cohort/schema, notebook-source execution metadata and stated numerical checks. No population or legal conclusion.'}
(ROOT/'reports/VALIDATION_REPORT.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'Passed {len(checks)} data, notebook and arithmetic checks.')
