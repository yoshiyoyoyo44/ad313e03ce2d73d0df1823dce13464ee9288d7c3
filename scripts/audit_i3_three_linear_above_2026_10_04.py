"""Exact small algebraic certificates for the two b-minimal split orders."""

import json
from fractions import Fraction
from pathlib import Path

from sympy.polys.domains import ZZ
from sympy.polys.rings import ring


def main():
    _, x, y = ring("x,y", ZZ)
    f = (1-x)*(1-y)*(1+x+x*y)**2
    assert (1-x)*(1+x)**2-f == (1-x)*(
        (1-x)*(1+x)*y+x*(2+x)*y**2+x**2*y**3
    )
    assert 32-27*(1-x)*(1+x)**2 == (3*x-1)**2*(3*x+5)
    assert Fraction(4, 9)+Fraction(1, 12) < 1
    assert Fraction(3, 4)+Fraction(3, 25) < 1
    assert Fraction(27, 32)+Fraction(1, 50) < 1

    _, b, d, e = ring("b,d,e", ZZ)
    c, t = b+d, b+d+e
    bound = b*c*t*(t-b)*(t-c)-6*t**2-3*(t-b)*(t-c)
    shifted = bound.shift_list([4, 1, 1])
    assert len(shifted) == 40
    assert min(shifted.values()) == 1
    assert shifted.get((0, 0, 0)) == 18

    # b=1,c>t only permits c=t+1 for t=2,3, and then v is not integral.
    assert Fraction(27, 2) < 16 < Fraction(64, 3)
    assert Fraction(64, 3) < 27 < Fraction(125, 4)
    exceptional_v = [Fraction(5, 2), Fraction(17, 3)]
    assert all(v.denominator != 1 for v in exceptional_v)
    # t>c>b and c<2b leaves no positive v for b<=3.
    small_b = []
    for bv in range(1, 4):
        for cv in range(bv+1, 2*bv):
            tv = cv+1
            fc, ft = Fraction(cv**3, cv-bv), Fraction(tv**3, tv-bv)
            assert fc < 2*ft
            # f is increasing for all real arguments >=tv.
            assert 2*tv-3*bv > 0
            small_b.append([bv, cv, tv, str(fc), str(2*ft)])
    result = {
        "status": "passed",
        "problem699_completely_solved": False,
        "scope": "conditional standard-digit complete split degF4 degJ3 J0zero, three linear factors, c>t>b or t>c>b",
        "interval_maximum_identities": 2,
        "rational_bound_comparisons": 3,
        "last_order_positive_coefficients": [
            [list(m), int(v)] for m, v in sorted(shifted.items())
        ],
        "last_order_positive_coefficient_count": len(shifted),
        "b1_nonintegral_v": [str(v) for v in exceptional_v],
        "small_b_exclusions": small_b,
    }
    target = Path(__file__).resolve().parents[1]/"data/results/verification_i3_three_linear_above_2026-10-04.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "positive_coefficients": 40, "all_parameter_paper_bounds": 3}))


if __name__ == "__main__":
    main()
