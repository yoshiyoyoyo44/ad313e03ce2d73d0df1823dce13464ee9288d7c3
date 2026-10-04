"""Exact universal coefficient certificate for conditional i=3, b>c>t.

No numerical bound on parameters is used. This does not solve Erdős 699.
"""

import hashlib
import json
from pathlib import Path

from sympy.polys.domains import ZZ
from sympy.polys.rings import ring


def main():
    _, h, d, e, x, s, y = ring("h,d,e,x,s,y", ZZ)
    t, c, b = h, h+e, h+e+d
    D0 = d*e*(d+e)
    cap = (d+e)*c**2
    L = cap-2*d*t**2
    V0 = c**3*(d+e)-2*d*t**3
    W0 = V0*c-c**3*e*(d+e)
    assert V0 == c*L+2*d*e*t**2
    assert W0 == c*t*L
    # w>0 gives 0<L<cap. Set s=L/(cap-L)>0. Clearing cap-L
    # proves the following parametrization recovers the original v,w.
    assert c*cap*L+2*d*e*t**2*cap == cap*V0
    assert c*t*cap*L == cap*W0

    # Check the actual polynomial factorization before widening L to its
    # whole positive interval. Here y is an arbitrary polynomial argument.
    J0 = y*(1+b*y)*(V0+W0*y)
    K0 = (
        -c*V0*D0
        + c*(V0**2+D0*(V0*c-W0))*y
        + (W0*V0*(b+c)+c**2*W0*D0)*y**2
        + b*W0**2*y**3
    )
    assert K0*y*(1+b*y)*(1+c*y) == c*J0*(J0-D0)

    D = D0*(1+s)
    V = c*cap*s+2*d*e*t**2*(1+s)
    W = c*t*cap*s
    # v=V/D, w=W/D, a=b+c+t+v+x, q=abct+1+y.
    aN = D*(b+c+t+x)+V
    f1 = aN-D*(b+c+t)
    f2 = aN*(b+c+t)-D*(b*c+b*t+c*t)
    f3 = aN*(b*c+b*t+c*t)-D*b*c*t
    f4 = aN*b*c*t
    k1 = V**2+D*(V*c-W)
    k2 = W*V*(b+c)+c**2*W*D
    p2 = c*D**2*f3-3*c*D*V*f4-3*f1*b*W**2
    p1 = c*D**2*f2-3*c*D*V*f3-3*f1*k2
    p0 = c*(f1*D**2-3*V*f2*D-3*f1*k1)
    q0 = f4+D
    coefficients = [
        c*D**4*f4,
        3*c*D**3*f4*q0+D**2*p2,
        3*c*D**2*f4*q0**2+2*D*p2*q0+D**2*p1,
        c*D*f4*q0**3+p2*q0**2+D*p1*q0+D**2*p0,
    ]
    Q = q0+D*y
    AE = f1*D**3+f2*Q*D**2+f3*Q**2*D+f4*Q**3
    KE = -c*V*D**4+c*k1*Q*D**2+k2*Q**2*D+b*W**2*Q**3
    direct = c*D*(Q-3*V)*AE-3*f1*KE
    expanded = Q*sum(C*y**(3-i) for i, C in enumerate(coefficients))
    assert direct == expanded

    records = []
    for C in coefficients:
        shifted = C.shift_list([1, 1, 1, 0, 0, 0])
        assert min(shifted.values()) > 0
        constant = int(shifted.get((0,)*6, 0))
        assert constant > 0
        blob = json.dumps(
            [[list(m), int(v)] for m, v in sorted(shifted.items())],
            separators=(",", ":"),
        ).encode()
        records.append({
            "terms": len(shifted),
            "minimum_coefficient": int(min(shifted.values())),
            "constant_coefficient": constant,
            "sha256": hashlib.sha256(blob).hexdigest(),
        })
    assert [r["terms"] for r in records] == [10261, 30628, 66935, 124370]
    result = {
        "status": "passed",
        "problem699_completely_solved": False,
        "scope": "conditional standard-digit complete split, degF4 degJ3 J0zero, B0=1+bX B1=1+cX B2=1+tX, b>c>t",
        "parameter_limits_assumed": False,
        "interval": "0<L<(d+e)c^2, s=L/((d+e)c^2-L)>0",
        "exact_polynomial_identities": 6,
        "positive_coefficient_polynomials": records,
        "finite_search_cases": 0,
    }
    target = Path(__file__).resolve().parents[1]/"data/results/verification_i3_three_linear_b_c_t_2026-10-04.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "all_parameter_coefficient_polynomials": 4, "finite_search_cases": 0}))


if __name__ == "__main__":
    main()
