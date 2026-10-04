"""Finite boundary certificate for the arbitrary-degree linear J-2 quotient theorem."""
from fractions import Fraction
from pathlib import Path
import json
import sympy as sp


def main():
    rows = []
    exceptions = []
    q = 5
    for h in (1, 2):
        for a in range(2, q):
            for L in range(1, (q-1)//a+1):
                for s in range(1, L+1):
                    if L % s:
                        continue
                    for v in range(h, h*a):
                        if v*s >= q:
                            continue
                        upper = Fraction(3*v*v*q, L*(v*q-h)*(a*q-1))
                        row = (h,a,L,s,v,upper)
                        rows.append(row)
                        if upper >= 1:
                            exceptions.append(row)
    assert len(rows) == 19
    assert exceptions == [(2,2,1,1,3,Fraction(15,13))]
    assert all(row[-1]/5 < 1 for row in rows)  # d>=4 at q=5.
    # For q>=7, v<=2a-1 and (2a-1)/(aq-1)<2/q give ell<6/(q-1)<=1.
    assert Fraction(6,7-1) == 1
    a,q_symbol = sp.symbols('a q')
    assert sp.expand(2*(a*q_symbol-1)-q_symbol*(2*a-1)) == q_symbol-2
    w = sp.symbols('w')
    x = -2*w/3
    assert sp.expand(1+w*x*x+x**3) == 1+4*w**3/27
    assert 1+Fraction(4*(-2)**3,27) < 0
    assert 1-5**2+5**3 == 101
    assert Fraction(3*3**2*5**2,9*101) == Fraction(75,101) < 1
    result = dict(
        status='passed',
        scope='Conditional standard-digit complete allocation with (J-2)/B2 linear, B2 of any nonconstant degree, and deg(B0B1)>=2. No degree cap. Not general i=3 or Erdos 699.',
        q5_parameter_rows=len(rows),
        d3_boundary_exceptions=[dict(h=2,a=2,L=1,s=1,v=3,upper='15/13',final_upper='75/101')],
        degree2_certificate='verification_i3_quadratic_group_linear_residual_all_degrees.json',
    )
    previous = Path(__file__).resolve().parents[1]/'data/results/verification_i3_quadratic_group_linear_residual_all_degrees.json'
    assert json.loads(previous.read_text(encoding='utf-8'))['status'] == 'passed'
    output = previous.with_name('verification_i3_linear_J2_quotient_degree_ge2_all_degrees.json')
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
