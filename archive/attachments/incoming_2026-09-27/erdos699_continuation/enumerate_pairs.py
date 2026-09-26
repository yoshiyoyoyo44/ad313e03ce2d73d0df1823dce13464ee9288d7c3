"""Exhaust exact close pairs after the proven e,f<138 reduction.

Two independent enumeration formulations: sorted-list merging and CRT.
The values at most SMALL are harmless and are omitted from both enumerators.
"""
from math import gcd, isqrt
from pathlib import Path
import json, time
ROOT=Path(__file__).resolve().parent
P=[p for p in range(2,34) if all(p%d for d in range(2,isqrt(p)+1))]
A=1995; FIRST=933; EXP=138; DELTA=33; SMALL=2_000_000

def record(x,y,p,q,a,b,e,f):
    return dict(p=p,q=q,a=a,b=b,e=e,f=f,x=x,y=y,difference=abs(x-y))

def merge_scan():
    lists={p:sorted((a*p**e,a,e) for e in range(EXP) for a in range(1,A+1)
                    if a%p and a*p**e>SMALL-DELTA) for p in P}
    maximum=SMALL; witness=None; total=0
    for p in P:
        for q in P:
            if p>=q: continue
            ys=lists[q]; start=0
            for x,a,e in lists[p]:
                while start<len(ys) and ys[start][0]<x-DELTA: start+=1
                k=start
                while k<len(ys) and ys[k][0]<=x+DELTA:
                    y,b,f=ys[k]; k+=1
                    if min(a,b)>FIRST or max(x,y)<=SMALL: continue
                    total+=1
                    if max(x,y)>maximum:
                        maximum=max(x,y); witness=record(x,y,p,q,a,b,e,f)
        print('merge done',p,maximum,flush=True)
    return dict(maximum=maximum,witness=witness,pairs_above_small=total)

def ceildiv(a,b): return -((-a)//b)

def crt_scan():
    maximum=SMALL; witness=None; total=0; exponent_pairs=0
    for p in P:
        for q in P:
            if p>=q: continue
            for e in range(EXP):
                pe=p**e
                if A*pe+DELTA<=SMALL: continue
                for f in range(EXP):
                    qf=q**f
                    if pe>A*qf+DELTA or qf>A*pe+DELTA: continue
                    exponent_pairs+=1
                    inverse=pow(pe,-1,qf)
                    for delta in range(-DELTA,DELTA+1):
                        # x-y=delta, b=(a*p^e-delta)/q^f.
                        lower=max(1,ceildiv(qf+delta,pe),ceildiv(SMALL-DELTA+1,pe))
                        upper=min(A,(A*qf+delta)//pe)
                        a0=delta*inverse%qf
                        a=a0+ceildiv(lower-a0,qf)*qf
                        while a<=upper:
                            b=(a*pe-delta)//qf
                            x=a*pe; y=b*qf
                            if a%p and b%q and min(a,b)<=FIRST and max(x,y)>SMALL:
                                assert 1<=b<=A and x-y==delta
                                total+=1
                                if max(x,y)>maximum:
                                    maximum=max(x,y); witness=record(x,y,p,q,a,b,e,f)
                            a+=qf
        print('crt done',p,maximum,flush=True)
    return dict(maximum=maximum,witness=witness,pairs_above_small=total,exponent_pairs=exponent_pairs)

def main():
    if not __debug__: raise RuntimeError('Assertions are required.')
    start=time.time()
    one=merge_scan(); two=crt_scan()
    assert one['maximum']==two['maximum']==4_209_368_322
    assert one['pairs_above_small']==two['pairs_above_small']
    result=dict(status='EXHAUSTIVE-COMPUTATION',coefficient_max=A,first_max=FIRST,
                primes=P,exponents_less_than=EXP,difference=DELTA,small_omitted=SMALL,
                merge=one,crt=two,n_upper=one['maximum']+33)
    (ROOT/'pairs_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    print('seconds',time.time()-start,flush=True)

if __name__=='__main__': main()
