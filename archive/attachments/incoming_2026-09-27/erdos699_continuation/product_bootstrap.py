"""Strengthened finite bootstrap using the product of the two least cofactors.

For counterexamples with LOW<=n<=N, product(a_p)^d <= Cpow(N).
If m=#small primes, the product of the two least cofactors is at most
Cpow(N)^(2/(d*m)). Above this threshold both cross-coefficient inequalities
a<q^f and b<p^e hold, so one modular residue covers each exponent pair.
"""
from math import factorial,isqrt
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import json,argparse,time
ROOT=Path(__file__).resolve().parent
LOW=2_000_000

def primes(i): return [p for p in range(2,i) if all(p%d for d in range(2,isqrt(p)+1))]

def iroot(n,k):
    lo=0;hi=1<<((n.bit_length()+k-1)//k)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**k<=n:lo=mid
        else:hi=mid
    return lo

def parameters(i):
    h=i-1;m=len(primes(i));b=(2*h+2)//3;d=3*b-h;S=b*(b+1)//2
    defect=3*S-d*(i-m)
    correction=1 if len(primes(i+1))>m else i
    return m,d,S,defect,correction

def cpower(i,N):
    m,d,S,defect,correction=parameters(i)
    assert defect>=0
    return F(factorial(i),correction)**d*F(LOW,LOW-i+1)**(i*d)*N**defect/4**S

@lru_cache(None)
def cofactor_possible(i,n):
    m,d,S,defect,correction=parameters(i)
    product=1
    for p in primes(i):
        q=p;largest=1
        while q<=n:
            if n%q<i:largest=q
            q*=p
        # Minimize a_p over all ties of the maximizing p-adic row.
        product*= -((-(n-i+1))//largest)
    lhs=(correction*product)**d*4**S*(n-i+1)**(i*d)
    rhs=factorial(i)**d*n**(i*d+defect)
    return lhs<=rhs

def contract(i,N):
    h=i-1;m,d,S,defect,correction=parameters(i)
    C=cpower(i,N)
    first=iroot(C.numerator//C.denominator,d*m)
    A=iroot(C.numerator//C.denominator,d*(m-1))
    pair_product=iroot(C.numerator**2//(C.denominator**2),d*m)
    trivial=pair_product+2*h
    row=dict(i=i,input_cap=N,first=first,A=A,pair_product=pair_product,trivial_n_cap=trivial)
    if trivial>=N:return dict(**row,output_cap=N,stopped=True)
    powers={}
    for p in primes(i):
        v=p;e=1;seq=[]
        while v<=N:
            if A*v>pair_product:seq.append((v,e))
            v*=p;e+=1
        powers[p]=seq
    candidates=set();count=0;exp_pairs=0
    for p in powers:
        for q in powers:
            if p>=q:continue
            for pe,e in powers[p]:
                for qf,f in powers[q]:
                    if pe>A*qf+h or qf>A*pe+h:continue
                    exp_pairs+=1
                    inverse=pow(pe,-1,qf)
                    a=(-h*inverse)%qf
                    for delta in range(-h,h+1):
                        if 1<=a<=A and a%p:
                            x=a*pe;y=x-delta;b=y//qf
                            if (1<=b<=A and b%q and min(a,b)<=first and a*b<=pair_product
                                and x<=N and y<=N and min(x,y)>pair_product):
                                assert y==b*qf and a<qf and b<pe
                                lower=min(a,b)*max(a,b)**(m-1)
                                if lower**d*C.denominator<=C.numerator:
                                    count+=1
                                    candidates.update(range(max(LOW,trivial+1,x,y),min(N,min(x,y)+h)+1))
                        a=(a+inverse)%qf
    survivors=sorted(n for n in candidates if cofactor_possible(i,n))
    cap=max([trivial]+survivors)
    return dict(**row,output_cap=cap,stopped=False,exponent_pairs=exp_pairs,
                coefficient_pairs=count,candidate_n_count=len(candidates),surviving_n=survivors)

def main():
    if not __debug__: raise RuntimeError('Assertions required.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--indices',type=int,nargs='+',default=[i for i in range(5,34) if i not in (28,29,31)])
    parser.add_argument('--initial-power',type=int,default=87)
    args=parser.parse_args()
    rows=[]
    for i in args.indices:
        N=10**args.initial_power;steps=[];start=time.time()
        for _ in range(80):
            row=contract(i,N);steps.append(row)
            cap=row['output_cap']
            if cap*100>=N*99 or cap<LOW:break
            N=cap
        else:raise AssertionError(('budget',i))
        item=dict(i=i,initial_cap=10**args.initial_power,final_cap=steps[-1]['output_cap'],steps=steps)
        rows.append(item)
        (ROOT/'product_bootstrap.json').write_text(json.dumps(dict(schema=1,rows=rows),indent=2)+'\n')
        print(json.dumps(dict(i=i,final_cap=item['final_cap'],steps=len(steps),
                              candidate_n=sum(s.get('candidate_n_count',0) for s in steps),
                              seconds=round(time.time()-start,2))),flush=True)

if __name__=='__main__':main()
