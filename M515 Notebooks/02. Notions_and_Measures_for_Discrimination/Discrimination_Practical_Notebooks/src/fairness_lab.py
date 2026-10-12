"""Small, readable audit helpers. Rates are fractions; gaps become percentage points ×100."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm

def root_dir(start=None):
    start=Path(start or Path.cwd()).resolve()
    for candidate in [start,*start.parents]:
        if (candidate/'data/DATA_MANIFEST.json').exists() and (candidate/'src/fairness_lab.py').exists():
            return candidate
    raise FileNotFoundError('Extract the complete ZIP before opening its notebooks.')

def load_table(dataset,name,root=None):
    """Read an included processed CSV/CSV.gz; never silently download or generate data."""
    path=(root or root_dir())/'data/processed'/dataset/name
    if not path.exists():
        raise FileNotFoundError(f'Missing {path}; run python scripts/process_data.py from package root.')
    return pd.read_csv(path)

def safe_ratio(n,d):
    return n/d if d else np.nan

def confusion_counts(y,decision,weights=None):
    y=np.asarray(y);decision=np.asarray(decision)
    if len(y)!=len(decision) or not np.isin(y,[0,1]).all() or not np.isin(decision,[0,1]).all():
        raise ValueError('y and decision must be same-length, complete binary arrays.')
    w=np.ones(len(y)) if weights is None else np.asarray(weights,dtype=float)
    if len(w)!=len(y) or not np.isfinite(w).all() or (w<0).any():
        raise ValueError('Weights must be finite, nonnegative and aligned.')
    return {name:float(w[(y==label)&(decision==pred)].sum())
        for name,label,pred in [('TP',1,1),('FP',0,1),('FN',1,0),('TN',0,0)]}

def rates(c):
    tp,fp,fn,tn=[c[k] for k in ['TP','FP','FN','TN']]
    n=tp+fp+fn+tn
    return dict(n=n,positives=tp+fn,negatives=fp+tn,selected=tp+fp,**c,
        prevalence=safe_ratio(tp+fn,n),selection_rate=safe_ratio(tp+fp,n),
        accuracy=safe_ratio(tp+tn,n),TPR=safe_ratio(tp,tp+fn),FNR=safe_ratio(fn,tp+fn),
        FPR=safe_ratio(fp,fp+tn),TNR=safe_ratio(tn,fp+tn),
        PPV=safe_ratio(tp,tp+fp),FDR=safe_ratio(fp,tp+fp),
        FOR=safe_ratio(fn,fn+tn),NPV=safe_ratio(tn,fn+tn))

def audit_table(df,group='group',y='y',decision='decision',min_n=None):
    """Full denominators remain visible. Undefined metrics are NaN, never zero."""
    rows=[]
    for label,part in df.groupby(group,dropna=False,observed=True):
        row=rates(confusion_counts(part[y],part[decision]))
        row['group']=label
        row['small_group']=bool(min_n is not None and len(part)<min_n)
        rows.append(row)
    return pd.DataFrame(rows).set_index('group')

def rate_gaps(table,metrics=('selection_rate','TPR','FPR','PPV')):
    """Max-minus-min is unsigned. A signed gap requires an explicitly named reference."""
    return pd.Series({m:(np.nan if len(table)<2 or table[m].isna().any()
        else 100*(table[m].max()-table[m].min())) for m in metrics},name='gap_pp')

def wilson_interval(k,n,alpha=.05):
    if n==0:return (np.nan,np.nan)
    if not (0<=k<=n):raise ValueError('Need 0≤k≤n.')
    z=norm.ppf(1-alpha/2);p=k/n;den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return center-half,center+half

def bootstrap_mean_interval(values,n_boot=1000,seed=42):
    values=np.asarray(values,dtype=float);values=values[np.isfinite(values)]
    if not len(values):return (np.nan,np.nan)
    rng=np.random.default_rng(seed)
    estimates=np.array([rng.choice(values,size=len(values),replace=True).mean() for _ in range(n_boot)])
    return tuple(np.quantile(estimates,[.025,.975]))

def paired_summary(df,first='female_score',second='male_score',threshold=8):
    valid=df[[first,second]].notna().all(axis=1)
    part=df.loc[valid]
    if part.empty:raise ValueError('No complete pairs.')
    diff=part[first]-part[second]
    d1=part[first].ge(threshold);d2=part[second].ge(threshold)
    return pd.Series({'total_rows':len(df),'complete_pairs':len(part),'incomplete_pairs':int((~valid).sum()),
        'mean_score_gap':diff.mean(),'median_score_gap':diff.median(),
        'selection_first':d1.mean(),'selection_second':d2.mean(),
        'selection_gap_pp':100*(d1.mean()-d2.mean()),'flip_rate':d1.ne(d2).mean()})

def matching_scores(data, use_proxy=False):
    """Planted teaching scorer on [1,10]. These outputs are never presented as LLM results."""
    legitimate = 1 + 2*data.skill_hits + 2*np.minimum(data.experience_years/3, 1)
    if not use_proxy:
        return np.clip(legitimate, 1, 10)
    # Arbitrary planted effects, unrelated to actual institution quality or identities.
    institution = data.institution_category.map({"Ivy League":.8,"HBCU":-.4,
        "Women’s college":-.4,"Other college":0.})
    cue = data.name_cue.map({"Name cue A":.2,"Name cue B":-.2})
    if institution.isna().any() or cue.isna().any():
        raise ValueError("An unsupported simulation cue needs an explicit policy.")
    return np.clip(legitimate+institution+cue, 1, 10)

def alleged_age_veto(data):
    """Reconstruct only the two categories described in the EEOC allegation."""
    allowed={"female","male"}
    if not set(data.sex_rule_category).issubset(allowed):
        raise ValueError("The source supplies no rule for other categories; do not invent one.")
    if data.age_years.isna().any():
        raise ValueError("Missing age requires a separately designed policy.")
    return ((data.sex_rule_category.eq("female") & data.age_years.ge(55)) |
            (data.sex_rule_category.eq("male") & data.age_years.ge(60)))
