"""Independent backward-digit replay and rational bounds for the high-degree theorem."""
from fractions import Fraction
from pathlib import Path
from itertools import product
import json
import sympy as sp


def value(coeffs,x):
    acc=0
    for c in reversed(coeffs):
        acc=acc*x+c
    return acc


def main():
    counts=dict(standard_F=0,integer_Q=0,polynomial_allocation=0,numerical_range=0,four_divides_n=0)
    allocations=[]
    for q in (5,7):
        for a in range(2,q):
            for b in range(1,(q-1)//a+1):
                for s in range(1,(q-1)//(a*b)+1):
                    # Enumerate the four middle F digits, then reverse the carry.
                    for middle in product(range(q),repeat=4):
                        D=[0]*6
                        D[5]=b*s
                        good=True
                        for k,f in zip(range(5,1,-1),middle):
                            total=D[k]+f
                            if total%a:
                                good=False
                                break
                            D[k-1]=total//a
                            if D[k-1]<=0:
                                good=False
                                break
                        if not good:
                            continue
                        D[0]=1
                        F=[1,a-D[1]]+[a*D[k-1]-D[k] for k in range(2,6)]+[a*b*s]
                        if not 1<=F[1]<q:
                            continue
                        assert all(0<=f<q for f in F)
                        counts['standard_F']+=1
                        # Divide E from the leading end, independently of the forward Q recurrence.
                        Q=[0]*5
                        Q[4]=s
                        for k in range(4,0,-1):
                            numerator=D[k]-Q[k]
                            if numerator%b:
                                good=False
                                break
                            Q[k-1]=numerator//b
                        if not good or Q[0]!=1:
                            continue
                        counts['integer_Q']+=1
                        for h in (1,2):
                            for v in range(1,a*b//2+1):
                                for J1 in range(F[1]+1):
                                    u=J1+h*Q[1]
                                    J=[0]*7
                                    for k,c in enumerate(Q):
                                        J[k]-=h*c
                                        J[k+1]+=u*c
                                        J[k+2]+=v*c
                                    J[0]+=2
                                    if not all(0<=j<=f for j,f in zip(J,F)):
                                        continue
                                    if value(J,Fraction(-1,b)) not in (0,1):
                                        continue
                                    counts['polynomial_allocation']+=1
                                    n,j=value(F,q),value(J,q)
                                    allocations.append((q,a,b,s,h,u,v,n%4))
                                    if 4<=j and 2*j<=n:
                                        counts['numerical_range']+=1
                                        if n%4==0:
                                            counts['four_divides_n']+=1
    assert counts==dict(standard_F=167,integer_Q=40,polynomial_allocation=6,numerical_range=4,four_divides_n=0)
    assert all(row[-1]==2 for row in allocations)
    # Uniform inequalities, checked through exact polynomial identities and positive coefficients.
    t=sp.symbols('t',nonnegative=True)
    assert all(c>0 for c in sp.Poly(sp.expand(10*(t+5)**3-81*(t+6)),t).all_coeffs())
    p=sp.Poly(sp.expand(10*(t+9)**2-81*(t+10)),t)
    assert p.TC()==0 and all(c>0 for c in p.all_coeffs()[:-1])
    P,R,Q,ell=sp.symbols('P R Q ell')
    assert sp.expand(3*(2+R*Q)*(1+R*Q)-(6+ell*Q)*(1+P*Q)
                     -Q*((3*R**2-ell*P)*Q-(6*P+ell-9*R)))==0
    assert sp.expand(3*R**2-9*P*R+6*P**2-3*(R-P)*(R-2*P))==0
    assert Fraction(5,6)*5**4>500 and 3*500>6*114
    result=dict(status='passed',scope='Conditional complete allocation: E linear, J-2 quotient quadratic, deg Q>=4 excluded. Not general i=3.',
                independent_method='middle F digits and backward carry; leading-end E division',counts=counts,
                derived_finite_bases=[5,7],derived_finite_degree=4,
                allocations=allocations,uniform_bound_identities=True)
    out=Path(__file__).resolve().parents[1]/'data/results/verification_i3_quadratic_J2_Elinear_high_degree_independent.json'
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
