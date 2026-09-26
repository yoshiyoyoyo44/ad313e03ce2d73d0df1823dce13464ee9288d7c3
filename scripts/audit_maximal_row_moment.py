"""Exact audit of the maximal-row moment bound and its exponent relaxation.

The all-n implication is proved in the accompanying note. Integer comparisons
certify its constants; two enumerations count the retained row sets. No LP
solver or third-party package is needed to replay the rational witnesses.
"""
from fractions import Fraction as F
from math import comb, factorial, gcd, isqrt, prod
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
N = 10**87
INDICES = [27, 30, 33]


def primes_below(i):
    return [p for p in range(2, i) if all(p % q for q in range(2, isqrt(p) + 1))]


def valuation(value, p):
    exponent = 0
    while value % p == 0:
        value //= p
        exponent += 1
    return exponent


def enumerate_sets(i, m, cap):
    def visit(prefix, start, left, total):
        if left == 0:
            yield list(prefix)
            return
        for r in range(start, i - left + 1):
            # Smallest completion r, r+1, ..., r+left-1.
            if total + left * r + left * (left - 1) // 2 > cap:
                break
            yield from visit((*prefix, r), r + 1, left - 1, total + r)
    return list(visit((), 0, m, 0))


def subset_sum_counts(i, m):
    # Independent coefficient extraction from product_r (1 + y*x^r).
    counts = [dict() for _ in range(m + 1)]
    counts[0][0] = 1
    for r in range(i):
        for k in range(min(m, r + 1), 0, -1):
            for total, number in list(counts[k - 1].items()):
                counts[k][total + r] = counts[k].get(total + r, 0) + number
    assert sum(counts[m].values()) == comb(i, m)
    return counts[m]


def audit_parameters(i):
    h = i - 1
    ps = primes_below(i)
    m = len(ps)
    c = i if any(i % p == 0 for p in ps) else 1
    b0 = (2 * h + 2) // 3
    d0, S0 = 3 * b0 - h, b0 * (b0 + 1) // 2
    D0 = 3 * S0 - d0 * (i - m)
    beta = F(D0, d0)
    assert 0 <= beta < 1
    # Bernoulli gives (n/(n-h))^(i*d0) < 2 for every n >= N.
    assert N > 2 * i * d0 * h
    C0 = 2 * F(factorial(i), c)**d0 / 4**S0
    # Stronger than distinctness: each p^E_p > h and product(a_p) < n-h.
    assert (N - h)**d0 > C0 * h**d0 * N**D0
    # (n-h)^d0/n^D0 has positive derivative for n>h.
    assert d0 > D0 >= 0

    k = i - m
    b = k - 1
    d = 2 * b
    S = b * (b + 1) // 2
    H = i * h // 2 - k * (k - 1)
    assert 0 < b <= h < d
    assert N > 2 * i * d * h
    assert i * h // 2 + 2 * S - d * (i - m) == H
    cells = 0
    for s in range(i):
        for u in range(s + 1):
            assert s + max(0, b - u) + max(0, b - (s - u)) >= d
            cells += 1
    assert sum(range(i)) == i * h // 2
    assert sum(max(0, b - u) for u in range(i)) == S
    C = 2 * F(factorial(i), c)**d / 4**S
    allowance = 0
    while N**(allowance + 1) <= C:
        allowance += 1
    assert N**allowance <= C < N**(allowance + 1)
    tail_power = 1
    while 10**tail_power <= C:
        tail_power += 1
    assert 10**(tail_power - 1) <= C < 10**tail_power
    cap = H + allowance
    sets = enumerate_sets(i, m, cap)
    counts = subset_sum_counts(i, m)
    assert len(sets) == sum(v for s, v in counts.items() if s <= cap)
    assert len({tuple(rs) for rs in sets}) == len(sets)
    assert all(len(rs) == m and rs == sorted(set(rs)) and sum(rs) <= cap for rs in sets)
    eventual = [rs for rs in sets if sum(rs) <= H]
    assert len(eventual) == sum(v for s, v in counts.items() if s <= H)
    return dict(i=i, m=m, c=c, beta=str(beta), b=b, d=d, S=S, H=H,
                C_numerator=str(C.numerator), C_denominator=str(C.denominator),
                n_lower=N, row_sum_upper=cap, original_row_sets=comb(i, m),
                retained_row_sets=len(sets), eventual_n_power=tail_power,
                eventual_row_sum_upper=H, eventual_row_sets=len(eventual),
                weight_cells_checked=cells,
                retained_sum_distribution={str(s): counts[s] for s in sorted(counts) if s <= cap}), sets


def check_relaxation():
    cert = json.loads((ROOT / 'data/certificates/maximal_row_relaxation_2026-09-27.json')
                      .read_text(encoding='utf-8'))
    assert cert['schema'] == 1 and [r['i'] for r in cert['rows']] == INDICES
    summaries = []
    for row in cert['rows']:
        i = row['i']
        m = len(primes_below(i))
        assert row['maximal_rows'] == list(range(m))
        assert row['cell_exponent'] == '1/2'
        occupied = [tuple(c) for c in row['occupied_cells']]
        assert len(occupied) == len(set(occupied)) == 2 * (i - m)
        assert all(0 <= u <= s < i for s, u in occupied)
        values = {(s, u): F(1, 2) for s, u in occupied}
        for s in range(i):
            assert sum(x for (r, u), x in values.items() if r == s) == int(s >= m)
        for u in range(i):
            assert sum(x for (r, v), x in values.items() if v == u) <= 1
            assert sum(x for (r, v), x in values.items() if r - v == u) <= 1
        assert all(x + y <= 1 for c, x in values.items() for e, y in values.items() if c != e)
        b0 = (2 * (i - 1) + 2) // 3
        d0, S0 = 3 * b0 - i + 1, b0 * (b0 + 1) // 2
        assert d0 * (i - m) <= 3 * S0
        H = i * (i - 1) // 2 - (i - m) * (i - m - 1)
        assert sum(row['maximal_rows']) <= H
        summaries.append(dict(i=i, occupied_cells=len(occupied), cofactor_exponent=0,
                              Q_exponent=i-m, pair_exponent_upper=1,
                              feasible=True, integer_counterexample=False))
    return summaries


def arithmetic_diagnostics():
    rows_checked = cells_checked = 0
    for i in INDICES:
        ps = primes_below(i)
        m = len(ps)
        h = i - 1
        b = i - m - 1
        d, S = 2 * b, b * (b + 1) // 2
        for n in range(2 * i + 2, 601):
            selected = [max(range(i), key=lambda r: (valuation(n-r, p), -(n-r))) for p in ps]
            if len(set(selected)) != m:
                continue
            cofactors = [(n-r)//p**valuation(n-r, p) for p, r in zip(ps, selected)]
            Q = comb(n, i)
            for p in ps:
                while Q % p == 0:
                    Q //= p
            qs = [gcd(Q, n-s) for s in range(i)]
            assert prod(qs) == Q
            assert all(qs[r] <= a for r, a in zip(selected, cofactors))
            assert Q * factorial(i) * n**m >= i * prod(cofactors) * (n-h)**i
            rows_checked += 1
            for j in sorted({i+1, n//3, n//2}):
                if not i < j <= n//2:
                    continue
                B = {(s, u): gcd(qs[s], j-u) for s in range(i) for u in range(s+1)}
                T = prod(B.values())
                weighted = prod(v**(s+max(0,b-u)+max(0,b-s+u)) for (s,u),v in B.items())
                upper = n**(i*h//2-sum(selected)+2*S) * prod(a**r for a,r in zip(cofactors,selected))
                assert T**d <= weighted
                assert 4**S * weighted <= upper
                cells_checked += len(B)
    assert rows_checked > 0
    return dict(distinct_row_examples=rows_checked, cell_occurrences=cells_checked,
                scope='Finite diagnostics of unconditional inequalities; not an all-n proof')


def main():
    if not __debug__:
        raise RuntimeError('Assertions are required; do not use -O.')
    rows, cases = [], []
    for i in INDICES:
        row, sets = audit_parameters(i)
        rows.append(row)
        cases.append(dict(i=i, row_sum_upper=row['row_sum_upper'], row_sets=sets))
        print(f"i={i}: {row['original_row_sets']} -> {len(sets)} row sets; "
              f"sum <= {row['row_sum_upper']}", flush=True)
    assert [r['row_sum_upper'] for r in rows] == [54, 67, 81]
    assert [r['retained_row_sets'] for r in rows] == [1410, 3887, 9950]
    assert [r['eventual_row_sets'] for r in rows] == [97, 139, 195]
    payload = (json.dumps(dict(schema=1, n_lower=N, rows=cases), separators=(',', ':'))+'\n').encode()
    case_path = ROOT / 'data/cases/maximal_row_sets_2026-09-27.json.gz'
    case_path.write_bytes(gzip.compress(payload, mtime=0))
    assert gzip.decompress(case_path.read_bytes()) == payload
    result = dict(status='PASS', theorem_scope='Necessary conditions for i=27,30,33 and n>=10^87',
                  new_fully_solved_indices=[], rows=rows,
                  row_sets_uncompressed_sha256=hashlib.sha256(payload).hexdigest(),
                  rational_relaxation=check_relaxation(), diagnostics=arithmetic_diagnostics(),
                  proof='research/general/maximal_row_moment_2026-09-27.md',
                  independent_peer_review=False, formal_lean_verification=False)
    (ROOT / 'data/results/verification_maximal_row_moment.json').write_text(
        json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print('PASS exact constants, independent subset counts, rational witnesses and diagnostics')


if __name__ == '__main__':
    main()
