"""Exact checks for adjacent-resultant bounds and the geometric-family proof.

Universal statements are proved in the accompanying note. Finite diagnostics
are not an exhaustive search for counterexamples to Erdos problem 699.
"""

import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
X = sp.symbols("X")


def poly(expression):
    return sp.Poly(expression, X, domain=sp.ZZ)


def primitive_positive(A):
    A = A.primitive()[1]
    return -A if A.LC() < 0 else A


def unshared_part(A, P):
    """Remove entire primary factors shared with P, without factorization."""
    V = primitive_positive(A)
    rounds = 0
    while True:
        D = primitive_positive(sp.gcd(V, P))
        if D.degree() == 0:
            return V, rounds
        V = V.exquo(D)
        rounds += 1
        assert rounds <= A.degree()


def factorization_unshared(A, P):
    answer = poly(1)
    for factor, exponent in A.factor_list()[1]:
        if sp.gcd(factor, P).degree() == 0:
            answer *= factor**exponent
    return primitive_positive(answer)


def sylvester_resultant(A, B):
    # Independent of SymPy's resultant algorithm and argument ordering.
    a, b = A.all_coeffs(), B.all_coeffs()
    d, k = A.degree(), B.degree()
    rows = []
    for shift in range(k):
        rows.append([0]*shift + a + [0]*(k-1-shift))
    for shift in range(d):
        rows.append([0]*shift + b + [0]*(d-1-shift))
    return int(sp.Matrix(rows).det())


def resultant(A, B):
    # Explicit ordering avoids the swapped-degree sign convention in Poly.
    if A.degree() < B.degree():
        return int((-1)**(A.degree()*B.degree()) * B.resultant(A))
    return int(A.resultant(B))


def digits(value, base):
    answer = []
    while value:
        answer.append(value % base)
        value //= base
    return answer or [0]


def digit_poly(value, base):
    return poly(sum(c*X**i for i, c in enumerate(digits(value, base))))


def coefficient_norm(A):
    return sum(abs(int(c)) for c in A.all_coeffs())


def audit_primary_parts():
    factors = [poly(X), poly(2*X-1), poly(X+1),
               poly(X**2+X+1), poly(X**2+1)]
    cases, multiple_rounds = 0, 0
    for exponents in product((1, 2, 3), repeat=3):
        for mask in range(8):
            A = poly(6)
            P = factors[3]
            for i, e in enumerate(exponents):
                A *= factors[i]**e
                if mask & (1 << i):
                    P *= factors[i]
            A *= factors[4]**2
            U, rounds = unshared_part(A, P)
            assert U == factorization_unshared(A, P)
            assert A.rem(U).is_zero
            assert sp.gcd(U, P).degree() == 0
            cases += 1
            multiple_rounds += rounds > 1

    A = poly(7*(2*X-1)**4*(X+1)**3*(X**2+X+1)**2)
    P = poly((2*X-1)*(X+1)**2)
    naive = primitive_positive(A).exquo(primitive_positive(sp.gcd(A, P)))
    assert sp.gcd(naive, P).degree() > 0
    assert resultant(naive, P) == 0
    U, rounds = unshared_part(A, P)
    assert U == poly((X**2+X+1)**2)
    assert resultant(U, P) != 0 and rounds == 4
    return {"factorization_comparisons": cases,
            "cases_requiring_multiple_gcd_rounds": multiple_rounds,
            "single_gcd_is_insufficient": True,
            "retained_unshared_multiplicity": 2}


def audit_norms():
    cases = 0
    for H in range(2, 61):
        for e in (0, 1):
            for S in range(e, H+e):
                norms = [abs(e-s)+S-e for s in range(3)]
                assert math.prod(norms[:2]) <= H*(H-1)
                assert math.prod(norms) <= (H-1)*H*(H+1)
                cases += 1
        assert H*(H-1) >= 2*H-2
    return {"coefficient_norm_comparisons": cases}


def audit_local_case(n, j, q):
    assert 4 <= j <= n//2
    assert 3*j*(j-1) % (n-1) == 0
    assert 6*j*(j-1)*(j-2) % (n-2) == 0
    F, J = digit_poly(n, q), digit_poly(j, q)
    assert F.nth(0) == 1
    assert all(0 <= J.nth(i) <= F.nth(i)
               for i in range(F.degree()+1))
    m, b, H = F.degree(), J.degree(), int(F.eval(1))
    assert 1 <= b <= m
    degrees, results, values, eta_options = [], [], [], []
    determinant_count = 0
    for ell in (1, 2):
        P = poly(1)
        for s in range(ell+1):
            P *= J-s
        U, _ = unshared_part(F-ell, P)
        assert U == factorization_unshared(F-ell, P)
        r = U.degree()
        assert ell == 1 or r >= 1
        Rs = [resultant(U, J-s) for s in range(ell+1)]
        for s, R in enumerate(Rs):
            assert R == sylvester_resultant(U, J-s)
            determinant_count += 1
            assert R != 0
        Rprod = math.prod(Rs)
        assert Rprod == resultant(U, P)
        value = int(U.eval(q))
        assert value and (n-ell) % value == 0
        assert (3 if ell == 1 else 6)*Rprod % value == 0
        if r:
            M_cap = H-1 if ell == 1 else H
            norm_cap = H*(H-1) if ell == 1 else (H-1)*H*(H+1)
            assert abs(Rprod) <= M_cap**((ell+1)*b)*norm_cap**r
            coefficient = 6 if ell == 1 else 12
            assert (q-1)**r <= coefficient*M_cap**((ell+1)*b)*norm_cap**r
            if q >= 2*H-1:
                assert 2*abs(value) >= (q-1)**r
            eta_options.append(Fraction((ell+1)*b, r))
        degrees.append(r)
        results.append(Rprod)
        values.append(value)
    assert math.gcd(*values) == 1
    assert 18*math.prod(results) % math.prod(values) == 0
    positive_factors = [g for g, e in (F-2).factor_list()[1]
                        if g.eval(0) < 0 and g.eval(1) >= 0]
    assert len(positive_factors) == 1
    d = positive_factors[0].degree()
    assert degrees[1] >= d
    eta = min(eta_options)
    assert eta <= Fraction(3*m, d)
    # Raise the fractional-exponent bound to an integer power.
    exponent = eta + 3
    assert q**exponent.denominator < (
        13**exponent.denominator*(H+2)**exponent.numerator)
    return {"n": n, "j": j, "q": q, "n_mod_4": n % 4,
            "m": m, "b": b, "H": H, "r1": degrees[0], "r2": degrees[1],
            "positive_factor_degree": d,
            "eta": [eta.numerator, eta.denominator],
            "resultant_products": results,
            "unshared_part_values": values,
            "sylvester_determinants": determinant_count,
            "scope": "Both integer divisibilities and one radix's digits only."}


def audit_numerical_diagnostics():
    inputs = [(76672, 26775, 1217),
              (3258244432, 1087547175, 19),
              (1004566, 501415, 5),
              (11603334, 5798717, 7),
              (433633542, 216798737, 11),
              (1683743062, 841835995, 13)]
    cases = [audit_local_case(*case) for case in inputs]
    assert all(case["n_mod_4"] == 2 for case in cases[2:])
    return {"local_cases": cases,
            "sylvester_determinants": sum(c["sylvester_determinants"]
                                         for c in cases),
            "true_counterexamples_asserted": 0}


def audit_family_polynomials():
    a, c = sp.symbols("a c")
    cases = 0
    for m in (3, 4, 5, 8, 12, 20):
        G = sum(X**i for i in range(m))
        A = (a-1)*G+X**(m-1)
        F, J = 2+(a*X-1)*G, c*X*G
        assert sp.expand(F-1-X*A) == 0
        assert sp.expand((a*X-1)*(J-1)-c*X**2*A
                         +(a+c)*X-1) == 0
        assert sp.expand((X-1)*A-(a*X-1)*X**(m-1)+(a-1)) == 0
        cases += 3

    allocations = []
    for m, a0, c0 in ((3, 2, 1), (8, 3, 1), (12, 7, 6), (20, 2, 1)):
        G = sum(X**i for i in range(m))
        A = poly((a0-1)*G+X**(m-1))
        F, J = poly(2+(a0*X-1)*G), poly(c0*X*G)
        for JJ in (J, F-J):
            U1, _ = unshared_part(F-1, JJ*(JJ-1))
            U2, _ = unshared_part(F-2, JJ*(JJ-1)*(JJ-2))
            assert U1 == A and U2 == poly(a0*X-1)
            assert min(Fraction(2*m, U1.degree()),
                       Fraction(3*m, U2.degree())) <= 3
            allocations.append({"m": m, "a": a0, "c": c0,
                                "complement": JJ == F-J,
                                "r1": U1.degree(), "r2": U2.degree()})
    assert sp.factor((a+1)**2-(6*a-9+3/a)
                     -((a-2)**2+6-3/a)) == 0
    return {"symbolic_family_identities": cases+1,
            "unshared_degree_diagnostics": allocations}


def audit_cubic_reduction():
    a, c, q, t, h, z = sp.symbols("a c q t h z")
    A = a*q*q+(a-1)*q+(a-1)
    E = (3*h*c*c+3*(h-t)*a*c-t*t*a*a
         +(t*t-t*h)*a+t*h-h*h)
    q_expression = (t*(a-1)+3*c)/h
    # Elimination identity, including its exact nonzero factor.
    assert sp.expand(h*h*(t*A-3*c*((a+c)*q-1))
                     .subs(q, q_expression) + (t*(a-1)+3*c)*E) == 0
    assert sp.expand(E.subs(c, 0)
                     +t*t*a*(a-1)+t*h*(a-1)+h*h) == 0
    edge_allowed = {1: {1, 2, 3}, 2: {2, 3, 4}, 3: {4, 5},
                    4: {5, 6}, 5: {7}}
    threshold_expected = {
        (1, 2): 2*(a*a+2*a-2),
        (1, 3): 3*(7*a*a+4*a-5),
        (2, 4): 8*(2*a*a+4*a-1),
        (3, 5): 5*(a*a+12*a+3),
    }
    expected_discriminants = {
        (1, 1): 12*a*a,
        (2, 2): 96*a*a,
        (2, 3): 9*(17*a*a+8*a+12),
        (3, 4): 441*a*a+144*a+192,
        (4, 5): 969*a*a+240*a+300,
        (4, 6): 36*(33*a*a+16*a+24),
        (5, 7): 2136*a*a+840*a+1176,
    }
    certificates, retained = [], []
    for tt in range(1, 6):
        for hh in range(1, tt+3):
            E0 = E.subs({t: tt, h: hh})
            edge = sp.expand(E0.subs(c, a))
            shifted = sp.Poly(edge.subs(a, z+2), z)
            record = {"t": tt, "h": hh, "edge": str(edge)}
            if hh not in edge_allowed[tt]:
                assert all(v <= 0 for v in shifted.all_coeffs())
                record["excluded_by"] = "E(a,a) <= 0 for a >= 2"
                record["shifted_edge_coefficients"] = [
                    int(v) for v in shifted.all_coeffs()]
            elif (tt, hh) in threshold_expected:
                c0 = ((hh-tt)*a+tt)/3
                assert hh > tt
                threshold = sp.expand(3*E0.subs(c, c0))
                assert sp.expand(threshold-threshold_expected[tt, hh]) == 0
                coefficients = sp.Poly(threshold.subs(a, z+2), z).all_coeffs()
                assert all(v > 0 for v in coefficients)
                record["excluded_by"] = "positive threshold beyond positive root"
                record["threshold"] = str(threshold)
                record["shifted_threshold_coefficients"] = [
                    int(v) for v in coefficients]
            else:
                D = sp.discriminant(E0, c)
                assert sp.expand(D-expected_discriminants[tt, hh]) == 0
                record["discriminant"] = str(sp.factor(D))
                retained.append((tt, hh))
            certificates.append(record)
    assert set(retained) == set(expected_discriminants)

    for pair in ((2, 3), (4, 5)):
        for residue in (1, 3, 5, 7):
            assert int(expected_discriminants[pair].subs(a, residue)) % 8 == 5
    for residue in range(16):
        assert int(expected_discriminants[5, 7].subs(a, residue)) % 16 == 8
    D = expected_discriminants[3, 4]
    assert sp.expand(D-(21*a+3)**2-18*a-183) == 0
    assert sp.expand((21*a+4)**2-D-24*a+176) == 0
    small = [int(D.subs(a, aa)) for aa in range(2, 8)]
    assert small == [2244, 4593, 7824, 11937, 16932, 22809]
    assert all(math.isqrt(v)**2 != v for v in small)
    assert sp.expand((33*a+8)**2
                     -33*(33*a*a+16*a+24)+728) == 0
    residue_cases = 0
    for xx, yy in product(range(7), repeat=2):
        if (xx*xx-33*yy*yy) % 7 == 0:
            assert xx == yy == 0
        residue_cases += 1
    assert 728 % 7 == 0 and 728 % 49 != 0
    assert sp.cancel((a*a-4*a+10-3/a).subs(a, z+2)
                     -z*z-6+3/(z+2)) == 0
    return {"elimination_identities": 2, "all_25_pair_certificates": certificates,
            "retained_pairs": retained, "small_discriminants": small,
            "mod_8_comparisons": 8, "mod_16_comparisons": 16,
            "mod_7_pair_comparisons": residue_cases,
            "unbounded_sign_and_square_comparison_proof_in_note": True}


def audit_family_integers():
    cases, first_passes = 0, 0
    for a in range(2, 23):
        for c in range(1, a):
            for q in range(a+1, a+11):
                for m in range(3, 11):
                    G = (q**m-1)//(q-1)
                    A = (a-1)*G+q**(m-1)
                    n, J = q*A+1, c*q*G
                    assert math.gcd(A, G) == 1
                    assert (a*q-1)*(J-1) == c*q*q*A-((a+c)*q-1)
                    j = min(J, n-J)
                    assert 4 <= j <= n//2
                    first = 3*J*(J-1) % (n-1) == 0
                    assert first == (3*j*(j-1) % (n-1) == 0)
                    if first:
                        assert 3*c*((a+c)*q-1) % A == 0
                        assert m == 3 and a % 2 == 0 and n % 2 == 1
                        first_passes += 1
                    if m >= 4:
                        assert not first
                    cases += 1
    a, c, q = 382, 199, 453
    G = 1+q+q*q
    A = (a-1)*G+q*q
    n, J = q*A+1, c*q*G
    j = min(J, n-J)
    assert (n, j) == (35588953837, 17049051376)
    assert 3*j*(j-1) % (n-1) == 0
    assert n % 2 == 1 and 6*j*(j-1)*(j-2) % (n-2) != 0
    assert (3*c*((a+c)*q-1)//A,
            (2*(a-1)+3*c)//q) == (2, 3)
    return {"finite_supplementary_cases": cases,
            "first_condition_passes_in_small_box": first_passes,
            "sharp_scope_example": {"a": a, "c": c, "q": q,
                                   "n": n, "j": j, "t": 2, "h": 3,
                                   "n_mod_4": n % 4,
                                   "second_condition": False},
            "universal_proof_uses_no_parameter_cutoff": True}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled; do not use python -O.")
    output = {
        "scope": "Two adjacent necessary-condition bounds. Geometric family "
                 "a>=2, 1<=c<a, m>=3, q>a: every evaluation and its complement "
                 "excluded as an i=3 counterexample. General i=3 remains open.",
        "primary_parts": audit_primary_parts(),
        "norms": audit_norms(),
        "numerical_diagnostics": audit_numerical_diagnostics(),
        "family_polynomials": audit_family_polynomials(),
        "cubic_reduction": audit_cubic_reduction(),
        "family_integers": audit_family_integers(),
        "new_fully_resolved_indices": 0,
    }
    path = ROOT / "data/results/verification_i3_adjacent_resultants.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n",
                    encoding="utf-8")
    print("PASS adjacent-resultant bounds and geometric-family certificates.")
    print("General i=3 remains unresolved.")


if __name__ == "__main__":
    main()
