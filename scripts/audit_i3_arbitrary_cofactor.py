"""Replay exact certificates for the arbitrary-cofactor numerical exclusion.

The note proves the reductions for unbounded integer parameters. Congruence
certificates cover all integers; numerical examples below are diagnostics only.
General i=3 in Erdos problem 699 remains unresolved.
"""

import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp

from audit_i3_adjacent_resultants import audit_cubic_reduction

ROOT = Path(__file__).resolve().parent.parent
X = sp.symbols("X")
A, C, Q, B, D, T, H = sp.symbols("a c q b d t h")

# (b, d, t, h, modulus). Every modulus includes the original condition mod 4.
MODULAR_ROWS = (
    (1, 1, 1, 1, 4), (1, 1, 1, 2, 4), (1, 1, 1, 3, 4),
    (1, 1, 1, 4, 8), (1, 1, 2, 1, 4), (1, 1, 2, 2, 8),
    (1, 1, 2, 3, 4), (1, 1, 3, 1, 12), (1, 1, 3, 2, 4),
    (1, 1, 4, 1, 4), (2, 1, 1, 1, 4), (2, 1, 1, 2, 4),
    (2, 1, 2, 1, 4), (3, 1, 1, 1, 4), (4, 1, 1, 1, 4),
    (1, 2, 1, 2, 4), (2, 2, 1, 2, 8),
)
SIGN_ROWS = ((1, 2, 1, 1), (2, 2, 1, 1))


def equal(left, right=0):
    assert sp.cancel(left-right) == 0


def signed_certificate(expression, variables, sign):
    """Strict sign for every nonnegative value of the shifted variables."""
    P = sp.Poly(sp.cancel(expression), *variables)
    assert all(sign*v >= 0 for v in P.coeffs())
    assert sign*P.coeff_monomial(1) > 0
    return [{"powers": list(powers), "coefficient": int(coefficient)}
            for powers, coefficient in P.terms()]


def cofactor_forms(a, coefficients, c, form):
    BP = sum(v*X**k for k, v in enumerate(coefficients))
    F = sp.Poly(2+(a*X-1)*BP, X, domain=sp.ZZ)
    if form == "I":
        J = sp.Poly(c*X*BP, X, domain=sp.ZZ)
    elif form == "II":
        J = sp.Poly(1+c*X*BP, X, domain=sp.ZZ)
    else:
        assert form == "III"
        J = sp.Poly((1+c*X)*BP, X, domain=sp.ZZ)
    return sp.Poly(BP, X, domain=sp.ZZ), F, J


def integer_digits(n, q):
    digits = []
    while n:
        digits.append(n % q)
        n //= q
    return digits or [0]


def audit_arbitrary_identities():
    K = sp.symbols("K")
    BP = 1+X*K  # An arbitrary cofactor with constant coefficient 1.
    F = 2+(A*X-1)*BP
    AP = A+(A*X-1)*K
    equal(F-1, X*AP)
    equal(X*AP, (A*X-1)*BP+1)
    # These two identities certify the two evaluation gcds, including
    # nonmonic B: a common integer divisor must divide 1.
    equal(X*AP-(A*X-1)*BP, 1)
    J1 = C*X*BP
    J2 = 1+C*X*BP
    J3 = (1+C*X)*BP
    equal((A*X-1)*(J1-1), C*X**2*AP-((A+C)*X-1))
    equal((A*X-1)*J2, C*X**2*AP+((A-C)*X-1))
    equal((A*X-1)*(J3-1), X*((C*X+1)*AP-(A+C)))

    quotient_rows = []
    normal_pairs = {(0, 0): "I", (1, 1): "II", (0, 1): "III"}
    for s, e in product(range(3), range(2)):
        J = s+(C*X+e-s)*BP
        complementary = 2-s+((A-C)*X+(1-e)-(2-s))*BP
        equal(F-J, complementary)
        if (s, e) in normal_pairs:
            key, complemented = (s, e), False
        else:
            key, complemented = (2-s, 1-e), True
        assert key in normal_pairs
        quotient_rows.append({"s": s, "e": e,
                              "normal_form": normal_pairs[key],
                              "complemented": complemented})
    assert len(quotient_rows) == 6
    # Preservation of the first integer divisibility under j -> n-j.
    n, j = sp.symbols("n j")
    equal((n-j)*(n-j-1)-j*(j-1), (n-1)*(n-2*j))
    equal(3*A/4-3*C*(A-C)/A, 3*(A-2*C)**2/(4*A))
    return {"arbitrary_B_encoded_as": "B=1+X*K; K unrestricted",
            "normal_forms_cover_all_s_e": quotient_rows,
            "integer_gcds_certified_by_identity": ["gcd(A(q),B(q))=1",
                                                   "gcd(A(q),a*q-1)=1"],
            "first_divisibility_complement_identity": True,
            "three_quotient_identities": True}


def audit_unbounded_signs_and_reductions():
    z, u, v = sp.symbols("z u v", nonnegative=True)
    gap1 = A*((A+1)**2-(6*A-9+3/A))
    gap3 = A*((A+1)**2-6*(A-1)**2/A)
    equal(gap1, A*((A-2)**2+6-3/A))
    equal(gap3, A*((A-2)**2+9-6/A))
    certificates = {
        "I_degree_at_least_4_gap_a_ge_2": signed_certificate(
            gap1.subs(A, z+2), (z,), 1),
        "III_degree_at_least_4_gap_a_ge_3": signed_certificate(
            gap3.subs(A, z+3), (z,), 1),
    }
    e1d2 = 3*C**2-3*A*C-2*A**2+A*B+1
    equal(e1d2.subs(C, A-B), -2*A**2-2*A*B+3*B**2+1)
    e1b2 = 3*C**2-3*A*C-4*A**2+4*A+1
    equal(e1b2.subs(C, A), -4*A**2+4*A+1)
    e3d2 = 3*C**2-3*A*C-4*A**2-3*A*B+3
    equal(e3d2.subs(C, A-2*B), -4*A**2-9*A*B+12*B**2+3)
    for name, expr in (
        ("I_d2_constant", e1d2.subs(C, 0)),
        ("I_d2_upper", e1d2.subs(C, A-B)),
    ):
        certificates[name] = signed_certificate(
            expr.subs(A, B+v+1).subs(B, u+1), (u, v), -1)
    for name, expr in (
        ("I_b2_t2_h1_constant", e1b2.subs(C, 0)),
        ("I_b2_t2_h1_upper", e1b2.subs(C, A)),
    ):
        certificates[name] = signed_certificate(expr.subs(A, z+3), (z,), -1)
    for name, expr in (
        ("III_d2_h1_constant", e3d2.subs(C, 0)),
        ("III_d2_h1_upper", e3d2.subs(C, A-2*B)),
    ):
        certificates[name] = signed_certificate(
            expr.subs(A, 2*B+v+1).subs(B, u+1), (u, v), -1)

    # Complete finite consequences of the proved strict inequalities.
    # tb<6 bounds both b,t by 5; h bounds then give a finite exact set.
    i_pairs = {(bb, tt, hh) for bb, tt, hh in product(range(1, 6), repeat=3)
               if tt*bb < 6 and hh*bb < tt+3}
    nong = {(bb, tt, hh) for bb, tt, hh in i_pairs if bb != 1}
    assert nong == {(2, 1, 1), (2, 2, 1), (2, 2, 2), (3, 1, 1)}
    d1 = {(bb, 1, tt, hh)
          for bb, tt, hh in product(range(1, 6), repeat=3)
          if tt*bb < 6 and hh*bb < 6-tt}
    d2 = {(bb, 2, 1, hh) for bb, hh in product((1, 2), repeat=2)}
    assert len(d1) == 15 and len(d2) == 4
    modular = {row[:4] for row in MODULAR_ROWS}
    signs = set(SIGN_ROWS)
    assert len(modular) == 17 and len(signs) == 2
    assert not modular & signs
    assert d1 | d2 == modular | signs
    # h<=0 in III would require t=4,5; the proved bound contradicts t.
    h_nonpositive_gaps = {tt: Fraction(tt)-Fraction(tt*(tt-3), 3)
                          for tt in (4, 5)}
    assert all(gap > 0 for gap in h_nonpositive_gaps.values())
    return {"strict_sign_certificates_for_nonnegative_shifted_variables":
            certificates,
            "I_d1_non_geometric_pairs": sorted(nong),
            "III_d1_pairs": sorted(d1), "III_d2_pairs": sorted(d2),
            "III_all_19_pairs_covered_once": True,
            "III_h_nonpositive_contradiction_gaps":
            {str(tt): [gap.numerator, gap.denominator]
             for tt, gap in h_nonpositive_gaps.items()},
            "parameter_cutoffs_in_universal_proof": False}


def cubic_expressions():
    AP = A*D*Q**2+(A*B-D)*Q+A-B
    EI = (3*H*C**2+3*A*(H-D*T)*C-T**2*A**2*D
          +(T**2*D*B-T*H*B)*A+T*H*D-H**2)
    EIII = (3*H*C**2+3*A*(H-D*T)*C+A**2*D*T*(T-3)
            -A*B*T*(D*T+H)+D*H*T+H**2)
    return AP, EI, EIII


def audit_eliminations():
    AP, EI, EIII = cubic_expressions()
    LI, LIII = T*(A-B)+3*C, (3-T)*A+T*B+3*C
    RI, RIII = 3*C*((A+C)*Q-1), 3*(A+C)*(C*Q+1)
    equal(H**2*(T*AP-RI).subs(Q, LI/H), -LI*EI)
    equal(H**2*(T*AP-RIII).subs(Q, LIII/H), -LIII*EIII)
    for rem in (T*AP-RI, T*AP-RIII):
        # Reduction mod q proves that h is an integer.
        expected = LI if rem == T*AP-RI else -LIII
        equal(rem.subs(Q, 0), expected)
    equal(EI.subs({D: 2, T: 1, H: 1}),
          3*C**2-3*A*C-2*A**2+A*B+1)
    equal(EIII.subs({D: 2, T: 1, H: 1}),
          3*C**2-3*A*C-4*A**2-3*A*B+3)
    expected = {(2, 1, 1): 3*C**2-A**2,
                (2, 2, 1): 3*C**2-3*A*C-4*A**2+4*A+1,
                (2, 2, 2): 6*C**2-4*A**2,
                (3, 1, 1): 3*C**2-A**2}
    for (bb, tt, hh), expression in expected.items():
        equal(EI.subs({B: bb, D: 1, T: tt, H: hh}), expression)
    geometric = (3*H*C**2+3*(H-T)*A*C-T**2*A**2
                 +(T**2-T*H)*A+T*H-H**2)
    equal(EI.subs({B: 1, D: 1}), geometric)
    return {"I_exact_elimination": str(EI),
            "III_exact_elimination": str(EIII),
            "multipliers_are_minus_L_with_L_equals_hq_positive": True,
            "I_remaining_square_equations_excluded_by_odd_3_valuation": True,
            "geometric_remainder_is_exact_previous_equation": True}


def eval_conic(a, c, b, d, t, h):
    return (3*h*c*c+3*a*(h-d*t)*c+a*a*d*t*(t-3)
            -a*b*t*(d*t+h)+d*h*t+h*h)


def audit_complete_congruences():
    _, _, expression = cubic_expressions()
    records = []
    total = 0
    for b, d, t, h, modulus in MODULAR_ROWS:
        assert modulus % 4 == 0
        conic = sp.Poly(expression.subs({B: b, D: d, T: t, H: h}), A, C)
        # Independent polynomial evaluator from the expanded symbolic terms.
        terms = [(powers, int(coefficient)) for powers, coefficient in conic.terms()]
        quadratic_pairs, linear_triples, survivors = 0, 0, []
        for a, c in product(range(modulus), repeat=2):
            E = eval_conic(a, c, b, d, t, h)
            alternate = sum(v*a**i*c**j for (i, j), v in terms)
            assert E == alternate
            if E % modulus == 0:
                quadratic_pairs += 1
            for q in range(modulus):
                total += 1  # Count every point in the full residue cube.
                L = (3-t)*a+t*b+3*c
                if E % modulus or (L-h*q) % modulus:
                    continue
                linear_triples += 1
                n = 2+(a*q-1)*(1+b*q+d*q*q)
                if n % 4 == 0:
                    survivors.append([a, c, q])
        assert not survivors, (b, d, t, h, modulus, survivors)
        records.append({"b": b, "d": d, "t": t, "h": h,
                        "modulus": modulus,
                        "all_residue_triples": modulus**3,
                        "conic_residue_pairs": quadratic_pairs,
                        "after_conic_and_linear_relation": linear_triples,
                        "after_n_mod_4_zero": 0})
    assert total == 4096 and len(records) == 17
    return {"all_17_certificates": records, "all_residue_triples": total,
            "all_integer_solutions_covered_by_residue_projection": True}


def local_diagnostic(a, coefficients, c, q, form):
    BP, F, JP = cofactor_forms(a, coefficients, c, form)
    assert coefficients[0] == 1
    m = F.degree()
    assert all(0 <= JP.nth(k) <= F.nth(k) < q for k in range(m+1))
    n, J = int(F.eval(q)), int(JP.eval(q))
    assert integer_digits(n, q) == [int(F.nth(k)) for k in range(m+1)]
    j = min(J, n-J)
    assert 4 <= j <= n//2
    A_value = (n-1)//q
    B_value = int(BP.eval(q))
    assert math.gcd(A_value, B_value) == math.gcd(A_value, a*q-1) == 1
    first = 3*J*(J-1) % (n-1) == 0
    assert first == (3*j*(j-1) % (n-1) == 0)
    numerator = {"I": 3*c*((a+c)*q-1),
                 "II": 3*c*((a-c)*q-1),
                 "III": 3*(a+c)*(c*q+1)}[form]
    if first:
        assert numerator % A_value == 0
    if m >= 3:
        assert not (first and n % 4 == 0)
    return {"a": a, "B_coefficients": list(coefficients), "c": c,
            "q": q, "form": form, "m": m, "n": n, "J": J, "j": j,
            "n_mod_4": n % 4, "first_divisibility": first,
            "second_divisibility": 6*j*(j-1)*(j-2) % (n-2) == 0,
            "one_radix_digit_domination": True,
            "all_odd_prime_digit_conditions_asserted": False}


def audit_diagnostics_and_scope():
    inputs = ((5, (1, 2, 1, 1), 1, 11, "I"),
              (5, (1, 2, 1, 1), 1, 11, "II"),
              (9, (1, 2, 1, 1), 1, 19, "III"))
    diagnostics = [local_diagnostic(*parameters) for parameters in inputs]
    assert [record["n"] for record in diagnostics] == [79652, 79652, 1234032]
    assert all(record["n_mod_4"] == 0 and not record["first_divisibility"]
               for record in diagnostics)
    BP = sp.Poly(1+2*X+X**2+X**3, X, domain=sp.ZZ)
    assert BP.is_irreducible
    # Repeated factors are allowed when the entire B divides one J-s.
    for r in (2, 3, 5, 8):
        coefficients = tuple(math.comb(r, k) for k in range(r+1))
        for form in ("I", "II", "III"):
            a = 2*r+3 if form == "III" else r+2
            BP, F, JP = cofactor_forms(a, coefficients, 1, form)
            s = 1 if form == "II" else 0
            assert (JP-s).rem(BP).is_zero
            q = 2*max(int(v) for v in F.all_coeffs())+1
            diagnostics.append(local_diagnostic(a, coefficients, 1, q, form))
    # These witnesses show why the theorem retains degree >=3 and 4|n.
    degree2 = local_diagnostic(8, (1, 1), 5, 61, "I")
    assert (degree2["n"], degree2["j"]) == (30196, 11286)
    assert degree2["first_divisibility"] and degree2["n_mod_4"] == 0
    assert not degree2["second_divisibility"]
    assert (degree2["n"]-1) % 61 == 0 and (degree2["n"]-1) % 61**2 != 0
    assert sp.isprime(61)
    no4 = local_diagnostic(26, (1, 2, 2), 22, 60, "III")
    assert no4["first_divisibility"] and no4["n_mod_4"] % 2 == 1
    assert not no4["second_divisibility"]
    av = (no4["n"]-1)//60
    assert 3*(26+22)*(22*60+1)//av == 1
    assert (3*(26+22)-(26-2))//60 == 2
    # Boundary c=0 in III, including the numerical gcd and strict size gap.
    BP, F, _ = cofactor_forms(5, (1, 2, 1, 1), 0, "III")
    bvalue, n = int(BP.eval(11)), int(F.eval(11))
    assert math.gcd(n-1, bvalue) == 1
    assert 0 < 3*(bvalue-1) < n-1
    assert 3*bvalue*(bvalue-1) % (n-1) != 0
    return {"local_examples": diagnostics,
            "degree_2_scope_witness": degree2,
            "without_4_divides_n_scope_witness": no4,
            "constant_quotient_boundary": {"gcd": 1, "strict_size_gap": True},
            "true_counterexamples_asserted": 0,
            "finite_examples_are_not_the_universal_proof": True}


def audit_binomial_support():
    cases = []
    for degree in (1, 2, 3, 5):
        a = 5
        BP = 1+2*X**degree+X**(2*degree)+X**(3*degree)
        F = sp.Poly(2+(a*X**degree-1)*BP, X, domain=sp.ZZ)
        divisor = sp.Poly(a*X**degree-1, X, domain=sp.QQ)
        assert F.rem(divisor) == sp.Poly(2, X, domain=sp.QQ)
        assert all(F.nth(k) == 0 for k in range(F.degree()+1) if k % degree)
        # Coefficient of each remainder class is a sum of positive weights.
        symbolic_coeffs = sp.symbols(f"f0:{F.degree()+1}")
        generic = sp.Poly(sum(f*X**k for k, f in enumerate(symbolic_coeffs)),
                          X, domain=sp.EX)
        remainder = generic.rem(sp.Poly(a*X**degree-1, X, domain=sp.EX))
        for r in range(degree):
            expected = sum(symbolic_coeffs[k]*sp.Rational(1, a)**((k-r)//degree)
                           for k in range(r, F.degree()+1, degree))
            equal(remainder.nth(r), expected)
        q = 11
        assert (int(F.eval(q))-1) % q**degree == 0
        cases.append({"D": degree, "positive_weight_remainder_formula": True,
                      "n_minus_1_divisible_by_q_to_D": True})
    # The complete-prime-power contradiction is e*D>e for every e>=1,D>=2.
    z, w = sp.symbols("z w", nonnegative=True)
    strict_gap = signed_certificate((z+1)*(w+1), (z, w), 1)
    return {"symbolic_remainder_diagnostics": cases,
            "universal_nonnegative_weight_argument_in_note": True,
            "complete_prime_power_valuation_gap_e_times_D_minus_1": strict_gap,
            "D_ge_2_impossible_for_complete_q": True}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled; do not use python -O.")
    output = {
        "scope": "Canonical digit polynomials with degree F>=3 and "
                 "F-2=(aX-1)B, entire B dividing one J-s including multiplicity: "
                 "4|n and (n-1)|3j(j-1) cannot both hold. Arbitrary B. "
                 "General i=3 remains unresolved.",
        "arbitrary_identities": audit_arbitrary_identities(),
        "unbounded_signs_and_case_reductions": audit_unbounded_signs_and_reductions(),
        "cubic_eliminations": audit_eliminations(),
        "complete_congruences": audit_complete_congruences(),
        "previous_geometric_cubic_certificates_replayed": audit_cubic_reduction(),
        "numerical_diagnostics_and_scope": audit_diagnostics_and_scope(),
        "binomial_support": audit_binomial_support(),
        "irreducible_B_corollary": {
            "conditional_on_a_true_counterexample": True,
            "U2_equals_F_minus_2": True, "r2_equals_m": True,
            "eta_upper_bound": 3, "radix_bound": "q<13*(H+2)^6",
            "uniform_height_bound_proved": False},
        "new_fully_resolved_indices": 0,
    }
    path = ROOT / "data/results/verification_i3_arbitrary_cofactor.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("PASS arbitrary-cofactor identities, reductions and 4096 complete residues.")
    print("General i=3 remains unresolved.")


if __name__ == "__main__":
    main()
