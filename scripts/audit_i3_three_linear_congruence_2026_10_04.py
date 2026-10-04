"""Exact certificate for the short three-linear congruence argument.

This verifies conditional polynomial branches, not Erdős problem 699.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import isqrt
import json
import sympy as s


def run():
    x, y = s.symbols("x y")
    f = (1-x)*(1-y)*(1+x+x*y)**2
    gap = (1-x)*(1+x)**2-f
    assert s.expand(gap-(1-x)*((1-x)*(1+x)*y+x*(2+x)*y*y+x*x*y**3)) == 0
    assert s.expand(32-27*(1-x)*(1+x)**2-(3*x-1)**2*(3*x+5)) == 0
    assert Q(32,9*2**3)+Q(6,9*2*4) == Q(19,36) < 1
    assert Q(27,4**3)+Q(6,15*6*5) < 1
    assert Q(27,32)+Q(6,15*4*5) < 1

    B, C, T = s.symbols("B C T")
    b = 4+B
    c = b+1+C
    t = c+1+T
    de = (t-b)*(t-c)
    polynomial = s.Poly(s.expand(b*c*t*de-6*t*t-3*de), B,C,T)
    assert len(polynomial.terms()) == 40
    assert min(polynomial.coeffs()) == 1
    assert polynomial.coeff_monomial(1) == 18

    shapes = []
    for t in (1,2,3):
        for d in range(1,2*t**3+1):
            if 2*t**3 % d:
                continue
            b = t+d
            for c in range(t+1,b):
                v = (Q(c**3,c-b)-Q(2*t**3,t-b))/Q(t-c)
                w = c*v+Q(c**3,c-b)
                if v.denominator != 1 or w.denominator != 1 or v < 0 or w <= 0:
                    continue
                v, w = int(v), int(w)
                S1, S2, S3 = b+c+t, b*c+b*t+c*t, b*c*t
                amin = max(S1+v,
                           (S2+w+b*v+S1-1)//S1,
                           (S3+b*w+S2-1)//S2, 2)
                A = (amin-S1,amin*S1-S2,amin*S2-S3,amin*S3)
                K = (-Q(v),Q(v*(v+c)-w),Q(v*w*(b+c),c)+w*c,Q(b*w*w,c))
                assert all(value.denominator == 1 for value in K)
                diffs = tuple((S3-2)*A[i]-3*K[i] for i in range(4))
                assert all(value > 0 for value in diffs)
                assert all((S3-2)*slope > 0 for slope in (1,S1,S2,S3))
                shapes.append(dict(b=b,c=c,t=t,v=v,w=w,a_min=amin,
                                   positive_differences=[int(value) for value in diffs]))
    assert [sum(row['t']==t for row in shapes) for t in (1,2,3)] == [1,4,6]

    # Independently reconstruct the root equations and K polynomial for the finite set.
    X = s.Symbol("X")
    for row in shapes:
        b,c,t,v,w = (row[key] for key in ('b','c','t','v','w'))
        J = X*(1+b*X)*(v+w*X)
        assert J.subs(X,-Q(1,c)) == 1
        assert J.subs(X,-Q(1,t)) == 2
        quotient, remainder = s.div(s.Poly(J*(J-1),X),s.Poly(X*(1+b*X)*(1+c*X),X))
        assert remainder.is_zero
        expected = -v+(v*(v+c)-w)*X+(Q(v*w*(b+c),c)+w*c)*X**2+Q(b*w*w,c)*X**3
        assert s.expand(quotient.as_expr()-expected) == 0

    # J0=1, smallest t: the residual polynomial has an integer linear quotient.
    # A nonzero integer slope forces q <= |beta|; the following rational bounds
    # show |beta| < a*b*c*t for every t >= 6.
    assert Q(39,4*6**2) < 1
    assert 3*(Q(12,7*6)*(1+Q(1,2*6))+Q(1,4*6**2)) == Q(319,336) < 1
    assert 3*(Q(12,7*6)*(Q(1,2)+Q(1,7))+Q(1,7*8)) == Q(237,392) < 1
    assert Q(49,25) < 2  # 1/sqrt(2) < 5/7.
    bezout = []
    for k in (1,2,3):
        c = 1+x
        b = 1+s.Rational(6,k)/x
        v = s.factor((b**3/(b-c)-1/(c-1))/(b-1))
        w = s.factor(v-1/(c-1))
        a = s.factor(b+c+1+3*v/k)
        z = s.factor(c*w/b)
        S1,S2,S3 = b+c+1,b*c+b+c,b*c
        alpha = s.factor(k*a*S3-3*z*w)
        beta = s.factor(k*(a*S1-S2)-3*(w+v*(v-b)))
        R2 = k*(a*S2-S3)-3*(w*(v-b)+z*v)
        assert s.factor(R2-alpha-beta) == 0
        assert s.factor(k*(a-S1)-3*v) == 0
        P = s.Poly(s.fraction(alpha)[0],x,domain=s.QQ)
        Qpoly = s.Poly(s.fraction(beta)[0],x,domain=s.QQ)
        U,V,G = s.gcdex(P,Qpoly)
        assert G == 1 and U*P+V*Qpoly == 1
        bezout.append(dict(k=k,alpha_numerator=str(P.as_expr()),beta_numerator=str(Qpoly.as_expr()),
                           u=str(U.as_expr()),v=str(V.as_expr())))

    small_one = []
    for t in (1,2,3):
        for e in s.divisors(t**3):
            c = t+int(e)
            for delta in s.divisors(c**3):
                b = c+int(delta)
                v = (Q(b**3,b-c)-Q(t**3,c-t))/Q(b-t)
                w = t*v-Q(t**3,c-t)
                z = Q(c*w,b)
                if any(value.denominator != 1 for value in (v,w,z)) or v <= 0 or w <= 0:
                    continue
                v,w,z = int(v),int(w),int(z)
                S1,S2,S3 = b+c+t,b*c+b*t+c*t,b*c*t
                amin = max(S1+v,(S2+w+c*v+S1-1)//S1,(S3+c*w+S2-1)//S2)
                A = (amin-S1,amin*S1-S2,amin*S2-S3,amin*S3)
                K = (v,w+v*(v-b),w*(v-b)+z*v,z*w)
                differences = [(S3-2)*A[r]-3*K[r] for r in range(4)]
                if t == 1:
                    assert (b,c,v,w,z,amin) == (3,2,13,12,8,19)
                    assert differences == [13,-14,140,168]
                    # Positive for q >= 1, since 140*q^2-14*q > 0.
                else:
                    assert min(differences) > 0
                cases = []
                for k in (1,2,3):
                    a = S1+Q(3*v,k)
                    if a.denominator != 1:
                        continue
                    a = int(a)
                    assert a >= amin
                    H = k*(t-b)*(t-c)-6*t*t
                    if H:
                        assert abs(H) < 1+t*a*S3
                        cases.append(dict(k=k,a=a,H=H,reason="nonzero H below modulus"))
                    else:
                        alpha = Q(k*a*S3-3*z*w,t)
                        beta = k*(a*S1-S2)-3*K[1]
                        assert alpha.denominator == 1 and alpha != 0
                        root = Q(-beta,alpha)
                        assert root < a*S3
                        cases.append(dict(k=k,a=a,H=0,alpha=int(alpha),beta=beta,root=str(root)))
                small_one.append(dict(b=b,c=c,t=t,v=v,w=w,z=z,a_min=amin,
                                      differences=differences,cases=cases))
    assert [sum(row['t']==t for row in small_one) for t in (1,2,3)] == [1,4,7]

    medium_one = []
    for t in (4,5):
        for k in (1,2,3):
            de = 6*t*t//k
            for e in range(1,isqrt(de)+1):
                if de % e:
                    continue
                d = de//e
                if d <= e:
                    continue
                b,c = t+d,t+e
                v = (Q(b**3,b-c)-Q(t**3,c-t))/Q(b-t)
                w = t*v-Q(t**3,c-t)
                z = Q(c*w,b)
                a = b+c+t+Q(3*v,k)
                if any(value.denominator != 1 for value in (v,w,z,a)) or v <= 0 or w <= 0:
                    continue
                S1,S2,S3 = b+c+t,b*c+b*t+c*t,b*c*t
                alpha = Q(k*a*S3-3*z*w,t)
                beta = k*(a*S1-S2)-3*(w+v*(v-b))
                assert alpha != 0
                root = -beta/alpha
                assert root < 2
                medium_one.append(dict(b=b,c=c,t=t,k=k,v=int(v),w=int(w),a=int(a),root=str(root)))
    assert len(medium_one) == 2

    result = dict(status="passed", scope="Conditional standard-digit complete allocation; all three-linear orders for both constant digits. Not a proof of general i=3 or Erdős 699.",
                  universal_interval_identities=2,
                  largest_t_positive_polynomial=dict(terms=40,minimum_coefficient=1,constant=18),
                  smallest_t_complete_shapes=shapes,
                  smallest_t_small_shapes_total=len(shapes),
                  epsilon_one_large_t_nonidentity_bezout=bezout,
                  epsilon_one_smallest_t_small_shapes=small_one,
                  epsilon_one_smallest_t_medium_shapes=medium_one)
    out = Path(__file__).resolve().parents[1]/'data/results/verification_i3_three_linear_congruence_2026-10-04.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=result['status'],scope=result['scope'],
                          epsilon_zero_small_shapes=len(shapes),epsilon_one_small_shapes=len(small_one),
                          epsilon_one_medium_shapes=len(medium_one),bezout_certificates=len(bezout)),
                     ensure_ascii=False,indent=2))


if __name__ == '__main__':
    run()
