"""Exact audit of the quadratic-cofactor exclusion, including its finite tail.

The universal inequalities are proved in the companion note. The finite tail
is the *derived* complete domain m=6, 3<=q<=12, not a diagnostic search box.
Forward and backward enumerators do not call each other. Assertions required.
"""

import json
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent


def equal(left, right=0):
    assert sp.cancel(left-right) == 0


def horner(coefficients, q):
    value = 0
    for coefficient in reversed(coefficients):
        value = value*q+coefficient
    return value


def symbolic_audit():
    a, b, c, d, q, theta, A = sp.symbols("a b c d q theta A")
    g, k = a*q-1, b*q+1
    h = c*q+d*q*q-theta
    R0 = a*b*q+a-b
    V = c+d*q-theta*R0
    C = -V*(g*k-q*V)
    BP = (q*A-1)/(g*k)
    JP = theta+1+h*BP
    equal(g*g*k*k*JP*(JP-1)/q-C,
          A*(q*h*h*A+h*(g*k-2*q*V)))
    f, x = sp.symbols("f x")
    equal(V.subs(c, x+theta*(a-b-f)), x+d*q-theta*(f+a*b*q))
    equal(g*k-q*V, -1+q*(R0-V))
    u, y = sp.symbols("u y", nonnegative=True)
    # (t+1)^2/t is increasing for t>=2.
    equal(((u+2)+1)**2/(u+2), u+4+1/(u+2))
    equal((y+1)**2/y-(u+3)**2/(u+2),
          (y-(u+2))*(1-1/(y*(u+2))))
    bounds = {str(m): [12, (qv-1)*qv**(m-6)]
              for m, qv in ((8, 3), (7, 4), (6, 13))}
    assert all(Fraction(*entry) <= 1 for entry in bounds.values())
    # The one leftover m=7,q=3 would require D=G_7 and D(-1)=1.
    assert sum((-1)**e for e in range(7)) == 1
    # Additional result of this turn: s=1 closes already at m>=5.
    negative_gap = 4*q**3-3*(q-1)*(q+1)**2
    positive_gap = q**3-3*(q*q-q+1)
    equal(negative_gap,(q-1)**3+4)
    equal(positive_gap,(q-1)**3-2)
    assert all(v > 0 for v in sp.Poly(positive_gap.subs(q,y+3),y).coeffs())
    return {"compression_identity": True, "digit_reduction_of_V": True,
            "nonzero_mod_q_factor": True, "strict_ratio_bound":
            "|3C|/A < 12/((q-1)*q**(m-6))", "thresholds": bounds,
            "degree_7_radix_3_negative_root_impossible": True,
            "new_degree_5_s1_extension":{
                "F1_le_a_minus_1_from_positive_D1":True,
                "negative_C_ratio":"<3*(q-1)*(q+1)**2/(4*q**3)<1",
                "positive_C_ratio":"<3*(q*q-q+1)/q**3<1",
                "exact_positive_gaps":[str(negative_gap),str(positive_gap)]}}


def convert_D(a, b, coefficients):
    """D=(1+bX)B; B may have negative coefficients."""
    B = [1]
    for value in coefficients[1:-1]:
        B.append(value-b*B[-1])
    if b*B[-1] != coefficients[-1]:
        return None
    F = [1]+[a*coefficients[e-1]-coefficients[e]
             for e in range(1, len(coefficients))]+[a*coefficients[-1]]
    return tuple(B), tuple(F)


def forward_profiles(q, m=6):
    profiles, terminal = set(), 0
    for a in range(2, q):
        for b in range(1, a+1):
            if a*b >= q:
                continue
            upper = [0]*m
            upper[-1] = (q-1)//a
            for e in range(m-1, 0, -1):
                upper[e-1] = (q-1+upper[e])//a

            def walk(D):
                nonlocal terminal
                e = len(D)
                if e == m:
                    terminal += 1
                    converted = convert_D(a, b, D)
                    if converted is not None:
                        B, F = converted
                        assert all(0 <= value < q for value in F)
                        profiles.add((a, b, tuple(D), B, F))
                    return
                lo = max(1, a*D[-1]-(q-1))
                hi = min(a*D[-1], upper[e])
                for value in range(lo, hi+1):
                    walk(D+[value])

            walk([1])
    return profiles, terminal


def backward_profiles(q, m=6):
    profiles, terminal = set(), 0
    for a in range(2, q):
        for b in range(1, a+1):
            if a*b >= q:
                continue

            def walk(reverse_D):
                nonlocal terminal
                if len(reverse_D) == m:
                    if reverse_D[-1] != 1:
                        return
                    terminal += 1
                    D = tuple(reversed(reverse_D))
                    # Independent rational-root test, with no polynomial division.
                    if sum(value*(-1)**e*b**(m-1-e)
                           for e, value in enumerate(D)):
                        return
                    converted = convert_D(a, b, D)
                    assert converted is not None
                    B, F = converted
                    profiles.add((a, b, D, B, F))
                    return
                value = reverse_D[-1]
                lo = max(1, (value+a-1)//a)
                hi = (value+q-1)//a
                for previous in range(lo, hi+1):
                    walk(reverse_D+[previous])

            for lead in range(1, (q-1)//a+1):
                walk([lead])
    return profiles, terminal


def quotient_cases(q, profile):
    a, b, D, B, F = profile
    n = horner(F, q)
    count = 0
    for x, d, theta in product(range(F[1]+1), range(a*b+1), (-1, 0, 1)):
        c = x+theta*B[1]
        J = [1]
        for e in range(1, len(F)):
            at = lambda k: B[k] if 0 <= k < len(B) else 0
            J.append(c*at(e-1)+d*at(e-2)-theta*at(e))
        if any(not 0 <= j <= f for j, f in zip(J, F)):
            continue
        j = horner(J, q)
        if min(j, n-j) < 4:
            continue
        count += 1
        assert (3*j*(j-1)) % (n-1) != 0
        # Independent convolution and power evaluation.
        JJ = [0]*len(F)
        for e, value in enumerate(B):
            for shift, coefficient in enumerate((-theta, c, d)):
                JJ[e+shift] += value*coefficient
        JJ[0] += theta+1
        assert JJ == J
        assert sum(v*q**e for e, v in enumerate(JJ)) == j
        assert sum(v*q**e for e, v in enumerate(F)) == n
        A = (n-1)//q
        g, k = a*q-1, b*q+1
        h = c*q+d*q*q-theta
        V = c+d*q-theta*(a*b*q+a-b)
        C = -V*(g*k-q*V)
        assert j*(j-1) % q == 0
        assert g*g*k*k*(j*(j-1)//q)-C == (
            A*(q*h*h*A+h*(g*k-2*q*V)))
    return count


def finite_tail():
    expected = {3:(1,8), 4:(7,44), 5:(21,111), 6:(35,251), 7:(59,419),
                8:(92,897), 9:(126,1288), 10:(166,1977), 11:(220,3130),
                12:(266,4183)}
    rows, total_terminal, negative = [], 0, 0
    for q in range(3, 13):
        forward, f_terminal = forward_profiles(q)
        backward, b_terminal = backward_profiles(q)
        assert forward == backward
        assert f_terminal == b_terminal
        total_terminal += f_terminal
        cases = sum(quotient_cases(q, profile) for profile in sorted(forward))
        assert (len(forward), cases) == expected[q]
        negatives = sum(any(v < 0 for v in profile[3]) for profile in forward)
        negative += negatives
        rows.append({"q":q, "factor_profiles":len(forward),
                     "nontrivial_coefficient_cases":cases,
                     "negative_B_profiles":negatives,
                     "terminal_D_sequences":f_terminal, "first_hits":0})
    assert sum(row["factor_profiles"] for row in rows) == 993
    assert sum(row["nontrivial_coefficient_cases"] for row in rows) == 12308
    assert total_terminal == 9369 and negative == 98
    witness = convert_D(2, 1, [1,1,2,1,1,2])
    assert witness == ((1,0,2,-1,2), (1,1,0,3,1,0,4))
    return {"derived_complete_domain":"m=6,3<=q<=12",
            "two_enumerators_match":True, "factor_profiles":993,
            "nontrivial_coefficient_cases":12308, "first_hits":0,
            "terminal_D_sequences":total_terminal, "negative_B_profiles":negative,
            "rows":rows, "negative_cofactor_example":{"q":5,"a":2,"b":1,
            "D":[1,1,2,1,1,2],"B":list(witness[0]),"F":list(witness[1])}}


def degree5_diagnostic():
    """Small frontier diagnostic; not a universal s=0,2 proof."""
    profiles = cases = 0
    for q in range(3,25):
        rows,_ = forward_profiles(q,m=5)
        profiles += len(rows)
        cases += sum(quotient_cases(q,row) for row in sorted(rows))
    assert (profiles,cases) == (2976,92954)
    return {"domain":"m=5,3<=q<=24; diagnostic only", "profiles":profiles,
            "cases":cases,"first_hits":0,"s0_s2_universal_exclusion_proved":False}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled; do not use python -O.")
    result = {"scope":"arbitrary quadratic cofactor: all s for m>=6; s=1 for m>=5; general i=3 open",
              "symbolic":symbolic_audit(), "finite_tail":finite_tail(),
              "degree5_diagnostic":degree5_diagnostic()}
    target = ROOT/"data/results/verification_i3_quadratic_cofactor.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"symbolic":True, "profiles":993, "cases":12308,
                      "first_hits":0, "independent_enumerators":2}))


if __name__ == "__main__":
    main()
