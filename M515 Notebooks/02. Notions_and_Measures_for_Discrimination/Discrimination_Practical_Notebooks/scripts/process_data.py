"""Rebuild teaching tables from bundled raw files. No network or API keys required."""
from pathlib import Path
import json, hashlib, warnings
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
OUT = ROOT / 'data/processed'
outputs = []

def save(df, dataset, name, description, transformations):
    folder = OUT / dataset
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    compression = {'method':'gzip','mtime':0} if name.endswith('.gz') else None
    df.to_csv(path, index=False, compression=compression, float_format='%.12g')
    outputs.append({'path':str(path.relative_to(ROOT)), 'rows':len(df), 'columns':df.columns.tolist(),
        'dtypes':{k:str(v) for k,v in df.dtypes.items()},
        'missing_values':{k:int(v) for k,v in df.isna().sum().items()},
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'description':description,
        'transformations':transformations})

def process_an():
    folder = OUT / '01_an_resume'
    folder.mkdir(parents=True, exist_ok=True)
    dictionaries = {}
    for path in sorted((RAW / '01_an_resume').glob('*.dta')):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            with pd.io.stata.StataReader(path, convert_categoricals=False) as reader:
                df = reader.read()
                labels = reader.value_labels()
                dictionaries[path.name] = {'variable_labels':reader.variable_labels(),
                    'value_labels':{k:{str(int(key)):str(value) for key,value in labels[k].items()}
                        for k in ['igender','iethnicity','iposition','istate','highest_degree'] if k in labels},
                    'warnings':sorted({str(w.message).strip() for w in caught})}
        df.insert(0,'record_id',np.arange(len(df)))
        # Preserve original coded variables. Decode only documented audit categories.
        for source, target in [('igender','gender_cue'),('iethnicity','race_cue'),
                               ('iposition','occupation'),('istate','state'),('highest_degree','degree')]:
            if source in df and source in labels:
                df[target] = df[source].map(labels[source])
        if {'gender_cue','race_cue'}.issubset(df):
            df['audit_group'] = df.race_cue.astype(str) + ' / ' + df.gender_cue.astype(str)
        save(df,'01_an_resume',path.stem+'.csv.gz',
             'Author-released Stata table converted to compressed CSV; fictitious randomized resumes or author summary results.',
             ['Read with convert_categoricals=False to preserve original category codes.',
              'Decode group/occupation/state/degree labels using the embedded Stata mappings.',
              'Add a table-local record_id; it does not establish cross-file identity.',
              'Retain all rows and missing values; dates are serialized as ISO strings.'])
    (folder/'stata_dictionary.json').write_text(json.dumps(dictionaries,indent=2)+'\n')

def process_compas():
    df = pd.read_csv(RAW/'04_compas/compas-scores-two-years.csv')
    flow=[{'step':'raw','n':len(df)}]
    tests = [('known screening-arrest interval',df.days_b_screening_arrest.notna()),
             ('screening within plus/minus 30 days',df.days_b_screening_arrest.between(-30,30)),
             ('known is_recid flag',df.is_recid.ne(-1)),
             ('exclude ordinary traffic charges',df.c_charge_degree.ne('O')),
             ('known COMPAS score text',df.score_text.notna() & df.score_text.ne('NA'))]
    mask=pd.Series(True,index=df.index)
    for name,test in tests:
        mask &= test
        flow.append({'step':name,'n':int(mask.sum())})
    columns=['id','race','sex','age','age_cat','priors_count','c_charge_degree','decile_score','two_year_recid']
    clean=df.loc[mask,columns].rename(columns={'id':'record_id','two_year_recid':'y'})
    assert clean.record_id.is_unique
    assert clean.y.isin([0,1]).all() and clean.decile_score.between(1,10).all()
    save(clean,'04_compas','all_groups.csv.gz','Standard filtered COMPAS research cohort; positive outcome means observed two-year recidivism label.',
         [x[0] for x in tests]+['Drop names, dates of birth, case identifiers, detailed charges, and post-outcome fields.',
         'Retain all race categories; no race binarization in this table.'])
    bw=clean.loc[clean.race.isin(['African-American','Caucasian'])].copy()
    flow.append({'step':'Black/White comparative cohort','n':len(bw)})
    save(bw,'04_compas','black_white.csv.gz','Two-group research comparison used for paper-focused guided calculations.',
         ['Start with all_groups.csv.gz; restrict race to African-American or Caucasian.',
          'This exclusion is an explicit scope choice, not an assertion that other groups do not matter.'])
    save(pd.DataFrame(flow),'04_compas','filter_flow.csv','Sequential cohort selection counts.',['Count surviving rows after each filter.'])

def process_iso():
    records=[json.loads(line) for line in (RAW/'02_iso_matching/synthetic_matching.jsonl').read_text().splitlines()]
    df=pd.DataFrame(records)
    df['skill_hits']=[len(set(a)&set(b)) for a,b in zip(df.required_skills,df.resume_skills)]
    df['required_skills']=df.required_skills.map(lambda x:';'.join(x))
    df['resume_skills']=df.resume_skills.map(lambda x:';'.join(x))
    df['y']=df.reference_match
    assert df.variant_id.is_unique and df.base_pair_id.nunique()==18 and len(df)==144
    assert (df.y==((df.skill_hits==3)&(df.experience_years>=3)).astype(int)).all()
    save(df,'02_iso_matching','matching_variants.csv','144 controlled synthetic variants, not original Machamp data.',
         ['Parse nested JSONL records.','Count exact overlap of synthetic skill tokens.',
          'Serialize skill lists with semicolons for CSV.','Keep base_pair_id across all 8 variants.',
          'Copy the explicitly constructed reference_match to y. No model scores are stored in raw data.'])

def process_itutor():
    df=pd.read_csv(RAW/'03_itutorgroup/synthetic_applicants.csv')
    df['y']=df.teaching_eligible
    df['age_band']=pd.cut(df.age_years,[0,54,59,120],labels=['under 55','55–59','60 and over'])
    assert len(df)==36 and df.applicant_id.is_unique
    assert (df.y==df.work_sample.ge(70).astype(int)).all()
    save(df,'03_itutorgroup','applicant_grid.csv','36 fictional boundary tests of the alleged age/sex veto.',
         ['Read generated applicant CSV without treating it as real applicant records.',
          'Copy invented teaching eligibility into y.','Derive age bands at reported rule boundaries.',
          'Keep sex_rule_category as a reported-rule category, not a comprehensive gender ontology.'])

if __name__=='__main__':
    process_an(); process_iso(); process_itutor(); process_compas()
    report={'outputs':outputs,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'notes':'Raw data stay unchanged. Simulation outcomes remain explicitly labelled.'}
    (OUT/'PROCESSING_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'Rebuilt {len(outputs)} processed tables offline.')
