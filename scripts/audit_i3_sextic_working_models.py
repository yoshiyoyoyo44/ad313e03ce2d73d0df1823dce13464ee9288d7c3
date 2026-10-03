"""Check two explicit sextic working models, without certifying exhaustiveness."""
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent.parent


def main():
    z, x = s.symbols("z x")
    models = []
    for t, expected_degrees, expected_origin in (
        (s.Rational(1, 6), [3, 2, 1], s.Rational(2, 3)),
        (s.Rational(1, 3), [3, 1, 2], s.Rational(1, 3)),
    ):
        r = -1 - t
        beta = r * (r + 1)
        a = 1 / ((r + 1) * (2*r + 3))
        b = -2 / (2*r + 3)
        H = a*z**2 + b*z + 1
        U = s.cancel(((r+1) + H*z - beta*H**2/r) / ((r+1)*z))
        V = s.expand(beta*U + z/(r+1) - H)
        C = beta*H + z
        F = s.expand(U*V + 1)
        J = s.expand(1 + V*(t*U + H))
        assert all(s.denom(s.cancel(P)) == 1 for P in (U, V, H, C))
        assert s.expand(U*C - V*H) == 1
        assert s.degree(F, z) == s.degree(J, z) == 6
        assert s.LC(s.Poly(J, z)) / s.LC(s.Poly(F, z)) == t
        assert s.rem(J*(J-1), F-1, z) == 0
        assert s.rem(J*(J-1)*(J-2), F-2, z) == 0
        degrees = [s.degree(s.gcd(F-2, J-i), z) for i in range(3)]
        assert degrees == expected_degrees
        D0 = s.Poly(H-r*U, z)
        assert D0.degree() == 3 and D0.is_irreducible
        assert s.expand((H-r*U)*(V-(r+1)*beta*U/r) - (F-2)) == 0
        origins = s.polys.polytools.ground_roots(F-2, z)
        admissible = []
        for origin, multiplicity in origins.items():
            assert multiplicity == 1 and J.subs(z, origin) in (0, 1, 2)
            for sign in (1, -1):
                f = s.Poly(F.subs(z, origin+sign*x), x)
                j = s.Poly(J.subs(z, origin+sign*x), x)
                if all(f.nth(i) >= j.nth(i) >= 0 for i in range(7)):
                    admissible.append((origin, sign))
        assert admissible == [(expected_origin, 1)]
        models.append({
            "t": str(t),
            "F": str(F),
            "J": str(J),
            "F_minus_2_factorization": str(s.factor(F-2)),
            "factor_group_degrees": [int(d) for d in degrees],
            "rational_origins": sorted(str(q) for q in origins),
            "coefficientwise_nonnegative_origin": str(expected_origin),
            "positive_affine_scale_required": True,
        })
    result = {
        "status": "passed",
        "scope": "Exact identities and affine positivity for two explicit working models only.",
        "models": models,
        "exhaustive_sextic_classification_certified": False,
        "integer_parameter_classification_certified": False,
        "numerical_counterexample_exclusion_certified": False,
        "complete_problem_solution": False,
        "remaining_indices": 28,
    }
    output = ROOT / "data/results/verification_i3_sextic_working_models.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
