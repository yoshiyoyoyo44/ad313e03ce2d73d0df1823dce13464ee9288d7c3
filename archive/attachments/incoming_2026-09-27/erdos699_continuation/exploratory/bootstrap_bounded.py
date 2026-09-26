"""Exact moving-coefficient two-prime bootstrap on a bounded n interval.

No linear-forms theorem is used here: the initial cap bounds the exponents.
For each step, all close pairs above A^2+h are exhausted via modular inversion.
Below that height a trivial bound suffices. This is NOT an infinite-tail proof.
"""
from math import isqrt, factorial
from fractions import Fraction as F
from pathlib import Path
import json, argparse, time
ROOT=Path(__file__).resolve().parent
LOW=2_000_000

def primes(i):
    return [p for p in range(2,i) if all(p%d for d in range(2,isqrt(p)+1))]

def floorroot(n,k):
    lo=0;hi=1<<((n.bit_length()+k-1)//k)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**k<=n:lo=mid
        else:hi=mid
    assert lo**k<=n<(lo+1)**k
    return lo

def bounds(i,N):
    ps=primes(i);m=len(ps);h=i-1;b=(2*h+2)//3;d=3*b-h;S=b*(b+1)//2
    defect=3*S-d*(i-m)
    assert defect>0
    correction=1 if len(primes(i+1))>m else i
    C=F(factorial(i),correction)**d*F(LOW,LOW-h)**(i*d)*N**defect/4**S
    return [floorroot(C.numerator//C.denominator,d*(m-k+1)) for k in (1,2)]

def contract(i,N):
    first,A=bounds(i,N);h=i-1;T=A*A+h
    if T+h>=N: return dict(i=i,input_cap=N,first=first,A=A,trivial_value_cap=T,output_cap=N,stopped=True)
    powers={}
    for p in primes(i):
        v=p;e=1; seq=[]
        while v<=N:
            if v>A: seq.append((v,e))
            v*=p;e+=1
        powers[p]=seq
    maximum=T;witness=None;pairs=0;exponent_pairs=0
    for p in powers:
        for q in powers:
            if p>=q:continue
            for pe,e in powers[p]:
                for qf,f in powers[q]:
                    if pe>A*qf+h or qf>A*pe+h: continue
                    exponent_pairs+=1
                    inverse=pow(pe,-1,qf)
                    a=(-h*inverse)%qf
                    for delta in range(-h,h+1):
                        # q^f>A ensures at most one a in [1,A].
                        if 1<=a<=A:
                            x=a*pe;y=x-delta
                            b=y//qf
                            if 1<=b<=A and min(a,b)<=first and x<=N and y<=N and max(x,y)>T:
                                assert y==b*qf and abs(x-y)<=h
                                pairs+=1
                                if max(x,y)>maximum:
                                    maximum=max(x,y)
                                    witness=dict(p=p,q=q,a=a,b=b,e=e,f=f,x=x,y=y)
                        a=(a+inverse)%qf
    return dict(i=i,input_cap=N,first=first,A=A,trivial_value_cap=T,
                output_cap=min(N,maximum+h),witness=witness,pairs_above_trivial=pairs,
                exponent_pairs=exponent_pairs,stopped=False)

def main():
    if not __debug__: raise RuntimeError('Assertions are required.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--indices',type=int,nargs='+',default=[27,30,33])
    parser.add_argument('--initial-power',type=int,default=87)
    args=parser.parse_args()
    out=[]
    for i in args.indices:
        N=10**args.initial_power;steps=[]
        for _ in range(16):
            row=contract(i,N);steps.append(row)
            print(json.dumps(row),flush=True)
            new=row['output_cap']
            if new>=N or new<LOW: break
            N=new
        else: raise AssertionError('Iteration budget exhausted')
        out.append(dict(i=i,initial_cap=10**args.initial_power,final_cap=steps[-1]['output_cap'],steps=steps))
        (ROOT/'bounded_bootstrap.json').write_text(json.dumps(dict(schema=1,rows=out),indent=2)+'\n')

if __name__=='__main__': main()
