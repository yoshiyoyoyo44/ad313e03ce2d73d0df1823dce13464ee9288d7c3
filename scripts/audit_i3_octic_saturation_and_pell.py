"""Exact checks for saturation and the degree-unbounded Pell obstruction.

The accompanying paper gives the universal proofs and preserves all factor
multiplicities. No finite search is used as an all-degree proof.
"""
import json
import math
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent


def zero(expression):
    assert S.cancel(expression) == 0, S.factor(expression)


def model(variable, t, c, H, T):
    r = -1-t
    beta = r*(r+1)/c
    U = S.cancel((1-H**2/c)/T+H/(r+1))
    V = S.expand(beta*U+T/(r+1)-H/c)
    C = S.expand(beta*H+T)
    F = S.expand(U*V+1)
    J = S.expand(1+V*(t*U+H))
    zero(U*C-V*H-1)
    zero(F-2-(H-r*U)*(V-(r+1)**2/c*U))
    zero(S.rem(J*(J-1), F-1, variable))
    zero(S.rem(J*(J-1)*(J-2), F-2, variable))
    assert S.degree(F, variable) == 8
    return F, J


def no_root(poly, variable, prime):
    assert int(S.LC(S.Poly(poly, variable))) % prime
    values = [int(poly.subs(variable, k)) % prime for k in range(prime)]
    assert 0 not in values
    return {"polynomial": str(poly), "prime": prime, "residues": values}


def universal_saturation():
    H, T, c, r = S.symbols("H T c r", nonzero=True)
    beta = r*(r+1)/c
    U = (1-H*H/c)/T+H/(r+1)
    V = beta*U+T/(r+1)-H/c
    C = beta*H+T
    B = V-(r+1)**2/c*U
    zero(U*C-V*H-1)
    zero(U*V-1-(H-r*U)*B)
    zero((H-c*T/(r+1))**2-c-c**2/(r+1)*B*T)
    other, u = S.symbols("other u")
    v = (r+1)**2/c*u
    hh = other*u
    tt = (other+1)*v-beta*hh
    zero(tt-(r+1)*(r+other+1)/c*u)
    zero(S.rem(tt**2-(r+other+1)**2/c,
               u*u-c/(r+1)**2, u))
    y, lam, b = S.symbols("y lam b", nonzero=True)
    cubic = lam*y**3/2+2*lam*b*y-b
    zero(S.discriminant(cubic, y)+16*lam**4*b**3+S.Rational(27,4)*lam**2*b*b)
    return 6


def quarter_sign_conditions():
    A, B, K, tau, eta = S.symbols("A B K tau eta")
    plus = K*(eta*K-B*tau)**2-(K+tau)*(K+A*tau)**2
    minus = K*(eta*K-B*tau)**2-(K-tau)*(K-A*tau)**2
    zero((plus-minus)/(-2*tau)-((2*A+1)*K*K+A*A*tau*tau))
    zero((plus+minus)/(2*K)-((eta*K-B*tau)**2-K*K-(A*A+2*A)*tau*tau))
    e1 = (K+B/2)**2-K*K-(A*A+2*A)/4
    e2 = (-3*K-B/2)**2-K*K-(A*A+2*A)/4
    zero(e1-e2+2*K*(4*K+B))
    zero(e1.subs(B, -4*K)+(A*A+2*A)/4)
    zero(((2*A+1)*K*K+A*A/4).subs(A,-2)+3*K*K-1)
    # One group occupies a whole quadratic; the other has two linear groups.
    for eps in (-1, 1):
        for tau_heavy, eta_heavy, tau_other, eta_other in (
            (S.Rational(-1,2),1,S.Rational(1,2),-3),
            (S.Rational(1,2),-3,S.Rational(-1,2),1),
        ):
            k = eps*tau_heavy
            aa, bb = -1, eta_heavy*k/tau_heavy
            zero((2*aa+1)*k*k+aa*aa*tau_other**2)
            assert S.cancel((eta_other*k-bb*tau_other)**2-k*k
                            -(aa*aa+2*aa)*tau_other**2) == 1
    return 9


def octic_models():
    y, x = S.symbols("y x")
    quarter = 20*y**4+48*y**3-104*y*y-216*y-3
    certificates = [no_root(quarter,y,13)]
    origins = []
    admitted = None
    for t, H, T, expected, quartic in (
        (S.Rational(1,8), -y**3-y*y+2*y+1, (y*y-1)/4,
         y*(y-2)*(y*y-2)*(9*y**4+2*y**3-34*y*y-4*y+16)/4,
         9*y**4+2*y**3-34*y*y-4*y+16),
        (S.Rational(3,8), -y**3+5*y*y/3+2*y-S.Rational(5,3), -(y*y-1)/4,
         y*(y-2)*(y*y-2)*(33*y**4-94*y**3-34*y*y+188*y-32)/4,
         33*y**4-94*y**3-34*y*y+188*y-32),
    ):
        F, J = model(y,t,S.Integer(1),H,T)
        zero(F-2-expected)
        certificates.append(no_root(quartic,y,5))
        assert S.ground_roots(F-2,y) == {S.Integer(0):1,S.Integer(2):1}
        for origin in (0,2):
            for direction in (-1,1):
                f = S.Poly(F.subs(y,origin+direction*x),x)
                j = S.Poly(J.subs(y,origin+direction*x),x)
                failures = [(i,f.nth(i),j.nth(i)) for i in range(9)
                            if not 0 <= j.nth(i) <= f.nth(i)]
                origins.append({"t":str(t),"origin":origin,"direction":direction,
                                "admissible":not failures,
                                "first_failure":[str(a) for a in failures[0]] if failures else None})
                if not failures:
                    assert admitted is None and t == S.Rational(1,8) and origin == 2 and direction == 1
                    admitted = (f.as_expr(),j.as_expr())
    F, J = model(y,S.Rational(1,4),S.Integer(3),
                 -2*y**3/3-4*y*y/3+3*y+4,(y*y-3)/9)
    zero(F-2-(2*y*y-6*y+3)*(2*y*y+6*y+3)*quarter/432)
    assert S.ground_roots(F-2,y) == {}
    assert S.discriminant(2*y*y-6*y+3,y) == 12
    assert admitted is not None
    f,j = admitted
    assert S.Poly(f,x).nth(1) == 32 and S.Poly(j,x).nth(1) == S.Rational(107,4)
    assert math.gcd(128,107) == 1
    F,J = S.expand(f.subs(x,4*y)),S.expand(j.subs(x,4*y))
    for polynomial in (F,J):
        assert all(coefficient.q == 1 for coefficient in S.Poly(polynomial,y).all_coeffs())
    assert all(int(coefficient)%64 == 0 for coefficient in S.Poly(F-2,y).all_coeffs())
    assert all(0 <= S.Poly(J,y).nth(i) <= S.Poly(F,y).nth(i) for i in range(9))
    return F,J,origins,certificates


def degree_unbounded_pell():
    a,Z,d = S.symbols("a Z d")
    b = S.Rational(32,9)-a*a
    delta = b*b-S.Rational(16,9)*a*a
    zero(delta-(3*a-8)*(3*a-4)*(3*a+4)*(3*a+8)/81)
    x = (Z+delta/Z-2*b)/(4*a*a)
    y = (Z-delta/Z)/(4*a)
    zero(y*y-a*a*x*x-b*x-S.Rational(4,9))
    z0,z1 = b+4*a/3,2*a*a+b-4*a
    f = (Z-z0)*(Z-z1)
    g = Z*f+4*a*((d-2)*f+Z*S.diff(f,Z))
    remainder = S.Poly(S.rem(g,Z*Z-delta,Z),Z)
    necessary = 9*a*a+18*(d-1)*a-16
    zero(remainder.nth(1)-S.Rational(16,81)*(3*a-8)*necessary)
    zero(remainder.nth(0)-S.Rational(32,729)*(3*a-8)*(3*a-4)*(3*a+4)*necessary)
    zero(S.discriminant(necessary,a)-36*(9*(d-1)**2+16))
    factor_pairs = [(q,16//q) for q in range(1,5) if 16%q == 0 and (q+16//q)%2 == 0]
    assert factor_pairs == [(2,8),(4,4)]
    assert [(right-left)//6 for left,right in factor_pairs] == [1,0]
    return 6


def main():
    if not __debug__:
        raise SystemExit("Do not disable assertions.")
    saturation_checks = universal_saturation()
    sign_checks = quarter_sign_conditions()
    F,J,origins,certificates = octic_models()
    pell_checks = degree_unbounded_pell()
    result = {
        "status":"passed",
        "scope":"All octic saturated branches and all balanced t=1/2 branches with d1=2, d>=3; not general i=3.",
        "universal_saturation_identity_checks":saturation_checks,
        "quarter_sign_reduction_checks":sign_checks,
        "degree_unbounded_pell_identity_checks":pell_checks,
        "all_rational_origin_and_sign_checks":origins,
        "rational_root_exclusion_certificates":certificates,
        "saturated_octic_integer_family":{"F":str(F),"J":str(J),"parameter":"y=k*X, k positive integer"},
        "integer_obstruction":"F-2 has all coefficients divisible by 64; 4 divides n is required for a counterexample",
        "unbounded_degree_obstruction":"t=1/2, d1=2, d>=3 forces 9*a^2+18*(d-1)*a-16=0, whose rational discriminant is impossible",
        "remaining_octic_branch":{"t":"3/8","d":[3,3,2],"h":3,"up_to_complement":True},
        "complete_prime_power_multiplicities_preserved":True,
        "octic_all_branches_excluded":False,
        "general_i3_solved":False,
        "complete_problem_solution":False,
    }
    output = ROOT/"data/results/verification_i3_octic_saturation_and_pell.json"
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
