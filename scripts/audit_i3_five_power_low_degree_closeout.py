"""Exact certificates excluding the Chebyshev cores D=25 and D=125.

This does not classify all degree-25/125 lifts and does not solve general i=3.
Only standard Python and SymPy are needed. Polynomial powers and Bezout
identities are replayed with integer lists, independently of the exploratory
finite-field package. All coefficient lists use ascending powers.
"""
import hashlib
import json
import math
from pathlib import Path

import sympy as S

from audit_i3_five_power_composition import f_mod, universal_root, universal_norm_constants
from audit_i3_quintic_closeout import add, mul, polynomial_power, remainder, scale, trim

ROOT = Path(__file__).resolve().parent.parent


def modular_polynomial(a, q):
    return trim([x % q for x in a])


def divide(a, b, q):
    a, b = modular_polynomial(a,q), modular_polynomial(b,q)
    quotient = [0]*max(1,len(a)-len(b)+1)
    inverse = pow(b[-1],-1,q)
    while a != [0] and len(a) >= len(b):
        shift = len(a)-len(b)
        coefficient = a[-1]*inverse % q
        quotient[shift] = coefficient
        for i, value in enumerate(b):
            a[i+shift] = (a[i+shift]-coefficient*value) % q
        a = trim(a)
    return trim(quotient), a


def extended_gcd(a, b, q):
    r0,r1 = modular_polynomial(a,q),modular_polynomial(b,q)
    c0,c1,e0,e1 = [1],[0],[0],[1]
    while r1 != [0]:
        quotient,r2 = divide(r0,r1,q)
        c2 = modular_polynomial(add(c0,scale(mul(quotient,c1),-1)),q)
        e2 = modular_polynomial(add(e0,scale(mul(quotient,e1),-1)),q)
        r0,r1,c0,c1,e0,e1 = r1,r2,c1,c2,e1,e2
    inverse = pow(r0[-1],-1,q)
    return (modular_polynomial(scale(r0,inverse),q),
            modular_polynomial(scale(c0,inverse),q),
            modular_polynomial(scale(e0,inverse),q))


def prime_and_order(q, order):
    assert q > 2 and q % 2
    assert all(q % d for d in range(3,math.isqrt(q)+1,2))
    assert pow(2,order,q) == 1
    factors = [int(p) for p in S.factorint(order)]
    assert all(pow(2,order//p,q) != 1 for p in factors)
    return {"q":q,"order_2":order,"order_prime_factors":factors,
            "primality_checked_by":"trial division through isqrt(q)"}


def exponent_residue(m, n_residue, precision):
    u = next(u for u in range(4) if m*pow(2,u,5) % 5 == n_residue % 5)
    for r in range(1,precision):
        period = 4*5**(r-1)
        roots = [u+h*period for h in range(5)
                 if m*pow(2,u+h*period,5**(r+1)) % 5**(r+1) == n_residue % 5**(r+1)]
        assert len(roots) == 1
        u = roots[0]
    assert 0 <= u < 4*5**(precision-1)
    return u


def core_coefficients(d):
    w = S.symbols("w")
    expression = (S.chebyshevt(d,w)+d*(w-1)*S.chebyshevu(d-1,w)+3)/2
    polynomial = S.Poly(expression,w,domain=S.QQ)
    assert polynomial.degree() == d
    coefficients = [polynomial.nth(k) for k in range(d+1)]
    assert all(c.q == 1 for c in coefficients)
    assert polynomial.eval(1) == 2 and polynomial.eval(-1) == 1-d*d
    return [int(c) for c in coefficients]


def frobenius_certificate(coefficients, q, target):
    polynomial = modular_polynomial(add(coefficients,[-target]),q)
    frobenius = remainder(add(polynomial_power([0,1],q,polynomial,q),[0,-1]),polynomial,q)
    gcd,c,e = extended_gcd(polynomial,frobenius,q)
    assert gcd == [1]
    assert modular_polynomial(add(mul(c,polynomial),mul(e,frobenius)),q) == [1]
    return {"q":q,"target":target,"polynomial":polynomial,
            "frobenius_remainder":frobenius,"bezout_C":c,"bezout_E":e,
            "identity":"C*polynomial+E*frobenius_remainder=1 in F_q[w]"}


def audit_core(a, specifications):
    d = 5**a
    precision = 4*a+1
    eta,_ = universal_root(2*a)
    zeta,_ = universal_norm_constants(eta,2*a)
    modulus = 5**precision
    n_residue = (2+5**(2*a+1)*zeta) % modulus
    coefficients = core_coefficients(d)
    w = 1+5*eta
    exact_n = sum(c*w**k for k,c in enumerate(coefficients))
    assert exact_n % modulus == n_residue == f_mod(d,w,modulus)
    odd_part = d*d-1
    while odd_part % 2 == 0:
        odd_part //= 2
    odd_divisors = [int(m) for m in S.divisors(odd_part)]
    exponents = {m:exponent_residue(m,n_residue,precision) for m in odd_divisors}
    period = 4*5**(precision-1)
    multiplier = 1 if a == 2 else 3
    covered = set()
    certificates, prime_records = [],[]
    for q,order,selections in specifications:
        prime_records.append(prime_and_order(q,order))
        assert (multiplier*period) % order == 0
        subclass_count = order//math.gcd(order,period)
        assert subclass_count in (1,multiplier)
        for m,subclasses in selections.items():
            assert m in exponents
            for h in subclasses:
                assert 0 <= h < subclass_count
                u = exponents[m]+period*h
                target = m*pow(2,u,q) % q
                certificate = frobenius_certificate(coefficients,q,target)
                certificate.update({"M":m,"subclass":h,"subclass_count":subclass_count,
                                    "u_representative":u})
                certificates.append(certificate)
                for global_h in range(multiplier):
                    if (global_h-h) % subclass_count == 0:
                        assert m*pow(2,exponents[m]+period*global_h,q) % q == target
                        covered.add((m,global_h))
    expected = {(m,h) for m in odd_divisors for h in range(multiplier)}
    assert covered == expected
    return {"a":a,"D":d,"eta_mod_5_to_2a":eta,
            "necessary_n_five_modulus":modulus,"necessary_n_residue":n_residue,
            "exponent_period":period,"exponent_residues":exponents,
            "core_coefficients":coefficients,"odd_part_D_squared_minus_one":odd_part,
            "all_odd_divisors":odd_divisors,"global_subclass_multiplier":multiplier,
            "primes":prime_records,"covered_cases":len(covered),"certificates":certificates,
            "scope":"all counterexample evaluations of this Chebyshev core excluded; not all degree-D lifts"}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled: do not use python -O.")
    cases = [audit_core(2,[
        (62501,62500,{1:[0],39:[0]}),
        (437501,62500,{3:[0],13:[0]}),
    ]),audit_core(3,[
        (4750000001,312500,{1:[0],7:[0],63:[0]}),
        (2031251,156250,{3:[0],93:[0],279:[0],1953:[0]}),
        (937501,937500,{651:[0,1,2]}),
        (30000001,234375,{9:[0,1,2]}),
        (255000001,468750,{31:[0,1,2]}),
        (16406251,2343750,{21:[1,2],217:[0,1]}),
        (18750001,1171875,{21:[0]}),
        (9375001,4687500,{217:[2]}),
    ])]
    certificate = {"coefficient_order":"ascending","cases":cases,
                   "complete_problem_solution":False}
    path = ROOT/"data/certificates/i3_five_power_low_degree_closeout_2026-10-01.json"
    raw = (json.dumps(certificate,indent=2)+"\n").encode()
    path.write_bytes(raw)
    result = {"passed":True,"excluded_Chebyshev_cores":[25,125],
              "certificate_count":sum(len(case["certificates"]) for case in cases),
              "covered_cases":[case["covered_cases"] for case in cases],
              "certificate_sha256":hashlib.sha256(raw).hexdigest(),
              "independent_integer_polynomial_replay":True,
              "all_degrees_25_and_125_classified":False,
              "all_five_power_cores_closed":False,"complete_problem_solution":False,
              "remaining_five_power_core_exponents":"a >= 4",
              "remaining_indices":28}
    (ROOT/"data/results/verification_i3_five_power_low_degree_closeout.json").write_text(
        json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
