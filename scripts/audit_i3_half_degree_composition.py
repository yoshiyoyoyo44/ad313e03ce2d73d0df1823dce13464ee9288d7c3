"""Exact diagnostics for the arbitrary-degree half-degree boundary theorem.

The universal theorem is proved in the accompanying note. Polynomial examples
validate substitutions and denominators; they are not numerical counterexamples.
"""

import json
import math
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent
X, Y = S.symbols("X Y")


def zero(expression):
    assert S.cancel(expression) == 0, S.factor(expression)


def valuation(value, p):
    value = S.Rational(value)
    if value == 0:
        return math.inf
    numerator, denominator = abs(int(value.p)), int(value.q)
    exponent = 0
    while numerator % p == 0:
        numerator //= p
        exponent += 1
    while denominator % p == 0:
        denominator //= p
        exponent -= 1
    return exponent


def coefficient_valuation(poly, p):
    return min(valuation(c, p) for c in S.Poly(poly, X).all_coeffs())


def integer_coefficients(poly):
    return all(c.q == 1 for c in S.Poly(poly, X, domain=S.QQ).all_coeffs())


def boundary_identities():
    h, z, w, e = S.symbols("h z w e", nonzero=True)
    U = -z*h*h/w-h/z+e/w
    R = (w/z**2-z*e/w)*h*h-2*e*h/z+e*e/w
    D = -w*h/z+e
    zero(z*h*h+w*U-D)
    zero(U*D-h**3-R)
    zero(h**3+R-z*h*h*U-w*U*U)
    zero(R.subs(e, w*w/z**3)+2*w*w*h/z**4-w**3/z**6)
    zero(U.subs({w: -z**3, e: z**3})-(h*h/z**2-h/z-1))
    zero(R.subs({w: -z**3, e: z**3})+2*z*z*h+z**3)
    return {"symbolic_identities": 6,
            "possible_v_over_h": [2, 3]}


def composition_divisibility():
    cases = 0
    bases = (X, X**2+X, X**3-X+2, X**5+3*X**2,
             X**8+X**3+1)
    for H in bases:
        for degree in (1, 2, 3):
            A = Y**degree+Y+1
            Q = Y**2-Y+3
            for remainder in (S.Integer(0), S.Integer(1), Y if degree > 1 else 2):
                B = A*Q+remainder
                core_rem = S.rem(B, A, Y)
                lifted_rem = S.rem(B.subs(Y, H), A.subs(Y, H), X)
                assert (core_rem == 0) == (lifted_rem == 0)
                if core_rem:
                    assert S.degree(core_rem.subs(Y, H), X) < S.degree(A.subs(Y, H), X)
                cases += 1
    return {"exact_composition_divisibilities": cases}


def quartic_family(parameter):
    K = parameter
    F = 320*K**4+512*K**3+240*K**2+32*K+2
    J = 80*K**4+168*K**3+114*K**2+27*K+2
    U = 8*K*K+8*K+1
    V = 40*K*K+24*K+1
    H = K+S.Rational(3, 4)
    C = 5*K+S.Rational(7, 4)
    return F, J, U, V, H, C, S.Rational(1, 4)


def quintic_family(parameter):
    K = parameter
    F = 150000*K**5+125000*K**4+35000*K**3+3750*K*K+125*K+2
    J = 30000*K**5+31000*K**4+11400*K**3+1770*K*K+105*K+2
    U = 100*K*K+30*K+1
    V = 1500*K**3+800*K*K+95*K+1
    H = 4*K+S.Rational(4, 5)
    C = 60*K*K+26*K+S.Rational(9, 5)
    return F, J, U, V, H, C, S.Rational(1, 5)


def cores_and_origins():
    identities = 0
    F, J, U, V, H, C, t = quartic_family(Y)
    P = S.prod(H-(i-1-t)*U for i in range(3))
    R = -S.Rational(3, 8)*H*H-H/8-S.Rational(1, 128)
    for expr in (F-1-U*V, U*C-V*H-1, J-1-V*(t*U+H), P-R*(F-2)):
        zero(expr)
        identities += 1
    assert S.rem(J*(J-1), F-1, Y) == 0
    assert S.rem(J*(J-1)*(J-2), F-2, Y) == 0
    identities += 2

    # The quartic rational-origin obstruction has nonsquare discriminant.
    alpha = S.symbols("alpha")
    obstruction = 125*alpha**2-114*alpha+5
    discriminant = int(S.discriminant(obstruction, alpha))
    assert discriminant == 256*41
    assert math.isqrt(discriminant)**2 != discriminant

    rows = []
    discriminants = []
    for t in (S.Rational(1, 5), S.Rational(2, 5), S.Rational(3, 5)):
        z = 1-3*t
        U = Y*Y/z**2-Y/z-1
        R = -2*z*z*Y-z**3
        P = S.prod(Y-(i-1-t)*U for i in range(3))
        F = S.cancel(P/R+2)
        V = S.cancel((F-1)/U)
        J = S.cancel(1+V*(t*U+Y))
        C = S.cancel((1+V*Y)/U)
        for item in (F, V, J, C):
            assert S.denom(item) in S.QQ
        assert S.degree(F, Y) == 5 and S.degree(V, Y) == 3
        zero(U*C-V*Y-1)
        assert S.rem(J*(J-1), F-1, Y) == 0
        assert S.rem(J*(J-1)*(J-2), F-2, Y) == 0
        identities += 3
        f = S.Poly(F.subs(Y, z*(2+X)), X)
        j = S.Poly(J.subs(Y, z*(2+X)), X)
        u = S.Poly(U.subs(Y, z*(2+X)), X)
        zero(u.as_expr()-X*X-3*X-1)
        identities += 1
        for s in (0, 1, 2):
            r = s-1-t
            delta = S.factor((1+z/r)**2+4)
            square = (math.isqrt(int(delta.p))**2 == delta.p
                      and math.isqrt(int(delta.q))**2 == delta.q)
            discriminants.append({"t": str(t), "s": s,
                                  "discriminant": str(delta), "square": square})
            if square:
                zero(r-2*z)
        rows.append({"t": str(t), "F": str(f.as_expr()),
                     "J": str(j.as_expr()), "linear_F": str(f.nth(1)),
                     "leading_F": str(f.LC())})
        if t == S.Rational(1, 5):
            positive_f, positive_j, *_ = quintic_family(X)
            zero(f.as_expr().subs(X, 10*X)-positive_f)
            zero(j.as_expr().subs(X, 10*X)-positive_j)
            identities += 2
    assert sum(row["square"] for row in discriminants) == 3
    return {"core_identities_and_divisibilities": identities,
            "quartic_origin_discriminant": discriminant,
            "quintic_models": rows, "quintic_origin_cases": discriminants}


def content_and_mod_five():
    quartet_f, quartet_j, *_ = quartic_family(Y)
    quintet_f, quintet_j, *_ = quintic_family(Y/5)
    # Y/5 corresponds to T=2Y, whose coprime linear coefficients are 25,21.
    assert S.Poly(quartet_f, Y).nth(1) == 32
    assert S.Poly(quartet_j, Y).nth(1) == 27
    assert S.Poly(quintet_f, Y).nth(1) == 25
    assert S.Poly(quintet_j, Y).nth(1) == 21
    checks = 0
    for p in (2, 3, 5, 7, 11, 13):
        for exponent in (1, 2, 3):
            for numerator in (1, 2, 4, 7):
                Q = S.Rational(numerator, p**exponent)*(X+2*X**3)+X**5
                v = coefficient_valuation(Q, p)
                for pair in ((quartet_f, quartet_j), (quintet_f, quintet_j)):
                    values = []
                    for core in pair:
                        coefficients = S.Poly(core, Y).as_dict()
                        predicted = min(valuation(c, p)+i[0]*v
                                        for i, c in coefficients.items())
                        lifted = S.expand(core.subs(Y, Q))
                        actual = coefficient_valuation(lifted, p)
                        assert actual == predicted
                        values.append(actual)
                        checks += 1
                    if v < 0:
                        assert min(values) < 0

    # One integral composition alone need not force an integral parameter.
    bad_parameter = X/2
    assert integer_coefficients(quartet_f.subs(Y, bad_parameter))
    assert not integer_coefficients(quartet_j.subs(Y, bad_parameter))
    five_j = S.Poly(5*quintet_j, Y, modulus=5)
    assert S.Poly(five_j.as_expr()-(3*Y**5+3*Y**4+Y**3+4*Y**2),
                  Y, modulus=5).is_zero
    mod_cases = 0
    for degree in range(1, 13):
        for first in range(5):
            for leading in range(1, 5):
                Q = first*X+leading*X**(degree+1)
                composed = S.Poly(five_j.as_expr().subs(Y, Q), X, modulus=5)
                assert not composed.is_zero and composed.degree() == 5*(degree+1)
                mod_cases += 1
    return {"exact_content_comparisons": checks,
            "nonconstant_mod_five_obstructions": mod_cases,
            "one_polynomial_insufficient_example": str(bad_parameter)}


def family_substitutions():
    cases, integer_values = 0, 0
    negative_K = X**5+2*X**4-X**3+2*X**2+X
    parameters = [X**degree for degree in range(1, 17)]
    parameters += [X+X**degree for degree in range(2, 13)]
    parameters.append(negative_K)
    max_degree = 0
    for K in parameters:
        h = S.degree(K, X)
        for family, multiplier in ((quartic_family, 4), (quintic_family, 5)):
            F, J, U, V, H, C, t = family(K)
            f, j = S.Poly(F, X), S.Poly(J, X)
            for poly in (f, j, S.Poly(F-J, X)):
                assert all(c >= 0 and c.q == 1 for c in poly.all_coeffs())
            assert f.degree() == multiplier*h
            assert S.degree(U, X) == 2*h
            assert S.degree(V, X) == (multiplier-2)*h
            assert S.degree(H, X) == h
            assert S.Poly(U, X).LC() > 0 and S.Poly(V, X).LC() > 0
            zero(U*C-V*H-1)
            zero(F-1-U*V)
            zero(J-1-V*(t*U+H))
            assert S.rem(J*(J-1), F-1, X) == 0
            assert S.rem(J*(J-1)*(J-2), F-2, X) == 0
            max_degree = max(max_degree, f.degree())
            for x in (1, 2, 3):
                k = int(K.subs(X, x))
                assert k > 0
                n, index = int(f.eval(x)), int(j.eval(x))
                assert 4 <= index < n
                if multiplier == 4:
                    assert n % 16 == 2
                integer_values += 1
            cases += 1
    assert S.Poly(negative_K, X).nth(3) == -1
    return {"polynomial_substitutions": cases,
            "integer_evaluation_diagnostics": integer_values,
            "maximum_degree_checked": max_degree,
            "negative_coefficient_parameter": str(negative_K),
            "examples_are_not_numerical_counterexamples": True}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled: do not use python -O.")
    result = {"scope": "Conditional polynomial boundary; general i=3 remains open",
              "boundary": boundary_identities(),
              "composition": composition_divisibility(),
              "rational_cores": cores_and_origins(),
              "integrality": content_and_mod_five(),
              "diagnostics": family_substitutions()}
    destination = ROOT/"data/results/verification_i3_half_degree_composition.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",
                           encoding="utf-8")
    print(json.dumps({"status": "passed", "output": str(destination),
                      "scope": result["scope"],
                      "diagnostics": result["diagnostics"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
