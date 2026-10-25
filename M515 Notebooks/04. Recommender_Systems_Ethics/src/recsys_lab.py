"""Small, transparent teaching recommenders. All row/column IDs are 0-based internally."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.optimize import minimize
from threadpoolctl import threadpool_limits

GENRES = ['unknown','Action','Adventure','Animation',"Children's",'Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']

def load_raw(root):
    root = Path(root)
    raw = root/'data/raw/movielens-100k'
    ratings = pd.read_csv(raw/'u.data', sep='\t', names=['user_id','item_id','rating','timestamp'])
    movies = pd.read_csv(raw/'u.item', sep='|', encoding='latin-1', names=['item_id','title','release_date','video_date','imdb_url']+GENRES)
    # The original user file is retained for provenance; personal attributes are not model features.
    return ratings, movies

def prepare(root):
    ratings,movies = load_raw(root)
    assert len(ratings)==100000 and ratings.user_id.nunique()==943 and movies.item_id.nunique()==1682
    assert not ratings.duplicated(['user_id','item_id']).any()
    assert ratings.rating.between(1,5).all()
    assert set(ratings.item_id).issubset(set(movies.item_id))
    # Global time order prevents another user's future events entering an earlier training period.
    ratings = ratings.sort_values(['timestamp','user_id','item_id'],kind='stable').reset_index(drop=True)
    ratings['time_utc'] = pd.to_datetime(ratings.timestamp,unit='s',utc=True).astype(str)
    splits = {'train':ratings.iloc[:80000].copy(),'validation':ratings.iloc[80000:90000].copy(),'test':ratings.iloc[90000:].copy()}
    assert splits['train'].timestamp.max() <= splits['validation'].timestamp.min()
    assert splits['validation'].timestamp.max() <= splits['test'].timestamp.min()
    out=Path(root)/'data/processed';out.mkdir(parents=True,exist_ok=True)
    for name,frame in splits.items():frame.to_csv(out/f'{name}.csv',index=False)
    movies.drop(columns=['imdb_url','video_date']).to_csv(out/'movies.csv',index=False)
    return ratings,movies,splits

def matrix(frame, n_users=943, n_items=1682):
    R = np.zeros((n_users,n_items),dtype=np.float64)
    R[frame.user_id.to_numpy()-1,frame.item_id.to_numpy()-1] = frame.rating.to_numpy()
    return R

class Popularity:
    """Rank by observed training rating count. Predict stars using a shrunk item mean."""
    def fit(self,frame):
        self.R=matrix(frame);self.mask=self.R!=0
        self.count=self.mask.sum(axis=0);self.mu=float(frame.rating.mean())
        means=(self.R.sum(axis=0)+20*self.mu)/(self.count+20)
        self.pred=np.tile(means,(943,1));self.rank_scores=np.tile(self.count.astype(float),(943,1))
        return self

class ItemKNN:
    """Co-rated adjusted cosine; positive neighbors; count shrinkage; per-target top k."""
    def __init__(self,k=40,min_common=3,shrink=20):
        self.k,self.min_common,self.shrink=k,min_common,shrink
    def fit(self,frame):
        self.R=matrix(frame);self.mask=self.R!=0
        M=self.mask.astype(float);self.mu=float(frame.rating.mean())
        counts=M.sum(axis=1)
        self.user_mean=np.divide(self.R.sum(axis=1),counts,out=np.full(943,self.mu),where=counts>0)
        D=np.where(self.mask,self.R-self.user_mean[:,None],0)
        with threadpool_limits(limits=1):
            common=M.T@M; num=D.T@D; A=(D*D).T@M
        den=np.sqrt(np.maximum(A*A.T,0))
        S=np.divide(num,den,out=np.zeros_like(num),where=den>0)
        S*=common/(common+self.shrink)
        S[(common<self.min_common)|(S<0)]=0;np.fill_diagonal(S,0)
        self.sim=S
        self.pred=np.empty_like(self.R)
        for u in range(943):
            rated=np.flatnonzero(self.mask[u])
            if len(rated)==0:self.pred[u]=self.mu;continue
            W=S[:,rated].copy()
            if len(rated)>self.k:
                keep=np.argpartition(W,-self.k,axis=1)[:,-self.k:]
                sparseW=np.zeros_like(W);np.put_along_axis(sparseW,keep,np.take_along_axis(W,keep,axis=1),axis=1);W=sparseW
            numerator=W@D[u,rated];denominator=W.sum(axis=1)
            adjustment=np.divide(numerator,denominator,out=np.zeros(1682),where=denominator>0)
            self.pred[u]=np.clip(self.user_mean[u]+adjustment,1,5)
        self.rank_scores=self.pred.copy()
        return self

class BiasedMF:
    """Fit only observed ratings, with regularized user/item biases and 12 latent factors."""
    def __init__(self,factors=12,reg=10,maxiter=1000,seed=7):
        self.factors,self.reg,self.maxiter,self.seed=factors,reg,maxiter,seed
    def fit(self,frame):
        self.R=matrix(frame);self.mask=self.R!=0;self.mu=float(frame.rating.mean())
        u=frame.user_id.to_numpy()-1;i=frame.item_id.to_numpy()-1;y=frame.rating.to_numpy(float)
        nu,ni,k=943,1682,self.factors;rng=np.random.default_rng(self.seed)
        cuts=[nu,nu+ni,nu+ni+nu*k]
        def unpack(x):return x[:cuts[0]],x[cuts[0]:cuts[1]],x[cuts[1]:cuts[2]].reshape(nu,k),x[cuts[2]:].reshape(ni,k)
        x0=np.concatenate([np.zeros(nu+ni),rng.normal(0,.05,nu*k+ni*k)])
        def loss_gradient(x):
            bu,bi,P,Q=unpack(x)
            e=self.mu+bu[u]+bi[i]+np.einsum('ij,ij->i',P[u],Q[i])-y
            loss=float(e@e+self.reg*(x@x))
            E=csr_matrix((e,(u,i)),shape=(nu,ni))
            gb=2*np.bincount(u,weights=e,minlength=nu)+2*self.reg*bu
            gi=2*np.bincount(i,weights=e,minlength=ni)+2*self.reg*bi
            gP=2*(E@Q)+2*self.reg*P;gQ=2*(E.T@P)+2*self.reg*Q
            return loss,np.concatenate([gb,gi,gP.ravel(),gQ.ravel()])
        with threadpool_limits(limits=1):
            opt=minimize(loss_gradient,x0,jac=True,method='L-BFGS-B',options={'maxiter':self.maxiter,'ftol':1e-6})
            self.bu,self.bi,self.P,self.Q=unpack(opt.x)
            self.pred=np.clip(self.mu+self.bu[:,None]+self.bi[None,:]+self.P@self.Q.T,1,5)
        self.optimization={'iterations':int(opt.nit),'success':bool(opt.success),'message':str(opt.message),'loss':float(opt.fun)}
        self.rank_scores=self.pred.copy()
        return self

def rank_all(model,k=10):
    """Candidates: observed training catalog minus that user's already-rated items."""
    scores=model.rank_scores.copy()
    catalog=model.mask.any(axis=0)
    scores[:,~catalog]=-np.inf;scores[model.mask]=-np.inf
    # Stable ID tie-break makes exact reruns reproducible.
    order=np.argsort(-scores,axis=1,kind='stable')[:,:k]
    return order

def evaluate(model,test,k=10,recommendations=None):
    pred=model.pred[test.user_id.to_numpy()-1,test.item_id.to_numpy()-1]
    residual=pred-test.rating.to_numpy()
    rec=rank_all(model,k) if recommendations is None else recommendations
    positives=test[test.rating>=4].groupby('user_id').item_id.apply(lambda a:set(a-1)).to_dict()
    rows=[];weights=1/np.log2(np.arange(2,k+2))
    for uid,truth in positives.items():
        hit=np.array([x in truth for x in rec[uid-1]],dtype=float)
        idcg=weights[:min(k,len(truth))].sum()
        rows.append({'user_id':uid,'positives':len(truth),'precision':hit.mean(),'recall':hit.sum()/len(truth),'ndcg':float(hit@weights/idcg),'history_count':int(model.mask[uid-1].sum())})
    per=pd.DataFrame(rows)
    summary={'RMSE':float(np.sqrt(np.mean(residual**2))),'MAE':float(np.mean(abs(residual))),'NDCG@10':float(per.ndcg.mean()),'Recall@10':float(per.recall.mean()),'Precision@10':float(per.precision.mean()),'evaluated_users':len(per),'test_users':int(test.user_id.nunique()),'cold_test_users':int(sum(~model.mask.any(axis=1)[test.user_id.unique()-1])),'cold_positive_events':int((~model.mask.any(axis=0)[test.loc[test.rating>=4,'item_id']-1]).sum())}
    return summary,per,rec

def audit(rec,model,movies,users=None):
    """Computed recommendation exposure is a simulation of position attention, not logged impressions."""
    rec=rec if users is None else rec[np.asarray(users)-1]
    catalog=model.mask.any(axis=0);count=model.mask.sum(axis=0)
    ordered=np.argsort(-count,kind='stable');head=set(ordered[:int(np.ceil(catalog.sum()*.2))])
    weights=1/np.log2(np.arange(2,rec.shape[1]+2));W=np.tile(weights,(len(rec),1))
    tail=np.array([[i not in head for i in row]for row in rec])
    G=movies.sort_values('item_id')[GENRES].to_numpy(float);norm=np.linalg.norm(G,axis=1);G=G/np.maximum(norm[:,None],1)
    diversity=[]
    for row in rec:
        sim=G[row]@G[row].T;a,b=np.triu_indices(len(row),1);diversity.append(float((1-sim[a,b]).mean()))
    novelty=-np.log2((count[rec]+1)/(count.sum()+len(count)))
    return {'catalog_coverage':float(len(np.unique(rec))/catalog.sum()),'long_tail_exposure_share':float((tail*W).sum()/W.sum()),'mean_genre_diversity':float(np.mean(diversity)),'mean_novelty_bits':float(novelty.mean())}

def mmr(model,movies,k=10,pool=50,lam=.75):
    """MMR uses min-max score normalization within each 50-candidate pool; genre cosine is [0,1]."""
    poolids=rank_all(model,pool)
    G=movies.sort_values('item_id')[GENRES].to_numpy(float);G/=np.maximum(np.linalg.norm(G,axis=1)[:,None],1)
    out=np.empty((943,k),dtype=int)
    for u,ids in enumerate(poolids):
        scores=model.rank_scores[u,ids];r=(scores-scores.min())/(np.ptp(scores)+1e-12)
        sim=G[ids]@G[ids].T;selected=[];remaining=list(range(len(ids)))
        for step in range(k):
            penalty=np.max(sim[:,selected],axis=1) if selected else np.zeros(len(ids))
            objective=lam*r-(1-lam)*penalty
            j=max(remaining,key=lambda j:objective[j]);selected.append(j);remaining.remove(j)
        out[u]=ids[selected]
    return out

def bootstrap_mean(values,seed=7,n=1000):
    a=np.asarray(values,float);rng=np.random.default_rng(seed)
    means=np.array([rng.choice(a,len(a),replace=True).mean()for _ in range(n)])
    return [float(a.mean()),*np.quantile(means,[.025,.975]).tolist()]

def feedback_simulation():
    """Controlled toy: equal appeal, 20 impressions/round, clicks = 0.5*exposure, pseudocount updates."""
    rows=[]
    for policy in ['exploit','explore_20pct']:
        counts=np.array([8.,2.])
        for t in range(5):
            share=counts/counts.sum()
            if policy=='explore_20pct':share=.8*share+.2*np.array([.5,.5])
            exposure=20*share;clicks=.5*exposure
            rows.append({'policy':policy,'round':t,'head_exposure':exposure[0],'tail_exposure':exposure[1],'head_clicks':clicks[0],'tail_clicks':clicks[1]})
            counts+=clicks
    return pd.DataFrame(rows)
