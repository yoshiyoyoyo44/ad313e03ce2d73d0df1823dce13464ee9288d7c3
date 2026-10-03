"""Exact identities and valuation diagnostics for the all-degree boundary.

The note proves the general classification and prime-transfer conclusions;
finite diagnostics below are not a proof of general numerical i=3.
"""
import json
import math
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent
w, x, lam = S.symbols("w x lambda")


def vp(n, p):
    n = abs(int(n))
    assert n
    result = 0
    while n % p == 0:
        result += 1
        n //= p
    return result


def binomial_vp(n, j, p):
    result, power = 0, p
    while power <= n:
        result += n//power-j//power-(n-j)//power
        power *= p
    return result


def half_polynomials(r):
    if r == 0:
        return S.Integer(1), S.Integer(1)
    tr, ur = S.chebyshevt(r, w), S.chebyshevu(r-1, w)
    return S.expand(tr+(w-1)*ur), S.expand(tr+(w+1)*ur)


def identities():
    r, k = S.symbols("r k", integer=True, positive=True)
    plus = (r+k+1)/(r-k+1)
    minus = (r-k)/(r+k)
    previous_k = k*(2*k-1)/((r+k)*(r-k+1))
    assert S.cancel(plus-2-2*previous_k+minus) == 0
    assert S.cancel((2*r+3)*plus-2*(2*r+1)
                    -2*(2*r+1)*(2*k+1)/(2*k-1)*previous_k+(2*r-1)*minus) == 0
    cases = []
    for r in range(1, 21):
        d = 2*r+1
        pp, qq = half_polynomials(r)
        p = S.Poly(pp, w, domain=S.QQ)
        q = S.Poly(qq, w, domain=S.QQ)
        assert all(int(c) % 2 == (1 if i == 0 else 0) for i, c in enumerate(reversed(p.all_coeffs())))
        assert all(int(c) % 2 == (1 if i == 0 else 0) for i, c in enumerate(reversed(q.all_coeffs())))
        assert S.expand((w+1)*pp**2-(w-1)*qq**2-2) == 0
        assert S.expand(d*pp+qq-2*S.diff((w-1)*qq, w)) == 0
        assert S.expand((w+1)*pp**2-S.chebyshevt(d, w)-1) == 0
        assert S.expand((w-1)*qq**2-S.chebyshevt(d, w)+1) == 0
        assert S.expand(pp*qq-S.chebyshevu(d-1, w)) == 0
        phi = ((d+1)*lam**(d+1)-(d-1)*lam**d
               +(d-1)*lam-(d+1))
        assert S.cancel(phi-lam**r*(lam**2-1)*(d*pp+qq).subs(
            w, (lam+1/lam)/2)) == 0
        pseries = sum(2**k*math.comb(r+k, 2*k)*x**k for k in range(r+1))
        qseries = sum(S.Rational(2**k*math.comb(r+k, 2*k), 2*k+1)*x**k for k in range(r+1))
        assert S.expand(pp.subs(w, 1+x)-pseries) == 0
        assert S.expand(qq.subs(w, 1+x)/d-qseries) == 0
        assert S.expand(x*(x+2)*S.diff(pseries,x,2)+(2*x+1)*S.diff(pseries,x)-r*(r+1)*pseries) == 0
        assert S.expand(x*(x+2)*S.diff(qseries,x,2)+(2*x+3)*S.diff(qseries,x)-r*(r+1)*qseries) == 0
        f = S.Poly(2+(w-1)*qq*(d*pp+qq)/2, w, domain=S.ZZ)
        j = S.Poly((w+1)*pp*(d*pp+qq)/(2*d), w, domain=S.QQ)
        assert f.LC() == (d+1)*2**(d-2)
        assert f.diff().eval(1) == d*d
        assert j.diff().eval(1) == S.Rational(5*d*d+1, 6)
        assert S.Poly(j.as_expr().subs(w, 1+x),x).nth(2) == S.Rational((d*d-1)*(7*d*d+2),60)
        assert math.gcd(d*d, int(f.LC())) == 1
        assert f.eval(-1) == 1-d*d
        assert S.expand(f.as_expr()-1-pp*((w+1)*pp+d*(w-1)*qq)/2) == 0
        assert ((f-1).rem(p)).is_zero
        vv = (f-1).exquo(p)
        assert (j-1-vv*q.mul_ground(S.Rational(1, d))).is_zero
        assert (j*(j-1)).rem(f-1).is_zero
        assert (j*(j-1)*(j-2)).rem(f-2).is_zero
        assert S.expand(f.as_expr()-(S.chebyshevt(d,w)+d*(w-1)*S.chebyshevu(d-1,w)+3)/2) == 0
        assert S.expand(j.as_expr()-(S.chebyshevt(d,w)+(w+1)*S.chebyshevu(d-1,w)/d+1)/2) == 0
        shapes = [
            (2+(w-1)*qq*(2*qq-d*pp)/4, S.Rational(-2, d), S.Rational(d-2, d)),
            (2-(w-1)*(3*d*pp-qq)*(d*pp+qq)/2, S.Rational(-1, 2*d), S.Rational(r, d)),
            (f.as_expr(), S.Rational(1, d), S.Rational(1, d)),
        ]
        for epsilon, (ff, tau, trace) in enumerate(shapes):
            fj = S.Poly(ff, w, domain=S.QQ)
            vv0 = (fj-1).exquo(p)
            jj = 1+vv0.as_expr()*((2-epsilon)*pp/2+tau*qq)
            jp = S.Poly(jj, w, domain=S.QQ)
            assert jp.LC()/fj.LC() == trace
            assert (jp*(jp-1)).rem(fj-1).is_zero
            assert (jp*(jp-1)*(jp-2)).rem(fj-2).is_zero
        cases.append({"D": d, "degree_F": f.degree(), "primitive_nonconstant_content": True})
    return {"coefficient_recurrence_identities": 2, "cases": cases}

def rational_origin_certificates():
    """The denominator lemma and root interval reduce this proof to D<=19."""
    cases = []
    nonzero_certificates = 0
    for d in range(3, 20, 2):
        pp, qq = half_polynomials((d-1)//2)
        primitive = S.Poly(d*pp+qq, w, domain=S.ZZ).primitive()[1]
        degree = primitive.degree()
        roots, certificates = [], []
        for denominator in S.divisors(d+1):
            for numerator in range(-denominator+1, denominator):
                if math.gcd(numerator, denominator) != 1:
                    continue
                cleared = primitive.eval(S.Rational(numerator, denominator))*denominator**degree
                assert cleared.q == 1
                if cleared == 0:
                    roots.append(str(S.Rational(numerator, denominator)))
                else:
                    certificates.append({"numerator": numerator, "denominator": denominator,
                                         "cleared_value": str(cleared)})
        assert roots == (["1/4"] if d == 3 else [])
        if d >= 5:
            nonzero_certificates += len(certificates)
        cases.append({"D": d, "primitive_coefficients": [int(c) for c in primitive.all_coeffs()],
                      "rational_roots_in_minus_one_one": roots, "certificates": certificates})
    return {"finite_reduction": "D>=21 excluded by denominator and root-position lemma",
            "nonzero_certificates_for_D_5_to_19": nonzero_certificates, "cases": cases}

def hensel_diagnostics():
    cases = []
    for a, expected in ((1, 6), (2, 56)):
        d = 5**a
        pp, qq = half_polynomials((d-1)//2)
        j = (w+1)*pp*(d*pp+qq)/(2*d)
        ss = S.Poly(S.cancel((j.subs(w,1+5*x)-2)/(5*x)),x,domain=S.ZZ)
        assert S.Poly(ss.as_expr()-(1-x),x,modulus=5).is_zero
        root, modulus = 1, 5
        lifts = []
        for step in range(1,2*a):
            next_modulus = 5*modulus
            candidates = [root+digit*modulus for digit in range(5)]
            roots = [value for value in candidates if int(ss.eval(value)) % next_modulus == 0]
            assert len(roots) == 1
            root,modulus = roots[0],next_modulus
            lifts.append({"modulus":modulus,"root":root})
        assert modulus == 5**(2*a) and root == expected
        cases.append({"D":d,"lifts":lifts,"necessary_y_residue":root,"modulus":modulus})
    return cases


def numerical_diagnostics():
    cases = []
    prime_checks = 0
    for d in range(3, 76, 2):
        factors = list(S.factorint(d))
        uniform_witnesses = [p for p in factors if p == 3 or p >= 7]
        radical = math.prod(factors)
        pp, qq = half_polynomials((d-1)//2)
        for y in range(1, 25):
            xx = radical*y
            ww = 1+xx
            pval, qval = int(pp.subs(w, ww)), int(qq.subs(w, ww))
            assert qval % d == 0
            qnormal = qval//d
            n = 2+xx*qval*(d*pval+qval)//2
            j = (ww+1)*pval*(d*pval+qval)//(2*d)
            assert 4 <= j <= n//2
            common = math.gcd(n, j)
            while common % 2 == 0:
                common //= 2
            assert (d*d-1) % common == 0
            witnesses = list(uniform_witnesses)
            if 5 in factors:
                b5 = vp(xx, 5)
                if b5 >= 2:
                    assert vp(n-2, 5) == b5+2*vp(d, 5)
                    assert vp(j-2, 5) == b5
                    witnesses.append(5)
                else:
                    yy = xx//5
                    assert (j-2)//5 % 5 == (yy-yy*yy) % 5
                    if yy % 5 != 1:
                        assert vp(j-2, 5) == 1
                        witnesses.append(5)
            for prime in witnesses:
                a, b = vp(d, prime), vp(xx, prime)
                if prime == 5 or prime >= 7:
                    assert vp(n-2, prime) == b+2*a
                    assert vp(j-2, prime) == b
                elif b >= 2:
                    assert vp(n-2, 3) == b+2*a
                    assert vp(j-2, 3) == b-1
                else:
                    local_y = xx//3
                    assert pval % 3 == 1 and qnormal % 3 == (1-local_y) % 3
                    if local_y % 3 == 1:
                        assert vp(j-1, 3) == vp(qnormal, 3)
                        assert vp(n-2, 3) == 1+2*a+vp(j-1, 3)
                    else:
                        assert local_y % 3 == 2
                        assert vp(j, 3) == vp(pval+qnormal, 3)
                        assert vp(n-2, 3) == 1+2*a+vp(j, 3)
                assert binomial_vp(n, 3, prime) > 0
                assert binomial_vp(n, j, prime) > 0
                prime_checks += 1
            cases.append({"D": d, "y": y, "witness_primes": witnesses})
    return {"integer_models": len(cases), "witness_checks": prime_checks,
            "D_with_no_uniform_closeout_in_this_audit": [5, 25]}


def main():
    result = {"passed": True,
              "scope": "all-degree constant-norm boundary; epsilon=2 family closed when D has divisor 3 or a prime >=7; remaining powers of 5 and other frontiers are not solved",
              "identities": identities(), "rational_origin": rational_origin_certificates(),
              "hensel": hensel_diagnostics(), "numerical": numerical_diagnostics()}
    path = ROOT/"data/results/verification_i3_chebyshev_boundary.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"passed": True, "identity_degrees": 20,
                      "rational_origin_certificates": result["rational_origin"]["nonzero_certificates_for_D_5_to_19"],
                      **result["numerical"]}))


if __name__ == "__main__":
    main()
