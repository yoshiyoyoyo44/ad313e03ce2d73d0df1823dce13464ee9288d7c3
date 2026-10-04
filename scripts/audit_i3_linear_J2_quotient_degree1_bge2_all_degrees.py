"""Exhaustive exact finite certificate for the E=1+bX, b>=2 branch.

The proof derives b<=6 and N<=3; neither bound is an exploratory truncation.
All odd integer bases in the derived domain are included, not only prime powers.
"""

from fractions import Fraction
from math import gcd, isqrt
import json
from pathlib import Path
import sympy as sp


def divisors(value: int) -> list[int]:
    return sorted({
        divisor
        for small in range(1, isqrt(value) + 1)
        if value % small == 0
        for divisor in (small, value // small)
    })


def run() -> dict:
    assert Fraction(36, 49) + Fraction(12, 63) == Fraction(952, 1029) < 1
    # q^3-6q^2-3q-3=(q-9)^3+21(q-9)^2+132(q-9)+213.
    for q in range(9, 30):
        x = q - 9
        assert q**3 - 6*q*q - 3*q - 3 == x**3 + 21*x*x + 132*x + 213
        assert 6*q**3 + 3*q*q + 3*q < q**4

    # b=1: z=q^N keeps the coefficient identity valid for arbitrary N.
    aq, base, z = sp.symbols("a q z")
    whole_n_minus_one = 1 + (aq*base - 1)*(1 + base)*(base*z - 1)/(base - 1)
    normalized_a = (
        aq*base*z + (2*aq - 1)*z
        + (2*aq - 2)*(z - base)/(base - 1) + (aq - 2)
    )
    assert sp.cancel(whole_n_minus_one - base*normalized_a) == 0
    assert 5*5**2 - 2 > 0  # Minimum of the positive q^N term minus negative constant.

    root_rows = 0
    base_rows = 0
    parameter_rows = 0
    final_candidates = []
    certificates = []
    for b in range(2, 7):
        for degree in range(1, 4):
            for h in (1, 2):
                for g in (0, 1):
                    d = 2 - g
                    for divisor in divisors(d * b**(degree + 1)):
                        v = divisor - h*b
                        if v < h:
                            continue
                        root_rows += 1
                        minimum_a = max(b + 2, v//h + 1)
                        minimum_q = minimum_a*b + 1
                        if minimum_q % 2 == 0:
                            minimum_q += 1
                        maximum_q = ((6 + 3*d*h)*v + 6*h*b - 1)//b
                        maximum_ell = (3*h*v - 1)//b
                        local_count = 0
                        for q in range(minimum_q, maximum_q + 1, 2):
                            base_rows += 1
                            assert q >= 9
                            e = 1 + b*q
                            rhs = 6*v*q - 6*h
                            common = gcd(d, e)
                            if rhs % common:
                                continue
                            modulus = e//common
                            first_ell = (rhs//common) * pow(d//common, -1, modulus) % modulus
                            if first_ell == 0:
                                first_ell = modulus
                            for ell in range(first_ell, maximum_ell + 1, modulus):
                                c = rhs - d*ell
                                if c <= 0 or c % e:
                                    continue
                                lam = c//e
                                assert 0 < lam*b < 6*v
                                assert q*(6*v - b*lam) == lam + 6*h + d*ell
                                maximum_a = min((q - 1)//b, (3*v*v - 1)//(b*ell))
                                for a in range(minimum_a, maximum_a + 1):
                                    parameter_rows += 1
                                    local_count += 1
                                    assert a >= b + 2 and h <= v < h*a and a*b < q
                                    assert ell*a*b < 3*v*v and ell*b < 3*h*v
                                    p = (a*q - 1)*e
                                    r = v*q - h
                                    t = 3*r*r - ell*p
                                    value = 6*p + ell - 9*r
                                    assert p > a*b*q*q and p > 9*r
                                    assert 0 < value < 6*q**3 + 3*q*q + 3*q < q**4
                                    if t == 0:
                                        assert value != 0
                                        continue
                                    if value % t:
                                        continue
                                    cofactor = value//t
                                    if cofactor > q and cofactor % q == 1:
                                        final_candidates.append({
                                            "b": b, "N": degree, "h": h, "g": g,
                                            "v": v, "q": q, "a": a, "ell": ell,
                                            "lambda": lam, "Q_at_q": cofactor,
                                        })
                        certificates.append({
                            "b": b, "N": degree, "h": h, "g": g, "v": v,
                            "root_divisor": divisor,
                            "q_lower_odd": minimum_q,
                            "q_upper_integer": maximum_q,
                            "ell_upper_integer": maximum_ell,
                            "parameter_rows": local_count,
                        })
    assert (root_rows, base_rows, parameter_rows) == (297, 5465, 596)
    assert not final_candidates
    result = {
        "status": "passed",
        "scope": "Conditional standard-digit linear J-2 quotient, degree E=1, b>=2, all N>=1. Not general i=3.",
        "derived_degree_bound": 3,
        "derived_b_bound": 6,
        "root_parameter_rows": root_rows,
        "base_rows": base_rows,
        "integer_parameter_rows": parameter_rows,
        "final_integer_Q_candidates": final_candidates,
        "root_parameter_certificates": certificates,
        "b_equals_one_included": False,
        "b_equals_one_primitive_corollary": {
            "coefficient_identity": "symbolically passed for arbitrary N",
            "additional_input": "gcd(q,(n-1)/q)=1",
            "n_minus_one_coprime_to_q": False,
        },
    }
    output = Path(__file__).resolve().parents[1] / "data/results/verification_i3_linear_J2_quotient_degree1_bge2_all_degrees.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = run()
    print(json.dumps({key: value for key, value in result.items()
                      if key != "root_parameter_certificates"}, ensure_ascii=False, indent=2))
