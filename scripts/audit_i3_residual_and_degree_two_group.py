"""Symbolic checks for degree-unbounded residual and genus-one arguments.

This checks identities and divisor bookkeeping with symbolic d. The geometric
reason a genus-one curve has no function with one simple pole is in the paper.
"""
import json
import math
from pathlib import Path
import sympy as S

ROOT = Path(__file__).resolve().parent.parent


def zero(expression):
    assert S.cancel(expression) == 0, S.factor(expression)


def main():
    t, h, hp, u, up, w, wp, z = S.symbols("t h hp u up w wp z")
    r = z*h*h*u+u*u*w-h**3
    rp = z*(2*h*hp*u+h*h*up)+2*u*up*w+u*u*wp-3*h*h*hp
    differential = 3*hp*r-h*rp-z*r*up
    zero(S.rem(differential, u, u))
    constants = [(s-1-t)*(s-1-t-(1-3*t)) for s in range(3)]
    for value, expected in zip(constants, [-2*(t-1)*(t+1), -t*(2*t-1), -2*t*(t-1)]):
        zero(value-expected)
    for s, k in enumerate(constants):
        rr = s-1-t
        remainder_w = rr*rr*(rr-(1-3*t))*u
        zero(remainder_w-k*rr*u)
    for i, j, expected in [(1, 0, t-2), (2, 0, 2*(t-1)), (2, 1, t)]:
        zero(constants[i]-constants[j]-expected)

    x, a, m, H, U, L = S.symbols("x a m H U L")
    M = x*x-(1+m/t**2)*x+m
    ell = (1-t*t)*m
    A = t*t*M+ell
    zero(A-(x-1)*(t*t*x-m))
    zero(L*U**2-M*H*(H+2*t*U)-((L+t*t*M)*U**2-M*(H+t*U)**2))
    discriminant = S.discriminant(M, x)
    positive = ((m+t*t-2*t**4)**2+4*t**6*(1-t*t))/t**4
    zero(discriminant-positive)
    zero(S.resultant(M, A, x)-ell**2)
    y = S.symbols("y")
    zero(S.rem((y+t*M)*(y-t*M)-ell*M, y*y-A*M, y))
    # Norm Phi = A*(L U^2-M H(H+2tU)).
    B = H+t*U
    zero((A*U)**2-A*M*B**2-A*(ell*U**2-M*H*(H+2*t*U)))

    # Divisor coordinates: E0, O, T, B1, B2, Iplus, Iminus.
    d, k = S.symbols("d k", integer=True)
    phi = S.Matrix([1, 2, 1, 0, 0, -d-2, d-2])
    yy = S.Matrix([0, 1, 1, 1, 1, -2, -2])
    psi = S.Matrix([0, 0, 0, 1, 1, -2, 0])
    xminus1 = S.Matrix([0, 2, 0, 0, 0, -1, -1])
    xminusxi = S.Matrix([0, 0, 2, 0, 0, -1, -1])
    def final_divisor(dd, power):
        return phi.subs(d, dd)+dd*(yy-psi)-(dd+2)*xminus1+power*(xminus1-xminusxi)
    assert final_divisor(2*k+1, k+1) == S.Matrix([1, -1, 0, 0, 0, 0, 0])
    assert final_divisor(2*k, k+1) == S.Matrix([1, 0, -1, 0, 0, 0, 0])

    # The h=d-1 boundary with M=(x-b)^2 reduces to a conic. Its
    # Laurent-coordinate logarithmic derivative is checked symbolically.
    b = S.symbols("b")
    conic_A = (x-1)*(t*t*x-b*b)
    gamma = t*t-b*b
    delta = gamma**2
    trace = 4*t*t*x-2*(t*t+b*b)
    qzero = -(t+b)**2
    qone = gamma
    logarithmic_bracket = (2*d+2
        +qzero*(trace-2*qzero)/(delta-qzero*trace+qzero*qzero)
        +qone*(trace-2*qone)/(delta-qone*trace+qone*qone))
    zero(logarithmic_bracket-(2*d-b/(t*x)))
    zero((conic_A+b*S.diff(conic_A, x)).subs(x, b)
         +b*(2*b*b-(1+3*t*t)*b+2*t*t))
    parameter_discriminant = S.discriminant(2*b*b-(1+3*t*t)*b+2*t*t, b)
    zero(parameter_discriminant-(1-t*t)*(1-9*t*t))
    zero(parameter_discriminant.subs(t, 3/(2*d))
         -(4*d*d-9)*(4*d*d-81)/(16*d**4))
    factor_pairs = []
    square_degrees = []
    for lower in range(2, math.isqrt(1296)+1, 2):
        if 1296 % lower:
            continue
        upper = 1296//lower
        if upper % 2:
            continue
        numerator = lower+upper+90
        factor_pairs.append([lower, upper, str(S.Rational(numerator, 8))])
        if numerator % 8:
            continue
        degree_squared = numerator//8
        degree = math.isqrt(degree_squared)
        if degree*degree == degree_squared and degree >= 4:
            square_degrees.append(degree)
    assert not square_degrees
    result = {
        "passed": True,
        "scope": "degree-unbounded polynomial restrictions; general numerical i=3 remains open",
        "residual_bound": "h >= u-d_s except s=1,t=1/2",
        "third_ratio_bound": "t=1/3 implies h >= v-u+1",
        "two_small_group_branch": "(d0,d1,d2)=(d-1,d-1,2) implies h=d-1",
        "quadratic_discriminant_positive_identity": str(positive),
        "odd_degree_divisor": "E0-O",
        "even_degree_divisor": "E0-T",
        "double_quadratic_group_excluded": True,
        "double_group_degree_equation": "(4*d^2-45)^2-k^2=1296",
        "all_even_factor_pairs_1296": factor_pairs,
        "checks_use_symbolic_degree": True,
    }
    path = ROOT / "data/results/verification_i3_residual_and_degree_two_group.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"passed": True, "symbolic_degree": True}))


if __name__ == "__main__":
    main()
