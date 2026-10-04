"""Finite floating-point anchor search; candidates are not proof certificates."""
from math import gcd,log,sqrt
from pathlib import Path
import json,time

ROOT=Path(__file__).resolve().parents[1]
TABLE=[
(9,8,1.1742,25),(8,7,1.1951,28),(7,6,1.2219,53),
(6,5,1.2581,35),(5,4,1.3098,50),(9,7,1.3317,15),
(7,5,1.4135,74),(4,3,1.4170,153),(3,2,1.5395,138),
(8,5,1.5407,53),(5,3,1.5454,86),(3,1,1.5498,260),
(25,17,1.5540,582),(7,4,1.6219,60),(8,3,1.6560,149),
(9,5,1.6636,79),(5,2,1.7017,231),(7,3,1.7282,161),
(9,4,1.7666,87),(2,1,1.9377,150)]
PAIRS=[(2,17),(3,17),(5,17),(7,17),(11,17),(13,17),(7,11)]
PRE=[(c,d,c/d,log(L1),L1,m0,(c/d+1)*log(c/d+1)-(c/d-1)*log(c/d-1))
     for c,d,L1,m0 in TABLE]


def search(pair,max_exponent=12,max_coefficient=500):
    left,right=pair
    top=[]
    count=0
    for k in range(1,max_exponent+1):
        P=left**k
        for l in range(1,max_exponent+1):
            Q=right**l
            if P>max_coefficient*Q or Q>max_coefficient*P:
                continue
            start=max(1,(Q+P-1)//P-1)
            for a0 in range(start,max_coefficient+1):
                if a0%left==0:
                    continue
                nearest=(a0*P)//Q
                for b0 in (nearest,nearest+1):
                    if not 1<=b0<=max_coefficient or b0%right==0 or gcd(a0,b0)!=1:
                        continue
                    diff=a0*P-b0*Q
                    if not diff:
                        continue
                    if diff>0:
                        p,k0,a,q,l0,b=left,k,a0,right,l,b0
                        A,B=P,Q
                    else:
                        p,k0,a,q,l0,b=right,l,b0,left,k,a0
                        A,B=Q,P
                    D0=abs(diff)
                    z=D0/(a*A)
                    if z>=0.8:
                        continue
                    minlog=min(log(A),log(B));maxlog=max(log(A),log(B))
                    logA=log(A);loga=log(a);logb=log(b)
                    logvalue=log(a*A);logD=log(D0)
                    for c,d,s,logL,L1,m0,logalpha in PRE:
                        if s>=1/z:
                            continue
                        radical=sqrt(s*s*z*z+4-4*z)
                        u1=2*(s-1)/(s*(2-z)+radical)
                        u2=2/(s*z+2+radical)
                        logQ=logalpha+(s-1)*log(u1)+log(1-u1)+log(1-u1+z*u1)
                        logE=logalpha+log(u2)+log(1-u2)+(s-1)*log(1-z*u2)
                        logO3=(s-1)*logA+logL-loga-s*logb-logQ
                        logO4=s*minlog+logL-(s-1)*logvalue-2*logD-logE
                        if logO3<=0 or logO4<=0:
                            continue
                        count+=1
                        lam=logO4/(s*maxlog+logO4)
                        item=dict(pair=list(pair),p=p,k0=k0,a=a,q=q,l0=l0,b=b,
                            D0=D0,c=c,d=d,L1=L1,m0=m0,lambda3_diagnostic=lam,
                            logOmega3=logO3,logOmega4=logO4)
                        if len(top)<10 or lam>top[-1]["lambda3_diagnostic"]:
                            top.append(item)
                            top.sort(key=lambda r:r["lambda3_diagnostic"],reverse=True)
                            top=top[:10]
    return dict(pair=list(pair),valid_anchor_parameters=count,top=top)


def main():
    start=time.perf_counter();rows=[]
    for pair in PAIRS:
        result=search(pair)
        rows.append(result)
        path=ROOT/"data/results/diagnostic_bft_anchor_i19_2026_10_04.json"
        path.write_text(json.dumps(dict(finite_diagnostic_only=True,
            exact_interval_verified=False,max_exponent=12,max_coefficient=500,
            rows=rows),indent=2)+"\n",encoding="utf-8")
        print(pair,"best",result["top"][:1],"elapsed",time.perf_counter()-start,flush=True)


if __name__=="__main__":
    main()
