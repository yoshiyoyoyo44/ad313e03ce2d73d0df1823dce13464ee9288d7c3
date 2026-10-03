"""Exact audit of two square remainders and the strict central 11/15 bound.

All-degree exclusions are paper proofs, not extrapolations from degree loops.
The general numerical i=3 problem and remaining odd five-power cores stay open.
"""
import json
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/results/verification_i3_central_square_descent.json"


def zero(expr):
    assert S.cancel(expr) == 0


def identities():
    q, k, d, eps, e, rho, sig, lam = S.symbols(
        "Q K delta epsilon E rho sigma lambda", nonzero=True
    )
    quartic = sig**2*q**4+k*q**3+4*rho*k*e*q-k*k*e
    w0 = sig*q*q+k*q/(2*sig)-k*k/(8*sig**3)
    gap1 = k*q*(4*rho*e+k*k/(8*sig**4))-k*k*e-k**4/(64*sig**6)
    zero(quartic-w0*w0-gap1)
    aa = 2*d*sig
    bb = d*k/sig-k**3/(8*sig**4)-4*rho*e*k
    cc = k**4/(64*sig**6)+(e-d/(4*sig**3))*k*k+d*d
    quadratic = aa*q*q+bb*q+cc
    zero((w0+d)**2-quartic-quadratic)
    discriminant = S.expand(bb*bb-4*aa*cc)
    zero((2*aa*q+bb)**2-discriminant-4*aa*quadratic)
    z0 = -k**3/(8*sig**4)+(3*d/(2*sig)-4*rho*e)*k
    gap2 = d*k*k*(3*d/(4*sig**2)+4*e*(rho-2*sig**2)/sig)-8*sig*d**3
    zero(discriminant-z0*z0-gap2)
    second_relation = (
        k*k*(eps*k/(4*sig**4)+3*d*d/(4*sig**2)
             +4*e*(rho-2*sig**2)*d/sig)
        +eps*k*(8*e*rho-3*d/sig)-8*d**3*sig-eps*eps
    )
    zero((z0+eps)**2-discriminant+second_relation)
    b0 = 16*e*sig**3*(rho-2*sig**2)
    a0 = 24*e*sig**2*(rho-4*sig**2)
    c0 = -128*e*e*sig**3*rho*(rho-2*sig**2)
    exchange_defect = eps*k+3*sig**2*d*d+b0*d-lam
    multiplier = k*k/(4*sig**4)+8*e*rho-3*d/sig
    norm = eps*eps-lam*multiplier-sig*d**3-a0*d*d-c0*d
    zero(norm+second_relation-multiplier*exchange_defect)
    eliminated = (
        lam*(lam-3*sig**2*d*d-b0*d)**2/(4*sig**4)
        +eps*eps*(sig*d**3+a0*d*d+c0*d
                   +lam*(8*e*rho-3*d/sig)-eps*eps)
    )
    zero(eliminated+eps*eps*norm
         -lam*exchange_defect*(exchange_defect-2*eps*k)/(4*sig**4))
    return {"exact_identity_checks": 7,
            "variable_E_allowed_for_degree_bound": True,
            "remainder_degree_formulas": ["r=3*k-ell", "s=2*r-k", "deg(Lambda)=3*r-2*k"]}


def endpoint_coefficients():
    y, d, e, rho, sig, lam, tt = S.symbols(
        "Y D E rho sigma lambda T", nonzero=True
    )
    b0 = 16*e*sig**3*(rho-2*sig**2)
    a0 = 24*e*sig**2*(rho-4*sig**2)
    c0 = -128*e*e*sig**3*rho*(rho-2*sig**2)
    f = (lam*(lam-3*sig**2*d*d-b0*d)**2/(4*sig**4)
         +y*y*(sig*d**3+a0*d*d+c0*d
               +lam*(8*e*rho-3*d/sig)-y*y))
    assert S.Poly(f, d).LC() == 9*lam/4
    aa = -4*sig/(9*lam)
    cp = 8*e*sig*(5*rho-28*sig**2)/3
    after = S.Poly(S.expand(f.subs(d, aa*y*y+tt)), y)
    assert after.degree() == 6
    zero(after.nth(6)+16*sig**3*(tt-cp)/(81*lam*lam))
    for power, tdegree in [(4, 2), (2, 3), (0, 4)]:
        assert S.Poly(after.nth(power), tt).degree() <= tdegree
    assert all(after.nth(i) == 0 for i in (1, 3, 5))
    final = S.Poly(S.expand(after.as_expr().subs(tt, cp)), y)
    assert final.degree() == 4
    n4 = (17152*e*e*rho*rho*sig**4-123904*e*e*rho*sig**6
          +262144*e*e*sig**8+3*lam)
    n0 = (2240*e*e*rho*rho*sig**4-22784*e*e*rho*sig**6
          +57344*e*e*sig**8-3*lam)
    zero(final.nth(4)-n4/(81*lam))
    zero(final.nth(0)-lam*n0*n0/(36*sig**4))
    positive = 101*rho*rho-764*rho*sig*sig+1664*sig**4
    zero(n4+n0-192*e*e*sig**4*positive)
    zero(positive-((101*rho-382*sig*sig)**2+22140*sig**4)/101)
    x = S.symbols("x")
    assert S.discriminant(101*x*x-764*x+1664, x) == -88560
    return {"endpoint_quartic_degree": 4,
            "nonconstant_T_degree_obstruction_checked": True,
            "quadratic_approximation": "delta=-4*sigma*epsilon^2/(9*lambda)+8*E*sigma*(5*rho-28*sigma^2)/3",
            "coefficient_incompatibility": "N4+N0=192*E^2*sigma^4*((101*rho-382*sigma^2)^2+22140*sigma^4)/101",
            "positive_quadratic_discriminant": -88560}


def degree_diagnostics():
    cases = eligible = first_negative = second_negative = 0
    for u in range(1, 81):
        for v in range(u, 2*u):
            for h in range((u+1)//2, u):
                for d in range(max(1, u-h), u+1):
                    k = 3*h+v-2*u-d
                    ell = 2*h+v-u-d
                    e = u+v-2*d
                    r = 3*k-ell
                    selected = e < r < k
                    translated = 7*h > 6*u-v and 4*h < 3*u-v+d
                    assert selected == translated
                    cases += 1
                    if not selected:
                        continue
                    eligible += 1
                    assert k > r > e >= 0 and ell > 2*k
                    assert 3*k+ell > max(k+ell+e, 2*k+e, 4*k)
                    assert 2*r+2*k > max(e+r+2*k, 3*r)
                    ss = 2*r-k
                    ll = 3*r-2*k
                    assert ss == 11*h+3*v-8*u-3*d
                    assert ll == 15*h+4*v-11*u-4*d
                    if ss < 0:
                        first_negative += 1
                    elif ll < 0:
                        second_negative += 1
                    assert 4*r-2*k < 3*r
                    assert max(e+2*r, 2*e+r) < 3*r
                    assert (ll >= 0) == (15*h+4*v >= 11*u+4*d)
    endpoint_cases = rounding_cases = 0
    for u in range(1, 501):
        # Central saturation at half ratio is already strictly above 3*u/4.
        for h in range((5*u)//7+1, u):
            if 4*h >= 3*u:
                assert 15*h > 11*u
            else:
                k, ell, r = 3*h-2*u, 2*h-u, 7*h-5*u
                assert 0 < r < k
                assert (3*r >= 2*k) == (15*h >= 11*u)
            rounding_cases += 1
            if 15*h == 11*u:
                assert u % 15 == 0
                assert (3*h-2*u, 2*h-u, 7*h-5*u, 11*h-8*u) == (
                    u//5, 7*u//15, 2*u//15, u//15)
                endpoint_cases += 1
        assert (11*u)//15+1 >= (5*u)//7+1
    low_remainder_cases = 0
    for ss in range(1, 101):
        for mm in range(1, 2*ss):
            assert max(4*ss+2*mm, 2*ss+3*mm, 4*mm, 6*ss) < 6*ss+mm
            low_remainder_cases += 1
    odd_cores = 0
    for q in range(3, 1001):
        u, v, h, d = q, q+1, q-1, q
        assert (7*h <= 6*u-v or 4*h >= 3*u-v+d
                or 15*h+4*v >= 11*u+4*d)
        odd_cores += 1
    return {"degree_translation_cases": cases,
            "two_step_eligible_cases": eligible,
            "first_negative_degree_exclusions": first_negative,
            "second_negative_degree_exclusions": second_negative,
            "central_integer_rounding_cases": rounding_cases,
            "central_11_over_15_endpoints": endpoint_cases,
            "nonconstant_T_dominance_cases": low_remainder_cases,
            "odd_core_nonexclusion_diagnostics": odd_cores}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    result = {
        "scope": "Lifted polynomial portraits only; general numerical i=3 remains open.",
        "exact_identities": identities(),
        "strict_endpoint_coefficients": endpoint_coefficients(),
        "degree_diagnostics": degree_diagnostics(),
        "proved_in_paper": [
            "t!=1/2: 7*h<=6*u-v or 4*h>=3*u-v+d1 or 15*h+4*v>=11*u+4*d1",
            "balanced central saturation: h>11*u/15 at every ratio",
        ],
        "not_proved": ["infinite square descent", "h>=3*u/4 at every ratio",
                       "all larger difference degrees", "odd five-power cores a>=4",
                       "general numerical lifting"],
        "new_fully_resolved_indices": 0,
        "complete_i3_solution": False,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"passed": True, "degree_diagnostics": result["degree_diagnostics"],
                      "general_i3": "open"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
