"""Independent bounded-bootstrap replay.

Uses the opposite CRT coordinate (b modulo p^e) and the actual large-prime
part of binomial(n,i), instead of the generator's maximizing-row cofactors.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt,factorial,comb
from functools import lru_cache
import json,time
ROOT=Path(__file__).resolve().parent
LOW=2_000_000

def primes(i):return [p for p in range(2,i) if all(p%a for a in range(2,isqrt(p)+1))]

def parameters(i):
    h=i-1;ps=primes(i);m=len(ps);b=-((-2*h)//3);d=3*b-h;S=b*(b+1)//2
    defect=3*S-d*(i-m);correction=1 if all(i%a for a in range(2,isqrt(i)+1)) else i
    return ps,m,d,S,defect,correction

@lru_cache(None)
def excluded(i,n):
    ps,m,d,S,defect,correction=parameters(i)
    Q=comb(n,i)
    for p in ps:
        while Q%p==0:Q//=p
    return 4**S*Q**d>n**(3*S)

def verify_step(i,row):
    N,cap=row['input_cap'],row['output_cap']
    assert LOW<=N and cap<=N
    ps,m,d,S,defect,correction=parameters(i)
    assert defect>=0
    C=F(factorial(i)**d*LOW**(i*d)*N**defect,
        correction**d*4**S*(LOW-i+1)**(i*d))
    first,A,B=row['first'],row['A'],row['pair_product']
    assert first**(d*m)<=C<(first+1)**(d*m)
    assert A**(d*(m-1))<=C<(A+1)**(d*(m-1))
    assert B**(d*m)<=C*C<(B+1)**(d*m)
    assert B>=A
    assert row['trivial_n_cap']==B+2*(i-1)
    if cap==N:return 0
    assert cap>=row['trivial_n_cap']
    powers={p:[] for p in ps}
    for p in ps:
        value=p
        while value<=N:
            powers[p].append(value);value*=p
    needed=set();h=i-1
    for p in ps:
        for q in ps:
            if p>=q:continue
            for pe in powers[p]:
                if A*pe<=B:continue
                for qf in powers[q]:
                    if A*qf<=B or pe>A*qf+h or qf>A*pe+h:continue
                    inverse=pow(qf,-1,pe)
                    # x-y=delta, b*q^f == -delta (mod p^e).
                    for delta in range(-h,h+1):
                        b=(-delta*inverse)%pe
                        if not 1<=b<=A or b%q==0:continue
                        y=b*qf;x=y+delta
                        if x%pe:raise AssertionError('CRT failure')
                        a=x//pe
                        if not 1<=a<=A or a%p==0:continue
                        if min(a,b)>first or a*b>B:continue
                        if min(x,y)<=B or max(x,y)>N:continue
                        lower=min(a,b)*max(a,b)**(m-1)
                        if lower**d>C:continue
                        lo=max(LOW,cap+1,x,y);hi=min(N,x+h,y+h)
                        needed.update(range(lo,hi+1))
    for n in sorted(needed):assert excluded(i,n),('unverified n',i,n)
    return len(needed)

def main():
    if not __debug__:raise RuntimeError('Assertions required.')
    cert=json.loads((ROOT/'product_bootstrap.json').read_text())
    expected=[i for i in range(5,34) if i not in (28,29,31)]
    assert cert['schema']==1 and [r['i'] for r in cert['rows']]==expected
    result=[]
    for row in cert['rows']:
        i=row['i'];last=10**87;count=0;start=time.time()
        assert row['initial_cap']==last
        for step in row['steps']:
            assert step['i']==i and step['input_cap']==last
            count+=verify_step(i,step);last=step['output_cap']
        assert last==row['final_cap']
        item=dict(i=i,steps=len(row['steps']),final_cap=last,exact_binomial_checks=count)
        result.append(item)
        print(json.dumps(dict(**item,seconds=round(time.time()-start,2))),flush=True)
    out=dict(status='EXHAUSTIVE-COMPUTATION',initial_cap=10**87,lower=LOW,
             proof='Opposite CRT coordinate plus actual binomial large-prime part',rows=result)
    (ROOT/'product_bootstrap_verification.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
