"""Exact symbolic/threshold audit of the i=5 Pell primitive-unit reduction.

This is a checker for the specified lemmas, not a search or a proof of Erdos699.
All unbounded Chebyshev identities are certified by recurrences and initial data.
The existing exclusion of square n is explicitly an imported input.
"""

from __future__ import annotations

import json
from math import isqrt

import sympy as sp


def assert_zero(expr: sp.Expr) -> None:
    assert sp.expand(expr) == 0, sp.expand(expr)


def main() -> None:
    x, r0, r1, q = sp.symbols("x r0 r1 q")
    c = 4 * x**2 - 1

    # Squares of any sequence R_{r+1}=2x R_r-R_{r-1} obey one order-3 recurrence.
    r2 = 2 * x * r1 - r0
    r3 = 2 * x * r2 - r1
    assert_zero(r3**2 - c * r2**2 + c * r1**2 - r0**2)

    # T_{2r+1} obeys W_{r+2}=(4x^2-2)W_{r+1}-W_r.
    # W_r +/-1 therefore has the same order-3 recurrence as R_r^2.
    w0, w1 = sp.symbols("w0 w1")
    w2 = (4 * x**2 - 2) * w1 - w0
    w3 = (4 * x**2 - 2) * w2 - w1
    for sign in (-1, 1):
        assert_zero(
            (w3 + sign) - c * (w2 + sign)
            + c * (w1 + sign) - (w0 + sign)
        )
        for r in (0, 1, 2):
            ur = sp.chebyshevu(r, x)
            prev = sp.chebyshevu(r - 1, x) if r else 0
            rr = ur - sign * prev
            assert_zero(sp.chebyshevt(2 * r + 1, x) + sign - (x + sign) * rr**2)

    # Double-index identity: independent Laurent substitution gives the generic result.
    tx = (q + 1 / q) / 2
    t2x = (q**2 + q**-2) / 2
    assert sp.cancel(t2x - (2 * tx**2 - 1)) == 0

    # Parity of U_r: U_0=1,U_1=2x=0 mod2, U_{r+1}=U_{r-1} mod2.
    parity = [1, 0]
    for r in range(2, 40):
        parity.append(parity[r - 2])
    assert all((parity[r] - parity[r - 1]) % 2 == 1 for r in range(1, 40))

    # Induction coefficient for T_{m+1}>=x T_m from T_m>=x T_{m-1}.
    assert_zero((2 * x - 1 / x) - x - (x**2 - 1) / x)

    # Trace and factorization of the nonintegral positive-norm-one cube.
    n_expr = (x**3 - 3 * x + 2) / 4
    assert_zero(n_expr - ((x - 1) / 2)**2 * (x + 2))
    assert_zero(n_expr - 1 - ((x + 1) / 2)**2 * (x - 2))
    assert_zero((x**3 - 3 * x) - ((x**2 - 1) * x - 2 * x))

    # Exact polynomial certificates valid for all x>=15 (odd branch), or all x (even).
    assert_zero((x - 1)**2 - 12 * x - ((x - 15)**2 + 16 * (x - 15) + 16))
    assert_zero((x + 1)**2 - 12 * (x - 2) - (x - 5)**2)
    assert n_expr.subs(x, 13) < 1000
    assert (2 * 2**sp.Rational(1, 3))**3 == 16
    assert 16 < 27

    # Integer checks in place of real roots or logarithms.
    tail = 10**87
    c6 = 1_458_000_000
    k9 = 71_191_406_250_000
    odd_index_bound = (3**5 * c6)**3
    even_index_square_bound = 3**9 * k9
    half_trace_square_bound = c6 * 3**6 // 2
    assert c6 * 3**6 % 2 == 0
    assert odd_index_bound < tail
    assert even_index_square_bound < tail**2
    assert half_trace_square_bound == 729000**2
    assert 729000**3 < 4 * 10**17
    assert 10**17 < tail

    # Numerical Pell witnesses independently test the signs/cofactor placement.
    witnesses = 0
    for d, xx, yy in ((2, 3, 2), (3, 2, 1), (5, 9, 4), (6, 5, 2), (13, 649, 180)):
        assert xx * xx - d * yy * yy == 1
        xm, ym = 1, 0
        for m in range(1, 20):
            xm, ym = xx * xm + d * yy * ym, yy * xm + xx * ym
            assert xm * xm - d * ym * ym == 1
            assert xm == sp.chebyshevt(m, xx)
            if m % 2 == 0:
                assert (xm + 1) // 2 == sp.chebyshevt(m // 2, xx)**2
            elif xx % 2:
                n = (xm + 1) // 2
                sigma = 1 if n % 2 == 0 else -1
                r = (m - 1) // 2
                rr = int(sp.chebyshevu(r, xx)) - sigma * (
                    int(sp.chebyshevu(r - 1, xx)) if r else 0
                )
                assert rr % 2 == 1
                even_member = n if sigma == 1 else n - 1
                assert even_member == (xx + sigma) // 2 * rr * rr
                if m >= 3:
                    # rr^2 > n^(2/3)/3, checked after cubing.
                    assert 27 * rr**6 > n * n
            witnesses += 1

    # O_D index-three examples; the norm equation is checked independently.
    ring_examples = []
    for d, a, b in ((5, 3, 1), (13, 11, 3), (29, 27, 5)):
        assert a % 2 == b % 2 == 1
        assert a * a - d * b * b == 4
        xp = (a**3 - 3 * a) // 2
        yp = (a*a - 1) * b // 2
        assert xp*xp - d * yp*yp == 1
        assert (a*a - 1) % 2 == 0
        assert (a*a - 1) * b % 2 == 0
        ring_examples.append({"D": d, "trace_eta": a, "integer_cube": [xp, yp]})

    print(json.dumps({
        "ok": True,
        "symbolic_certificate": "shared order-3 recurrence and three initial values",
        "integer_index_bound_odd": odd_index_bound,
        "integer_index_square_bound_even": even_index_square_bound,
        "half_integer_trace_bound_strict": isqrt(half_trace_square_bound),
        "half_integer_n_bound_strict": 729000**3 // 4,
        "pell_witness_checks": witnesses,
        "ring_examples": ring_examples,
        "imported_input": "existing tail exclusion for square n",
        "unresolved": "Kummer-to-common-square-class descent for j or n-j",
    }, indent=2))


if __name__ == "__main__":
    main()
