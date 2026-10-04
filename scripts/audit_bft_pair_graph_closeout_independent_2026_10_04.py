"""Independent exact audit of six all-n extensions via BFT's pair graph.

No workspace proof module is imported. BFT Theorem 2.1 and the previously
replayed finite theorem n<=10^87 remain explicitly named dependencies.
The analytic argument is in the accompanying research note; this checker
also exhausts every edge orientation independently of its five-case proof.
"""

from fractions import Fraction
from itertools import product
from math import factorial, isqrt, prod
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
N = 10**87
PRIMES = (2, 3, 5, 7, 11, 13)
EDGES = (
    (2, 3, 285), (2, 5, 258), (2, 7, 259),
    (2, 11, 59), (2, 13, 54), (3, 5, 216),
    (3, 7, 38), (3, 11, 329), (3, 13, 231),
    (5, 7, 227), (5, 11, 199), (5, 13, 163),
    (7, 13, 98), (11, 13, 37),
)
NEW_INDICES = (17, 23, 26, 27, 30, 33)


def primes_below(i):
    return [p for p in range(2, i)
            if all(p % d for d in range(2, isqrt(p)+1))]


def orientation_audit():
    best = None
    minimizers = set()
    examined = 0
    for choices in product((0, 1), repeat=len(EDGES)):
        lower = {p: 0 for p in PRIMES}
        for (p, q, lam), side in zip(EDGES, choices):
            vertex = (p, q)[side]
            lower[vertex] = max(lower[vertex], lam)
        total = sum(lower.values())
        vector = tuple(lower[p] for p in PRIMES)
        if best is None or total < best:
            best, minimizers = total, {vector}
        elif total == best:
            minimizers.add(vector)
        examined += 1
    assert examined == 2**14
    assert best == 913
    assert minimizers == {(259, 329, 227, 0, 0, 98)}
    # Closed branch lower bounds in units of 1/1000. Strictness comes
    # from y3>329 or y11>329, not from rounding these integer sums.
    branches = (329+259+227+98, 329+259+227+199,
                329+259+258+199, 329+259+258+59+37,
                329+285+216+98)
    assert branches == (913, 1014, 1045, 942, 928)
    return dict(orientations=examined, minimum_sum=best,
                minimizing_vector=list(next(iter(minimizers))),
                analytic_branch_bounds=list(branches))


def ceil_log10(value):
    e = 0
    while value >= 10**e:
        e += 1
    assert value < 10**e
    assert e == 0 or value >= 10**(e-1)
    return e


def audit_index(i):
    h = i-1
    ps = primes_below(i)
    m = len(ps)
    assert set(PRIMES) <= set(ps)
    # c_i is the part of i supported on primes strictly less than i.
    c = 1
    for p in ps:
        quotient = i
        while quotient % p == 0:
            c *= p
            quotient //= p
    A = factorial(i)//c
    assert A*c == factorial(i)
    b = (2*h+2)//3
    d = 3*b-h
    S = b*(b+1)//2
    D = 3*S-d*(i-m)
    assert d > 0 and b <= h
    w = [max(0, s-(h-b)) for s in range(i)]
    x = [max(0, b-u) for u in range(i)]
    assert sum(w) == sum(x) == S
    cells = 0
    for s in range(i):
        for u in range(s+1):
            assert w[s]+x[u]+x[s-u] >= d
            cells += 1
    # Both Bernoulli relaxations hold throughout n>=N.
    assert N > 2*h*i*d
    assert N > 2*h*913*d
    assert h <= 100 and N-h > 1771561
    gap = 913*d-1000*D
    A_digits = ceil_log10(A)
    # 4^(1000*S) > 10^(600*S), since 4^5>10^3.
    # 2^1001 < 10^302. No logarithmic floating point or gigantic
    # decimal exponentiation is needed for the cutoff comparison.
    assert 4**5 > 10**3 and 2**1001 < 10**302
    lhs_decimal_lower = 87*gap+600*S
    rhs_decimal_upper = 302+1000*d*A_digits
    passes = gap > 0 and lhs_decimal_lower >= rhs_decimal_upper
    # At equality the integer inequality is still strict: both sides
    # were bounded strictly in opposite directions.
    return dict(i=i, h=h, small_primes=m, c_i=c, b=b, d=d, S=S, D=D,
                beta=str(Fraction(D,d)), product_lower_exponent="913/1000",
                cutoff_gap_integer=gap, factorial_bound_exponent=A_digits,
                exact_coarse_decimal_margin=lhs_decimal_lower-rhs_decimal_upper,
                closes_at_existing_cutoff=passes, weight_cells_checked=cells)


def main():
    graph = orientation_audit()
    rows = [audit_index(i) for i in range(14,35)]
    closed = [r['i'] for r in rows if r['closes_at_existing_cutoff']]
    assert closed == [17,23,26,27,28,29,30,31,33,34]
    assert [i for i in closed if i not in (28,29,31,34)] == list(NEW_INDICES)
    selected = [r for r in rows if r['i'] in NEW_INDICES]
    assert all(r['exact_coarse_decimal_margin'] > 0 for r in selected)
    result = dict(
        status="passed", independent_review="Paper and exact checker audited independently by root, i5_attack, and i3_attack; finite input freshly replayed by root and i5_attack",
        new_all_n_indices=list(NEW_INDICES),
        scope="Every n,j with 1<=i<j<=n/2, for the six listed indices, combining this tail proof with the previously certified n<=10^87 theorem",
        tail_scope="For each listed i, no numerical counterexample exists at n>=10^87; no polynomial full-sharing hypothesis",
        proof="research/general/bft_pair_graph_closeout_six_indices_2026-10-04.md",
        external_dependency={
            "authors":"Bennett, Filaseta, Trifonov", "theorem":"Theorem 2.1",
            "url":"https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf",
            "pdf_page_zero_based":3, "exception_maximum":1771561,
            "theorem_proof_reproduced_here":False},
        finite_dependency="scripts/audit_bft_six_finite_dependency_2026_10_04.py: fresh exhaustive replay of all six n<=10^87 inputs, including bootstrap and complete prefix",
        graph_audit=graph, new_index_comparisons=selected,
        all_small_index_comparisons=rows,
        limitation="i3 and i5 remain unresolved; this is not a full solution of Problem 699 or a Lean verification",
    )
    dest = ROOT/'data/results/verification_bft_pair_graph_closeout_independent_2026-10-04.json'
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='all_small_index_comparisons'},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
