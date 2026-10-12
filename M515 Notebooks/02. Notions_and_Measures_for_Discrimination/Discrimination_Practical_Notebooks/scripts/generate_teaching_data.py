"""Regenerate the disclosed synthetic examples. Does not download unavailable records."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
# Controlled matching simulation, independent of the proprietary Machamp data.
folder=ROOT/'data/raw/02_iso_matching';folder.mkdir(exist_ok=True)
jobs=[('data_analyst',['python','sql','statistics']),
      ('software_engineer',['python','git','testing']),
      ('project_coordinator',['planning','communication','reporting'])]
institutions=['Ivy League','HBCU',"Women’s college",'Other college']
rows=[]
for job_id,required in jobs:
    for overlap in [1,2,3]:
        for years in [1,5]:
            base=f'{job_id}_{overlap}_{years}'
            actual=required[:overlap]+['gardening']
            for institution in institutions:
                for cue in ['Name cue A','Name cue B']:
                    rows.append({'variant_id':f'V{len(rows)+1:03d}', 'base_pair_id':base,
                       'job_id':job_id,'required_skills':required,'required_years':3,
                       'resume_skills':actual,'experience_years':years,'institution_category':institution,
                       'name_cue':cue,'job_text':f'{job_id}: '+', '.join(required)+'; 3 years relevant experience.',
                       'resume_text':f'{cue}; skills '+', '.join(actual)+f'; {years} years relevant experience; {institution}.',
                       'reference_match':int(overlap==3 and years>=3),
                       'provenance':'generated teaching simulation; not Machamp or LLM output'})
(folder/'synthetic_matching.jsonl').write_text('\n'.join(json.dumps(r,ensure_ascii=False) for r in rows)+'\n')
(folder/'SOURCE_AND_SCOPE.json').write_text(json.dumps({
    'paper':'Iso et al. (2025), NAACL Industry','url':'https://aclanthology.org/2025.naacl-industry.55/',
    'original_dataset':'proprietary Machamp job–résumé pairs',
    'original_unit':'job–résumé pair, repeatedly evaluated under controlled cue changes',
    'reported_design':{'occupational_groups':40,'base_pairs':400,'variants_per_pair':80,'LLMs':12},
    'original_inputs':['job text','résumé text','manipulated names','manipulated educational institutions'],
    'original_output':'LLM match score from 1 to 10',
    'original_reference':'source matched/unmatched status; annotation validity remains an audit question',
    'availability':'Exact experiment records are not shared in the paper. No original microdata are included here.',
    'teaching_simulation':{'base_pairs':18,'variants':144,'reference_rule':'all 3 skills AND at least 3 years',
                           'scorer':'transparent arithmetic teaching scorer, not an LLM'}},indent=2,ensure_ascii=False)+'\n')

# Boundary grid reconstructed from the alleged rule in the EEOC case summary.
folder=ROOT/'data/raw/03_itutorgroup';folder.mkdir(exist_ok=True)
ages=[30,40,54,55,56,59,60,61,70]
rows=[]
for age in ages:
    for sex in ['female','male']:
        for meets in [False,True]:
            rows.append({'applicant_id':f'T{len(rows)+1:03d}','age_years':age,'sex_rule_category':sex,
                'work_sample':80 if meets else 50,'teaching_eligible':int(meets),
                'provenance':'generated boundary grid; not actual iTutorGroup applicants'})
import pandas as pd
pd.DataFrame(rows).to_csv(folder/'synthetic_applicants.csv',index=False)
(folder/'CASE_FACTS.json').write_text(json.dumps({
    'source_url':'https://www.eeoc.gov/newsroom/itutorgroup-pay-365000-settle-eeoc-discriminatory-hiring-suit',
    'source_date':'2023-09-11','source_kind':'EEOC settlement press release; no applicant-level dataset supplied',
    'reported_allegation':{'female_min_rejection_age':55,'male_min_rejection_age':60,
                           'affected_qualified_applicants':'more than 200'},
    'settlement_usd':365000,
    'known_mechanism_inputs':['age','sex category'],
    'known_mechanism_output':'automatic application rejection',
    'unknown':['complete applicant features','all applicant outcomes','job-performance labels','sampling frame'],
    'teaching_grid':'36 fictional rows: 9 ages × 2 rule categories × 2 invented eligibility states',
    'teaching_eligibility':'invented work-sample score ≥70; not the real employer’s rubric',
    'scope':'Reconstruct the reported veto. Do not infer actual selection rates or an LLM model from this grid.'
},indent=2)+'\n')

print('Regenerated C2 and C3 teaching grids. Run scripts/process_data.py next.')
