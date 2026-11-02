"""Transparent counts and uncertainty for the two linked hiring practicals."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm, fisher_exact

def project_root(start=None):
    here=Path(start or Path.cwd()).resolve()
    for p in [here,*here.parents]:
        if (p/'src/audit.py').is_file():return p
    raise FileNotFoundError('Keep the extracted pack structure and open a notebook inside it.')

def wilson(x,n,level=.95):
    """Two-sided Wilson score interval for independent Bernoulli observations."""
    if not (0<=x<=n and n>0 and 0<level<1):raise ValueError('Require 0<=x<=n, n>0, 0<level<1.')
    phat=x/n;z=norm.ppf((1+level)/2);den=1+z*z/n
    center=(phat+z*z/(2*n))/den
    half=z*np.sqrt(phat*(1-phat)/n+z*z/(4*n*n))/den
    return {'level':level,'x':int(x),'n':int(n),'phat':phat,'z':float(z),'denominator':float(den),'center':float(center),'half_width':float(half),'lower':float(center-half),'upper':float(center+half)}

def report(frame,outcome='denied'):
    """Each reported rate uses its displayed count and denominator."""
    rows=[]
    for group in ['Women','Men']:
        a=frame.loc[frame.group.eq(group)]
        n=len(a);x=int(a[outcome].sum())
        rows.append({'group':group,'events':x,'total':n,'rate':x/n if n else np.nan})
    return pd.DataFrame(rows)

def rule_metrics(frame,context=None):
    """Audited group=Women, comparator=Men, adverse outcome=denied."""
    context=context or {};part=frame
    for k,v in context.items():part=part.loc[part[k].eq(v)]
    a=part.loc[part.group.eq('Women')];b=part.loc[part.group.eq('Men')]
    na,nb=len(a),len(b);xa,xb=int(a.denied.sum()),int(b.denied.sum())
    qa=xa/na if na else np.nan;qb=xb/nb if nb else np.nan;base=(xa+xb)/(na+nb) if na+nb else np.nan
    return {'context':context,'women_denied':xa,'women_n':na,'men_denied':xb,'men_n':nb,'women_rate':qa,'men_rate':qb,'context_rate':base,'support':xa/len(frame),'confidence':qa,'extended_lift':qa/base if base>0 else np.nan,'gap':qa-qb,'risk_ratio':qa/qb if qb>0 else np.nan,'favorable_ratio':(1-qa)/(1-qb) if qb<1 else np.nan}

def search_contexts(frame,min_per_group=5,review_ratio=1.25):
    """Five declared contexts: all, two certificate values, two experience bands."""
    contexts=[{}, {'certificate':0},{'certificate':1},{'experience_band':'Under3'},{'experience_band':'3plus'}]
    rows=[]
    for c in contexts:
        r=rule_metrics(frame,c)
        if min(r['women_n'],r['men_n'])>=min_per_group:
            rows.append({'context_name':' & '.join(f'{k}={v}' for k,v in c.items()) or 'All applicants',**r,'review_flag':bool(r['extended_lift']>=review_ratio)})
    return pd.DataFrame(rows)

def family_false_alarm(m,alpha=.05):
    """Exact under independent tests, all nulls true, actual size=alpha each."""
    return 1-(1-alpha)**np.asarray(m)

def lottery_pvalue():
    """A possible fair-lottery result: 8/10 vs 2/10 denials; two-sided Fisher."""
    return float(fisher_exact([[8,2],[2,8]],alternative='two-sided').pvalue)
