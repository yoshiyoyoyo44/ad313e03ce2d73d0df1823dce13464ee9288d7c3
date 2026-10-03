"""Exact checks for the paper proof closing all sextic digit-polynomial branches.

The universal assertions are proved in the accompanying note. Symbolic
identities, complete rational-origin tables, and valuation formulas are checked
here; finite integer examples are explicitly diagnostic, not the proof.
"""
import json
import math
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent


def zero(expr):
    assert S.cancel(expr) == 0, S.factor(expr)


def vp(n, p):
    assert n != 0
    n, exponent = abs(int(n)), 0
    while n % p == 0:
        n //= p
        exponent += 1
    return exponent


def binomial_vp(n, j, p):
    exponent, q = 0, p
    while q <= n:
        exponent += n // q - j // q - (n - j) // q
        q *= p
    return exponent


def saturated_group_identities():
    U, H, T, r, beta = S.symbols("U H T r beta", nonzero=True)
    C = beta * H + T
    V = beta * U + T / (r + 1) - beta * H / (r * (r + 1))
    alpha = (r + 1) * beta / r
    zero(C - (r + 1) * V - alpha * (H - r * U))
    zero((r + 1) * (U * C - V * H - 1)
         - ((r + 1) * T * U - (r + 1) - H * T + beta * H**2 / r))
    return 2


def outer_reduction():
    Y, z, a, b, c, r = S.symbols("Y z a b c r", nonzero=True)
    beta = r * (r + 1) / c**2
    H = a * Y**2 + b * Y + c
    U = S.cancel(((r + 1) + H * Y - beta * H**2 / r) / ((r + 1) * Y))
    V = S.expand(beta * U + Y / (r + 1) - H / c**2)
    C = beta * H + Y
    assert S.Poly(U, Y).degree() == 3
    zero(U * C - V * H - 1)
    alpha = (r + 1)**2 / c**2
    B = b - c**2 / (r + 1)
    Q = a * Y**2 + B * Y + 2 * c
    zero(V - alpha * U - (r + 1) * Q * (a * Y + B) / c**4)
    F = S.expand(U * V + 1)
    J = S.expand(1 + V * ((-1 - r) * U + H))
    zero(F - 2 - (H - r * U) * (V - alpha * U))
    zero(S.rem(J, Q, Y) - (c * Y - 2 * r - 1))
    fixed_a = c**3 / ((r + 1) * (2 * r + 3))
    fixed_b = -2 * c**2 / (2 * r + 3)
    Q_fixed = S.expand(Q.subs({a: fixed_a, b: fixed_b}))
    zero(Q_fixed - fixed_a * (Y - 2 * (r + 1) / c) * (Y - (2 * r + 3) / c))
    H0 = z**2 / ((r + 1) * (2 * r + 3)) - 2 * z / (2 * r + 3) + 1
    U0 = S.cancel(((r + 1) + H0 * z - (r + 1) * H0**2) / ((r + 1) * z))
    V0 = S.expand(r * (r + 1) * U0 + z / (r + 1) - H0)
    zero(H.subs({a: fixed_a, b: fixed_b}).subs(Y, z / c) - c * H0)
    zero(U.subs({a: fixed_a, b: fixed_b}).subs(Y, z / c) - c * U0)
    zero(V.subs({a: fixed_a, b: fixed_b}).subs(Y, z / c) - V0 / c)
    return 8


def symmetric_obstruction():
    # First check the elimination without relying on a Groebner solver.
    D, A, B, H, C = S.symbols("D A B H C")
    Q = A * C - B * H
    U, V = D * A - 2 * H, D * B + 2 * C
    zero(U * C - V * H - (D * Q - 4 * H * C))
    zero(U * V - 1 - (D**2 * A * B + 4 * H * C + 1)
         - 2 * (D * Q - 4 * H * C - 1))

    Y, beta, a, f, lam = S.symbols("Y beta a f lam", nonzero=True)
    d = a + beta
    Q = beta * Y**2 + Y - lam
    H = a * Y**2 + (f - 1) * Y + lam
    C = beta * H + d * Y + f
    E = S.Poly(S.expand(Q**2 + 4 * Q + lam * (4 * H * C + 1)), Y)
    zero(E.nth(4) - beta * (beta + 4 * lam * a**2))
    lam_fixed = -beta / (4 * a**2)
    zero(E.nth(3).subs(lam, lam_fixed) - beta * (a - 2 * beta * f + beta) / a)
    a_fixed = beta * (2 * f - 1)
    reduced = {i: S.cancel(E.nth(i).subs(lam, lam_fixed).subs(a, a_fixed))
               for i in (0, 1, 2)}
    N2 = 4 * beta * (2 * f - 1)**3 + f**2 * (3 - 2 * f)
    N0 = 3 * beta * (2 * f - 1)**4 + f**2 * (4 * f - 3)
    zero(reduced[2] - N2 / (2 * f - 1)**3)
    zero(reduced[1] - N2 / (beta * (2 * f - 1)**3))
    zero(reduced[0] - N0 / (4 * beta**2 * (2 * f - 1)**6))
    zero(4 * N0 - 3 * (2 * f - 1) * N2 - f**2 * (12 * f**2 - 8 * f - 3))
    assert N2.subs(f, 0) == -4 * beta
    discriminant = 208
    assert discriminant == (-8)**2 - 4 * 12 * (-3)
    assert math.isqrt(discriminant)**2 != discriminant
    return 11


def model(t, z):
    r = -1 - t
    beta = r * (r + 1)
    H = z**2 / ((r + 1) * (2 * r + 3)) - 2 * z / (2 * r + 3) + 1
    U = S.cancel(((r + 1) + H * z - beta * H**2 / r) / ((r + 1) * z))
    V = S.expand(beta * U + z / (r + 1) - H)
    return S.expand(U * V + 1), S.expand(1 + V * (t * U + H))


def affine_origins_and_integer_families():
    z, x, y = S.symbols("z x y")
    origin_rows, families = [], {}
    for t, cubic, prime, origin, scale in (
        (S.Rational(1, 6), 189*z**3 + 18*z**2 - 57*z - 2, 5, S.Rational(2, 3), 4),
        (S.Rational(1, 3), 108*z**3 + 117*z**2 + 6*z - 13, 7, S.Rational(1, 3), 1),
    ):
        F, J = model(t, z)
        zero(S.rem(J * (J - 1), F - 1, z))
        zero(S.rem(J * (J - 1) * (J - 2), F - 2, z))
        residues = [int(cubic.subs(z, q)) % prime for q in range(prime)]
        assert all(residues) and int(S.LC(S.Poly(cubic, z))) % prime
        origins = S.polys.polytools.ground_roots(F - 2, z)
        assert len(origins) == 3 and all(m == 1 for m in origins.values())
        good = []
        for q in sorted(origins):
            for sign in (1, -1):
                f, j = S.Poly(F.subs(z, q + sign*x), x), S.Poly(J.subs(z, q + sign*x), x)
                bad = [(i, f.nth(i), j.nth(i)) for i in range(7)
                       if not f.nth(i) >= j.nth(i) >= 0]
                if not bad:
                    good.append((q, sign))
                origin_rows.append({"t": str(t), "origin": str(q), "sign": sign,
                                    "admissible": not bad,
                                    "first_failure": [str(a) for a in bad[0]] if bad else None})
        assert good == [(origin, 1)]
        f, j = S.expand(F.subs(z, origin + scale*y)), S.expand(J.subs(z, origin + scale*y))
        assert all(c.q == 1 for P in (f, j) for c in S.Poly(P, y).all_coeffs())
        assert all(S.Poly(f, y).nth(i) >= S.Poly(j, y).nth(i) >= 0 for i in range(7))
        families[str(t)] = (f, j)
    # Linear coefficients force kappa/4 to be integral in the first model.
    u, v, gcd = S.gcdex(S.Integer(216), S.Integer(181))
    assert gcd == 1 and u * 216 + v * 181 == 1
    # Second model: 2*kappa is integral, then 1263*(2*kappa)^2/4 is integral.
    assert math.gcd(108, 94) == 2 and 1263 % 4 == 3
    f, j = families["1/6"]
    assert all(int(S.Poly(f - 2, y).nth(i)) % 4 == 0 for i in range(7))
    f, j = families["1/3"]
    P = 36*y**3 + 75*y**2 + 40*y + 2
    K = 324*y**4 + 1107*y**3 + 1296*y**2 + 561*y + 47
    zero(f - 2 - 27*y*(y + 1)*(3*y + 2)*P)
    zero(j - (27*y**3 + 54*y**2 + 27*y + 1)*P)
    zero(j - 1 - (y + 1)*(9*y**2 + 12*y + 1)*(108*y**3 + 189*y**2 + 81*y + 1))
    zero(j - 2 - y*(3*y + 2)*K)
    mod3 = {name: [int(poly.subs(y, q)) % 3 for q in range(3)] for name, poly in {
        "P": P, "K": K, "j_over_P": 27*y**3 + 54*y**2 + 27*y + 1,
        "j_minus_1_first_unit": 9*y**2 + 12*y + 1,
        "j_minus_1_second_unit": 108*y**3 + 189*y**2 + 81*y + 1,
    }.items()}
    assert mod3["P"] == [2, 0, 1]
    assert mod3["K"] == [2, 2, 2]
    assert all(mod3[k] == [1, 1, 1] for k in mod3 if k not in ("P", "K"))
    diagnostic = 0
    for q in range(1, 257):
        n, jn = int(f.subs(y, q)), int(j.subs(y, q))
        e = vp(n - 2, 3)
        chosen = {0: 2, 1: 0, 2: 1}[q % 3]
        assert vp(jn - chosen, 3) == e - 3
        assert jn % (3**e) not in (0, 1, 2)
        assert binomial_vp(n, 3, 3) == e - 1
        assert binomial_vp(n, jn, 3) > 0
        diagnostic += 1
    return origin_rows, {
        t: {"F": str(f), "J": str(j)} for t, (f, j) in families.items()
    }, mod3, diagnostic


def main():
    if not __debug__:
        raise SystemExit("Do not run with assertions disabled.")
    saturation = saturated_group_identities()
    outer = outer_reduction()
    symmetric = symmetric_obstruction()
    origins, families, mod3, diagnostics = affine_origins_and_integer_families()
    result = {
        "status": "passed",
        "scope": "Paper proof and exact identities for all sextic digit-polynomial branches; not all i=3 integers.",
        "saturated_group_identities": saturation,
        "outer_reduction_identities": outer,
        "symmetric_obstruction_checks": symmetric,
        "symmetric_rational_obstruction": "12*f^2-8*f-3=0; discriminant 208 is not a rational square",
        "affine_origin_table": origins,
        "integer_families": families,
        "t_one_third_mod3_unit_table": mod3,
        "integer_valuation_diagnostics": diagnostics,
        "universal_argument": "The accompanying paper proof, including complete prime-power multiplicities and all rational affine origins.",
        "sextic_polynomial_counterexample_exclusion_proved": True,
        "max_digit_degree_for_uniform_height_bound": 6,
        "odd_half_degree_central_saturation_excluded": True,
        "lean_formalization_completed": False,
        "external_peer_review_completed": False,
        "new_fully_resolved_indices": 0,
        "complete_problem_solution": False,
        "remaining_indices": 28,
    }
    output = ROOT / "data/results/verification_i3_sextic_closeout.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
