#!/usr/bin/env python3
"""Independent verifier. Does NOT import either certificate generator.

Uses a direct integer-rational logarithm series (128 bits), whereas the
generator uses 192-bit interval recurrences. Checks coverage, not sampling.
"""
from functools import lru_cache
from math import factorial,isqrt,comb,gcd,prod
from pathlib import Path
import json,time,random,sys

ROOT=Path(__file__).resolve().parent
INDICES=[95,99,103,107,119]
SCALE=1<<128; TERMS=48

def direct_mantissa(a,b):
    assert b<=a<=2*b
    A=a-b;B=a+b;aa=A*A;bb=B*B
    numerator=A;denominator=B;total=0
    for k in range(TERMS):
        total+=(2*SCALE*numerator)//((2*k+1)*denominator)
        numerator*=aa;denominator*=bb
    # Tail <=9/(4*(2T+1)*3^(2T+1)) < 1/SCALE.
    assert 9*SCALE<4*(2*TERMS+1)*3**(2*TERMS+1)
    return total,total+TERMS+1

L2,U2=direct_mantissa(2,1)
@lru_cache(None)
def log_interval(n):
    assert n>0
    e=n.bit_length()-1;l,u=direct_mantissa(n,1<<e)
    return l+e*L2,u+e*U2

def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))

def check_intervals(cert):
    assert cert['schema']==1 and [r['i'] for r in cert['rows']]==INDICES
    results=[]
    for row in cert['rows']:
        i=row['i'];a=row['a'];b=row['b'];d=row['d'];S=row['S']
        assert a==i-1-b and 0<=a<i and 0<b<i and d==2*b-a>0
        assert S==b*(b+1)//2
        weights=0
        for s in range(i):
            for u in range(s+1):
                assert max(0,s-a)+max(0,b-u)+max(0,b-(s-u))>=d
                weights+=1
        assert sum(max(0,s-a) for s in range(i))==S
        assert sum(max(0,b-u) for u in range(i))==S
        ps=[p for p in range(2,i) if prime(p)];pi=len(ps)
        assert row['pi']==pi
        hsmall=1 if prime(i) else i
        N=10**row['tail']['n_power']
        delta=d*(i-pi)-3*S
        assert delta>0 and delta==row['tail']['degree_gap']
        assert row['tail']['small_part_correction']==hsmall
        # Independent exact integer tail check, no logarithms.
        assert 4**S*hsmall**d*(N-i+1)**(i*d)>factorial(i)**d*N**(pi*d+3*S)
        factorial_upper=sum(log_interval(k)[1] for k in range(1,i+1))
        pdata=[]
        for p in ps:
            qs=[];q=p
            while q<N:qs.append((q,i%q));q*=p
            pdata.append((log_interval(p)[1],qs))
        expected=2_000_000;minimum=None;st=time.time()
        for number,(lo,hi) in enumerate(row['intervals']['leaves'],1):
            assert lo==expected and lo<=hi<N;expected=hi+1
            total_upper=0
            for lp,qs in pdata:
                power=0
                for q,r in qs:
                    if q>hi:break
                    # Different interval-intersection formulation from generator.
                    power+=int(r>0 and -((-(lo-r+1))//q)<=hi//q)
                total_upper+=power*lp
            margin=(2*S*L2+d*i*log_interval(lo-i+1)[0]
                    -d*factorial_upper-d*total_upper-3*S*log_interval(hi)[1])
            assert margin>0,(i,lo,hi,margin)
            minimum=margin if minimum is None else min(minimum,margin)
            if number%10000==0:print(json.dumps(dict(check_i=i,checked=number,seconds=round(time.time()-st,2))),flush=True)
        assert expected==N
        count=len(row['intervals']['leaves'])
        assert row['intervals']['tested_nodes']==2*count-1
        results.append(dict(i=i,tail_power=row['tail']['n_power'],interval_count=count,
            grid_cells_checked=weights,minimum_log_margin_lower_numerator=str(minimum),
            minimum_log_margin_lower_denominator=str(SCALE)))
        print(json.dumps(dict(verified_i=i,intervals=count,seconds=round(time.time()-st,2))),flush=True)
    return results

def check_small(cert):
    assert cert['schema']==1 and cert['covered_upper']==1_999_999
    N=cert['limit'];assert N>2_000_000
    flags=bytearray(b'\x01')*(N+1);flags[:2]=b'\x00\x00'
    for p in range(2,isqrt(N)+1):
        if flags[p]:flags[p*p::p]=b'\x00'*((N-p*p)//p+1)
    ps=[p for p in range(2,N+1) if flags[p]]
    assert len(ps)==cert['prime_count'] and ps[-1]==cert['last_prime']>=2_000_000
    gaps=[[x,y] for x,y in zip(ps,ps[1:]) if y-x>min(INDICES)]
    assert gaps==cert['long_gaps']
    needed=sorted((i,n) for i in INDICES for x,y in gaps for n in range(x+i,y)
                  if 2*i+2<=n<2_000_000)
    assert [(r['i'],r['n']) for r in cert['exceptions']]==needed
    for row in cert['exceptions']:
        i=row['i'];n=row['n']
        def constraint(c):
            p,e,r=c['p'],c['e'],c['r']
            assert prime(p) and p>i and e>=1 and 0<=r<i and n%p**e==r
            return p**e,r
        q,r=constraint(row['anchor'])
        # Exhaust all residue bands intersecting the allowed interval.
        left=[]
        for k in range(n//(2*q)+1):
            low=max(i+1,k*q);high=min(n//2,k*q+r)
            left.extend(range(low,high+1))
        assert len(left)==row['initial_count']
        for c in row['constraints']:
            modulus,rem=constraint(c)
            kept=[j for j in left if j%modulus<=rem]
            assert len(left)-len(kept)==c['eliminated'];left=kept
        assert not left
    return dict(sieve_limit=N,prime_count=len(ps),exception_count=len(needed),
        per_index={str(i):sum(j==i for j,n in needed) for i in INDICES},
        maximum_anchor_candidates=max(r['initial_count'] for r in cert['exceptions']))

def check_formula():
    count=intersections=0
    for n in range(1,161):
        for i in range(1,n+1):
            A=comb(n,i)
            for p in [2,3,5,7,11]:
                q=p;e=0
                while q<=n:e+=int(n%q<i%q);q*=p
                z=A;actual=0
                while z%p==0:z//=p;actual+=1
                assert e==actual;count+=1
    for q in range(2,40):
        for r in range(q):
            for lo in range(2*q):
                for width in [0,1,q//2,q,2*q]:
                    hi=lo+width
                    expected=any(n%q<r for n in range(lo,hi+1))
                    actual=r>0 and -((-(lo-r+1))//q)<=hi//q
                    assert expected==actual;intersections+=1
    return dict(valuation_checks=count,interval_intersection_checks=intersections)

def main():
    rows=check_intervals(json.loads((ROOT/'interval_certificate.json').read_text()))
    small=check_small(json.loads((ROOT/'small_certificate.json').read_text()))
    formula=check_formula()
    result=dict(status='PASS',proved_indices=INDICES,
        domain='All integers i<j<=n/2 for each listed i; all n.',
        uses_a100_certificate=False,uses_discriminant=False,
        verification_arithmetic='exact integers and rigorous 128-bit log enclosures',
        interval_rows=rows,small_range=small,formula_tests=formula,
        independent_peer_review=False,formal_lean_verification=False)
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
