"""Audit odd-prime gluing and partial sharing for odd half-degrees >=5.

The universal gluing/reduction and inequalities are proved in the note.
Assignment/CRT examples are finite diagnostics, not a proof for all degrees.
"""

import json
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
Y = sp.symbols("Y")


def equal(left,right=0):
    assert sp.cancel(left-right) == 0


def assignment_checks():
    total=valid=0
    rows=[]
    for m,b in ((6,2),(10,6),(14,4),(18,2),(30,2),(42,4)):
        orders=[int(v) for v in sp.divisors(m) if v>1]
        edges=[(i,j,p) for i,d in enumerate(orders) for p in sp.factorint(m)
               if p>=3 and b%p and p*d in orders
               for j in [orders.index(p*d)]]
        accepted=[]
        for values in product(range(3),repeat=len(orders)):
            total+=1
            if any((values[i]-values[j])%p for i,j,p in edges):continue
            accepted.append(values)
            assert len({v for d,v in zip(orders,values) if d%2})==1
            assert len({v for d,v in zip(orders,values) if d%2==0})==1
        assert len(accepted)==9
        valid+=len(accepted)
        rows.append({"m":m,"b":b,"assignments":3**len(orders),
                     "admissible":len(accepted),"gluing_edges":len(edges)})
    assert (total,valid)==(4698,54)
    return {"assignments":total,"admissible":valid,"rows":rows}


def crt_checks():
    count=0
    for r in (3,5,7):
        K=sp.Poly(sum(Y**(2*e) for e in range(r)),Y,domain=sp.QQ)
        factors=[sp.Poly(sp.cyclotomic_poly(order,Y),Y,domain=sp.QQ)
                 for order in sp.divisors(2*r) if order>2]
        for so,se,e0 in product(range(3),range(3),range(2)):
            theta=sp.Rational(so+se,2)-e0
            beta=sp.Rational(so-se,2)
            JP=e0+theta*Y**(2*r)+beta*Y**r
            CRT=sp.Poly(0,Y,domain=sp.QQ)
            for P in factors:
                order=next(order for order in sp.divisors(2*r)
                           if sp.Poly(sp.cyclotomic_poly(order,Y),Y,domain=sp.QQ)==P)
                value=so if order%2 else se
                quotient=K.exquo(P)
                CRT+=value*quotient*sp.invert(quotient,P)
            assert sp.rem(CRT.as_expr()-JP,K.as_expr(),Y)==0
            assert sp.Poly(JP.subs(Y,2*Y),Y,domain=sp.ZZ).nth(0)==e0
            count+=1
    assert count==54
    # Frobenius congruence sample, with integer polynomial division mod p.
    frobenius=0
    for p in (3,5,7):
        for e in (1,2,4):
            if e%p==0:continue
            for k in (1,2):
                left=sp.Poly(sp.cyclotomic_poly(e*p**k,Y),Y,modulus=p)
                right=sp.Poly(sp.cyclotomic_poly(e,Y)**(p**(k-1)*(p-1)),Y,modulus=p)
                assert left==right
                frobenius+=1
    return {"partial_normal_forms_compared_with_CRT":count,
            "Frobenius_identities_diagnostic":frobenius,"finite_diagnostics_only":True}


def compression_audit():
    a,b,c,d,q,z,theta,beta,t,A0=sp.symbols("a b c d q z theta beta t A")
    Q,g,k,delta=b*q,a*q-1,b*q+1,a-b
    A=(g*b*Q*z*z-delta)/(Q-1)
    BP=(Q*Q*z*z-1)/(Q*Q-1)
    J=1+q*(c+d*q)*BP+theta*Q*Q*z*z+beta*Q*z
    V=c+d*q-theta*delta*k
    L=g*k-2*q*V
    C=beta*beta*g*k*k*delta-V*(g*k-q*V)
    N=C+beta*g*k*b*z*L
    H=q*(c+d*q)+theta*k*(Q-1)
    equal(g*g*k*k*J*(J-1)/q-N,
          A*(q*H*H*A+H*L+2*beta*H*g*k*Q*z+beta*beta*g*k*k*(Q-1)))
    nu=sp.symbols("nu")
    D=t*Q*z-nu*beta*k*(Q-1)*L
    equal(D*g*b*z-(t*delta+nu*(Q-1)*C)
          -(Q-1)*(t*A0-nu*N), t*(g*b*Q*z*z-(Q-1)*A0-delta))
    assert sp.expand(D).subs(q,0)==-nu*beta
    return {"arbitrary_half_degree_compression":True,
            "second_integer_identity":True,"D_mod_q":True}


def bound_and_small_tail():
    bound=Fraction(1344,2**21*3**10)+Fraction(480,2**16*3**5)+Fraction(672,2**11)
    assert bound==Fraction(7,644972544)+Fraction(5,165888)+Fraction(21,64)<1
    tbound=Fraction(3904,729)
    assert tbound<6
    q,u=sp.symbols("q u",nonnegative=True)
    gap=3*q**5-3*q*(q-1)*(q+1)**2*(q-2)-5
    assert all(v>0 for v in sp.Poly(sp.expand(gap.subs(q,u+3)),u).coeffs())
    candidates=[(qq,D,ep) for qq in range(3,6) for D in (1,2) for ep in (-1,1)
                if (D+3*ep)%qq==0]
    assert candidates==[(4,1,1),(5,2,1)]
    q5=0
    for a in range(2,5):
        delta=a-1
        for c,d in product(range(delta),range(delta+1)):
            if c==d:continue
            V=c+5*d
            g,k=5*a-1,6
            C=g*k*k*delta-V*(g*k-5*V)
            L=g*k-10*V
            assert V>=1 and -56<=L<=104 and Fraction(C,g)<=108
            q5+=1
    assert q5==14
    assert Fraction(108,625**2)+Fraction(624,625)==Fraction(390108,390625)<1
    return {"b_ge_2_D_bound":[bound.numerator,bound.denominator],
            "b1_abs_t_bound":[tbound.numerator,tbound.denominator],
            "b1_D_less_than_3_gap":str(gap),"D_candidates":candidates,
            "radix5_nonconstant_pairs":q5}


def scope_witness():
    a,b,m,q=5,2,12,10243
    G=sum((b*Y)**e for e in range(m))
    F=2+(a*Y-1)*G
    J=1+2*Y*G-sp.Rational(3,4)*(b*Y)**12+sp.Rational(1,4)*sum((b*Y)**e for e in (3,6,9))
    F,J=sp.Poly(F,Y,domain=sp.ZZ),sp.Poly(J,Y,domain=sp.ZZ)
    assert all(0<=J.nth(e)<=F.nth(e)<q for e in range(13))
    assert sp.rem(J.as_expr()*(J.as_expr()-1)*(J.as_expr()-2),G,Y)==0
    n,j=int(F.eval(q)),int(J.eval(q))
    assert n%4==0 and 3*j*(j-1)%(n-1)!=0
    return {"m":m,"a":a,"b":b,"q":q,"J_coefficients":[int(J.nth(e)) for e in range(13)],
            "full_polynomial_sharing":True,"first_divisibility":False,
            "outside_odd_half_degree_theorem":True,"true_counterexample":False}


def main():
    if not __debug__:raise SystemExit("Assertions required; do not use python -O.")
    result={"scope":"odd half-degree partial sharing; general i=3 open",
            "gluing_diagnostics":assignment_checks(),"CRT_diagnostics":crt_checks(),
            "compression":compression_audit(),"bounds":bound_and_small_tail(),
            "scope_witness":scope_witness()}
    path=ROOT/"data/results/verification_i3_even_multiplier.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"assignments":4698,"admissible":54,"CRT":54,
                      "compression":True,"scope_witness_verified":True}))


if __name__=="__main__":main()
