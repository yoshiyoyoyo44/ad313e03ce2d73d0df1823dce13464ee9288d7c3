#!/usr/bin/env python3
"""Exact EEES exception audit and the all-n i=4, 5<=j<=1000 region.

The i=4 finite-j infinite tail uses an elementary Legendre valuation bound.
The separate known near-diagonal theorem depends on published EEES78; this
script does not independently reproduce the proof of EEES78.
Only Python's standard library is required. Run without python -O.
"""
from collections import defaultdict
from hashlib import sha256
import json
from math import comb, gcd, isqrt, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'sources/literature_2026-09-30'
EXCEPTIONS = [(8,3), (9,4), (10,5), (12,5), (21,7), (21,8),
              (30,7), (33,13), (33,14), (36,13), (36,17), (56,13)]


def factor(n):
    result = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            result[p] = result.get(p, 0)+1
            n //= p
        p += 1
    if n > 1:
        result[n] = 1
    return result


def q4(n):
    q = comb(n, 4)
    while q % 2 == 0:
        q //= 2
    while q % 3 == 0:
        q //= 3
    return q


def divisors(factors):
    ds = [1]
    for p,e in sorted(factors.items()):
        previous = ds[:]
        power = 1
        for _ in range(e):
            power *= p
            ds.extend(d*power for d in previous)
    return ds


def exception_audit():
    records = []
    for n,i in EXCEPTIONS:
        A = comb(n,i)
        factors = factor(A)
        v = prod(p**e for p,e in factors.items() if p >= i)
        u = A//v
        assert u > v and u*v == A and gcd(u,v) == 1
        js = []
        for j in range(i+1,n//2+1):
            D = gcd(A,comb(n,j))
            p = max(factor(D))
            assert p >= i and factor(p) == {p:1}
            assert A % p == 0 and comb(n,j) % p == 0
            js.append(dict(j=j, common_prime=p, common_gcd=str(D)))
        records.append(dict(n=n,i=i,A=str(A),u=str(u),v=str(v),witnesses=js))
    assert sum(len(r['witnesses']) for r in records) == 41
    return records


def fixed_j_audit(J=1000):
    # Factors of C(j,4) >=5 can be computed from j,j-1,j-2,j-3.
    # The denominator 24 contains no such prime.
    index = defaultdict(list)
    qjs = []
    divisor_count = 0
    for j in range(5,J+1):
        fs = defaultdict(int)
        for r in range(4):
            for p,e in factor(j-r).items():
                if p >= 5:
                    fs[p] += e
        q = prod(p**e for p,e in fs.items())
        assert q == q4(j)
        ds = divisors(fs)
        assert len(ds) == prod(e+1 for e in fs.values())
        assert len(set(ds)) == len(ds)
        assert all(q % d == 0 for d in ds)
        divisor_count += len(ds)
        for d in ds:
            if d > 1:
                index[d].append(j)
        qjs.append(q)

    # Legendre: the p=2 layers e=1,2 vanish, and every other layer is
    # at most one. Hence 2^v2(C(n,4))<=n/4 and 3^v3(C(n,4))<=n.
    # Q4(n)>=4*C(n,4)/n^2=(n-1)(n-2)(n-3)/(6*n).
    # If Q4(n) divides Q4(j), it cannot exceed max Q4(j).
    largest_q = max(qjs)
    lo,hi = 3,J*J
    assert (hi-1)*(hi-2)*(hi-3) > 6*hi*largest_q
    while lo < hi:
        middle = (lo+hi+1)//2
        if (middle-1)*(middle-2)*(middle-3) <= 6*middle*largest_q:
            lo = middle
        else:
            hi = middle-1
    N = lo
    assert (N-1)*(N-2)*(N-3) <= 6*N*largest_q
    assert N*(N-1)*(N-2) > 6*(N+1)*largest_q

    candidates = []
    n_hits = 0
    square_theorem_checks = 0
    for n in range(10,N+1):
        A = comb(n,4)
        q = q4(n)
        assert q*n*n >= 4*A
        # This finite scan incidentally rechecks the EEES inequality for
        # every n in the finite region. The infinite tail uses only
        # the elementary Legendre bound above.
        assert q*q > A
        square_theorem_checks += 1
        js = index.get(q,())
        if js:
            n_hits += 1
        for j in js:
            if 2*j > n:
                continue
            assert q4(j) % q == 0
            D = gcd(A,comb(n,j))
            eligible = sorted({p for r in range(4) for p in factor(n-r) if p>=5})
            p = next(p for p in eligible if D % p == 0)
            assert A % p == 0 and comb(n,j) % p == 0
            candidates.append(dict(n=n,j=j,large_part=str(q),common_prime=p,
                                   common_gcd=str(D)))
    return dict(i=4,j_lower=5,j_upper=J,n_upper=N,
                tail_dependency='Elementary Legendre bounds only; no EEES theorem.',
                max_Q4_j=str(largest_q),C_N_4=str(comb(N,4)),
                C_N_plus_1_4=str(comb(N+1,4)),
                tail_comparison_at_N=[str((N-1)*(N-2)*(N-3)),str(6*N*largest_q)],
                tail_comparison_at_N_plus_1=[str(N*(N-1)*(N-2)),str(6*(N+1)*largest_q)],
                all_divisors_generated=divisor_count,
                distinct_large_divisors=len(index),
                n_hits_before_j_range_filter=n_hits,
                finite_EEES_inequality_checks=square_theorem_checks,
                bridge_candidates=len(candidates),
                records=candidates)


def bridge_algebra_audit():
    cases = 0
    for n in range(4,81):
        for i in range(1,min(12,n//2)):
            A = comb(n,i)
            for j in range(i+1,n//2+1):
                B = comb(n,j)
                assert A*comb(n-i,j-i) == B*comb(j,i)
                assert A*comb(n-i,j) == B*comb(n-j,i)
                a = A//gcd(A,B)
                assert comb(j,i) % a == 0
                assert comb(n-j,i) % a == 0
                cases += 1
    return cases


def small_j_endpoints():
    records = []
    for i in range(3,35):
        j=i+1
        while comb(j,i)**2 < comb(2*j,i):
            j += 1
        assert comb(j-1,i)**2 < comb(2*(j-1),i)
        assert comb(j,i)**2 >= comb(2*j,i)
        records.append(dict(i=i,j_upper=j-1))
    return records


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    out = dict(
        scope='EEES78 exception audit, known bridge connection, and i=4 all-n finite-j region; not a solution of the general conjecture.',
        dependency='The known j<=3i/2 connection invokes EEES78. The i=4 finite-j theorem uses elementary Legendre bounds for its tail.',
        exception_pairs=exception_audit(),
        bridge_algebra_cases=bridge_algebra_audit(),
        known_small_j_endpoints=small_j_endpoints(),
        i4_fixed_j=fixed_j_audit(),
    )
    out['source_sha256'] = {p.name:sha256(p.read_bytes()).hexdigest()
                            for p in sorted(SOURCES.glob('1978-*.pdf'))}
    path = ROOT/'data/certificates/known_bridge_and_i4_fixed_j_2026-09-30.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    summary = dict(exception_pairs=len(out['exception_pairs']),
                   exception_j_cases=41,
                   bridge_algebra_cases=out['bridge_algebra_cases'],
                   i4_fixed_j={k:v for k,v in out['i4_fixed_j'].items() if k!='records'},
                   source_sha256=out['source_sha256'])
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
