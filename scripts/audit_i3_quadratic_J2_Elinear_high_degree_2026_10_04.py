"""Exact finite end of the E-linear / quadratic J-2 quotient bound.

This certifies only the explicitly stated complete-polynomial-allocation
branch.  It does not claim the bridge from arbitrary numerical candidates.
"""

from fractions import Fraction
from itertools import product
import json


def evaluate(coefficients, argument):
    value = 0
    for coefficient in reversed(coefficients):
        value = value * argument + coefficient
    return value


def multiply(left, right):
    result = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return result


def certify():
    counts = {name: 0 for name in [
        "D_parameter_rows", "standard_F", "integer_Q", "quotient_rows",
        "standard_J", "polynomial_allocation", "numerical_range",
        "four_divides_n", "first_divisibility", "second_divisibility",
    ]}
    final = []
    pre_first = []
    allocation_rows = []
    for q in (5, 7):
        for a in range(2, q):
            maximum_D = (q - 1) // (a - 1)
            for b in range(1, (q - 1) // a + 1):
                for s in range(1, (q - 1) // (a * b) + 1):
                    # deg D=5, D(0)=1, D_5=b*s, 1 <= D_1 <= a-1.
                    for D1 in range(1, min(a - 1, maximum_D) + 1):
                        for middle in product(range(1, maximum_D + 1), repeat=3):
                            D = [1, D1, *middle, b * s]
                            counts["D_parameter_rows"] += 1
                            F = [1] + [a * D[k - 1] - D[k] for k in range(1, 6)] + [a * b * s]
                            if not (1 <= F[1] < q and all(0 <= z < q for z in F)):
                                continue
                            counts["standard_F"] += 1
                            Q = [1]
                            for k in range(1, 5):
                                Q.append(D[k] - b * Q[-1])
                            if Q[4] != s or b * Q[4] != D[5]:
                                continue
                            assert multiply([1, b], Q) == D
                            counts["integer_Q"] += 1
                            for h in (1, 2):
                                for v in range(1, a * b // 2 + 1):
                                    for J1 in range(F[1] + 1):
                                        u = h * Q[1] + J1
                                        counts["quotient_rows"] += 1
                                        J = multiply([-h, u, v], Q)
                                        J[0] += 2
                                        if not all(0 <= x <= y for x, y in zip(J, F)):
                                            continue
                                        counts["standard_J"] += 1
                                        at_E_root = evaluate(J, Fraction(-1, b))
                                        if at_E_root not in (0, 1):
                                            continue
                                        counts["polynomial_allocation"] += 1
                                        n, j = evaluate(F, q), evaluate(J, q)
                                        allocation_rows.append(dict(q=q, a=a, b=b, s=s, h=h,
                                                                    u=u, v=v, D=D, Q=Q, F=F,
                                                                    J=J, n=n, j=j))
                                        if not (4 <= j and 2 * j <= n):
                                            continue
                                        counts["numerical_range"] += 1
                                        if n % 4:
                                            continue
                                        counts["four_divides_n"] += 1
                                        row = dict(q=q, a=a, b=b, s=s, h=h, u=u, v=v,
                                                   D=D, Q=Q, F=F, J=J, n=n, j=j,
                                                   first_remainder=3*j*(j-1) % (n-1))
                                        pre_first.append(row)
                                        if row["first_remainder"]:
                                            continue
                                        counts["first_divisibility"] += 1
                                        if 6 * j * (j - 1) * (j - 2) % (n - 2):
                                            continue
                                        counts["second_divisibility"] += 1
                                        final.append(row)
    assert not final
    assert counts["polynomial_allocation"] == 6
    assert counts["numerical_range"] == 4
    assert counts["four_divides_n"] == 0
    assert all(row["n"] % 4 == 2 for row in allocation_rows)
    assert counts["first_divisibility"] == 0
    return {"scope": "complete allocation; E=1+bX; deg Q=4; deg (J-2)/Q=2; q=5,7",
            "counts": counts, "allocation_rows": allocation_rows,
            "pre_first": pre_first, "survivors": final}


if __name__ == "__main__":
    result = certify()
    print(json.dumps(result, ensure_ascii=False, indent=2))
