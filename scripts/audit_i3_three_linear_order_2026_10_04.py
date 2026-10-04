"""Exact all-parameter certificate for one conditional i=3 split ordering.

This closes b > t > c in the standard-digit degree-four, full polynomial
allocation model. It does not establish polynomial allocation for a general
numerical counterexample and does not solve Erdős 699.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from sympy.polys.domains import ZZ
from sympy.polys.rings import ring


def coefficient_record(poly):
    coefficients = list(poly.values())
    assert coefficients and min(coefficients) > 0
    origin = (0,) * poly.ring.ngens
    constant = int(poly.get(origin, 0))
    assert constant > 0
    serialized = json.dumps(
        [[list(monomial), int(value)] for monomial, value in sorted(poly.items())],
        separators=(",", ":"),
    ).encode()
    return {
        "terms": len(coefficients),
        "minimum_coefficient": int(min(coefficients)),
        "constant_coefficient": constant,
        "sha256": hashlib.sha256(serialized).hexdigest(),
    }


def main():
    _, h, d, e, x, y = ring("h,d,e,x,y", ZZ)
    # h=c, d=b-t, e=t-c; all three are positive integers.
    b, c, t = h + d + e, h, h + e
    denominator = d * e * (d + e)
    V = 2 * t**3 * (d + e) - c**3 * d
    W = V * c - c**3 * d * e
    # v=V/denominator, w=W/denominator, a=b+c+t+v+x.
    a_numerator = denominator * (b + c + t + x) + V
    f1 = a_numerator - denominator * (b + c + t)
    f2 = a_numerator * (b + c + t) - denominator * (b*c + b*t + c*t)
    f3 = a_numerator * (b*c + b*t + c*t) - denominator * b*c*t
    f4 = a_numerator * b*c*t
    K1 = V**2 + denominator * (V*c - W)
    K2 = W*V*(b+c) + c**2*W*denominator
    P2 = c*denominator**2*f3 - 3*c*denominator*V*f4 - 3*f1*b*W**2
    P1 = c*denominator**2*f2 - 3*c*denominator*V*f3 - 3*f1*K2
    P0 = c*(f1*denominator**2 - 3*V*f2*denominator - 3*f1*K1)
    q0 = f4 + denominator
    # Coefficients, in descending order, of c*denominator^5 * P(q)/q
    # after q=a*b*c*t+1+y; P=(q-3v)A-3F1*K.
    coefficients = [
        c*denominator**4*f4,
        3*c*denominator**3*f4*q0 + denominator**2*P2,
        3*c*denominator**2*f4*q0**2 + 2*denominator*P2*q0 + denominator**2*P1,
        c*denominator*f4*q0**3 + P2*q0**2 + denominator*P1*q0 + denominator**2*P0,
    ]

    # Verify the coefficient construction by a separate cleared-denominator
    # evaluation of A and K, rather than numerical sampling.
    Q = q0 + denominator*y
    A_evaluation = f1*denominator**3 + f2*Q*denominator**2 + f3*Q**2*denominator + f4*Q**3
    K_evaluation = (
        -c*V*denominator**4
        + c*K1*Q*denominator**2
        + K2*Q**2*denominator
        + b*W**2*Q**3
    )
    J_evaluation = Q*(denominator+b*Q)*(V*denominator+W*Q)
    assert K_evaluation*Q*(denominator+b*Q)*(denominator+c*Q) == c*J_evaluation*(J_evaluation-denominator**4)
    direct_P = c*denominator*(Q-3*V)*A_evaluation - 3*f1*K_evaluation
    expanded_P = Q*sum(coefficient*y**(3-index) for index, coefficient in enumerate(coefficients))
    assert direct_P == expanded_P

    cones = []
    cones.append({
        "region": "h>=4, d>=1, e>=1, x>=0",
        "coefficients": [coefficient_record(C.shift_list([4, 1, 1, 0, 0])) for C in coefficients],
    })
    for H, shifts in [(1, [(2, 1), (1, 4)]), (2, [(2, 1), (1, 2)]), (3, [(2, 1), (1, 2)])]:
        for d0, e0 in shifts:
            cones.append({
                "region": f"h={H}, d>={d0}, e>={e0}, x>=0",
                "coefficients": [coefficient_record(C.evaluate(h, H).shift_list([d0, e0, 0, 0])) for C in coefficients],
            })

    uncovered = [(1, 1, 1), (1, 1, 2), (1, 1, 3), (2, 1, 1), (3, 1, 1)]
    integral_shapes = []
    for H, D, E in uncovered:
        bv, cv, tv = H+D+E, H, H+E
        v = (2*Fraction(tv**3, bv-tv)-Fraction(cv**3, bv-cv))/(tv-cv)
        w = v*cv-Fraction(cv**3, bv-cv)
        if v.denominator == w.denominator == 1:
            integral_shapes.append([bv, cv, tv, int(v), int(w)])
    assert integral_shapes == [[4, 2, 3, 50, 96]]

    # For this shape, a>=59, q>=26a-23.  The exact positive difference
    # a*(2304*A/a - 3K) has constant, linear and quadratic coefficients
    # 2454a-20736, 13224a-59904, 16128a-55296. Thus k<2304/a.
    assert all(slope*59 + intercept > 0 for slope, intercept in [
        (2454, -20736), (13224, -59904), (16128, -55296)
    ])
    # 0 < k(a-9)+150 < 2454 < 2q, and q divides this integer.
    # Hence q=k(a-9)+150 and 59<=a<=95; every admissible integer pair
    # can now be checked, with no primality restriction or extrapolation.
    assert 2454 < 2*(26*59-23)
    finite_cases = []
    for a in range(59, 96):
        for k in range(1, 2303//a+1):
            q = k*(a-9)+150
            if q < 26*a-23:
                continue
            A = a-9 + (9*a-26)*q + (26*a-24)*q*q + 24*a*q**3
            K = -50 + 2504*q + 14592*q*q + 18432*q**3
            assert k*A != 3*K, (a, k, q)
            finite_cases.append([a, k, q])
    assert len(finite_cases) == 147
    result = {
        "status": "passed",
        "problem699_completely_solved": False,
        "scope": "conditional standard-digit complete split, deg F=4, deg J=3, J0=0, B0=1+bX,B1=1+cX,B2=1+tX, b>t>c",
        "universal_polynomial_identities": 2,
        "positive_coefficient_cones": cones,
        "uncovered_parameter_triples": [list(p) for p in uncovered],
        "integral_shapes": integral_shapes,
        "finite_integer_cases": finite_cases,
        "finite_integer_case_count": len(finite_cases),
    }
    target = Path(__file__).resolve().parents[1] / "data/results/verification_i3_three_linear_order_2026-10-04.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "positive_cones": len(cones), "coefficient_polynomials": 4*len(cones), "finite_cases": len(finite_cases)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
