"""Exact identities for the all-degree half-ratio and central-group bounds.

No sampled degree is used to prove an all-degree exclusion. The polynomial
square arguments and their scope are stated in the accompanying paper.
"""
import json
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/results/verification_i3_half_ratio_central_bounds.json"


def zero(expr):
    assert S.cancel(expr) == 0


def half_identities():
    u, v, h, c, d = S.symbols("U V H C D", nonzero=True)
    defect = u*c-v*h-1
    a, b = (u+2*h)/d, (v-2*c)/d
    e, q = a*b, a*c-b*h
    zero(d*q-(4*h*c+1)-defect)
    zero((u*v-1)-d*(d*e+q)-defect)
    ss, pp, qq = S.symbols("s p q", nonzero=True)
    dd, ee = (ss*qq+4)/pp, (qq-pp)/ss
    square = qq**2+ee*(dd*qq-1)
    zero(ss*pp*square-(ss*qq**3+4*qq**2-5*pp*qq+pp**2))
    lam, z = S.symbols("lambda z", nonzero=True)
    cubic = z**3+4*z**2+5*lam*z+lam**2
    disc = S.factor(S.discriminant(cubic, z))
    assert disc == -lam**2*(27*lam**2+140*lam-144)
    assert S.discriminant(27*lam**2+140*lam-144, lam) == 52**2*13
    return {"portrait_identities": 2, "square_identity": 1,
            "cubic_discriminant": str(disc), "constant_4_preserved": True}


def generic_identities():
    u, v, h, c, d, t = S.symbols("U V H C D t", nonzero=True)
    rho, sig = t*(1-t), 2*t-1
    a, b = (t*u+h)/d, ((1-t)*v-c)/d
    e = a*b
    q, r = (1-t)*a*c-t*b*h, t*a*c-(1-t)*b*h
    defect = u*c-v*h-1
    zero(d*q-h*c-rho-rho*defect)
    zero((u*v-1)-d*(d*e+r)/rho-defect)
    g = h*c+(t-S.Rational(1, 2))*(u*c+v*h)-rho-S.Rational(1, 2)
    zero((d*r-1)-g-(S.Rational(1, 2)-rho)*defect)
    zero(sig**2*a*c*b*h-(rho*(q*q+r*r)-(1-2*rho)*q*r))
    ss, qq, rr, ee = S.symbols("s q r e", nonzero=True)
    pp, dd = rr-ss*ee, (ss*rr+1)/(rr-ss*ee)
    ac = (-(1-t)*qq+t*rr)/sig
    bh = (-t*qq+(1-t)*rr)/sig
    kk = rho*pp-sig**2*qq
    norm = kk*(rr**2+ee)+rho*pp*(qq**2-2*qq*rr-4*rho*ee)
    zero(norm-sig**2*pp*(ac*bh-ee*(dd*qq-rho)))
    k = S.symbols("k", nonzero=True)
    p = (k+sig**2*qq)/rho
    relation = k*(rr**2+ee)+rho*p*(qq**2-2*qq*rr-4*rho*ee)
    quartic = sig**2*qq**4+k*qq**3+4*rho*k*ee*qq-k*k*ee
    remainder = S.rem(S.Poly((k*rr-rho*p*qq)**2-sig**2*quartic, rr), S.Poly(relation, rr))
    zero(remainder.as_expr())
    # At a common zero of p and q: s**2*e=-1 and r=s*e.
    # The product relation then gives rho*e*(sig**2-1)=-4*rho**2*e.
    zero(rho*ee*(sig**2-1)+4*rho**2*ee)
    return {"portrait_identities": 4, "norm_identity": 1,
            "quartic_square_identity": 1, "coprimality_reduction": 1}


def square_gap_identities():
    k, q, e, rho, sig, delta = S.symbols("k q e rho sigma delta", nonzero=True)
    quartic = sig**2*q**4+k*q**3+4*rho*k*e*q-k*k*e
    approximation = sig*q*q+k*q/(2*sig)-k*k/(8*sig**3)
    gap = k*q*(4*rho*e+k*k/(8*sig**4))-k*k*e-k**4/(64*sig**6)
    zero(quartic-approximation**2-gap)
    zero(gap/k-(q*(4*rho*e+k*k/(8*sig**4))-k*e-k**3/(64*sig**6)))
    ratio = S.solve(rho-2*(1-4*rho), rho)
    assert ratio == [S.Rational(2, 9)]
    t = S.symbols("t")
    assert set(S.solve(t*(1-t)-S.Rational(2, 9), t)) == {S.Rational(1, 3), S.Rational(2, 3)}
    # Constant-gap endpoint, degree(K)=degree(Q)/3, degree(E)=0.
    aa = 2*delta*sig
    bb = delta*k/sig-k**3/(8*sig**4)-4*rho*e*k
    cc = k**4/(64*sig**6)+(e-delta/(4*sig**3))*k*k+delta**2
    zero((approximation+delta)**2-quartic-(aa*q*q+bb*q+cc))
    discriminant = S.Poly(S.expand(bb*bb-4*aa*cc), k)
    assert discriminant.degree() == 6
    assert discriminant.LC() == 1/(64*sig**8)
    assert discriminant.nth(0) == -8*delta**3*sig
    assert all(discriminant.nth(i) == 0 for i in (1, 3, 5))
    zero((2*aa*q+bb)**2-(bb*bb-4*aa*cc)-4*aa*(aa*q*q+bb*q+cc))
    return {"quartic_approximation_identities": 3,
            "exceptional_ratios": ["1/3", "2/3"],
            "endpoint_discriminant_degree": 6,
            "endpoint_discriminant_even": True,
            "endpoint_discriminant_constant": "-8*delta**3*sigma",
            "endpoint_square_obstruction": "Even degree 6 with nonzero constant has two odd-multiplicity roots."}


def degree_diagnostics():
    half_cases = generic_cases = negative_k = square_gap_exclusions = 0
    constant_endpoints = 0
    for u in range(1, 101):
        for v in range(u, 2*u):
            for d in range(1, u+1):
                raw = max((2*u-d+1)//2, (3*u-v+d+3)//4)
                target = (5*u-v)//6+1
                if raw < target:
                    assert 6*raw == 5*u-v
                    assert 2*raw-2*u+d == 0
                    assert 4*raw+v-3*u-d == 0
                    raw += 1  # The proved constant cubic-square obstruction.
                    constant_endpoints += 1
                assert raw >= target
                half_cases += 1
            for h in range((u+1)//2, u):
                for d in range(max(1, u-h), u+1):
                    k = 3*h+v-2*u-d
                    n = 2*h+v-u-d
                    alpha = h+v-d
                    e = u+v-2*d
                    assert alpha-n == u-h
                    assert n-k == u-h
                    assert 2*n-alpha == k
                    assert n+alpha-e == 3*h+v-2*u > 0
                    if k < 0:
                        negative_k += 1
                        continue
                    assert n > k >= 0 and e >= 0
                    left = k+max(e, 2*k) >= n
                    right = h+v >= 2*d or 7*h+2*v >= 5*u+2*d
                    assert left == right
                    square_gap_exclusions += not left
                    generic_cases += 1
    saturated_endpoints = 0
    for u in range(1, 401):
        for h in range((u+1)//2, u):
            k, n = 3*h-2*u, 2*h-u
            if k < 0:
                continue
            allowed = 3*k >= n
            assert allowed == (7*h >= 5*u)
            if allowed and 7*h == 5*u:
                assert n == 3*k and k > 0
                saturated_endpoints += 1
    # Existing odd Chebyshev cores automatically satisfy the new bounds.
    # This check explicitly prevents presenting these theorems as their closure.
    for q in range(3, 1001):
        u, v, h, d = q, q+1, q-1, q
        assert 3*h >= 2*u-v+d
        assert h+v >= 2*d or 7*h+2*v >= 5*u+2*d
    return {"half_degree_rounding_cases": half_cases,
            "half_constant_endpoints": constant_endpoints,
            "generic_nonnegative_degree_cases": generic_cases,
            "negative_K_degree_exclusions": negative_k,
            "square_gap_degree_exclusions": square_gap_exclusions,
            "central_saturated_sextic_endpoints": saturated_endpoints,
            "odd_core_nonexclusion_diagnostics": 998}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    result = {
        "scope": "Lifted polynomial portraits only; general numerical i=3 remains open.",
        "half_ratio_identities": half_identities(),
        "generic_central_identities": generic_identities(),
        "polynomial_square_gap": square_gap_identities(),
        "degree_diagnostics": degree_diagnostics(),
        "proved_in_paper": [
            "t=1/2: h>(5*u-v)/6, including unbalanced and unsaturated partitions",
            "t!=1/2: h>=(2*u-v+d1)/3",
            "t!=1/2: h+v>=2*d1 or 7*h+2*v>=5*u+2*d1",
            "balanced d1=u and t!=1/2: h>5*u/7",
        ],
        "not_closed": ["all larger difference degrees", "odd five-power cores a>=4", "general numerical lifting"],
        "new_fully_resolved_indices": 0,
        "complete_i3_solution": False,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"passed": True, "degree_diagnostics": result["degree_diagnostics"],
                      "general_i3": "open"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
