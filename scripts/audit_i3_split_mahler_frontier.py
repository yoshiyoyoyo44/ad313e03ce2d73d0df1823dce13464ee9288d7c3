"""Exact positive-polynomial certificates for the split Mahler frontier.

The measure inequality and degree induction are proved in the accompanying
paper. This audit verifies the integer certificates, not general i=3.
"""

import json
from fractions import Fraction
from math import isqrt
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
Q, Y, D, S = sp.symbols("q y d S")


def positive_shift(polynomial, origin):
    shifted = sp.Poly(sp.expand(polynomial).subs(Q, Y+origin), Y)
    coefficients = list(reversed(shifted.all_coeffs()))
    assert all(value > 0 for value in coefficients), coefficients
    return {"q_origin": origin, "ascending_coefficients": [int(v) for v in coefficients]}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    # sqrt(S*(S+1)) < S+1/2 for all S>=0, with an exact constant gap.
    assert sp.expand((S+sp.Rational(1, 2))**2-S*(S+1)) == sp.Rational(1, 4)
    frontier = []
    for rho, degree in ((4, 4), (5, 4), (6, 5)):
        difference = 4*Q**(3*degree-rho)-3*(2*degree*(Q-1)**2+1)*(Q+1)**(rho-2)
        frontier.append({"rho": rho, "minimum_degree_J": degree,
                         **positive_shift(difference, 3)})
    # The right side grows by <2 when d increases by 1; left by q^3>=27.
    right = 2*D*(Q-1)**2+1
    induction_gap = sp.Poly((2*right-right.subs(D, D+1)).subs({D: Y+1, Q: S+3}), Y, S)
    assert all(cc >= 0 for cc in induction_gap.coeffs())
    assert induction_gap.coeff_monomial(1) > 0

    H = sp.Rational(3, 2)*(8*(Q-1)**2+1)*(Q+1)**4/Q**6
    derivative = -3*(Q+1)**3*(8*Q**2-31*Q+27)/Q**7
    assert sp.cancel(sp.diff(H, Q)-derivative) == 0
    derivative_certificate = positive_shift(8*Q**2-31*Q+27, 3)
    h15 = Fraction(H.subs(Q, 15))
    assert h15 == Fraction(17137664, 1265625) < 14
    # Thus a*D6<=13, since a*D6>=14 would force q>=15 and a*D6<H(q)<14.

    rows = []
    upper_measure_ratios = []
    for aa in range(2, 14):
        coefficient_square_bound = sum((aa**k-1)**2 for k in range(1, 5))
        measure_bound = coefficient_square_bound+Fraction(1, 2)
        ratio = 3*measure_bound/aa
        upper_measure_ratios.append(ratio)
        coarse_q_squared_bound = ratio*Fraction(aa+2, aa+1)**4
        coarse_q_bound = isqrt(coarse_q_squared_bound.numerator//coarse_q_squared_bound.denominator)
        rows.append({"a": aa, "maximum_D6": 13//aa,
                     "S_bound": coefficient_square_bound,
                     "3_measure_bound_over_a": str(ratio),
                     "coarse_q_upper_bound": coarse_q_bound})
    B = max(upper_measure_ratios)
    assert B == Fraction(4923146307, 26)
    cutoff = isqrt(B.numerator//B.denominator)
    while Fraction(cutoff**6, (cutoff+1)**4) <= B:
        cutoff += 1
    assert cutoff == 13763
    q_certificate = positive_shift(B.denominator*Q**6-B.numerator*(Q+1)**4, cutoff)

    result = {
        "status": "passed", "general_i3_solved": False,
        "hypotheses": "F0=1, digit domination, F1>=1, F-2=(aX-1)D, complete D allocation, first condition",
        "general_necessary_bound": "2*a*Dlead*q^(3*d-rho) < 3*(2*d*(q-1)^2+1)*(q+1)^(rho-2)",
        "infinite_degree_certificates": frontier,
        "rho5": "d>=4 excluded here; d=3 excluded by the separate 14-case repair",
        "rho6": "only d=3,m=4 and d=4,m=7 remain; neither is claimed solved",
        "rho6_d4_leading_bound": {"a_times_D6_maximum": 13,
                                 "H_at_15": str(h15),
                                 "H_decreasing_for_q_ge3": derivative_certificate},
        "rho6_d4_coefficient_and_base_bounds": rows,
        "rho6_d4_final_q_bound": 13762,
        "final_q_certificate": q_certificate,
        "exhaustive_rho6_d4_search_performed": False,
    }
    output = ROOT/"data/results/verification_i3_split_mahler_frontier.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "rho5_high_degrees_excluded": True,
                      "rho6_d4_a_times_D6_maximum": 13, "rho6_d4_q_maximum": 13762,
                      "general_i3_solved": False}, indent=2))


if __name__ == "__main__":
    main()
