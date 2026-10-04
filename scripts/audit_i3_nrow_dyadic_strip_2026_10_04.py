"""Exact certificates for n-row dyadic strips and a resultant-zero exclusion.

This is a conditional necessary-condition result, not a proof of Erdos 699.
"""
from pathlib import Path
from math import gcd
from fractions import Fraction
import json
import sympy as sp


def divisors(value):
    small, large = [], []
    root = sp.integer_nthroot(value, 2)[0]
    for d in range(1, root + 1):
        if value % d == 0:
            small.append(d)
            if d * d != value:
                large.append(value // d)
    return small + large[::-1]


def v2(value):
    assert value > 0
    return (value & -value).bit_length() - 1


def run():
    X, a, s, c, j, r = sp.symbols('X a s c j r')
    # The complete range inequality, with n=2j+r and r>=0.
    n = 2*j + r
    assert sp.expand(n*(n-2)-4*j*(j-1)-r*(4*j+r-2)) == 0
    gamma0 = Fraction(139,160)
    joint_threshold = Fraction(4,3)*gamma0*gamma0
    assert joint_threshold == Fraction(19321,19200) > 1

    F = 1+(a-s)*X+a*s*X**2
    R = c*c-a*c+s*(a+c)
    B = c*(a-s)-2*a*s
    assert sp.expand(c*c*F-(a*s*(1+c*X)+B)*(1+c*X)-R) == 0
    assert sp.expand(sp.resultant(F, 1+c*X, X)-R) == 0
    M, H, q = sp.symbols('M H q')
    pell = (2*a*s*q+a-s)**2-4*a*s*M*H-(a*a-6*a*s+s*s)
    assert sp.expand(pell-4*a*s*(F.subs(X,q)-M*H)) == 0

    W, x = sp.symbols('W x')
    w = 1+W
    sr = w+x
    dr = sr+w
    cr = sr*(2*sr+w)/w
    ar = cr+dr+sr
    assert sp.cancel(ar*sr-cr*dr) == 0
    assert sp.cancel(cr*cr-ar*cr+sr*(ar+cr)) == 0
    assert sp.cancel(F.subs({a:ar,s:sr})-(1+cr*X)*(1+dr*X)) == 0
    difference = sp.cancel(w*w*(cr*cr*dr*dr+cr+dr-3*(2*cr+dr+sr)))
    certificate = sp.Poly(sp.expand(difference),W,x)
    assert len(certificate.terms()) == 28
    assert min(certificate.coeffs()) == 4
    assert certificate.coeff_monomial(1) == 14

    # Strict low coefficient/range argument a>=2v.
    # Set a-2v=-1-z, h<=2 and epsilon>=0. This is a universal majorant.
    z = sp.symbols('z')
    majorant = 1+(3*s-1)*q-s*q*q
    assert sp.expand(majorant-(1-q-s*q*(q-3))) == 0
    shifted = sp.Poly(sp.expand(-majorant.subs({q:5+W,s:1+x})),W,x)
    assert all(coefficient > 0 for coefficient in shifted.coeffs())

    # Exact numerical diagnostics independently use the raw n-row and first
    # conditions, then discover each admissible q,D01 and verify all gcds.
    # These are weak necessary-condition tuples, never claimed counterexamples.
    raw_count = 0
    strip_count = 0
    examples = []
    for nv in range(8,2001,4):
        Hv = 1 << v2(nv)
        Mv = nv//Hv
        qs = [d for d in divisors(nv-1) if d >= 5]
        for jv in range(4,nv//2+1):
            numerator = 3*jv*(jv-1)
            if numerator % (nv-1) or 3*jv % Mv:
                continue
            raw_count += 1
            for Dv in divisors(gcd(nv-2,jv*(jv-1))):
                kv = numerator//((nv-1)*Dv)
                if numerator % ((nv-1)*Dv):
                    continue
                for qv in qs:
                    if jv*(jv-1) % (qv*Dv):
                        continue
                    Av = (nv-1)//qv
                    assert gcd(Mv,qv*Dv*Av) == 1
                    assert kv % Mv == 0
                    eta = v2(Dv)
                    assert eta in (0,1)
                    omega = v2(kv)
                    assert omega == v2(jv*(jv-1))-eta
                    assert Hv > Fraction(4,3)*(1 << omega)*Dv
                    assert Fraction(nv,kv) >= Fraction(4*(nv-1)*Dv,3*(nv-2))
                    strip_count += 1
                    if len(examples) < 8:
                        examples.append(dict(n=nv,j=jv,q=qv,D01=Dv,M=Mv,H=Hv,k=kv,omega=omega))
    assert raw_count > 0 and strip_count > 0

    result = dict(
        status='passed',
        scope='Conditional n-row dyadic strip and E0 N1 resultant-zero exclusion; not general i=3 or Erdos 699.',
        exact_identities=8,
        general_joint_degree_budget=dict(
            shared_factor_lower_constant=str(gamma0),strict_threshold=str(joint_threshold),
            hypotheses='Largest full Q1 prime-power q>=2^24; general exact G0,G1; no complete allocation.',
            conclusion='floor(log_q oddpart(n))+deg(G0)+deg(G1)<=deg(F)'),
        resultant_zero_positive_certificate=dict(
            terms=len(certificate.terms()),minimum_coefficient=int(min(certificate.coeffs())),constant=int(certificate.coeff_monomial(1)),
            coefficients=[dict(powers=list(powers),coefficient=int(coefficient)) for powers,coefficient in certificate.terms()]),
        numerical_diagnostics=dict(n_max=2000,raw_first_and_nrow_pairs=raw_count,admissible_strip_tuples=strip_count,examples=examples),
        remaining='High H and nonzero resultant branches are not closed. No extrapolation from finite diagnostics.')
    assert result['status'] == 'passed'
    path = Path(__file__).resolve().parents[1]/'data/results/verification_i3_nrow_dyadic_strip_2026-10-04.json'
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],scope=result['scope'],strip_tuples=strip_count,
                          positive_terms=len(certificate.terms())),ensure_ascii=False,indent=2))
    return result


if __name__ == '__main__':
    assert run()['status'] == 'passed'
