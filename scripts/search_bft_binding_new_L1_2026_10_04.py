"""Finite diagnostic of rational s and the asymptotic BFT L(s).

This uses mpmath digamma and is not a universal G lower bound. No candidate
is a theorem-2.4 certificate until its explicit L1,m0 are proved.
"""
from math import gcd,log,sqrt
from fractions import Fraction
from pathlib import Path
import json,time
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1]
mp.mp.dps=25
SEEDS=[
dict(pair=[2,7],p=2,k0=3,a=1,q=7,l0=1,b=1,target=.274),
dict(pair=[3,11],p=3,k0=5,a=1,q=11,l0=2,b=2,target=.343),
dict(pair=[5,7],p=5,k0=2,a=2,q=7,l0=2,b=1,target=.264),
dict(pair=[7,13],p=7,k0=3,a=1,q=13,l0=2,b=2,target=.121)]
DENOMINATOR_CAP=59
NUMERATOR_CAP=60


def log_L(c,d):
    h=c+d
    inv=pow(d,-1,h)
    total=mp.mpf(0)
    for j in range(h//2+1,h):
        r=(j*inv)%h
        if j>=c:
            f=mp.mpf(1+(d*r)//h)/d
        else:
            f=mp.mpf(1+((c-d)*r)//h)/(c-d)
        total+=mp.digamma(f)-mp.digamma(mp.mpf(r)/h)
    return float(total/d)


def evaluate(row,c,d,logL):
    P=row["p"]**row["k0"];Q=row["q"]**row["l0"]
    a,b=row["a"],row["b"]
    D0=a*P-b*Q
    s=c/d;z=D0/(a*P)
    radical=sqrt(s*s*z*z+4-4*z)
    u1=2*(s-1)/(s*(2-z)+radical)
    u2=2/(s*z+2+radical)
    alpha=(s+1)*log(s+1)-(s-1)*log(s-1)
    lQ=alpha+(s-1)*log(u1)+log(1-u1)+log(1-u1+z*u1)
    lE=alpha+log(u2)+log(1-u2)+(s-1)*log(1-z*u2)
    lM1=log(min(P,Q));lM2=log(max(P,Q))
    lO3=(s-1)*log(P)+logL-log(a)-s*log(b)-lQ
    lO4=s*lM1+logL-(s-1)*log(a*P)-2*log(D0)-lE
    if lO3<=0 or lO4<=0:
        return None
    lam=lO4/(s*lM2+lO4)
    # Leave explicit epsilon=1/10000 for theorem-2.4.
    requested=row["target"]+.0001
    needed3=log(a)+s*log(b)+lQ-(s-1)*log(P)
    needed4=(requested/(1-requested))*s*lM2-s*lM1+(s-1)*log(a*P)+2*log(D0)+lE
    needed=max(needed3,needed4)
    return dict(pair=row["pair"],c=c,d=d,s=s,L_asymptotic=mp.exp(logL).__float__(),
                lambda_asymptotic=lam,Omega3_asymptotic=mp.exp(lO3).__float__(),
                target=row["target"],epsilon=.0001,
                required_L1_above=mp.exp(needed).__float__(),
                allowable_log_L1_loss=logL-needed,
                universal_G_bound_proved=False)


def main():
    results=[dict(seed=row,candidates=[]) for row in SEEDS]
    start=time.perf_counter()
    for c in range(2,NUMERATOR_CAP+1):
        for d in range(max(1,(c+2)//3),min(c,DENOMINATOR_CAP+1)):
            if gcd(c,d)!=1:
                continue
            value=log_L(c,d)
            for row,result in zip(SEEDS,results):
                info=evaluate(row,c,d,value)
                if info and info["allowable_log_L1_loss"]>0:
                    result["candidates"].append(info)
    for result in results:
        result["candidates"].sort(key=lambda r:(r["c"],-r["allowable_log_L1_loss"]))
        print(result["seed"]["pair"],"lowest-c candidates",result["candidates"][:5],flush=True)
    out=dict(diagnostic_only=True,new_L1_theorem_proved=False,
             numerator_cap=NUMERATOR_CAP,rows=results,
             elapsed_seconds=time.perf_counter()-start)
    (ROOT/"data/results/diagnostic_bft_binding_new_L1_2026_10_04.json").write_text(
        json.dumps(out,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    main()
