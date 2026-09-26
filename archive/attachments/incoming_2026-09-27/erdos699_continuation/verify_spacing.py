"""Independent exact replay: rational Taylor sums, no generator imports."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from math import gcd, isqrt, factorial
import json

ROOT=Path(__file__).resolve().parent
BITS=192
SCALE=1<<BITS
TERMS=80
M=10**16
A=1995
CUTOFF=128
PRIMES=[p for p in range(2,34) if all(p%d for d in range(2,isqrt(p)+1))]

def floor(v): return v.numerator//v.denominator
def ceil(v): return -((-v.numerator)//v.denominator)

def series(a,b):
    t=F(a-b,a+b)
    assert 0<=t<=F(1,3)
    total=2*sum((t**(2*k+1)/F(2*k+1) for k in range(TERMS)),F(0))
    tail=2*t**(2*TERMS+1)/(F(2*TERMS+1)*(1-t*t))
    return floor(total*SCALE),ceil((total+tail)*SCALE)

LOG2=series(2,1)

@lru_cache(None)
def log(n):
    assert n>0
    e=n.bit_length()-1
    lo,hi=series(n,1<<e)
    return lo+e*LOG2[0],hi+e*LOG2[1]

def quotient(top,bottom):
    assert bottom[0]>0
    corners=[F(t,b)*SCALE for t in top for b in bottom]
    return floor(min(corners)),ceil(max(corners))

def floorroot_ratio(n,d,k):
    lo,hi=0,1
    while d*hi**k<=n: hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if d*mid**k<=n: lo=mid
        else: hi=mid
    assert d*lo**k<=n<d*(lo+1)**k
    return lo

def cofactor_bounds():
    results=[]
    for i in (28,31,34):
        m=sum(p<i for p in PRIMES)
        b=(2*(i-1)+2)//3; d=3*b-i+1; S=b*(b+1)//2
        assert 3*S==d*(i-m)
        correction=1 if i in PRIMES else i
        Cpow=F(factorial(i),correction)**d*F(2_000_000,2_000_000-i+1)**(i*d)/4**S
        bounds=[floorroot_ratio(Cpow.numerator,Cpow.denominator,d*(m-k+1)) for k in (1,2,3)]
        results.append(dict(i=i,m=m,b=b,d=d,S=S,product_upper=floorroot_ratio(Cpow.numerator,Cpow.denominator,d),ordered_bounds=bounds))
    assert [max(r['ordered_bounds'][k] for r in results) for k in range(3)]==[933,1995,5159]
    return results

def main():
    if not __debug__: raise RuntimeError('Do not run with python -O.')
    cert=json.loads((ROOT/'spacing_certificate.json').read_text())
    assert (cert['schema'],cert['A'],cert['difference'],cert['M'],cert['cutoff'])==(1,A,33,M,CUTOFF)
    assert cert['primes']==PRIMES
    assert [(r['p'],r['q']) for r in cert['rows']]==[(p,q) for p in PRIMES for q in PRIMES if p<q]
    # Matveev Corollary 2.3 over Q, A1=A2=4, A3=8, at most three logs.
    K=4*10**13
    assert F(7,5)*30**6*3**5*4*4*8<K
    assert log(31)[1]<4*SCALE and log(A)[1]<8*SCALE
    assert 100*LOG2[0]>69*SCALE
    assert log(66)[1]<5*SCALE and log(M)[1]<37*SCALE
    assert F(69,100)*M>5+38*K
    assert F(69,100)>F(K,M)
    assert F(66*100,69)<400
    assert 2**10<=A<2**11
    # Identical values and cross-cancellation with nonpositive exponent are small.
    assert A*A+33<4_209_368_322
    gap_summary=[]
    for row in cert['rows']:
        p,q,P,Q=(row[k] for k in ('p','q','P','Q'))
        assert Q>6*M and P>0 and gcd(P,Q)==1
        alpha=quotient(log(p),log(q))
        error=max(abs(Q*alpha[0]-P*SCALE),abs(Q*alpha[1]-P*SCALE))
        assert 2*M*error<SCALE and p**CUTOFF>800*Q
        intervals=[]
        for a in range(1,A+1):
            if gcd(a,p*q)!=1: continue
            lo,hi=quotient(log(a),log(q))
            lo*=Q; hi*=Q
            k=lo//SCALE
            assert hi//SCALE==k
            intervals.append((lo-k*SCALE,hi-k*SCALE,a))
        intervals.sort()
        assert len(intervals)==row['count']
        gaps=[intervals[k+1][0]-intervals[k][1] for k in range(len(intervals)-1)]
        gaps.append(SCALE+intervals[0][0]-intervals[-1][1])
        gap=min(gaps)
        epsilon=gap-M*error
        assert epsilon>0 and epsilon*p**CUTOFF>400*Q*SCALE,(p,q)
        gap_summary.append(dict(p=p,q=q,Q=Q,coefficient_count=len(intervals),epsilon_lower=str(F(epsilon,SCALE))))
    out=dict(status='VERIFIED',prime_pairs=len(gap_summary),log_bits=BITS,series_terms=TERMS,
             initial_exponent_bound=M,normalized_exponents_less_than=CUTOFF,
             original_exponents_less_than=138,matveev_constant_upper=K,
             cofactor_bounds=cofactor_bounds(),rows=gap_summary)
    (ROOT/'spacing_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2),flush=True)

if __name__=='__main__': main()
