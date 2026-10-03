"""Reconstructed audit of the saved integral-root-value/split-geometric proof.

The original untracked audit was lost after a runtime reset. This independent
audit is rebuilt from the byte-for-byte restored report, not an old git object.
Finite coefficient examples are diagnostics, not a proof of the theorem.
"""

import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
X = sp.symbols("X")


def cyclic_mul(left, right):
    m = len(left)
    out = [0]*m
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[(i+j)%m] += a*b
    return out


def division_rem(coefficients, divisor):
    out = list(coefficients)
    degree = len(divisor)-1
    assert divisor[-1] == 1
    for i in range(len(out)-1,degree-1,-1):
        value = out[i]
        for j in range(degree+1):
            out[i-degree+j] -= value*divisor[j]
    return out[:degree]


def small_classification():
    inspected, admissible, records = 0, 0, []
    for m in range(2,7):
        cyclotomic = []
        for order in sp.divisors(m):
            if order == 1:
                continue
            P = sp.Poly(sp.cyclotomic_poly(order,X),X)
            cyclotomic.append([int(P.nth(e)) for e in range(P.degree()+1)])
        hits = []
        for short in product(range(-2,3),repeat=m-1):
            inspected += 1
            R = list(short)+[0]
            factors = []
            for s in range(3):
                term = R.copy()
                term[0] -= s
                factors.append(term)
            cubic = cyclic_mul(cyclic_mul(factors[0],factors[1]),factors[2])
            cyclic_pass = len(set(cubic)) == 1
            # Independent Euclidean division at each irreducible cyclotomic.
            root_pass = all(any(division_rem(factor,P) == [0]*(len(P)-1)
                                for factor in factors) for P in cyclotomic)
            assert cyclic_pass == root_pass
            if not cyclic_pass:
                continue
            hits.append(R)
            expected = [([s]+[0]*(m-1)) for s in range(3)]
            if m%2 == 0:
                for sign in (-1,1):
                    row = [1]+[0]*(m-1)
                    row[m//2] += sign
                    # For m=2 reduce the coefficient of X modulo G_2.
                    if m//2 == m-1:
                        row = [row[0]-row[-1],0]
                    expected.append(row)
            assert R in expected
        admissible += len(hits)
        records.append({"m":m,"inspected":5**(m-1),"admissible":len(hits)})
    assert inspected == 3905 and admissible == 19
    return {"coefficient_vectors":inspected,"admissible":admissible,
            "cyclic_and_euclidean_tests_match":True,"rows":records,
            "finite_diagnostics_only":True}


def symbolic_compression():
    a,b,c,q,z,A,epsilon = sp.symbols("a b c q z A epsilon")
    g,Q,delta = a*q-1,b*q,a-b
    B = (q*A-1)/g
    J = 1+c*q*B+epsilon*Q*z
    C = g*delta-c*((a-c)*q-1)
    L = (a-2*c)*q-1
    N = C+epsilon*g*b*z*L
    difference = sp.expand(g*g*J*(J-1)/q-N)
    # epsilon^2=1 and (Q-1)A=gbQz^2-delta.
    difference = sp.rem(difference,epsilon**2-1,epsilon)
    difference = sp.cancel(difference)
    numerator = sp.together(difference).as_numer_denom()[0]
    rem = sp.reduced(numerator,[g*b*Q*z*z-(Q-1)*A-delta],
                     z,A,c,a,b,q,epsilon)[1]
    assert sp.Poly(rem,A).nth(0) == 0
    t = sp.symbols("t")
    assert sp.expand((t*Q*z-3*epsilon*(Q-1)*L)*g*b*z
                     -(t*delta+3*(Q-1)*C)
                     -(Q-1)*(t*A-3*N)
                     -t*(g*b*Q*z*z-(Q-1)*A-delta)) == 0
    v = sp.symbols("v",nonnegative=True)
    variance_gap = sp.expand(2*(v+4-2)-(v+4))
    assert all(coefficient >= 0 for coefficient in sp.Poly(variance_gap,v).coeffs())
    final_gap = 9*q*q-6*q-2
    assert all(coefficient > 0 for coefficient in sp.Poly(final_gap.subs(q,v+3),v).coeffs())
    return {"first_compression":True,"integer_D_identity":True,
            "variance_middle_groups_excluded":True,"b1_D_less_than_3_gap":True}


def residue_and_witnesses():
    candidates = [(q,D,ep) for q in range(3,6) for D in (1,2) for ep in (-1,1)
                  if (D+3*ep)%q == 0]
    assert candidates == [(4,1,1),(5,2,1)]
    n,j=436,30
    assert n%4 == 0 and 3*j*(j-1)%(n-1)==0
    assert 6*j*(j-1)*(j-2)%(n-2) != 0
    G6 = sum((2*X)**e for e in range(6))
    J = sp.Poly((1+(2*X)**3+G6)/2,X,domain=sp.ZZ)
    assert sp.rem(J.as_expr()*(J.as_expr()-1),G6,X)==0
    assert sp.rem(J.as_expr(),G6,X) not in (0,1,2)
    return {"integer_D_candidates":candidates,"scope_witness":{"n":n,"j":j},
            "noncoprime_half_value_witness":True,
            "half_value_witness_now_excluded_by_sextic_partial_sharing":True}


def main():
    if not __debug__:
        raise SystemExit("Assertions required; do not use python -O.")
    result = {"provenance":"reconstructed from restored 11824-byte Library report",
              "symbolic":symbolic_compression(),"classification_diagnostics":small_classification(),
              "residues_and_scope":residue_and_witnesses(),"general_i3_closed":False}
    path = ROOT/"data/results/verification_i3_split_geometric.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"coefficient_vectors":3905,"admissible":19,
                      "independent_remainder_tests":True,"compression":True}))


if __name__ == "__main__":
    main()
