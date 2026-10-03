"""Replay the complete exclusion of the classified quintic i=3 family.

Only standard Python is needed. Polynomial lists use ascending powers.
The proof of the coefficient-unbounded classification is in the research note.
"""
from math import comb, isqrt
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
F = [2, 125, 3750, 35000, 125000, 150000]
J = [2, 105, 1770, 11400, 31000, 30000]


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def scale(a, c):
    return trim([c*x for x in a])


def evaluate(a, x):
    v = 0
    for c in reversed(a):
        v = v*x+c
    return v


def remainder(a, b, q):
    a = trim([x % q for x in a])
    inverse = pow(b[-1] % q, -1, q)
    while a != [0] and len(a) >= len(b):
        shift = len(a)-len(b)
        c = a[-1]*inverse % q
        for i, x in enumerate(b):
            a[i+shift] = (a[i+shift]-c*x) % q
        a = trim(a)
    return a


def polynomial_power(a, n, modulus, q):
    result = [1]
    while n:
        if n & 1:
            result = remainder(mul(result, a), modulus, q)
        a = remainder(mul(a, a), modulus, q)
        n //= 2
    return result


def shifted_power(c, n):
    return [comb(n, i)*c**(n-i) for i in range(n+1)]


def main():
    # Integer Bezout identity: no odd gcd factor except a single 3.
    A = [107, 3550, 42200, 169000, 210000]
    B = [-95, -5250, -105000, -635000, -1050000]
    assert add(mul(A, F), mul(B, J)) == [24]
    k = [21, 354, 2280, 6200, 6000]
    assert add(J, [-2]) == mul([0, 5], k)
    assert add(F, [-2]) == mul(mul([0, 125], [1, 10, 20]), [1, 20, 60])
    assert {y for y in range(25) if evaluate(k, y) % 25 == 0} == {6}
    assert [c % 625 for c in F] == [2, 125, 0, 0, 0, 0]

    # Entire M=3 branch: the integer fifth power lies strictly between neighbours.
    g = [4, 25, 75, 70, 25, 3]
    assert [c*10**i for i, c in enumerate(g)] == scale(F, 2)
    lower = add(g, scale(shifted_power(1, 5), -3))
    upper = add(scale(shifted_power(2, 5), 3), scale(g, -1))
    assert lower == [1, 10, 45, 40, 10] and upper == [92, 215, 165, 50, 5]
    assert all(c > 0 for c in lower+upper)
    assert pow(2, 20, 25) == 1 and pow(2, 10, 25) != 1 and pow(2, 4, 25) != 1
    assert [u for u in range(20) if 3*pow(2, u, 25) % 25 == 2] == [14]

    # Necessary exponent for the M=1 counterexample branch.
    assert pow(2, 500, 625) == 1
    assert pow(2, 250, 625) != 1 and pow(2, 100, 625) != 1
    assert pow(2, 101, 625) == 127
    assert [u for u in range(500) if pow(2, u, 625) == 127] == [101]

    q = 28001
    assert all(q % d for d in range(2, isqrt(q)+1))
    target = 18059
    assert pow(2, 500, q) == 1 and pow(2, 101, q) == target
    p = [9944, 125, 3750, 6999, 12996, 9995]
    r = [7394, -5767, 5050, 11650, -11135]
    c = [5742, 797, 2379, -7364]
    d = [8558, -2780, 12185, -1072, -3429]
    assert [a % q for a in add(F, [-target])] == p
    actual = remainder(add(polynomial_power([0, 1], q, p, q), [0, -1]), p, q)
    assert actual == [a % q for a in r]
    assert trim([a % q for a in add(mul(c, p), mul(d, r))]) == [1]
    roots = [y for y in range(q) if evaluate(F, y) % q == target]
    assert roots == []

    certificate = {'modulus': q, 'target': target, 'polynomial': p,
                   'frobenius_remainder': r, 'bezout_C': c, 'bezout_D': d,
                   'coefficient_order': 'ascending', 'integer_gcd_bound': 24,
                   'M3_lower_difference': lower, 'M3_upper_difference': upper}
    raw = (json.dumps(certificate, indent=2)+'\n').encode()
    (ROOT/'data/certificates/i3_quintic_closeout_2026-09-30.json').write_bytes(raw)
    result = {'status': 'passed', 'scope': 'All positive integer evaluations of the classified quintic family share an odd prime in the two binomial coefficients; general i=3 remains open.',
              'certificate_sha256': hashlib.sha256(raw).hexdigest(),
              'M3_entire_nonnegative_integer_branch_excluded': True,
              'M1_counterexample_branch_excluded': True,
              'M1_unconstrained_integer_points_computed': False,
              'M1_necessary_exponent_residue': 101, 'M1_exponent_modulus': 500,
              'modular_residues_exhausted': q, 'modular_roots': roots,
              'independent_polynomial_certificate_verified': True,
              'new_digit_degree_bound': 5, 'complete_problem_solution': False,
              'remaining_indices': 28}
    (ROOT/'data/results/verification_i3_quintic_closeout.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
