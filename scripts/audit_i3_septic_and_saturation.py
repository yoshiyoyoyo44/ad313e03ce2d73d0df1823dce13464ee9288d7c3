"""Exact certificates for the septic classification and arbitrary-degree lemma.

Universal claims are proved in the three accompanying notes. These checks verify
the symbolic reductions, all rational origins, and the valuation identities;
finite integer evaluations are explicitly diagnostic rather than the proof.
"""
import json
import math
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent


def zero(expr):
    assert S.cancel(expr) == 0, S.factor(expr)


def vp(n, p):
    n = abs(int(n))
    assert n
    exponent = 0
    while n % p == 0:
        n //= p
        exponent += 1
    return exponent


def binomial_vp(n, j, p):
    exponent, power = 0, p
    while power <= n:
        exponent += n // power - j // power - (n - j) // power
        power *= p
    return exponent


def symmetric_saturation():
    D, A, B, H, C, k = S.symbols("D A B H C k")
    Q = A*C - B*H
    U, V = D*A - 2*H, D*B + 2*C
    determinant = D*Q - 4*H*C - 1
    zero(U*C - V*H - 1 - determinant)
    zero(U*V - 1 - D*(D*A*B + Q) - determinant)
    # The degree argument reduces the boundary to a nonzero rational constant.
    q, lam = S.symbols("q lam", nonzero=True)
    hc = -(q*q + 4*q + lam)/(4*lam)
    zero(lam*(q*q + 4*(q + lam)*hc)
         + q**3 + 4*q*q + 5*lam*q + lam*lam)
    g = q**3 + 4*q*q + 5*lam*q + lam*lam
    zero(S.discriminant(g, q) + lam**2*(27*lam**2 + 140*lam - 144))
    assert 140**2 + 4*27*144 == 16*13**3
    assert math.isqrt(16*13**3)**2 != 16*13**3
    return 5


def coefficient_reduction():
    # Degree-independent reduction used again for the octic 3+5 exclusion.
    U, H, W, t = S.symbols("U H W t")
    z = 1 - 3*t
    P = S.prod(H - (i - 1 - t)*U for i in range(3))
    R = z*H*H*U + U*U*W - H**3
    identity = H*P + R*(U + H)
    zero(identity - U*U*(z*H*H + (H + U)*W
                         + (3*t*t - 1)*H*H + t*(t*t - 1)*H*U))
    x, z, A, B, c = S.symbols("x z A B c", nonzero=True)
    D = (2*A*A*c*z + B*B*z + 2*B)/(A*z)
    E = (2*A*A*B*c*z*z + A*A*c*z + B**3*z*z + 3*B*B*z + 4*B)/(A*A*z*z)
    H = x*x + c
    U = A*x**3 + B*x*x + D*x + E
    W = -z*x/A + (B*z + 1)/(A*A)
    raw = S.Poly(S.expand(H**3 - z*H*H*U - U*U*W), x)
    for degree in range(4, 8):
        zero(raw.nth(degree))
    a, v, w = S.symbols("a v w", nonzero=True)
    relation = (w + (v + 1)**2)**2 + 4*v - 1
    zero(raw.nth(3).subs({A: a/z, B: v/z, c: w/a**2}) + relation/a**3)
    y, q = S.symbols("y q")
    fixed_v = (1 - q*q)/4
    fixed_w = q - (fixed_v + 1)**2
    zero(relation.subs({v: fixed_v, w: fixed_w}))
    U0 = y**3 + v*y*y + (2*w + v*v + 2*v)*y + (2*v + 1)*w + v**3 + 3*v*v + 4*v
    replacements = {A: a/z, B: v/z, c: w/a**2, x: y/a}
    zero(a*a*z*U.subs(replacements) - U0)
    zero(a*a*z*H.subs(replacements) - z*(y*y + w))
    zero(a*a*z*W.subs(replacements) - z**3*(-y + v + 1))
    return 10


def no_root_mod(poly, variable, prime):
    assert int(S.LC(S.Poly(poly, variable))) % prime
    residues = [int(poly.subs(variable, i)) % prime for i in range(prime)]
    assert 0 not in residues
    return {"prime": prime, "residues": residues}


def quadratic_algebra():
    y, q, z = S.symbols("y q z")
    v = (1 - q*q)/4
    w = q - (v + 1)**2
    U = y**3 + v*y*y + (2*w + v*v + 2*v)*y + (2*v + 1)*w + v**3 + 3*v*v + 4*v
    H = z*(y*y + w)
    W = z**3*(-y + v + 1)
    R = S.Poly(S.expand(z*H*H*U + U*U*W - H**3), y)
    assert R.degree() == 2
    zero(R.LC() + z**3*(q - 1)**2*(q*q + 2*q + 3)/2)
    zero(S.resultant(H, U, y) - z**3*(q - 1)**3*(q*q + 3*q + 4)/4)
    a, b = S.cancel(R.nth(1)/R.LC()), S.cancel(R.nth(0)/R.LC())
    ur = S.Poly(S.rem(U, R.as_expr(), y), y)
    hr = S.Poly(S.rem(H, R.as_expr(), y), y)
    u1, u0, h1, h0 = ur.nth(1), ur.nth(0), hr.nth(1), hr.nth(0)
    norm_u = u0*u0 - a*u0*u1 + b*u1*u1
    delta = h1*u0 - h0*u1
    zero(norm_u - (q - 1)**3*(q*q + 3*q + 4)**3/(8*(q*q + 2*q + 3)**3))
    zero(delta - z*(q - 1)**2*(q + 3)*(q*q + 3*q + 4)/(4*(q*q + 2*q + 3)**2))
    trace = (2*h0*u0 - a*(h1*u0 + h0*u1) + 2*b*h1*u1)/norm_u
    norm = (h0*h0 - a*h0*h1 + b*h1*h1)/norm_u
    norm_expected = 2*q*z*z*(q*q + 2*q + 3)/((q - 1)*(q*q + 3*q + 4))
    zero(trace - 3*z)
    zero(norm - norm_expected)
    # A direct characteristic identity in the quotient ring.
    zero(S.rem(H*H - 3*z*H*U + norm_expected*U*U, R.as_expr(), y))
    zero(S.rem((H - 3*z*U/2).subs(q, -3), R.as_expr().subs(q, -3), y))
    zero(R.as_expr().subs(q, -3) + 16*z**3*(3*y*y + 4*y - 8))
    p1 = 3*q**3 + 6*q*q + 4*q - 10
    p2 = 3*q**3 + 6*q*q + 53*q + 88
    denominator = (q - 1)*(q*q + 3*q + 4)
    rows = []
    for t, pair, expected, scale in (
        (S.Rational(2, 7), (1, 2), p1, S.Rational(4, 49)),
        (S.Rational(3, 7), (0, 2), p1, S.Rational(16, 49)),
        (S.Rational(4, 7), (0, 1), p2, S.Rational(2, 49)),
    ):
        Z = 1 - 3*t
        r1, r2 = (i - 1 - t for i in pair)
        zero(r1 + r2 - 3*Z)
        zero(denominator*(norm_expected.subs(z, Z) - r1*r2) - scale*expected)
        rows.append({"t": str(t), "pair": list(pair), "obstruction": str(expected)})
    cubic_certificates = [no_root_mod(p, q, 13) for p in (p1, p2)]
    return rows, cubic_certificates


def septic_models():
    y, x = S.symbols("y x")
    U = y**3 - 2*y*y - 8*y + 8
    origin_rows = []
    cubics = [y**3 + 2*y*y - 8*y - 8, 2*y**3 - 3*y*y - 16*y + 12,
              5*y**3 - 11*y*y - 40*y + 44, 5*y**3 - 18*y*y - 40*y + 72]
    certificates = [no_root_mod(p, y, prime) for p, prime in zip(cubics, (3, 11, 3, 13))]
    admitted = None
    for t in (S.Rational(1, 7), S.Rational(3, 7), S.Rational(5, 7)):
        z = 1 - 3*t
        H = z*(y*y - 4)
        R = -16*z**3*(3*y*y + 4*y - 8)
        P = S.prod(H - (i - 1 - t)*U for i in range(3))
        C = S.cancel((H*P + R*(U + H))/(R*U*U))
        V = S.cancel((U*C - 1)/H)
        assert S.Poly(C, y).degree() == 3 and S.Poly(V, y).degree() == 4
        F, J = S.expand(U*V + 1), S.expand(1 + V*(t*U + H))
        zero(U*C - V*H - 1)
        zero(P - R*(F - 2))
        zero(S.rem(J*(J - 1), F - 1, y))
        zero(S.rem(J*(J - 1)*(J - 2), F - 2, y))
        expected = {
            S.Rational(1, 7): (y - 4)*cubics[0]*cubics[1]/128,
            S.Rational(3, 7): -(y - 4)*cubics[1]*cubics[2]/32,
            S.Rational(5, 7): -(y - 4)*cubics[0]*cubics[3]/1024,
        }[t]
        zero(F - 2 - expected)
        assert S.ground_roots(F - 2, y) == {S.Integer(4): 1}
        for sign in (1, -1):
            f = S.Poly(F.subs(y, 4 + sign*x), x)
            j = S.Poly(J.subs(y, 4 + sign*x), x)
            bad = [(i, f.nth(i), j.nth(i)) for i in range(8)
                   if not f.nth(i) >= j.nth(i) >= 0]
            origin_rows.append({"t": str(t), "origin": "4", "sign": sign,
                                "admissible": not bad,
                                "first_failure": [str(a) for a in bad[0]] if bad else None})
            if not bad:
                assert t == S.Rational(1, 7) and sign == 1 and admitted is None
                admitted = (f.as_expr(), j.as_expr())
    assert admitted is not None
    f, j = admitted
    assert S.Poly(f, x).nth(1) == S.Rational(49, 4)
    assert S.Poly(j, x).nth(1) == S.Rational(41, 4)
    assert math.gcd(49, 41) == 1
    assert S.Poly(j.subs(x, 4*x), x).nth(7) == S.Rational(256, 7)
    F, J = S.expand(f.subs(x, 28*y)), S.expand(j.subs(x, 28*y))
    assert all(c.q == 1 for p in (F, J) for c in S.Poly(p, y).all_coeffs())
    assert all(S.Poly(F, y).nth(i) >= S.Poly(J, y).nth(i) >= 0 for i in range(8))
    return F, J, origin_rows, certificates


def universal_seven_valuation(F, J):
    y = next(iter(F.free_symbols))
    A = 392*y**3 + 196*y*y + 28*y + 1
    B = 1568*y**3 + 588*y*y + 56*y + 1
    K = 4302592*y**6 + 4379424*y**5 + 1761648*y**4 + 354760*y**3 + 37296*y*y + 1932*y + 41
    zero(F - 2 - 343*y*A*B)
    zero(J - 2 - 7*y*K)
    for polynomial, residue in ((A, 1), (B, 1), (K, 6)):
        assert int(S.Poly(polynomial, y).nth(0)) % 7 == residue
        assert all(int(c) % 7 == 0 for c in S.Poly(polynomial - residue, y).all_coeffs())
    samples = sorted(set(range(1, 257)) | {7**i for i in range(1, 9)})
    for q in samples:
        n, j = int(F.subs(y, q)), int(J.subs(y, q))
        e = vp(n - 2, 7)
        assert e == 3 + vp(q, 7)
        assert vp(j - 2, 7) == e - 2
        assert j % 7 == 2 and j % (7**e) not in (0, 1, 2)
        assert binomial_vp(n, 3, 7) == e
        assert binomial_vp(n, j, 7) > 0
        assert binomial_vp(n, n - j, 7) > 0
    return len(samples)


def main():
    if not __debug__:
        raise SystemExit("Do not run with assertions disabled.")
    saturation_checks = symmetric_saturation()
    coefficient_checks = coefficient_reduction()
    norm_rows, parameter_certificates = quadratic_algebra()
    F, J, origins, origin_certificates = septic_models()
    diagnostics = universal_seven_valuation(F, J)
    result = {
        "status": "passed",
        "scope": "All septic digit-polynomial branches, arbitrary-degree difference and saturation bounds, and the octic 3+5 exclusion; not all i=3 integers.",
        "symmetric_saturation_identity_checks": saturation_checks,
        "symmetric_saturation_necessary_condition": "t=1/2, deg U=deg V=d, H nonconstant, d0+d2=2h imply h>2d/3",
        "coefficient_reduction_checks": coefficient_checks,
        "quadratic_algebra_obstruction_table": norm_rows,
        "parameter_cubic_irreducibility_certificates": parameter_certificates,
        "origin_cubic_irreducibility_certificates": origin_certificates,
        "all_rational_origin_and_sign_checks": origins,
        "integer_family": {"F": str(F), "J": str(J), "parameter": "y=h*X, h positive integer"},
        "universal_integer_valuation": "v7(F(y)-2)=3+v7(y), v7(J(y)-2)=1+v7(y); common prime 7",
        "finite_integer_diagnostics": diagnostics,
        "septic_polynomial_counterexample_exclusion_proved": True,
        "max_digit_degree_for_uniform_height_bound": 7,
        "complete_prime_power_multiplicities_preserved": True,
        "general_nonconstant_difference_degree_bound": "deg U=u<=deg V=v<=2u implies h>=ceil(u/2); at t=1/3, h>=ceil(2u/3)",
        "octic_three_plus_five_split_excluded": True,
        "octic_polynomial_counterexample_exclusion_proved": False,
        "universal_argument": "The three accompanying paper proofs; all symbolic calculations use exact rational arithmetic.",
        "lean_formalization_completed": False,
        "external_peer_review_completed": False,
        "new_fully_resolved_indices": 0,
        "complete_problem_solution": False,
        "remaining_indices": 28,
    }
    output = ROOT / "data/results/verification_i3_septic_and_saturation.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
