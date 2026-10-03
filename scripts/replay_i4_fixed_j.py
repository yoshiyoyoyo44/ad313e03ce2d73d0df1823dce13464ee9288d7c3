#!/usr/bin/env python3
"""Separate replay of the finite-j certificate using different arithmetic.

Q4(t) is obtained by stripping 2 and 3 from the four numerator factors.
The denominator 24 then contributes no primes >=5. The generator instead
uses math.comb followed by stripping its small-prime part during the n scan.
"""
from hashlib import sha256
from itertools import product
import json
from math import comb, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'sources/literature_2026-09-30'


def rough(x):
    while x % 2 == 0:
        x //= 2
    while x % 3 == 0:
        x //= 3
    return x


def large_numerator_part(t):
    return prod(rough(t-r) for r in (0,1,2,3))


def primes(cap):
    marks = bytearray([1])*(cap+1)
    marks[:2] = b'\0\0'
    p = 2
    while p*p <= cap:
        if marks[p]:
            marks[p*p::p] = b'\0'*((cap-p*p)//p+1)
        p += 1
    return [p for p in range(5,cap+1) if marks[p]]


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    source = json.loads((ROOT/'data/certificates/known_bridge_and_i4_fixed_j_2026-09-30.json').read_text())
    item = source['i4_fixed_j']
    J,N = item['j_upper'],item['n_upper']
    ps = primes(J)
    lookup = {}
    total = 0
    max_q = 0
    for j in range(5,J+1):
        q = large_numerator_part(j)
        assert q == rough(comb(j,4))
        max_q = max(max_q,q)
        remainder = q
        powers = []
        for p in ps:
            if remainder % p:
                continue
            group = [1]
            while remainder % p == 0:
                remainder //= p
                group.append(group[-1]*p)
            powers.append(group)
        assert remainder == 1
        ds = [prod(xs) for xs in product(*powers)]
        assert len(set(ds)) == len(ds)
        total += len(ds)
        for d in ds:
            if d > 1:
                lookup.setdefault(d,set()).add(j)
    assert total == item['all_divisors_generated']
    assert len(lookup) == item['distinct_large_divisors']
    assert max_q == int(item['max_Q4_j'])
    assert (N-1)*(N-2)*(N-3) <= 6*N*max_q
    assert N*(N-1)*(N-2) > 6*(N+1)*max_q

    expected = {(r['n'],r['j']):r for r in item['records']}
    actual = set()
    hits = 0
    for n in range(10,N+1):
        q = large_numerator_part(n)
        assert q*6*n >= (n-1)*(n-2)*(n-3)
        assert q*q > n*(n-1)*(n-2)*(n-3)//24
        js = lookup.get(q,set())
        hits += bool(js)
        for j in js:
            if j > n//2:
                continue
            actual.add((n,j))
            record = expected[n,j]
            p = record['common_prime']
            assert p in ps
            assert comb(n,4) % p == 0 and comb(n,j) % p == 0
    assert actual == set(expected)
    assert hits == item['n_hits_before_j_range_filter']
    assert len(actual) == item['bridge_candidates']
    for name,digest in source['source_sha256'].items():
        assert sha256((SOURCES/name).read_bytes()).hexdigest() == digest
    # The sole bridge survivor has an upper Kummer obstruction at p=5.
    assert actual == {(57,22)}
    assert 57 % 5 >= 22 % 5
    assert 57 % 25 < 22 % 25
    result = dict(status='passed',j_upper=J,n_upper=N,
                  scanned_n=N-9,all_divisors=total,
                  sole_bridge_candidate=[57,22],common_prime=5,
                  upper_Kummer_modulus=25,
                  theorem_dependency='Elementary Legendre valuation bound; no EEES theorem required for fixed j.')
    (ROOT/'data/results/verification_i4_fixed_j.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
