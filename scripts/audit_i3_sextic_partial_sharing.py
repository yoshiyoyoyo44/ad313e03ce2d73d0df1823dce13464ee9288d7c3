"""Exact symbolic and integer certificates for sextic partial sharing.

This checks identities and uniform bound certificates, not a finite search
purporting to settle arbitrary i=3. The b=1 tail also needs complete Q1 and
odd-prime Kummer conditions, as explained in the companion proof.
"""

import json
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
a, b, c, d, q = sp.symbols("a b c d q")
VARIABLES = (a, b, c, d)


def equal(left, right=0):
    assert sp.cancel(left-right) == 0


def geom(x, length):
    return sum(x**e for e in range(length))


def expressions(theta, beta):
    Q = b*q
    g, k, delta = a*q-1, Q+1, a-b
    A = delta*geom(Q, 5)+a*Q**5
    J = 1+(c*q+d*q*q)*geom(Q*Q, 3)+theta*Q**6+beta*Q**3
    V = c+d*q-theta*delta*k
    L = g*k-2*q*V
    C = beta*beta*g*k*k*delta-V*(g*k-q*V)
    N = C+beta*g*k*b*Q**2*L
    H = q*(c+d*q)+theta*k*(Q-1)
    equal(g*g*k*k*J*(J-1)/q-N,
          A*(q*H*H*A+H*L+2*beta*H*g*k*Q**3
             +beta*beta*g*k*k*(Q-1)))
    T = 12*beta*(((2*theta+1)*a*b-2*theta*b*b-2*d)*q
                 +(2*theta+1)*delta-2*c)
    R = sp.Poly(sp.expand(12*b*N-T*A), q)
    assert R.degree() <= 4
    return {"A":A,"J":J,"V":V,"L":L,"C":C,"N":N,
            "H":H,"R":R,"g":g,"k":k,"T":T}


def weighted_norm(expression, exponent):
    P = sp.Poly(sp.expand(expression), *VARIABLES)
    for powers, coefficient in P.terms():
        ia, ib, ic, id_ = powers
        assert ia+ib+ic+2*id_ == exponent+2
        assert ia+ic+id_ <= 2
    return int(sum(abs(coefficient) for coefficient in P.coeffs()))


def audit_six_cases():
    expected = {
        (0,1):[42,90,72,54,24], (0,2):[132,288,288,168,48],
        (1,0):[18,54,108,90,24], (1,2):[102,270,312,162,24],
        (2,0):[60,96,96,96,48], (2,1):[42,72,66,60,24],
    }
    rows, case_polynomials = [], {}
    for so, se in product(range(3), repeat=2):
        if so == se:
            continue
        theta = sp.Rational(so+se, 2)-1
        beta = sp.Rational(so-se, 2)
        obj = expressions(theta, beta)
        R = obj["R"]
        W = (2*theta+1)*a*b+(1-2*theta)*b*b-2*d
        equal(R.nth(4), -12*a*b**3*beta*W)
        norms = [weighted_norm(R.nth(e), e) for e in range(5)]
        assert norms == expected[(so,se)]
        rows.append({"so":so,"se":se,"theta":str(theta),"beta":str(beta),
                     "coefficient_norms_ascending":norms,
                     "R_coefficients_ascending":[str(R.nth(e)) for e in range(5)]})
        case_polynomials[(theta, beta)] = R
    return rows, case_polynomials


def audit_degenerate_leading(polynomials):
    certificates = []
    z = sp.symbols("z", nonnegative=True)

    def positive_after_a(expression, multiple):
        coeffs = sp.Poly(sp.expand(expression.subs(a,multiple*b+z)),b,z).coeffs()
        assert all(value >= 0 for value in coeffs)

    def endpoint_bounds(expression, bound, multiple, upper=a-b, lower=0):
        for endpoint in (lower,upper):
            val = sp.expand(expression.subs(c,endpoint))
            positive_after_a(bound-val,multiple)
            positive_after_a(bound+val,multiple)

    # theta=0: W=0 forces d=b(a+b)/2. Odd a, even b.
    for epsilon in (-1, 1):
        R = polynomials[(0, sp.Integer(epsilon))]
        coeff = [sp.factor(R.nth(e).subs(d, b*(a+b)/2)) for e in range(5)]
        E = a*a-8*a*c-b*b if epsilon == 1 else 7*a*a-8*a*b-8*a*c+b*b
        equal(coeff[3], -epsilon*3*b**3*E)
        equal(coeff[4], 0)
        certificates.append({"theta":"0","beta":str(epsilon),
                             "coefficients_ascending":[str(v) for v in coeff]})
        # Coefficient bounds used with the parity lower bound |E|>=1.
        # With 0<=c<=a-b all are bounded by these weighted norms.
        for expression,bound in zip(coeff[:3],(12*a*a,24*a*a*b,30*a*a*b*b)):
            endpoint_bounds(expression,bound,3)
        # R0,R2 are linear in c. R1 is monotone on [0,a-b].
        derivative = sp.diff(coeff[1],c)
        positive_after_a(derivative.subs(c,0) if epsilon==1 else
                         -derivative.subs(c,a-b),3)
        for endpoint in (0,a-b):
            positive_after_a(coeff[2].subs(c,endpoint),3)
    # theta=-1/2: W=0 forces d=b^2. theta=+1/2 has W>0.
    for epsilon in (-1, 1):
        R = polynomials[(sp.Rational(-1,2), sp.Rational(epsilon,2))]
        coeff = [sp.factor(R.nth(e).subs(d, b*b)) for e in range(5)]
        E = a*(b-4*c)-b*b if epsilon == 1 else a*(b+4*c)-b*b
        equal(coeff[3], -3*b**3*E)
        equal(coeff[4], 0)
        certificates.append({"theta":"-1/2","beta":str(sp.Rational(epsilon,2)),
                             "coefficients_ascending":[str(v) for v in coeff]})
        if epsilon == -1:
            endpoint_bounds(coeff[0],12*a*a,2)
            endpoint_bounds(coeff[2],12*a*a*b*b,2)
            # R1 is concave inside -3b: endpoints and its vertex suffice.
            inside = sp.cancel(-coeff[1]/(3*b))
            for endpoint in (0,a-b,(a-b)/2):
                val=sp.expand(inside.subs(c,endpoint))
                positive_after_a(a*a-val,2)
                positive_after_a(a*a+val,2)
        else:
            for expression,bound in zip(coeff[:3],
                                       (6*a*b,15*a*b*b,sp.Rational(15,2)*a*b**3)):
                endpoint_bounds(expression,bound,2,upper=b/4)
                positive_after_a(expression.subs(c,0),2)
                positive_after_a(sp.diff(expression,c).subs(c,0),2)
    return certificates


def audit_exact_bounds():
    # Each is the monotone worst endpoint of a proved uniform bound.
    B, Q = Fraction(2), Fraction(64)
    bounds = {
        "R_over_A":(48+168/(B*Q)+312/(B*Q)**2+288/(B*Q)**3
                      +132/(B*Q)**4)/B**6,
        "nonzero_quartic_lower_tail":(28+52/(B*Q)+48/(B*Q)**2
                                      +22/(B*Q)**3)/B**5,
        "zero_quartic_integer_beta_b_ge_4":None,
        "zero_quartic_integer_beta_b_eq_2":None,
        "zero_quartic_half_beta_negative":None,
        "zero_quartic_half_beta_positive":None,
    }
    B, Q = Fraction(4), Fraction(4**6)
    bounds["zero_quartic_integer_beta_b_ge_4"] = (
        2*B*B*(10/B**6+8/(B**7*Q)+4/(B**8*Q*Q)))
    B, Q = Fraction(2), Fraction(224)
    bounds["zero_quartic_integer_beta_b_eq_2"] = (
        Fraction(7,3)*(10/B**6+8/(B**7*Q)+4/(B**8*Q*Q)))
    # a<q/b^5 and the sharper bounds displayed in the note.
    B, Q = Fraction(2), Fraction(64)
    bounds["zero_quartic_half_beta_negative"] = (
        8/B**7+2/(B**8*Q)+8/(B**9*Q*Q))
    Q = Fraction(128)  # W=0 in the half case forces a>=2b.
    bounds["zero_quartic_half_beta_positive"] = (
        Fraction(5,2)*B*B/Q+5*B/Q**2+2/Q**3)
    expected = {
        "R_over_A":Fraction(3310593057,4294967296),
        "nonzero_quartic_lower_tail":Fraction(29789195,33554432),
        "zero_quartic_integer_beta_b_ge_4":Fraction(671121409,8589934592),
        "zero_quartic_integer_beta_b_eq_2":Fraction(502657,1376256),
        "zero_quartic_half_beta_negative":Fraction(16417,262144),
        "zero_quartic_half_beta_positive":Fraction(82561,1048576),
    }
    assert bounds == expected
    assert all(0 < value < 1 for value in bounds.values())
    b1_bound = 1+Fraction(3,9)+Fraction(26,9**2)+Fraction(24,9**3)+Fraction(11,9**4)
    assert b1_bound == Fraction(11081,6561) < 2
    return {**{key:[v.numerator,v.denominator] for key,v in bounds.items()},
            "b1_carry_absolute_bound":[b1_bound.numerator,b1_bound.denominator]}


def audit_b1():
    Rrecords = []
    for beta in (-1, 1):
        obj = expressions(sp.Integer(0), sp.Integer(beta))
        A, N, C, J = [sp.expand(obj[key].subs(b, 1)) for key in ("A","N","C","J")]
        g, k, delta = a*q-1, q+1, a-1
        V, Z = c+d*q, a*k-2*(c+d*q)
        Tprime = beta*(Z-1)
        RP = sp.Poly(sp.expand(N-Tprime*A), q)
        assert RP.degree() <= 4
        equal(RP.nth(4), -beta*a*(a-2*d+1))
        cubic = (-a*a+2*a*c+a*d-2*d+d*d+1 if beta==1 else
                 3*a*a-2*a-2*a*c-3*a*d+2*d+d*d-1)
        equal(RP.nth(3), cubic)
        # Sharp monotonic endpoint certificates for the cubic, no cutoffs.
        lo, hi = ((0,0),(a-1,a-1)) if beta == 1 else ((a-1,a-1),(0,0))
        u = sp.symbols("u", nonnegative=True)
        for value, sign in ((cubic.subs(dict(zip((c,d),lo)))+3*a*a,1),
                            (3*a*a-cubic.subs(dict(zip((c,d),hi))),1)):
            assert all(coefficient >= 0 for coefficient in
                       sp.Poly(sp.expand(value.subs(a,u+2)),u).coeffs())
        # For the lower three coefficients use d,c<=a; a>=2.
        norms = [sum(abs(v) for v in sp.Poly(RP.nth(e),a,c,d).coeffs())
                 for e in range(3)]
        assert all(norm <= bound for norm,bound in zip(norms,(11,24,26)))
        A3 = delta*(1+q+q*q)+a*q**3
        equal(A-g*k*q**3, A3)
        equal(beta*C-g*k*k*q*q-Z*A3, beta*(N-beta*Z*A))
        equal(RP.as_expr().subs(q,-1),
              -(c-d+1)**2 if beta == 1 else 2-(c-d-1)**2)
        equal(J.subs(q,-1), -3*(c-d) if beta==1 else -3*(c-d)+2)
        if beta == 1:
            equal(sp.diff(J,q).subs(q,-1), 3*(3*c-4*d+1))
        Rrecords.append({"beta":beta,"Rprime_coefficients_ascending":
                         [str(RP.nth(e)) for e in range(5)],
                         "cubic_endpoint_bounds":True,"negative_root_identities":True})
    y = sp.symbols("y", nonnegative=True)
    positive = (a-1)*(q-1)**2-a*(a-2)*q
    equal(positive, (a-1)*(q-a-1)**2+a*a*(q-a-1)+2*a)
    equal(geom(q,6), (q+1)*(q*q+q+1)*(q*q-q+1))
    t = sp.symbols("t")
    equal((q*q-q+1).subs(q,-1+3*t), 3-9*t+9*t*t)

    configs = 0
    for aa, qq, cc, dd, beta in product((0,2),(1,),range(4),range(4),(-1,1)):
        # Compute residues directly, independently of the parity formulas.
        kk, gg = qq+1, aa*qq-1
        VV = cc+dd*qq
        ZZ = aa*kk-2*VV
        AA = (aa-1)*geom(qq,5)+aa*qq**5
        CC = gg*kk*kk*(aa-1)-VV*(gg*kk-qq*VV)
        NN = CC+beta*gg*kk*qq*qq*(gg*kk-2*qq*VV)
        TT = beta*(ZZ-1)
        carries = [h for h in (-1,0,1) if (NN-(TT+h)*AA)%4 == 0]
        expected = [beta] if VV%2 == 0 else ([0] if beta==1 else [])
        assert carries == expected
        configs += 1
    assert configs == 64
    q5_cases = 0
    for aa in (2,4):
        delta = aa-1
        for cc, dd, beta in product(range(delta+1),range(delta+1),(-1,1)):
            if not 0 <= cc+beta <= delta:
                continue
            nn = 2+(aa*5-1)*geom(5,6)
            jj = 1+(cc*5+dd*25)*geom(25,3)+beta*125
            assert 3*jj*(jj-1)%(nn-1) != 0
            q5_cases += 1
    assert q5_cases == 28
    return {"Rprime":Rrecords,"parity_configs":configs,"radix_5_cases":q5_cases,
            "positive_quadratic_gap":True,"G6_factorization":True,
            "Phi6_valuation_identity":True,
            "remaining_b1_tail_requires_complete_Q1_and_odd_Kummer":True}


def main():
    if not __debug__:
        raise SystemExit("Assertions required; do not use python -O.")
    rows, polynomials = audit_six_cases()
    result = {"scope":"F-2=(aX-1)G6(bX), G6(bX)/(1+bX) shared; general i=3 open",
              "six_cases":rows,"zero_leading":audit_degenerate_leading(polynomials),
              "rational_bounds":audit_exact_bounds(),"b1":audit_b1()}
    path = ROOT/"data/results/verification_i3_sextic_partial_sharing.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"compression_identities":6,"coefficient_norms":30,
                      "strict_uniform_bounds":6,"b1_parity_configs":64,
                      "b1_radix_5_cases":28,"general_i3_closed":False}))


if __name__ == "__main__":
    main()
