"""Exact diagnostics for the all-exponent five-power frontier.

Modular evaluations use O(log D) ring powering; D=5**100 is never expanded
as a degree-D polynomial. The mathematical claims are proved in the note.
Local congruence certificates are not numerical counterexamples.
"""
import json
import math
from fractions import Fraction
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent


def chebyshev_pair(d, w, modulus=None):
    """(w+sqrt(w*w-1))**d = T_d(w)+U_{d-1}(w)*sqrt(...)."""
    delta = w*w-1
    if modulus is not None:
        delta %= modulus
        w %= modulus
    a, b, c, e = 1, 0, w, 1
    while d:
        if d & 1:
            a, b = a*c+delta*b*e, a*e+b*c
            if modulus is not None:
                a %= modulus
                b %= modulus
        c, e = c*c+delta*e*e, 2*c*e
        if modulus is not None:
            c %= modulus
            e %= modulus
        d //= 2
    return a, b


def f_mod(d, w, modulus):
    t, u = chebyshev_pair(d, w, 2*modulus)
    numerator = (t+d*(w-1)*u+3) % (2*modulus)
    assert numerator % 2 == 0
    return numerator//2


def j_mod(d, w, modulus):
    t, u = chebyshev_pair(d, w, 2*d*modulus)
    numerator = (d*(t+1)+(w+1)*u) % (2*d*modulus)
    assert numerator % (2*d) == 0
    return numerator//(2*d)


def s_mod(d, y, precision):
    assert y % 5
    modulus = 5**precision
    j = j_mod(d, 1+5*y, 5*modulus)
    assert (j-2) % 5 == 0
    return ((j-2)//5)*pow(y, -1, modulus) % modulus


def vp(n, p):
    assert n
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def limit_coefficients(precision):
    # c_k is the coefficient of Y**(k-1) in the universal S_0.
    coefficient = Fraction(1, 6)
    modulus = 5**precision
    result = []
    for k in range(1, 2*precision+1):
        assert coefficient.denominator % 5
        result.append(coefficient.numerator*pow(coefficient.denominator, -1, modulus) % modulus)
        coefficient *= Fraction(-5*k, 2*k+3)
    return result


def polynomial_value_derivative(coefficients, y, modulus):
    value, derivative = 0, 0
    for coefficient in reversed(coefficients):
        derivative = (derivative*y+value) % modulus
        value = (value*y+coefficient) % modulus
    return value, derivative


def universal_root(precision):
    coefficients = limit_coefficients(precision)
    root, current = 1, 1
    while current < precision:
        current = min(2*current, precision)
        modulus = 5**current
        value, derivative = polynomial_value_derivative(coefficients, root, modulus)
        assert derivative % 5 == 4
        root = (root-value*pow(derivative, -1, modulus)) % modulus
        assert polynomial_value_derivative(coefficients, root, modulus)[0] == 0
    return root, coefficients


def universal_norm_constants(eta, precision):
    """zeta=2*eta/(2+5*eta), kappa=5*zeta/(2*log(16)) in Z_5."""
    modulus = 5**precision
    zeta = 2*eta*pow(2+5*eta, -1, modulus) % modulus
    log_quotient = 0
    for k in range(1, 2*precision+3):
        term = Fraction((-1)**(k-1)*15**k, 5*k)
        assert term.denominator % 5
        log_quotient += term.numerator*pow(term.denominator, -1, modulus)
    log_quotient %= modulus
    assert log_quotient % 5 == 3
    kappa = zeta*pow(2*log_quotient, -1, modulus) % modulus
    assert zeta % 5 == kappa % 5 == 1
    return zeta, kappa


def independent_calibration():
    """Compare ring powering with independent second-order recurrences."""
    cases = []
    for d, w in ((1, 2), (3, 4), (5, -4), (5, 31), (25, 281), (125, 6531)):
        t0, t1 = 1, w
        for _ in range(1, d):
            t0, t1 = t1, 2*w*t1-t0
        u0, u1 = 0, 1
        for _ in range(1, d):
            u0, u1 = u1, 2*w*u1-u0
        assert chebyshev_pair(d, w) == (t1, u1)
        f_numerator = t1+d*(w-1)*u1+3
        j_numerator = d*(t1+1)+(w+1)*u1
        assert f_numerator % 2 == 0 and j_numerator % (2*d) == 0
        f, j = f_numerator//2, j_numerator//(2*d)
        for modulus in (3, 32, 625, 3125, 28001):
            assert chebyshev_pair(d, w, modulus) == (t1 % modulus, u1 % modulus)
            assert f_mod(d, w, modulus) == f % modulus
            assert j_mod(d, w, modulus) == j % modulus
        cases.append({"D":d, "w":w, "moduli_checked":5})
    return cases


def degree_root(d, a, precision, eta):
    current = min(precision, 2*a+1)
    root = eta % 5**current
    assert s_mod(d, root, current) == 0
    while current < precision:
        modulus = 5**current
        candidates = [root+digit*modulus for digit in range(5)]
        roots = [y for y in candidates if s_mod(d, y, current+1) == 0]
        assert len(roots) == 1
        root, current = roots[0], current+1
    return root


def root_mod_two(d, precision):
    root = 1
    assert f_mod(d, root, 2) == 0
    for r in range(1, precision):
        candidates = [root, root+2**r]
        roots = [w for w in candidates if f_mod(d, w, 2**(r+1)) == 0]
        assert len(roots) == 1
        root = roots[0]
    return root


def coprime_crt(first, modulus, second, next_modulus):
    assert math.gcd(modulus, next_modulus) == 1
    correction = (second-first)*pow(modulus, -1, next_modulus) % next_modulus
    return (first+modulus*correction) % (modulus*next_modulus), modulus*next_modulus


def exponent_mod_five(n_residue, a, precision):
    # n=2 mod 5**(2*a+1), so the logarithm starts at exponent 1.
    root, current = 1, 2*a+1
    assert pow(2, root, 5**current) == n_residue % 5**current
    while current < precision:
        period = 4*5**(current-1)
        candidates = [root+digit*period for digit in range(5)]
        roots = [u for u in candidates if pow(2, u, 5**(current+1)) == n_residue % 5**(current+1)]
        assert len(roots) == 1
        root, current = roots[0], current+1
    return root, 4*5**(precision-1)


def order_two(r):
    if r == 1:
        return 1
    order = int(S.n_order(2, r))
    assert pow(2, order, r) == 1
    assert all(pow(2, order//p, r) != 1 for p in S.factorint(order))
    return order


def local_certificate(a, r, two_precision, extra, eta):
    """A witness to consistency of finitely many congruences, not F=2**u."""
    assert math.gcd(r, 10) == 1
    assert extra >= 1
    d = 5**a
    order = order_two(r)
    assert order % 5 or vp(order, 5) <= 2*a
    precision = 2*a+1+extra
    modulus5 = 5**precision
    y = degree_root(d, a, precision-1, eta)
    w5 = 1+5*y
    assert j_mod(d, w5, modulus5) == 2
    n5 = f_mod(d, w5, modulus5)
    u5, period5 = exponent_mod_five(n5, a, precision)
    if extra:
        assert u5 % (4*5**(2*a+1)) == 1+4*5**(2*a)
    common = math.gcd(period5, order)
    assert (u5-1) % common == 0
    cofactor = order//common
    correction = 0 if cofactor == 1 else (
        ((1-u5)//common)*pow(period5//common, -1, cofactor) % cofactor)
    u = u5+period5*correction
    period = period5*cofactor
    while u < max(two_precision, 51):
        u += period
    w2 = root_mod_two(d, two_precision)
    w, modulus = w2, 2**two_precision
    if r > 1:
        w, modulus = coprime_crt(w, modulus, 1, r)
    w, modulus = coprime_crt(w, modulus, w5, modulus5)
    if w < 6:
        w += modulus
    assert (w-1) % 5 == 0 and ((w-1)//5) % 5 == 1
    assert f_mod(d, w, modulus) == pow(2, u, modulus)
    assert j_mod(d, w, r*modulus5) == 2
    assert f_mod(d, w, 4) == 0
    assert (pow(2, u, 5**(2*a+2))-2) % 5**(2*a+2) == 5**(2*a+1)
    return {"a":a,"R":r,"order_2_mod_R":order,
            "two_precision":two_precision,"extra_five_precision":extra,
            "u":str(u),"w":str(w),"modulus":str(modulus),
            "scope":"finite congruences only; equality F_D(w)=2^u is not asserted"}


def formal_composition():
    x, p, b, pk, bk, k = S.symbols("x p b P_k B_k k")
    nd = 2+25*k*k*x*b*bk*(p*pk+b*bk)/2
    nl = 2+25*x*b*b*k*k*bk*(pk+bk)/2
    jd = (x+2)*p*pk*(p*pk+b*bk)/2
    jl = (x+2)*p*p*pk*(pk+bk)/2
    assert S.expand(nd-nl-25*k*k*x*b*bk*pk*(p-b)/2) == 0
    assert S.expand(jd-jl+(x+2)*p*pk*bk*(p-b)/2) == 0
    y = S.symbols("y")
    pp = 1+30*y+100*y*y
    bb = 1+10*y+20*y*y
    assert S.expand(pp-bb-20*y*(1+4*y)) == 0
    assert S.expand((5*y+2)*pp**2-25*5*y*bb**2-2) == 0
    from audit_i3_chebyshev_boundary import half_polynomials, w as old_w
    cases = []
    for kk in (1, 5, 25):
        psmall, qsmall = half_polynomials(2)
        pk0, qk0 = half_polynomials((kk-1)//2)
        pd, qd = half_polynomials((5*kk-1)//2)
        inner = S.chebyshevt(5, old_w)
        assert S.expand(pd-psmall*pk0.subs(old_w,inner)) == 0
        assert S.expand(qd-qsmall*qk0.subs(old_w,inner)) == 0
        cases.append({"k":kk,"D":5*kk})
    return {"formal_correction_identities":4,"polynomial_composition_cases":cases}


def numerical_diagnostics():
    exponents = list(range(1,61))+[75,100]
    precision = 2*max(exponents)+1
    eta, coefficients = universal_root(precision)
    zeta, kappa = universal_norm_constants(eta, precision)
    prefix = [{"precision":r,"residue":str(eta % 5**r)} for r in range(1,13)]
    root_checks, norm_checks, modulo_three_checks, composition_cases = 0, 0, 0, []
    exponent_cases = []
    for a in exponents:
        d = 5**a
        current = 2*a+1
        modulus = 5**current
        for y in (1,2,6,56,eta % modulus):
            assert s_mod(d,y,current) == polynomial_value_derivative(coefficients,y,modulus)[0]
            root_checks += 1
        norm_modulus = 5**(4*a+1)
        eta_a = eta % 5**(2*a)
        n_residue = (2+5**(2*a+1)*zeta) % norm_modulus
        for digit in range(5):
            assert f_mod(d,1+5*(eta_a+digit*5**(2*a)),norm_modulus) == n_residue
            norm_checks += 1
        u = 1+4*d*d*(kappa % 5**(2*a))
        assert u < 4*d**4 and u >= 4*d*d+1
        assert pow(2,u,norm_modulus) == n_residue
        exponent_cases.append({"a":a,"modulus":str(4*d**4),"pure_power_u_residue":str(u),
                               "n_five_modulus":str(norm_modulus),"n_residue":str(n_residue)})
        for w in range(6):
            assert (f_mod(d,w,3) == 0) == ((w+1) % 3 == 0)
            modulo_three_checks += 1
        if a == 1:
            continue
        y = eta % 5**(2*a)
        w = 1+5*y
        p = 1+30*y+100*y*y
        b = 1+10*y+20*y*y
        assert vp(p-b,5) == 3
        lower_w = chebyshev_pair(5,w)[0]
        assert vp(lower_w-1,5) == 3
        mm = 5**(2*a+5)
        nu,ju = f_mod(d,w,mm),j_mod(d,w,mm)
        nl,jl = f_mod(d//5,lower_w,mm),j_mod(d//5,lower_w,mm)
        assert vp((nu-2) % mm,5) == 2*a+1
        assert vp((nl-2) % mm,5) == 2*a+1
        assert (ju-2) % 5**(2*a+1) == 0
        assert vp((jl-2) % mm,5) == 3
        assert vp((nu-nl) % mm,5) == 2*a+4
        assert vp((ju-jl) % mm,5) == 3
        composition_cases.append({"a":a,"n_difference_v5":2*a+4,"j_difference_v5":3,
                                  "lower_j_minus_two_v5":3})
    certificates = []
    for a in (2,3,5,10,25,50,100):
        for r, k2, extra in ((11,12,1),(31,17,3),(28001,23,8),(341,16,4)):
            certificates.append(local_certificate(a,r,k2,extra,eta))
    return {"universal_root_prefix":prefix,"root_congruence_checks":root_checks,
            "universal_norm_prefix":[{"precision":r,"zeta":str(zeta % 5**r),
                                       "kappa":str(kappa % 5**r)} for r in range(1,13)],
            "norm_residue_checks":norm_checks,"pure_power_exponent_cases":exponent_cases,
            "modulo_three_checks":modulo_three_checks,"composition_valuation_cases":composition_cases,
            "local_certificates":certificates,
            "maximum_a":max(exponents),"D_maximum":str(5**max(exponents))}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled: do not use python -O.")
    result = {"passed":True,
              "scope":"all-exponent composition corrections, common five-adic branch, pure-power height and fixed-modulus obstruction; no uniform five-power closeout",
              "independent_calibration":independent_calibration(),
              "formal":formal_composition(),"numerical":numerical_diagnostics()}
    path = ROOT/"data/results/verification_i3_five_power_composition.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    z = result["numerical"]
    print(json.dumps({"passed":True,"maximum_a":z["maximum_a"],
                      "root_congruence_checks":z["root_congruence_checks"],
                      "norm_residue_checks":z["norm_residue_checks"],
                      "modulo_three_checks":z["modulo_three_checks"],
                      "composition_valuation_cases":len(z["composition_valuation_cases"]),
                      "local_certificates":len(z["local_certificates"]),
                      "universal_root_prefix":z["universal_root_prefix"][:6]}))


if __name__ == "__main__":
    main()
