"""Generate the single fictional cohort used in both practical notebooks."""
from pathlib import Path
import json, hashlib
import pandas as pd

def prepare(root):
    root=Path(root);raw=root/'data/raw';out=root/'data/processed';raw.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
    rows=[]
    # Four cells of five people per group permit small, countable context searches.
    for group,counts,prefix in [('Women',[4,3,3,2],'W'),('Men',[1,1,1,1],'M')]:
        for cell,(cert,exp_band) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
            for j in range(5):
                denied=int(j<counts[cell]);idx=cell*5+j+1
                rows.append({'record_id':f'{prefix}{idx:02}','group':group,'role':'Analyst','skill_score':70+(idx*7)%31,'certificate':cert,'experience_years':(1+j%2) if exp_band==0 else 3+j%5,'has_car':1-denied,'application_complete':1})
    df=pd.DataFrame(rows);df.to_csv(raw/'applicants_40.csv',index=False)
    policy={'fictional':True,'benefit':'Invitation to an online Analyst assessment','minimum_skill':70,'assessment_seats':40,'working_mode':'online','raw_applications_complete':40,'original_rule':'invite if skill>=70 AND has_car==1','engineered_feature':'ready_for_work = has_car','misleading_reporting_rule':'include only ready_for_work==1, while describing the report as all complete applications','revised_rule':'invite if skill>=70, within the stated capacity of 40','group_note':'Two constructed categories for arithmetic, not a complete identity taxonomy.'}
    (raw/'policy_and_scenario.json').write_text(json.dumps(policy,indent=2))
    df['meets_minimum']=df.skill_score.ge(70).astype(int)
    df['experience_band']=df.experience_years.map(lambda x:'Under3' if x<3 else '3plus')
    df['ready_for_work']=df.has_car
    df['invited']=(df.meets_minimum.eq(1)&df.ready_for_work.eq(1)).astype(int)
    df['denied']=1-df.invited
    df['report_included']=df.ready_for_work
    df['exclusion_reason']=df.report_included.map({1:'included',0:'car filter'})
    df['invited_revised']=df.meets_minimum
    df['denied_revised']=1-df.invited_revised
    df.to_csv(out/'applicants_audit.csv',index=False)
    df.loc[df.report_included.eq(1)].to_csv(out/'misleading_selected_report.csv',index=False)
    df.loc[df.report_included.eq(0)].to_csv(out/'excluded_applicants.csv',index=False)
    definitions={'invited':'Benefit: access to an online assessment, not a job offer.','denied':'1 means assessment invitation denied.','meets_minimum':'Meets this fictional scenario\'s stated skill cutoff. Actual job validity is assumed for teaching.','ready_for_work':'Engineered from has_car. Its positive-sounding name does not establish validity.','report_included':'A misleading audit sample excludes carless people. Raw applications are all complete.','invited_revised':'Separate output from the reviewed rule; original decisions remain intact.','capacity':'40 assessment seats; all 40 meet the stated cutoff.'}
    (out/'variable_definitions.json').write_text(json.dumps(definitions,indent=2))
    return df
if __name__=='__main__':
    frame=prepare(Path(__file__).resolve().parents[1]);print('Prepared',len(frame),'fictional applicants.')
