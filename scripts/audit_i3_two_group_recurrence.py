"""Exact polynomial recurrence for the smooth two-linear-residual branch.

The genus-one derivation is degree-unbounded. Exact elimination below closes
only the d=4,5,6 instances, not every branch of degrees 10 and 12.
"""
import json
from pathlib import Path
import time
import sympy as S

ROOT = Path(__file__).resolve().parent.parent


def recurrence(degree):
    d = degree
    x, m, c = S.symbols("x m c")
    t = S.Rational(3, 2*d)
    u = {d: S.Integer(1)}
    bb = {d: t}
    def at(data, n):
        return data.get(n, S.Integer(0))
    for n in range(d-1, -1, -1):
        e = ((-2*(t*t+m)*(n+1)+m)*at(u, n+1)+m*(2*n+3)*at(u, n+2)
             -2*c*at(bb, n+1)-m*at(bb, n+2))
        o = ((2*(n+1)*(c-1)-(c+1))*at(bb, n+1)
             +(2*(n+2)*(m-c)-2*m)*at(bb, n+2)
             +m*(1-2*(n+3))*at(bb, n+3)
             -(2*c-3)*at(u, n+1)-(m-2*c)*at(u, n+2)+m*at(u, n+3))
        determinant = 4*n*n*t*t-9
        assert determinant != 0
        u[n] = S.expand((-2*n*e-3*o)/determinant)
        bb[n] = S.expand((-3*e-2*n*t*t*o)/determinant)
    field = S.QQ.poly_ring(m, c)
    U = S.Poly(sum(value*x**n for n, value in u.items()), x, domain=field)
    B = S.Poly(sum(value*x**n for n, value in bb.items()), x, domain=field)
    M = S.Poly(x*x+c*x+m, x, domain=field)
    A = S.Poly((x-1)*(t*t*x-m), x, domain=field)
    P2 = S.Poly(3*x*x+2*c*x+m, x, domain=field)
    E = (2*S.Poly(x, x)*A*U.diff()+S.Poly(m*(x-1), x, domain=field)*U-P2*B)
    O = (2*S.Poly(x*(x-1), x)*M*B.diff()
         +S.Poly(-(c+1)*x*x-2*m*x+m, x, domain=field)*B-S.Poly(x-1, x)*P2*U)
    assert E.degree() <= 1 and O.degree() <= 2
    assert S.cancel(B.nth(d-1)-t*U.nth(d-1)+(t*t*(c+1)+m)/(2*t)) == 0
    # Check that these two differential equations force the norm identity.
    N = A*U**2-M*B**2
    differential = S.Poly(x*(x-1), x)*N.diff()-S.Poly(2*x-1, x)*N
    assert (differential-(S.Poly(x-1, x)*U*E-B*O)).is_zero
    eqs = []
    for expression in [E.nth(i) for i in range(2)]+[O.nth(i) for i in range(3)]:
        if expression == 0:
            continue
        f = S.Poly(expression, m, c).clear_denoms()[1].primitive()[1].as_expr()
        while all(mon[0] > 0 for mon in S.Poly(f, m, c).monoms()):
            f = S.cancel(f/m)
        if f not in eqs and -f not in eqs:
            eqs.append(f)
    product = S.expand(m*(1+c+m)*(m-t*t)*(c*c-4*m)
                       *(t*t*(c+1)+m)*(m+c*t*t+t**4))
    product = S.Poly(product, m, c).clear_denoms()[1].primitive()[1].as_expr()
    return (m, c), eqs, product


def close(degree, prime):
    started = time.time()
    variables, equations, product = recurrence(degree)
    G = S.groebner(equations, *variables, order="grevlex", domain=S.QQ)
    inverse = S.symbols("inverse")
    saturated = S.groebner([f.as_expr() for f in G.polys]+[inverse*G.reduce(product)[1]-1],
                          inverse, *variables, order="grevlex", domain=S.QQ)
    assert saturated.is_zero_dimensional
    lex = saturated.fglm("lex")
    c = variables[-1]
    polys = [f.as_expr() for f in lex.polys if f.free_symbols <= {c}]
    assert len(polys) == 1
    P = S.Poly(polys[0], c, domain=S.QQ).clear_denoms()[1].primitive()[1]
    assert int(P.LC()) % prime != 0
    residues = [int(P.eval(i)) % prime for i in range(prime)]
    assert 0 not in residues
    assert P.degree() == {4: 9, 5: 16, 6: 21}[degree]
    return {
        "d": degree, "total_degree": 2*degree,
        "group_degrees": [degree-1, degree-1, 2], "t": str(S.Rational(3, 2*degree)),
        "equations": [str(e) for e in equations],
        "eliminant_coefficients_descending": [int(v) for v in P.all_coeffs()],
        "eliminant_degree": P.degree(), "prime": prime,
        "leading_coefficient_residue": int(P.LC()) % prime,
        "all_residues": residues, "rational_root_possible": False,
        "seconds": round(time.time()-started, 3),
    }


def main():
    cases = [close(d, p) for d, p in [(4, 19), (5, 23), (6, 11)]]
    result = {
        "passed": True,
        "scope": "two-linear-residual branches for d=4,5,6; not all degrees 10 or 12; not general numerical i=3",
        "recurrence_uses_exact_QQ": True,
        "cases": cases,
    }
    path = ROOT / "data/results/verification_i3_two_group_recurrence.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"passed": True, "d": [4, 5, 6], "seconds": [c["seconds"] for c in cases]}))


if __name__ == "__main__":
    main()
