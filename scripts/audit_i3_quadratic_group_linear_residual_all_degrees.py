"""Derived finite certificate for an arbitrary-degree conditional i=3 family."""
from fractions import Fraction
from pathlib import Path
import json
import sympy as s


def generate():
    count = 0
    quotients = []
    # These limits follow from the proof: ell <= 20, lambda <= 18, q <= 70.
    for h in (1,2):
        for g in (0,1):
            for ell in range(1,21):
                for lam in range(1,19):
                    Z = lam+6*h+(2-g)*ell
                    for q in range(5,min(70,Z)+1,2):
                        if Z % q:
                            continue
                        z = Z//q
                        for a in range(2,q):
                            for w in range(1,(q-1)//a+1):
                                for v in range(h,h*a):
                                    if (6*v-z) % lam:
                                        continue
                                    b = (6*v-z)//lam-w*q
                                    if b >= a or (b < 0 and b*b >= 4*w):
                                        continue
                                    E = 1+b*q+w*q*q
                                    P = (a*q-1)*E
                                    R = v*q-h
                                    T = 3*R*R-ell*P
                                    V = 6*P+ell-9*R
                                    assert E > 0 and P > 144
                                    assert lam*E == 6*v*q-6*h-(2-g)*ell
                                    count += 1
                                    if T == 0:
                                        assert V != 0
                                        continue
                                    if V % T:
                                        continue
                                    Q = V//T
                                    if Q > q and Q % q == 1:
                                        quotients.append(dict(q=q,h=h,g=g,a=a,b=b,w=w,v=v,
                                                              ell=ell,lam=lam,Q=Q))
    return count,quotients


def main():
    # All q, a, w, v and polynomial degrees in the proof are variable.
    # The inequalities below certify the constants used to derive finite bounds.
    assert (1-Fraction(1,10))*(1-Fraction(1,5))**2 == Fraction(72,125)
    assert 3/Fraction(72,125) == Fraction(125,24)
    assert Fraction(125*4,24) < 21
    assert Fraction(75*2,8) < 19
    assert 18+6*2+2*20 == 70
    assert Fraction(125*2,12*5) == Fraction(25,6)
    assert 6*5-Fraction(25,6)-6 > 0  # C > 0 using v >= h.
    # Split E = B0 B1: the bound excludes h=1 and h=2 with b,c >= 2.
    assert Fraction(10,3*2**2) == Fraction(5,6) < 1
    assert Fraction(10*2**2,3*4**2) == Fraction(5,6) < 1
    # If h=2 and b=1 or c=1, evaluating J at -1 would require
    # an integer multiple of v+h >= 4 to equal 2 or 1.
    assert 2 < 2+2 and 1 < 2+2
    P,R,Q,ell = s.symbols('P R Q ell')
    expanded = 3*(2+R*Q)*(1+R*Q)-(6+ell*Q)*(P*Q+1)
    assert s.expand(expanded-Q*((3*R**2-ell*P)*Q-(6*P+ell-9*R))) == 0
    assert s.expand(6*(3*R**2-ell*(9*R-ell)/6)-(3*R-ell)*(6*R-ell)) == 0
    count,quotients = generate()
    assert count == 12258
    assert not quotients
    result = dict(status='passed',scope='Conditional standard-digit complete allocation: B2 arbitrary nonconstant degree, (J-2)/B2 linear, and B0B1 of degree two (one quadratic group or two linear groups). All odd q >= 5 excluded. Not general i=3 or Erdős 699.',
                  derived_bounds=dict(q=70,ell=20,lambda_=18),
                  full_finite_parameter_rows=count,admissible_integer_Q_values=len(quotients),
                  identities_checked=2)
    output = Path(__file__).resolve().parents[1]/'data/results/verification_i3_quadratic_group_linear_residual_all_degrees.json'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
