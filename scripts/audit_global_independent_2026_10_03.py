"""Independent exact diagnostics for the October 3 global audit.

The all-degree weighted-division argument is a paper proof. The CRT examples
are not counterexamples to Erdos 699: they test only selected hypotheses.
"""
from fractions import Fraction
from itertools import product
from math import comb, gcd, prod
from pathlib import Path
import json


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def multiply(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def evaluate(a, x):
    result = 0
    for c in reversed(a):
        result = result*x+c
    return result


def weighted_norm(a, beta):
    return sum(abs(c)*beta**k for k, c in enumerate(a))


def reciprocal_remainder(a, b, beta):
    """Divide B* by -A*, checking each weighted norm exactly."""
    m = len(a)-1
    divisor = [-c for c in reversed(a)]
    assert divisor[-1] == 1
    work = list(reversed(b))
    while work != [0] and len(work)-1 >= m:
        before = weighted_norm(work, beta)
        shift = len(work)-1-m
        leading = work[-1]
        for k, c in enumerate(divisor):
            work[k+shift] -= leading*c
        work = trim(work)
        assert weighted_norm(work, beta) <= before
    return work


def valuation(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def digit_sum(n, base):
    answer = 0
    while n:
        answer += n % base
        n //= base
    return answer


def crt(congruences):
    x, modulus = 0, 1
    for residue, q in congruences:
        assert gcd(modulus, q) == 1
        x += modulus*((residue-x)*pow(modulus, -1, q) % q)
        modulus *= q
        x %= modulus
    return x, modulus


def audit_weighted_transfer():
    cases = divisibility_samples = 0
    for s in range(4):
        t = s+1
        for upper in ((1, 1), (2, 1), (1, 2), (1, 0, 1), (1, 0, 0, 1)):
            f = [s, *upper]
            a = [-1, *upper]
            m = len(f)-1
            beta = Fraction(1)
            while sum(Fraction(v)/beta**k for k, v in enumerate(upper, 1)) > 1:
                beta += Fraction(1, 8)
            for u in range(s+1):
                for lower in product(*(range(c+1) for c in upper)):
                    j = trim([u, *lower])
                    if not any(lower) or tuple(lower) == upper:
                        continue
                    delta = evaluate(j, 1/beta)-u
                    assert 0 < delta < 1
                    for c in (1, 6, 30):
                        b = [c]
                        for v in range(t+1):
                            factor = list(j)
                            factor[0] -= v
                            b = multiply(b, factor)
                        d = len(b)-1
                        bound = c*beta**d*prod(abs(u-v)+delta for v in range(t+1))
                        assert bound >= weighted_norm(list(reversed(b)), beta)
                        if d >= m:
                            remainder = reciprocal_remainder(a, b, beta)
                            assert remainder != [0]
                            assert weighted_norm(remainder, beta) <= bound
                        for q in range(2, 81):
                            aq = evaluate(a, q)
                            bq = evaluate(b, q)
                            if bq % aq == 0:
                                assert q <= 2*bound
                                divisibility_samples += 1
                        cases += 1
    # A sparse high-degree example: the new bound is strictly smaller.
    s, t, u, c, m = 2, 3, 0, 30, 100
    beta = Fraction(133, 128)
    assert 1/beta+1/beta**m <= 1
    delta = beta**(-50)
    new = 2*c*beta**200*prod(abs(u-v)+delta for v in range(t+1))
    old = 2*c*prod(4+v for v in range(t+1))*2**(t*m+1)
    assert new < old
    return {'polynomial_cases': cases,
            'integer_divisibility_samples': divisibility_samples,
            'sparse_example_old_bound': str(old),
            'sparse_example_new_bound': str(new),
            'sparse_example_new_bound_ceiling': -(-new.numerator//new.denominator),
            'universal_statement': 'paper proof; diagnostics use rational beta and exact arithmetic'}


def audit_structural_unboundedness():
    # Small exponents keep this diagnostic cheap; the CRT proof allows
    # the research thresholds u=112, v=100 with no exponent upper bound.
    u, v = 5, 3
    primes = (7, 11, 13, 17, 19, 23, 29, 31)
    pproduct = prod(primes)
    n, modulus = crt(((1, 2**u), (0, 3**v), (2+pproduct, pproduct**2)))
    assert n % 72 == 9
    assert valuation(n-1, 2) >= u and valuation(n, 3) >= v
    assert all(valuation(n-2, p) == 1 for p in primes)
    assert max(range(5), key=lambda r: valuation(n-r, 2)) == 1
    assert max(range(5), key=lambda r: valuation(n-r, 3)) == 0
    C, _ = crt(((0, 2**u), (1, 3**v), (-9, 49)))
    if C == 0:
        C = 49*2**u*3**v
    phi = 2**u*3**(v-1)
    heights = []
    for k in (1, 2, 3):
        m = k*phi
        nn = 7**m-C
        assert nn > 0 and nn % 72 == 9
        assert valuation(nn-1, 2) >= u and valuation(nn, 3) >= v
        assert valuation(nn-2, 7) == 1
        h = digit_sum(nn, 7)
        assert h == 6*m-digit_sum(C-1, 7)
        heights.append({'m': m, 'H': h})
    assert heights[0]['H'] < heights[1]['H'] < heights[2]['H']
    return {'prescribed_primes_in_row2': list(primes),
            'crt_n': str(n), 'crt_modulus': str(modulus),
            'fixed_C': C, 'digit_height_samples': heights,
            'scope': 'support and valuation hypotheses only; no j constructed and no Erdos counterexample claimed'}


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    result = {'status': 'PASS',
              'root_weighted_transfer': audit_weighted_transfer(),
              'structural_unboundedness': audit_structural_unboundedness()}
    target = Path(__file__).resolve().parents[1]/'data/results/verification_global_independent_2026-10-03.json'
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'status': 'PASS',
                      'polynomial_cases': result['root_weighted_transfer']['polynomial_cases'],
                      'integer_divisibility_samples': result['root_weighted_transfer']['integer_divisibility_samples'],
                      'sparse_example_new_bound_ceiling': result['root_weighted_transfer']['sparse_example_new_bound_ceiling'],
                      'scope': 'all-degree proof is in the new note; no new fully solved index'}))


if __name__ == '__main__':
    main()
