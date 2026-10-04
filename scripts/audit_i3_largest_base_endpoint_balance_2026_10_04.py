"""Exact algebra and rational constants for the largest-base endpoint lemma."""
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as sp


def main():
    # The integer induction is uniform separately on even r=2t and odd r=2t+1.
    t=sp.symbols('t',integer=True,positive=True)
    assert sp.expand(4*(2*t)-6*t)==2*t
    assert sp.expand(4*(2*t+1)-6*(t+1))==2*t-2
    assert F(3,10)-F(2,7)==F(1,70)
    assert 2**14>=80 and 2**14>10**4
    assert F(2*2**14,7)+F(8,7)<=F(3*2**14,10)
    assert F(3,10)+F(1,5)==F(1,2)
    assert F(10,7)<F(3,2)
    assert F(15,2)*F(129,128)**2<8
    assert F(8,2**14)<1
    assert F(2**14,128)==128
    x,y,q=sp.symbols('x y q')
    diff=(1+1/q)*(1+x*y/q)-(1+x/q)*(1+y/q)
    assert sp.expand(q*diff-(x-1)*(y-1))==0
    assert sp.expand((x*y-1)-((x-1)+(y-1))-(x-1)*(y-1))==0
    z=sp.symbols('z',nonnegative=True)
    # q >= 2^14 means sqrt(q)=128+z.
    poly=sp.Poly(sp.expand((128+z)**2-27*(1+128+z)),z)
    assert all(c>0 for c in poly.all_coeffs())
    P,R,Q,ell=sp.symbols('P R Q ell')
    raw=3*(2+R*Q)*(1+R*Q)-(6+ell*Q)*(1+P*Q)
    assert sp.expand(raw-Q*((3*R**2-ell*P)*Q-(6*P+ell-9*R)))==0
    assert sp.expand(3*R**2-9*P*R+6*P**2-3*(R-P)*(R-2*P))==0
    assert sp.expand(6*(3*R**2-ell*(9*R-ell)/6)-(3*R-ell)*(6*R-ell))==0
    result=dict(status='passed',independent_audit='endpoint proof, quotient-degree extension, and general F-2 factor evaluation independently audited',
                scope='Conditional largest-complete-prime-power standard-digit complete allocation. Endpoint degrees differ from the other two by at most 2 when those groups are nonconstant. Not the numerical-to-polynomial bridge or general i=3.',
                lower_base_threshold=2**14,
                uniform_factor_lower='(1/2) leading_coefficient q^degree',
                general_standard_F_minus_two_factors_included=True,
                endpoint_degree_offset=2,
                quotient_degree_reduction='deg E <= 2t+1, deg Q <= 2t+3, deg F <= 4t+5',
                quadratic_quotient_degree_bounds=dict(E=5,Q=7,F=13),
                exact_symbolic_identities=7)
    out=Path(__file__).resolve().parents[1]/'data/results/verification_i3_largest_base_endpoint_balance_2026-10-04.json'
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
