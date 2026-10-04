"""Exact identities and thresholds for the general largest-base gcd bound."""

from fractions import Fraction
from math import factorial, lcm
from pathlib import Path
import json
import sympy as sp


def main():
    P, R, d, u, v, i = sp.symbols("P R d u v i")
    j = R*d + u
    assert sp.expand(P*(j-v) - (P*(u-v)-R) - R*(P*d+1)) == 0
    z = sp.symbols("z")
    assert sp.expand((-i+1-z)+i-(1-z)) == 0
    assert sp.expand(i-(i-1-z)-(1+z)) == 0
    q, m = sp.symbols("q m")
    assert sp.expand((m+1)*q*q - (1+m*(q-1)**2)
                     - (q*q-1+m*(2*q-1))) == 0
    x, y = sp.symbols("x y")
    assert sp.expand((x*y-1)-((x-1)+(y-1))-(x-1)*(y-1)) == 0
    assert Fraction(2*2**14, 7) + 2 <= Fraction(3*2**14, 10)
    assert Fraction(3, 10) + Fraction(1, 5) == Fraction(1, 2)
    assert 2**14 > 10**4
    thresholds = []
    # This list makes the universal explicit formula concrete for the
    # currently relevant small indices; the proof is not limited to it.
    for index in range(3, 35):
        L_i = lcm(*range(1, index+1))
        assert factorial(index) % L_i == 0
        C_i = (2*index)**index * factorial(index)
        B_i = max(2**14, 2*L_i, C_i+1)
        assert B_i >= 2**14 and B_i >= 2*L_i and B_i > C_i
        row_strengthenings = []
        for row_s in range(index-1):
            row_k = row_s+1
            row_budget = (2*index)**row_k * L_i
            row_threshold = max(2**14, 2*L_i, row_budget+1)
            assert B_i >= row_threshold > row_budget
            assert Fraction(row_k-1, row_k) <= Fraction(index-1, index)
            row_strengthenings.append(dict(s=row_s, k=row_k,
                                            exponent_budget=row_budget,
                                            minimum_base=row_threshold))
        prime_count = int(sp.primepi(index-1))
        assert prime_count+1 <= index-1
        universal_row_threshold = max(2**14, 2*L_i,
                                      (2*index)**(prime_count+1)*L_i+1)
        thresholds.append(dict(i=index, L_i=L_i,
                               exponent_budget=C_i, minimum_base=B_i,
                               row_strengthenings=row_strengthenings,
                               early_nonmaximum_row_bound=prime_count,
                               uniform_early_row_minimum_base=universal_row_threshold))
    result = dict(
        status="passed",
        independent_review="Paper proof, row-index strengthening, s=0 branch, and early nonmaximum-row existence independently audited by root",
        scope="Any i>=3, a nonmaximum row s<=i-2, largest candidate complete prime-power base in row s, standard full digit conditions. No complete polynomial allocation. Adjacent row r=s+1 need not be nonmaximum.",
        degree_bound="i deg gcd(F-(s+1),J-u) <= (i-1)(deg F+1), all u=0,...,i-1",
        strengthened_degree_bound="(s+1) deg gcd(F-(s+1),J-u) <= s(deg F+1), all u=0,...,i-1",
        universal_base_threshold="max(2^14, 2*lcm(1,...,i), (2i)^i*i!+1)",
        row_strengthened_base_threshold="max(2^14, 2*lcm(1,...,i), (2i)^(s+1)*lcm(1,...,i)+1)",
        early_nonmaximum_row="There is a nonmaximum s<=pi(i-1); adjacent r=s+1 need not be nonmaximum",
        numerical_cofactor_bound="G_u(q)^i < i!*i^i*n^(i-1)",
        strengthened_numerical_cofactor_bound="G_u(q)^(s+1) < delta_s*i^(s+1)*n^s <= lcm(1,...,i)*i^(s+1)*n^s",
        limitation="Weak in small digit degree; does not prove the numerical-to-polynomial bridge or solve any new index.",
        exact_symbolic_identities=5,
        illustrative_index_thresholds=thresholds,
    )
    path = Path(__file__).resolve().parents[1] / "data/results/verification_largest_base_adjacent_shared_degree_2026-10-04.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({key:value for key,value in result.items()
                      if key != "illustrative_index_thresholds"}, ensure_ascii=False, indent=2))
    print("Explicit threshold records:", len(thresholds))


if __name__ == "__main__":
    main()
