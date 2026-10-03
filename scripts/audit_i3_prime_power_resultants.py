"""Exact diagnostics for the degree-unbounded prime-power/resultant note.

The universal statements are proved in the note. Constant-one examples satisfy
both numerical divisibilities; constant-zero examples require only the first.
One radix's inequalities are checked, not all primes or all numerical inputs.
"""

import json
import math
from itertools import product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
X = sp.symbols("X")


def digits(value, base):
    answer = []
    while value:
        answer.append(value % base)
        value //= base
    return answer or [0]


def dominated(lower, upper):
    return all(d <= (upper[i] if i < len(upper) else 0)
               for i, d in enumerate(lower))


def polynomial(coefficients):
    return sp.Poly(sum(c * X**i for i, c in enumerate(coefficients)),
                   X, domain=sp.ZZ)


def resultant(A, B):
    # Compute with the higher degree first, then restore the defining sign.
    # The convention is checked separately against Sylvester determinants.
    if A.degree() < B.degree():
        return int((-1)**(A.degree()*B.degree()) * B.resultant(A))
    return int(A.resultant(B))


def sylvester_resultant(A, B):
    a, b = A.all_coeffs(), B.all_coeffs()
    d, k = A.degree(), B.degree()
    rows = []
    for shift in range(k):
        rows.append([0]*shift+a+[0]*(k-1-shift))
    for shift in range(d):
        rows.append([0]*shift+b+[0]*(d-1-shift))
    return int(sp.Matrix(rows).det())


def positive_factor(F, target):
    # F-target has exactly one positive root in (0,1], by positive coefficients.
    # The root is simple, so exactly one irreducible factor changes sign here.
    factors = (F - target).factor_list()[1]
    selected = [(g, e) for g, e in factors
                if g.eval(0) < 0 and g.eval(1) >= 0]
    assert len(selected) == 1, (F, target, factors)
    g, exponent = selected[0]
    assert exponent == 1 and g.eval(0) == -1
    assert g.LC() > 0 and g.domain == sp.ZZ
    return g


def audit_grouping():
    implications = 0
    for p in (3, 5, 7, 11):
        p_digits = [digits(n, p) for n in range(256)]
        for e in (1, 2, 3):
            q = p**e
            q_digits = [digits(n, q) for n in range(256)]
            for n in range(256):
                for j in range(n + 1):
                    if dominated(p_digits[j], p_digits[n]):
                        assert dominated(q_digits[j], q_digits[n])
                        implications += 1
    n, j, p, q = 64, 18, 3, 9
    assert dominated(digits(j, q), digits(n, q))
    assert not dominated(digits(j, p), digits(n, p))
    assert (n - 1) % q == 0 and (n - 1) % (q*p) != 0
    return {"full_to_grouped_implications": implications,
            "grouped_only_example": {"n": n, "j": j, "p": p, "q": q,
                                     "n_digits_p": digits(n, p),
                                     "j_digits_p": digits(j, p)}}


def audit_inequalities():
    identities = 0
    for length in range(1, 9):
        variables = sp.symbols(f"z0:{length}")
        # All omitted monomials have nonnegative coefficients for z_i >= 0.
        extra = sp.Poly(sp.prod(1 + z for z in variables)
                        - 1 - sum(variables), *variables)
        assert all(c >= 0 for c in extra.coeffs())
        prefix = sp.Integer(1)
        telescoping = sp.Integer(1)
        for z in variables:
            telescoping -= z * prefix
            prefix *= 1-z
        assert sp.expand(telescoping - prefix) == 0
        identities += 2

    norm_cases = 0
    for H in range(2, 51):
        cap = (H-1)*H*(H+1)
        for constant in (0, 1):
            # S is the total nonnegative coefficient sum of J.
            for S in range(constant, H + constant):
                if constant == 0 and S > H-1:
                    continue
                if constant == 1 and S > H:
                    continue
                norms = [abs(constant-s) + S-constant for s in range(3)]
                assert math.prod(norms) <= cap
                norm_cases += 1
        assert cap >= 2*H - 2
        assert 1 + H**3 * cap > 2*H-1
    return {"symbolic_product_identities": identities,
            "coefficient_norm_cases": norm_cases}


def audit_lcm():
    limit = 600
    lcms = [1, 1]
    for n in range(2, limit + 1):
        lcms.append(math.lcm(lcms[-1], n))
    for n in range(1, limit + 1):
        upper_half = (n+1)//2
        central = math.comb(n, n//2)
        assert central % (lcms[n] // lcms[upper_half]) == 0
        assert lcms[n] <= 4**n
        if n % 2:
            assert central <= 4**(n//2)
        else:
            assert central <= 4**(n//2)
    return {"lcm_recursive_divisibilities": limit,
            "lcm_upper_bounds": limit}


def audit_budget():
    a, b, k, t, ell, z = sp.symbols("a b k t ell z")
    C = 2*a*k*k+b*k
    f = ell**2-C*ell-2*a*k*k*t
    assert sp.expand(f.subs(ell, C+t)-t*(k*b+t)) == 0
    assert sp.expand(f.subs(ell, C+t+z)
                     -t*(k*b+t)-z*(C+2*t)-z*z) == 0
    comparisons = 0
    for H, m in product(range(2, 31), range(1, 21)):
        threshold = 6*H*(H+1)*(H+2)**(2*m+2)+2
        assert threshold <= 7*(H+2)**(2*m+4)
        comparisons += 1
    return {"symbolic_budget_identities": 2,
            "integer_threshold_comparisons": comparisons}


def audit_positive_factors():
    # This family shows why selecting the positive-root factor matters:
    # F-2 has a large shared factor, so Res(F-2,J) is zero, while Res(g,J) is not.
    cases = []
    for m in (3, 5, 8, 12, 20):
        F = polynomial([1] + [1]*(m-1) + [2])
        J = polynomial([0] + [1]*m)
        g = positive_factor(F, 2)
        assert g.as_expr() == 2*X-1
        assert resultant(F-2, J) == 0
        resultants = [resultant(g, J-s) for s in range(3)]
        assert all(resultants)
        assert resultants[0] == 2**m-1
        assert resultants[1] == -1
        assert resultants[2] == -2**m-1
        assert resultants[0] == sylvester_resultant(g, J)
        cases.append({"m": m, "d": g.degree(), "H": int(F.eval(1)),
                      "resultants": resultants,
                      "whole_polynomial_resultant_is_zero": True})
    return {"partial_common_factor_diagnostics": cases}


def audit_local_case(n, j, base, expected_constant=None, require_both=True):
    assert 4 <= j <= n//2
    assert 3*j*(j-1) % (n-1) == 0
    second_divisibility = 6*j*(j-1)*(j-2) % (n-2) == 0
    if require_both:
        assert second_divisibility
    F = polynomial(digits(n, base))
    J = polynomial(digits(j, base))
    assert dominated(digits(j, base), digits(n, base))
    r = int(F.nth(0))
    if r == 1:
        assert second_divisibility
    if expected_constant is not None:
        assert r == expected_constant
    assert r in (0, 1)
    H, m = int(F.eval(1)), F.degree()
    target, coefficient = (1, 3) if r == 0 else (2, 6)
    g = positive_factor(F, target)
    d = g.degree()
    resultants = [resultant(g, J-s) for s in range(target+1)]
    for s, result in enumerate(resultants):
        assert result == sylvester_resultant(g, J-s)
    assert all(resultants)
    resultant_product = math.prod(resultants)
    value = int(g.eval(base))
    assert value and (n-target) % value == 0
    assert coefficient*resultant_product % value == 0
    assert sp.gcd(g, J*(J-1) if r == 0 else J*(J-1)*(J-2)).degree() == 0
    if r == 1:
        rhs = 12*H**(3*m)*((H-1)*H*(H+1))**d
    else:
        rhs = 6*(H+1)**(2*m)*(H*(H+1))**d
    assert (base-1)**d <= rhs
    return {"n": n, "j": j, "base": base, "constant": r,
            "H": H, "m": m, "d": d,
            "positive_factor": str(g.as_expr()),
            "resultants": resultants,
            "second_numerical_divisibility": second_divisibility,
            "required_both_divisibilities": require_both,
            "factor_value_divides_scaled_resultant": True}


def audit_numerical_diagnostics():
    # Earlier numerical relaxations: the listed base passes, other primes fail.
    cases = [audit_local_case(76672, 26775, 1217, 1),
             audit_local_case(3258244432, 1087547175, 19, 1)]

    # The constant-zero theorem needs only n-1 | 3*j*(j-1). This explicit
    # family passes all digits at the listed prime and has n == 0 (mod 4).
    # Its second divisibility is not required or asserted.
    for prime, exponent in ((79, 3), (83, 4)):
        k, t = 6*prime**exponent, 2
        r = prime*k+1
        n, j = prime*(r*r*t-k), prime*r*t
        case = audit_local_case(n, j, prime, 0, require_both=False)
        assert n % 4 == 0 and case["m"] >= 8
        case["constant_zero_family_parameters"] = {"k": k, "t": t}
        cases.append(case)

    # The known quadratic family has n == 2 (mod 4), hence is never a true
    # counterexample. Its values are useful tests of the weaker lemma inputs.
    # Search a bounded list solely to obtain local examples of degree >= 8.
    chosen = {}
    for parameter in range(1, 30001):
        n = 12*parameter**2+8*parameter+2
        j = 6*parameter**2+parameter
        if (3*j*(j-1) % (n-1)
                or 6*j*(j-1)*(j-2) % (n-2)):
            continue
        for base in (5, 7, 11, 13):
            r = n % base
            if r != 1:
                continue
            ds = digits(n, base)
            if len(ds)-1 < 8 or not dominated(digits(j, base), ds):
                continue
            key = (base, r)
            if key not in chosen:
                chosen[key] = (n, j, base, parameter)
        if len(chosen) == 4:
            break
    assert len(chosen) == 4
    for n, j, base, parameter in chosen.values():
        case = audit_local_case(n, j, base)
        case["quadratic_family_parameter"] = parameter
        case["n_mod_4"] = n % 4
        assert case["m"] >= 8 and case["n_mod_4"] == 2
        cases.append(case)
    return {"local_cases": cases,
            "scope": "Constant one uses both divisibilities; constant zero uses only the first. One radix is checked, not all primes."}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled; do not use python -O.")
    results = {"scope": "Degree-unbounded necessary conditions; i=3 remains unresolved.",
               "grouping": audit_grouping(),
               "inequalities": audit_inequalities(),
               "lcm": audit_lcm(),
               "budget": audit_budget(),
               "positive_factors": audit_positive_factors(),
               "numerical_diagnostics": audit_numerical_diagnostics()}
    destination = ROOT / "data/results/verification_i3_prime_power_resultants.json"
    destination.write_text(json.dumps(results, ensure_ascii=False, indent=2)+"\n",
                           encoding="utf-8")
    local_count = len(results["numerical_diagnostics"]["local_cases"])
    print(f"PASS prime-power grouping, integer resultant certificates, LCM and budgets; {local_count} local cases.")
    print("The universal proofs are in the note. General i=3 is unresolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
