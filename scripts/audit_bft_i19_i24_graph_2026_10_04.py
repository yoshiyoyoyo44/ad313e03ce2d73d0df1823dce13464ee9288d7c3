"""Exact graph lemmas and capacity comparisons for potential i19/i24 closure.

The additional BFT edge bounds and their threshold remain named proof
obligations. This checker certifies the graph and comparisons, not them.
"""
from fractions import Fraction
from itertools import product
from math import factorial, isqrt
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
GRAPHS = {
    19: ((2,7,259),(3,11,329),(5,13,163),(3,13,231),
         (7,13,98),(5,11,199),(2,17,337),(5,7,264)),
    24: ((2,7,259),(3,11,329),(3,13,231),(7,13,98),
         (2,17,337),(11,19,196),(17,19,191),(5,7,264),
         (5,23,206),(11,23,116)),
}
EXTRA = {(2,17),(11,19),(17,19),(5,7),(5,23),(11,23)}


def graph(i):
    edges = GRAPHS[i]
    ps = sorted({p for e in edges for p in e[:2]})
    assert all(p < i for p in ps)
    best = 10**9
    solutions = set()
    for choices in product((0,1),repeat=len(edges)):
        lower = {p:0 for p in ps}
        for (p,q,w),side in zip(edges,choices):
            v = (p,q)[side]
            lower[v] = max(lower[v],w)
        total = sum(lower.values())
        vector = tuple(lower[p] for p in ps)
        if total < best:
            best,solutions = total,set()
        if total == best:
            solutions.add(vector)
    assert best == {19:1028,24:1332}[i]
    return dict(i=i,primes=ps,edges=[list(e) for e in edges],
                orientations=2**len(edges),minimum_thousandths=best,
                minimizing_vectors=[list(v) for v in sorted(solutions)],
                extra_edge_obligations=[list(e) for e in edges if e[:2] in EXTRA])


def comparison(i):
    h=i-1
    m=sum(all(p%d for d in range(2,isqrt(p)+1)) for p in range(2,i))
    b=(2*h+2)//3
    d=3*b-h
    S=b*(b+1)//2
    D=3*S-d*(i-m)
    c=1 if all(i%p for p in range(2,isqrt(i)+1)) else i
    A=factorial(i)//c
    for s in range(i):
        for u in range(s+1):
            assert max(0,s-(h-b))+max(0,b-u)+max(0,b-s+u)>=d
    assert sum(max(0,s-(h-b)) for s in range(i))==S
    assert sum(max(0,b-u) for u in range(i))==S
    e=0
    while A>=10**e:
        e+=1
    alpha={19:Fraction(257,250),24:Fraction(333,250)}[i]
    gap=alpha.numerator*d-alpha.denominator*D
    assert gap>0 and alpha.denominator==250
    # Bernoulli gives losses below two. Therefore a counterexample
    # requires 4^(250S)n^gap < 2^251 A^(250d).
    assert 4**5>10**3 and 2**251<10**76 and A<10**e
    cutoff=(76+250*d*e-150*S)//gap+1
    margin=cutoff*gap+150*S-76-250*d*e
    assert margin>0
    assert cutoff=={19:551,24:1646}[i]
    assert 10**cutoff>2*h*i*d
    assert 10**cutoff>2*h*alpha.numerator*d
    # Imported finite Proposition 6.1 max formulation yields alpha=5/3
    # on [10^87, exp(10^6)); the comparison is independent of its proof.
    N=10**87
    prop_gap=5*d-3*D
    assert prop_gap>0
    assert N>2*h*i*d and N>2*h*5*d and N-h>3_000_000_000
    assert 4**(3*S)*N**prop_gap>16*A**(3*d)
    # A uniform extra-edge cutoff log x0<=999999 suffices for all
    # n>=exp(10^6): exp(10^6)-h > exp(999999) because e>2.
    assert 2**999999>h and 2**10>10**3 and cutoff<300000
    return dict(i=i,h=h,m=m,c_i=c,b=b,d=d,S=S,D=D,beta=str(Fraction(D,d)),
                tail_exponent=str(alpha),gap=gap,capacity_cutoff_power=cutoff,
                tail_decimal_margin=margin,intermediate_gap=prop_gap,
                intermediate_lower=10**87,intermediate_comparison=True,
                sufficient_uniform_extra_edge_log_threshold=999999)


def main():
    if not __debug__:
        raise RuntimeError('Assertions required.')
    # Independent analytic four-case proof for i19 in thousandths.
    branches=(337+259+329+163,337+329+264+231,
              337+329+264+98,337+329+264+199)
    assert branches==(1088,1161,1028,1129)
    result=dict(status='passed',scope='Graph lemmas and conditional comparisons only',
                analytic_i19_branches=list(branches),
                graphs=[graph(i) for i in (19,24)],
                comparisons=[comparison(i) for i in (19,24)],
                new_all_n_indices_claimed=[],
                obligations=['Prove all listed extra edge bounds with uniform log threshold <=999999',
                             'Import BFT Proposition 6.1 and replay n<=10^87 finite certificates'])
    dest=ROOT/'data/results/verification_bft_i19_i24_graph_2026-10-04.json'
    dest.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
