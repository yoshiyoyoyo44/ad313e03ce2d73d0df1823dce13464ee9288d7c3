"""Exact audit of the finite BFT Proposition 6.1 bridge.

This proves an intermediate interval, not the unbounded tail. BFT's
Proposition 6.1 is an external input.
"""
from itertools import combinations
from math import factorial,isqrt
from fractions import Fraction
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
N=10**87
PRIMES=(2,3,5,7,11,13)
TARGETS=(16,19,22,25)


def primes_below(i):
    return [p for p in range(2,i)
            if all(p%d for d in range(2,isqrt(p)+1))]


def audit(i):
    h=i-1
    small=primes_below(i);m=len(small)
    c=1 if all(i%d for d in range(2,isqrt(i)+1)) else i
    A=factorial(i)//c
    b=(2*h+2)//3;d=3*b-h;S=b*(b+1)//2
    D=3*S-d*(i-m)
    assert set(PRIMES)<=set(small)
    assert N-h>3_000_000_000 and h<=100
    assert N>2*h*i*d and N>2*h*5*d
    for s in range(i):
        for u in range(s+1):
            assert max(0,s-(h-b))+max(0,b-u)+max(0,b-s+u)>=d
    kappa=5*d-3*D
    assert kappa>0
    e=0
    while A>=10**e:
        e+=1
    assert A<10**e
    # Since 4^5>10^3, 4^(3S)>10^floor(9S/5).
    # 2^4<10^2. These strict coarse bounds suffice at N.
    assert 4**5>10**3 and 2**4<10**2
    lower=87*kappa+(9*S)//5
    upper=2+3*d*e
    assert lower>upper
    # Exhaust only the 64 possible low/high patterns. Each of the
    # 15 pair maxima being high means there are at most one low vertex.
    accepted=[]
    for mask in range(1<<len(PRIMES)):
        if all((mask>>a)&1 or (mask>>b)&1
               for a,b in combinations(range(len(PRIMES)),2)):
            accepted.append(mask)
            assert mask.bit_count()>=5
    assert len(accepted)==7
    return dict(i=i,h=h,m=m,c_i=c,b=b,d=d,S=S,D=D,
                beta=str(Fraction(D,d)),
                intermediate_product_exponent="5/3",
                comparison_kappa=kappa,
                exact_coarse_decimal_margin=lower-upper,
                factorial_decimal_upper=e,high_patterns=len(accepted))


def main():
    if not __debug__:
        raise RuntimeError("Assertions required.")
    rows=[audit(i) for i in TARGETS]
    assert [r["comparison_kappa"] for r in rows]==[30,36,42,48]
    result=dict(status="PASS",indices=list(TARGETS),rows=rows,
        interval_lower=N,interval_upper="exp(1000000), exclusive",
        exact_all_n_indices_added=[],
        external_dependency=dict(
            url="https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf",
            result="Proposition 6.1, second maximum-cofactor formulation",
            page_zero_based=20,
            safe_exception_ceiling=3_000_000_000,
            table_bound_on_first_component=2693359375,
            theorem_imported_not_reproved=True),
        missing_for_all_n="Explicit infinite-tail cutoff below exp(1000000)-h",
        proof="research/general/bft_proposition61_intermediate_bridge_2026-10-04.md")
    (ROOT/"data/results/verification_bft_proposition61_intermediate_bridge_2026_10_04.json").write_text(
        json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("PASS exact intermediate bridge for i16,19,22,25; no infinite-tail claim")
    print([(r["i"],r["exact_coarse_decimal_margin"]) for r in rows])


if __name__=="__main__":
    main()
