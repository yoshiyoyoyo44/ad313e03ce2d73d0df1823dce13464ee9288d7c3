"""Exact replay of the BFT disjoint-matching closeout for i=27,30,33.

The external BFT Theorem 2.1 is an explicit input, not re-proved by this
checker. All matching, cover, Bernoulli, constants and endpoint comparisons
used in the new note are checked by integer arithmetic.
"""
from fractions import Fraction
from math import factorial, isqrt, prod
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
N = 10**87
BFT_TABLE = [
    (2, 3, 285), (2, 5, 258), (2, 7, 259), (2, 11, 59),
    (2, 13, 54), (3, 5, 216), (3, 7, 38), (3, 11, 329),
    (3, 13, 231), (5, 7, 227), (5, 11, 199), (5, 13, 163),
    (7, 13, 98), (11, 13, 37)
]
BFT_EXCEPTION_MAX = 1771561
UNRESOLVED_INPUT = [i for i in range(5, 34) if i not in (28, 29, 31)]
SOLVED = (27, 30, 33)


def primes_below(i):
    return [p for p in range(2, i)
            if all(p % d for d in range(2, isqrt(p) + 1))]


def best_matching(i):
    edges = [edge for edge in BFT_TABLE if edge[1] < i]
    best = (0, [])
    def walk(at, used, weight, selected):
        nonlocal best
        if at == len(edges):
            if weight > best[0]:
                best = (weight, list(selected))
            return
        walk(at + 1, used, weight, selected)
        p, q, w = edges[at]
        if p not in used and q not in used:
            walk(at + 1, used | {p, q}, weight + w,
                 selected + [(p, q, w)])
    walk(0, set(), 0, [])
    return best


def parameters(i):
    h = i - 1
    ps = primes_below(i)
    m = len(ps)
    c = prod(p**valuation(i, p) for p in ps)
    b = (2*h + 2)//3
    d = 3*b - h
    S = b*(b+1)//2
    D = 3*S - d*(i-m)
    is_prime = all(i % d for d in range(2,isqrt(i)+1))
    assert c == (1 if is_prime else i)
    assert d > 0
    # Check the covering inequality at every cell, independently of row sets.
    a = h-b
    for s in range(i):
        for u in range(s+1):
            assert max(0,s-a)+max(0,b-u)+max(0,b-(s-u)) >= d
    assert sum(max(0,s-a) for s in range(i)) == S
    assert sum(max(0,b-u) for u in range(i)) == S
    return ps, c, b, d, S, D


def valuation(x,p):
    v=0
    while x % p == 0:
        x//=p
        v+=1
    return v


def comparison_at(i,E):
    ps,c,b,d,S,D = parameters(i)
    M,matching = best_matching(i)
    delta=M*d-1000*D
    X=10**E
    bernoulli=(X > 2*i*d*(i-1) and X > 2*M*d*(i-1))
    if delta <= 0:
        return False
    return bernoulli and (
        4**(1000*S)*X**delta >
        2**1001*(factorial(i)//c)**(1000*d)
    )


def summarize(i):
    ps,c,b,d,S,D = parameters(i)
    M,matching = best_matching(i)
    vertices=[p for p,q,w in matching for p in (p,q)]
    assert len(vertices)==len(set(vertices))
    assert all(p in ps for p in vertices)
    assert sum(w for p,q,w in matching)==M
    assert N-(i-1)>BFT_EXCEPTION_MAX
    assert i-1<=100
    delta=M*d-1000*D
    result=dict(i=i, small_primes=ps, c=c,b=b,d=d,S=S,D=D,
                beta=str(Fraction(D,d)), matching=matching,
                matching_numerator=M,matching_denominator=1000,
                comparison_exponent_delta=delta,
                closes_at_existing_cutoff=comparison_at(i,87))
    if delta>0:
        lo,hi=0,64
        while not comparison_at(i,hi):
            lo,hi=hi,2*hi
        while hi-lo>1:
            mid=(hi+lo)//2
            if comparison_at(i,mid):
                hi=mid
            else:
                lo=mid
        result["sufficient_tail_power"]=hi
        assert comparison_at(i,hi) and not comparison_at(i,hi-1)
    if i in SOLVED:
        assert M==751 and comparison_at(i,87)
        lhs=4**(1000*S)*N**delta
        rhs=2**1001*(factorial(i)//c)**(1000*d)
        result["strict_comparison_margin_bits"]=lhs.bit_length()-rhs.bit_length()
        assert d>D>=0 and delta>0
        # This endpoint has a positive integer n exponent delta, and both
        # Bernoulli hypotheses remain valid as n grows.
        assert N>2*i*d*(i-1)
        assert N>2*M*d*(i-1)
    return result


def main():
    if not __debug__:
        raise RuntimeError("Assertions are required.")
    rows=[summarize(i) for i in UNRESOLVED_INPUT]
    closed=[r["i"] for r in rows if r["closes_at_existing_cutoff"]]
    assert closed==list(SOLVED)
    for i,expected in [(27,(28,171,9)),(30,(31,210,10)),(33,(34,253,11))]:
        r=next(r for r in rows if r["i"]==i)
        assert (r["d"],r["S"],r["D"])==expected
        assert r["c"]==i
        assert sorted(r["matching"])==[(2,7,259),(3,11,329),(5,13,163)]
    result=dict(status="PASS",new_all_n_indices=closed,
                external_input=dict(
                    title="Bennett-Filaseta-Trifonov, On the factorization of consecutive integers",
                    url="https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf",
                    theorem="Theorem 2.1",printed_page=4,
                    exception_maximum=BFT_EXCEPTION_MAX,
                    imported_not_reproved=True),
                finite_input="Previously certified i>=5,n<=10^87",
                rows=rows,
                proof="research/general/bft_matching_closeout_i27_i30_i33_2026-10-04.md",
                global_problem_solved=False)
    out=ROOT/"data/results/verification_bft_matching_closeout_2026_10_04.json"
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    for r in rows:
        if r["closes_at_existing_cutoff"] or r["comparison_exponent_delta"]>0:
            print(f"i={r['i']}: matching={r['matching_numerator']}/1000, "
                  f"beta={r['beta']}, sufficient tail=10^{r['sufficient_tail_power']}, "
                  f"connects at 10^87={r['closes_at_existing_cutoff']}")
    print("PASS: new all-n indices 27,30,33")


if __name__=="__main__":
    main()
