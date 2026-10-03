"""Exact audit of the new degree-five endpoint bounds.

The infinite inequalities and case splits are proved in the companion note.
This checks the algebra and exact rational constants, and samples the entire
coefficient domain for small radices without treating that sample as a proof.
"""

import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

from audit_i3_quadratic_cofactor import forward_profiles, horner

ROOT = Path(__file__).resolve().parent.parent


def symbolic():
    a, b, b1, b2, b3, X = sp.symbols("a b b1 b2 b3 X")
    B = 1+b1*X+b2*X**2+b3*X**3
    D = sp.Poly(sp.expand((1+b*X)*B), X)
    F = sp.Poly(sp.expand(2+(a*X-1)*(1+b*X)*B), X)
    assert [D.nth(i) for i in range(5)] == [1, b+b1, b*b1+b2,
                                              b*b2+b3, b*b3]
    assert F.nth(0) == 1
    assert F.nth(1) == a-b-b1
    assert sp.expand(F.nth(2)-(a*b+(a-b)*b1-b2)) == 0
    assert sp.expand(F.nth(4)-((a-b)*b3+a*b*b2)) == 0
    assert F.nth(5) == a*b*b3
    assert Fraction(3, 4)*Fraction(17, 16)*(
        1+Fraction(2, 16)+Fraction(1, 2*16**2)) == Fraction(29427, 32768)
    assert Fraction(3, 4)*Fraction(17, 16)**2 == Fraction(867, 1024)
    assert 6*Fraction(66, 65)**2 < 7
    # At the least admissible q,z, the strict margin of formula (6).
    assert 16*(Fraction(2, 5)-Fraction(1, 17**2))-(
        Fraction(2, 25)+Fraction(1, 5*17**2)) > 0
    return {"coefficient_identity": True, "endpoint_ratio_constants": True,
            "small_integer_bound": True}


def sample():
    counts = {"profiles": 0, "quotient_cases": 0,
              "complete_prime_power_cases": 0}
    for q in range(3, 42):
        rows, _ = forward_profiles(q, m=5)
        for a, b, D, B, F in rows:
            counts["profiles"] += 1
            z, f, n = a*b, F[1], horner(F, q)
            assert q > (b+1)*f
            A = (n-1)//q
            gk = (a*q-1)*(b*q+1)
            for theta in (-1, 1):
                for d in range(z+1):
                    for x in range(f+1):
                        c = x+theta*B[1]
                        J = [1]+[
                            c*(B[e-1] if e-1 < len(B) else 0)
                            +d*(B[e-2] if 0 <= e-2 < len(B) else 0)
                            -theta*(B[e] if e < len(B) else 0)
                            for e in range(1, 6)]
                        if any(not 0 <= v <= w for v, w in zip(J, F)):
                            continue
                        j = horner(J, q)
                        if min(j, n-j) < 4:
                            continue
                        counts["quotient_cases"] += 1
                        V = x+d*q-theta*(f+z*q)
                        C = V*(q*V-gk)
                        assert C > 0
                        assert (3*C) % A or not (q >= 8*z or
                            (theta == 1 and b >= 8 and f >= 1))
                        if theta == -1 and b >= 4 and f >= 1:
                            assert 3*C < 6*A
                        if q % 2 and sp.isprime(q) and n % 4 == 0 and f:
                            counts["complete_prime_power_cases"] += 1
    # This is a structural limitation of the simple |3C|<A approach.
    q, a, b = 59, 8, 7
    F, J = [1, 1, 55, 0, 57, 56], [1, 1, 0, 0, 2, 1]
    n, j = horner(F, q), horner(J, q)
    assert n % 4 == 0 and (n-1) % q == 0 and (n-1) % (q*q) != 0
    assert all(0 <= x <= y < q for x, y in zip(J, F))
    A = (n-1)//q
    V = 1+q-(1+56*q)
    C = V*(q*V-(a*q-1)*(b*q+1))
    assert Fraction(3*C, A) == Fraction(68401473, 12550583) > 5
    assert (3*j*(j-1)) % (n-1) != 0
    counts["witness_ratio"] = "68401473/12550583"
    counts["sample_not_complete_proof"] = True
    return counts


def main():
    assert __debug__, "Run with assertions enabled."
    result = {"scope": "degree-five quadratic cofactor endpoint bounds; general i=3 open",
              "symbolic": symbolic(), "sample": sample()}
    target = ROOT/"data/results/verification_i3_quintic_quadratic_endpoint.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
