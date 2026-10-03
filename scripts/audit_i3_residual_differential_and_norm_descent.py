"""Exact checks for the all-degree residual differential and norm descent.

The accompanying note proves the arbitrary-degree claims. These symbolic
identities and polynomial diagnostics do not certify general numerical i=3.
"""
import json
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent
X = S.symbols("X")


def zero(expression):
    assert S.cancel(expression) == 0


def formal_identities():
    m, ell, tau, u, b = S.symbols("m ell tau u b")
    a = tau*tau*m+ell
    un = (a+tau*tau*m)*u-2*tau*m*b
    bn = (a+tau*tau*m)*b-2*tau*a*u
    zero(a*un**2-m*bn**2-ell**2*(a*u**2-m*b**2))
    zero(S.Matrix([[a+tau*tau*m, -2*tau*m],
                   [-2*tau*a, a+tau*tau*m]]).det()-ell**2)
    # Both eigenvalues in the Laurent-series field, with s^2=a/m.
    s = S.symbols("s")
    zero((un+bn/s-(a+tau*tau*m-2*tau*m*s)*(u+b/s)).subs(ell, m*(s*s-tau*tau)))
    zero((un-bn/s-(a+tau*tau*m+2*tau*m*s)*(u-b/s)).subs(ell, m*(s*s-tau*tau)))
    zero((un.subs(ell, 0)-2*tau*m*(tau*u-b)))
    zero((bn+tau*un).subs(ell, 0))
    # Complete the square for each of the three choices of the e-degree group.
    h, q, t, w = S.symbols("h q t w")
    z = 1-3*t
    table = []
    for epsilon in range(3):
        rr = epsilon-1-t
        kappa = rr*(rr-z)
        tau0 = (rr-z)/2
        hh = rr*u+q*m
        ww = kappa*hh+ell*q
        residual = z*hh**2*u+u*u*ww-hh**3
        norm = (tau0**2*m+ell)*u*u-m*(hh+tau0*u)**2
        zero(residual-q*norm)
        other = [j for j in range(3) if j != epsilon]
        values = [S.simplify(j-1-t+tau0) for j in other]
        table.append({"epsilon": epsilon, "tau": str(tau0),
                      "value_mod_M": str(S.simplify(rr+tau0)),
                      "values_at_linear_residuals": [str(v) for v in values]})
    return {"identities": 9, "norm_table": table}


def analyze_polynomials(F, J, label):
    field = S.QQ
    f = S.Poly(F, X, domain=field)
    j = S.Poly(J, X, domain=field)
    u = S.gcd(f-1, j)
    assert u.eval(0) != 0
    u = S.Poly(u.as_expr()/u.eval(0), X, domain=field)
    v = (f-1).exquo(u)
    assert u.degree() <= v.degree()
    t = j.LC()/f.LC()
    h = (j-1).exquo(v)-u.mul_ground(t)
    z = 1-3*t
    r_values = [s-1-t for s in range(3)]
    ds = [S.gcd(f-2, j-s).monic() for s in range(3)]
    rs = [(h-u.mul_ground(r)).exquo(d).monic() for r, d in zip(r_values, ds)]
    residual = S.Poly(S.prod((h-u.mul_ground(r)).as_expr() for r in r_values), X).exquo(f-2)
    w = (h**3+residual-h*h*u.mul_ground(z)).exquo(u*u)
    weighted = sum((residual.exquo(rr)*rr.diff()).mul_ground(r) for rr, r in zip(rs, r_values))
    differential = residual*h.diff().mul_ground(3)-h*residual.diff()-residual*u.diff().mul_ground(z)+u*weighted
    assert differential.is_zero
    kk = h-u.mul_ground(z/3)
    core = w+kk.mul_ground(z*z/3)+u.mul_ground(2*z**3/27)
    assert (kk**3+residual-u*u*core).is_zero
    universal = sum((residual.exquo(rr)*rr.diff()).mul_ground(4-3*s) for s, rr in enumerate(rs))
    assert (residual*kk.diff().mul_ground(3)-kk*residual.diff()-u*universal.mul_ground(S.Rational(1, 3))).is_zero
    assert S.gcd(kk, residual).degree() == 0
    result = {"label": label, "degree_F": f.degree(), "u": u.degree(),
              "v": v.degree(), "h": h.degree(), "degree_R": residual.degree(),
              "group_degrees": [p.degree() for p in ds],
              "residual_degrees": [p.degree() for p in rs],
              "repeated_residual": any(S.gcd(p, p.diff()).degree() > 0 for p in rs)}
    general_steps = 0
    for epsilon, mm in enumerate(ds):
        if mm.degree() == 0:
            continue
        kappa = r_values[epsilon]*(r_values[epsilon]-z)
        if kappa == 0:
            continue
        qq = (h-u.mul_ground(r_values[epsilon])).exquo(mm)
        ll = (w-h.mul_ground(kappa)).exquo(qq)
        tau = (r_values[epsilon]-z)/2
        bb = h+u.mul_ground(tau)
        aa = mm.mul_ground(tau*tau)+ll
        nn = residual.exquo(qq)
        assert aa*u*u-mm*bb*bb == nn
        assert nn.degree() == u.degree()-v.degree()+mm.degree()
        assert ll.degree() == h.degree()-u.degree()+mm.degree()
        assert S.gcd(ll,mm*nn).degree() == 0
        ur,br = u,bb
        for r in range(1,4):
            ur,br = ((aa+mm.mul_ground(tau*tau))*ur-mm*br.mul_ground(2*tau),
                     (aa+mm.mul_ground(tau*tau))*br-aa*ur.mul_ground(2*tau))
            expected = max(u.degree()-r*(mm.degree()-2*ll.degree()),r*mm.degree()-v.degree())
            assert max(ur.degree(),br.degree()) == expected
            assert (aa*ur*ur-mm*br*br-ll**(2*r)*nn).is_zero
            assert (br-ur.mul_ground(r_values[epsilon]+tau-2*r*tau)).rem(mm).is_zero
            general_steps += 1
    result["all_group_norm_steps"] = general_steps
    # Test the norm reduction on an actual polynomial model when applicable.
    linear = [s for s, p in enumerate(rs) if p.degree() == 1]
    if len(linear) == 2:
        epsilon = next(s for s in range(3) if s not in linear)
        mm = ds[epsilon]
        qq = (h-u.mul_ground(r_values[epsilon])).exquo(mm)
        kappa = r_values[epsilon]*(r_values[epsilon]-z)
        ll = (w-h.mul_ground(kappa)).exquo(qq)
        tau = (r_values[epsilon]-z)/2
        bb = h+u.mul_ground(tau)
        aa = mm.mul_ground(tau*tau)+ll
        nn = aa*u*u-mm*bb*bb
        assert nn == residual.exquo(qq)
        assert nn.degree() == 2 and S.gcd(nn, nn.diff()).degree() == 0
        assert ll.degree() == h.degree()-u.degree()+mm.degree()
        for r in range(1, 7):
            ur, br = u, bb
            for _ in range(r):
                ur, br = ((aa+mm.mul_ground(tau*tau))*ur-mm*br.mul_ground(2*tau),
                          (aa+mm.mul_ground(tau*tau))*br-aa*ur.mul_ground(2*tau))
            expected = max(u.degree()-r*(mm.degree()-2*ll.degree()),
                           r*mm.degree()-u.degree()+2-mm.degree())
            assert max(ur.degree(), br.degree()) == expected
            assert (aa*ur*ur-mm*br*br-ll**(2*r)*nn).is_zero
            assert (br-ur.mul_ground(r_values[epsilon]+tau-2*r*tau)).rem(mm).is_zero
        result["norm_descent_steps"] = 6
    return result, rs


def known_models():
    quartic = (320*X**4+512*X**3+240*X**2+32*X+2,
               80*X**4+168*X**3+114*X**2+27*X+2)
    quintic = (150000*X**5+125000*X**4+35000*X**3+3750*X**2+125*X+2,
                30000*X**5+31000*X**4+11400*X**3+1770*X**2+105*X+2)
    septic = (210827008*X**7+184473632*X**6+62118672*X**5+10084200*X**4
              +806736*X**3+28812*X**2+343*X+2,
              30118144*X**7+30655968*X**6+12331536*X**5+2483320*X**4
              +261072*X**3+13524*X**2+287*X+2)
    octic = (147456*X**8+524288*X**7+745472*X**6+540672*X**5
             +211200*X**4+43008*X**3+4032*X**2+128*X+2,
             18432*X**8+74752*X**7+123648*X**6+107136*X**5
             +51920*X**4+13896*X**3+1890*X**2+107*X+2)
    result = []
    for name, (f, j) in zip(("quartic", "quintic", "septic", "octic"),
                            (quartic, quintic, septic, octic)):
        row, rs = analyze_polynomials(f, j, name)
        result.append(row)
        inner = X-X**2
        row, _ = analyze_polynomials(S.expand(f.subs(X, inner)), S.expand(j.subs(X, inner)),
                                     name+"_negative_inner_coefficient")
        result.append(row)
        if name == "quartic":
            rr = next(p for p in rs if p.degree() == 1)
            origin = -rr.nth(0)/rr.nth(1)
            inner = X**2+origin
            row, _ = analyze_polynomials(S.expand(f.subs(X, inner)), S.expand(j.subs(X, inner)),
                                         "quartic_repeated_residual")
            assert row["repeated_residual"]
            result.append(row)
    return result


def degree_diagnostics():
    count = 0
    for e in range(2, 7):
        for delta in range(e):
            tau = S.Rational(2, 5)
            m = S.Poly(X**e+2*X+3, X, domain=S.QQ)
            ell = S.Poly(2 if delta == 0 else X**delta+2, X, domain=S.QQ)
            a = m.mul_ground(tau*tau)+ell
            one = S.Poly(1, X, domain=S.QQ)
            uf, bf = one, one
            n0 = a-m
            for k in range(1, 4):
                uf, bf = ((a+m.mul_ground(tau*tau))*uf+m*bf.mul_ground(2*tau),
                          (a+m.mul_ground(tau*tau))*bf+a*uf.mul_ground(2*tau))
                assert uf.degree() == k*e and bf.LC() == tau*uf.LC()
                nu = e+2*k*delta
                assert (a*uf*uf-m*bf*bf) == ell**(2*k)*n0
                ur, br = uf, bf
                for r in range(6):
                    expected = max(k*e-r*(e-2*delta), r*e-k*e+nu-e)
                    assert max(ur.degree(), br.degree()) == expected
                    assert (br-ur.mul_ground(1+2*(k-r)*tau)).rem(m).is_zero
                    count += 1
                    ur, br = ((a+m.mul_ground(tau*tau))*ur-m*br.mul_ground(2*tau),
                              (a+m.mul_ground(tau*tau))*br-a*ur.mul_ground(2*tau))
    return count


def degree_window_diagnostics():
    count = 0
    examples = []
    for u in range(2, 101):
        for e in range(2, u+1):
            rstar = (u+2*e-3)//e
            lower = (e*(rstar+1)-u+2*rstar-1)//(2*rstar)
            assert rstar >= 1 and lower >= 1
            assert rstar*e-u+2-e < e
            for delta in range(e):
                w = max(u-rstar*(e-2*delta), rstar*e-u+2-e)
                assert (w < e) == (delta < lower)
                count += 1
            if (u, e) in ((3, 3), (20, 12), (100, 20)):
                examples.append({"u": u, "e": e, "r_star": rstar,
                                 "delta_lower_bound": lower, "h_lower_bound": u-e+lower})
    return {"comparisons": count, "examples": examples}


def main():
    result = {"passed": True,
              "scope": "all-degree polynomial residual differential; complete minimal boundary exclusion for two linear residual groups; not general numerical i=3",
              "formal": formal_identities(), "known_models": known_models(),
              "degree_norm_diagnostics": degree_diagnostics(),
              "degree_window": degree_window_diagnostics()}
    path = ROOT/"data/results/verification_i3_residual_differential_and_norm_descent.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"passed": True, "models": len(result["known_models"]),
                      "norm_degree_diagnostics": result["degree_norm_diagnostics"],
                      "degree_window_comparisons": result["degree_window"]["comparisons"]}))


if __name__ == "__main__":
    main()
