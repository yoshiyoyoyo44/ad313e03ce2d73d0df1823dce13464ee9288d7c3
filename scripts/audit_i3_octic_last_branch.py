"""Exact ideal-membership certificate and rational-root obstruction.

The modular calculations used to discover the basis are not trusted by this
audit. Every candidate generator is first proved to belong to the original
ideal by checking an explicit rational linear combination.
"""
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import time

import sympy as S

ROOT = Path(__file__).resolve().parent.parent
CERT = ROOT / "data/certificates/i3_octic_last_branch_membership.json.gz"


def make_model():
    x, a, m, q1, q0 = S.symbols("x a m q1 q0")
    variables = (q0, q1, m, a)
    field = S.QQ.frac_field(*variables)
    M = x*x+(-S.Rational(64, 9)*m-1-S.Rational(16, 3)/a)*x+m
    L = S.Rational(3, 4)/a*x+S.Rational(55, 64)*m
    Q = -S.Rational(5, 8)*a*x*x+q1*x+q0
    w2 = S.Rational(1, 8)/a
    w0 = S.Rational(605, 512)*q0*m
    w1 = S.Rational(9, 256)*Q.subs(x, 1)*M.subs(x, 1)-w2-w0
    W = w2*x*x+w1*x+w0
    H = S.Poly((W-L*Q)/S.Rational(15, 32), x, domain=field)
    U = S.Poly((H.as_expr()-Q*M)/S.Rational(5, 8), x, domain=field)
    P = U**2*S.Poly(L, x, domain=field)-S.Poly(M, x, domain=field)*H*(H+S.Rational(3, 4)*U)
    assert H.degree() == 3 and H.LC() == 1
    assert U.degree() == 4 and U.LC() == a
    assert P.degree() == 7
    assert S.cancel(P.eval(0)) == 0 and S.cancel(P.eval(1)) == 0
    N = (-17600*a*a*m-88000*a*m*q0+183040*a*m*q1-38115*a*q0
         -76800*q0+24576*q1+16384-15360*a)
    assert S.cancel(19200*a*P.nth(1)-m*m*q0*N) == 0
    eqs = [S.Poly(S.together(P.nth(i)).as_numer_denom()[0], *variables).primitive()[1].as_expr()
           for i in range(7, 2, -1)]
    return variables, eqs, S.expand(a*m*q0*N)


def main():
    started = time.time()
    variables, eqs, product = make_model()
    with gzip.open(CERT, "rt") as handle:
        certificate = json.load(handle)
    local = {str(v): v for v in variables}
    assert certificate["variables"] == list(local)
    assert [S.sympify(s, locals=local) for s in certificate["generators"]] == eqs
    targets = [S.Poly(S.sympify(s, locals=local), *variables, domain=S.QQ)
               for s in certificate["targets"]]
    input_dicts = [S.Poly(f, *variables).as_dict() for f in eqs]
    rows = []
    for index, monomial in certificate["multipliers"]:
        rows.append({tuple(x+y for x, y in zip(mon, monomial)): int(c)
                     for mon, c in input_dicts[index].items()})
    assert len(rows) == len(certificate["coefficients"])
    verified = 0
    for j, target in enumerate(targets):
        obtained = {}
        for row, coefficients in zip(rows, certificate["coefficients"]):
            c = Fraction(coefficients[j])
            if not c:
                continue
            for monomial, value in row.items():
                obtained[monomial] = obtained.get(monomial, Fraction(0))+c*value
        obtained = {mon: c for mon, c in obtained.items() if c}
        expected = {mon: Fraction(int(c.p), int(c.q)) for mon, c in target.terms()}
        assert obtained == expected, (j, len(obtained), len(expected))
        verified += 1
    # All these generators are now proved consequences of the five inputs.
    # Computing a basis from them and the inverse equation preserves this
    # consequence relation; no modular reconstruction is used from here on.
    G = S.groebner([f.as_expr() for f in targets], *variables, order="grevlex", domain=S.QQ)
    assert len(G.polys) == 18
    assert all(G.reduce(f)[1] == 0 for f in eqs)
    inverse = S.symbols("inverse")
    saturated = S.groebner([f.as_expr() for f in G.polys]+[inverse*G.reduce(product)[1]-1],
                          inverse, *variables, order="grevlex", domain=S.QQ)
    assert saturated.is_zero_dimensional and len(saturated.polys) == 15
    lex = saturated.fglm("lex")
    a = variables[-1]
    univariate = [f.as_expr() for f in lex.polys if f.free_symbols <= {a}]
    assert len(univariate) == 1
    P = S.Poly(univariate[0], a, domain=S.QQ).clear_denoms()[1].primitive()[1]
    expected_coefficients = [
        108967609884375, 3883209370425000, 43637955542280000,
        26457957884160000, -2851654968470246400,
        -17264076353274617856, 10922529658125680640,
        400622296087419420672, 1224413964030468685824,
        1040197993628553969664,
    ]
    assert list(P.all_coeffs()) == expected_coefficients
    assert int(P.LC()) % 101 == 98
    residues = [int(P.eval(i)) % 101 for i in range(101)]
    assert 0 not in residues
    monic_mod = [(c*pow(98, -1, 101)) % 101 for c in expected_coefficients]
    assert monic_mod == [1, 54, 50, 30, 67, 36, 75, 70, 94, 55]
    result = {
        "passed": True, "scope": "last octic polynomial branch; general numerical i=3 remains open",
        "input_equations": 5, "verified_ideal_memberships": verified,
        "certificate_degree": certificate["degree"], "certificate_rows": len(rows),
        "certificate_sha256": hashlib.sha256(CERT.read_bytes()).hexdigest(),
        "exact_saturated_basis_size": len(saturated.polys),
        "eliminant_coefficients_descending": expected_coefficients,
        "prime": 101, "leading_coefficient_residue": 98,
        "monic_modular_coefficients_descending": monic_mod,
        "all_residues": residues, "rational_roots_possible": False,
        "seconds": round(time.time()-started, 3),
    }
    path = ROOT / "data/results/verification_i3_octic_last_branch.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"passed": True, "memberships": verified,
                      "rational_root_obstruction": 101, "seconds": result["seconds"]}))


if __name__ == "__main__":
    main()
