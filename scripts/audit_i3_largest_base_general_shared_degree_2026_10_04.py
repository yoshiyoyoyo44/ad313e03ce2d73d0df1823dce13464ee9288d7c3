"""Exact identities for the largest-base three-gcd degree bound.

The proof's arbitrary-degree root and factor statements are in the note;
this checker verifies algebra and uniform rational constants, not a finite
search extrapolated to arbitrary numerical candidates.
"""

from fractions import Fraction
from pathlib import Path
import json
import sympy as sp


def main():
    a, b, d = sp.symbols("a b d")
    modulus = a * d + 1
    for s in (0, 1, 2):
        j = b * d + s
        residual = (a * s - b) * (a * (s - 1) - b)
        quotient = b * b * modulus + b * (a * (2 * s - 1) - 2 * b)
        assert sp.expand(a * a * j * (j - 1) - residual - modulus * quotient) == 0
    assert sp.expand(a * a - 4 * b * (a - b) - (a - 2 * b)**2) == 0
    x = sp.symbols("x", positive=True)
    assert sp.expand(2 * a * a - b * (a + b) - (a - b) * (2 * a + b)) == 0
    assert sp.expand(2 * a * a - (2 * a - b) * (a - b) - b * (3 * a - b)) == 0
    n = sp.symbols("n")
    assert sp.expand(n * (n - 1) - (n - 2)**2 - (3 * n - 4)) == 0
    q, m = sp.symbols("q m")
    assert sp.expand((m + 1) * q * q - (1 + m * (q - 1)**2)
                     - (q*q - 1 + m * (2*q - 1))) == 0
    y = sp.symbols("y")
    assert sp.expand((x*y - 1) - ((x - 1) + (y - 1)) - (x - 1) * (y - 1)) == 0
    assert Fraction(3, 10) + Fraction(1, 5) == Fraction(1, 2)
    assert 2**14 > 10**4
    assert Fraction(2 * 2**14 + 8, 7) <= Fraction(3 * 2**14, 10)
    assert Fraction(1, 4) * 36 == 9
    assert Fraction(1, 4) * 3 == Fraction(3, 4)
    assert 2**14 > 36 > 3
    x_merge, y_merge, q_merge = sp.symbols("x_merge y_merge q_merge")
    assert sp.expand(q_merge * ((1 + 1/q_merge) * (1 + x_merge*y_merge/q_merge)
                               - (1 + x_merge/q_merge) * (1 + y_merge/q_merge))
                     - (x_merge - 1) * (y_merge - 1)) == 0
    assert Fraction(2**24, 6) + Fraction(13, 12) <= Fraction(2**24, 5)
    assert 2**24 == 64**4 == 4096**2
    assert Fraction(1, 10) + Fraction(1, 32) == Fraction(21, 160)
    assert Fraction(139, 160) > Fraction(6, 7)
    assert Fraction(6, 7) / Fraction(10, 9) / Fraction(3, 4) == Fraction(36, 35)
    assert 1 + Fraction(1, 4096) < Fraction(36, 35)
    gamma_squared = Fraction(139, 160)**2
    assert gamma_squared == Fraction(19321, 25600) > Fraction(3, 4)
    assert 6/gamma_squared < 8
    assert Fraction(9, 4)/gamma_squared < 3
    P_half, R_half = sp.symbols("P_half R_half")
    assert sp.expand(sp.Rational(9, 4)*P_half**2 - 3*R_half*(P_half+R_half)
                     - 3*(P_half/2-R_half)*(3*P_half/2+R_half)) == 0
    result = dict(
        status="passed",
        independent_review="Base theorem independently audited by root; central and endpoint border strengthening proposed by root and independently audited by global_audit",
        scope="General numerical i=3 necessary conditions, standard digits at the largest complete prime power of (n-1)/delta. No complete-allocation assumption. Not the numerical-to-polynomial full-sharing bridge.",
        lower_base_threshold=2**14,
        degree_bounds="2 deg gcd(F-2,J-s) <= deg F + 1 for s=0,1,2; full multiplicity gcds",
        factor_lower="H(q) > (1/2) leading(H) q^deg(H), any integer factor H of F-2 with positive leading coefficient",
        numerical_endpoint_bound="d^2 < 6n < 9n",
        numerical_middle_bound="d^2 < 3n/4",
        exponent_endpoint_constant=36,
        exponent_middle_constant=3,
        central_strengthening_threshold=2**24,
        central_strengthened_degree_bound="deg gcd(F-2,J-1) <= floor(deg F/2)",
        endpoint_border_classification="At q>=2^24 and 2 deg G_s=deg F+1, endpoint G_0,G_2 have leading coefficient <=2; in the original half range G_0 has leading coefficient 1",
        precise_border_factor_lower="(139/160) leading coefficient q^degree",
        exact_symbolic_identities=11,
    )
    path = Path(__file__).resolve().parents[1] / "data/results/verification_i3_largest_base_general_shared_degree_2026-10-04.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
