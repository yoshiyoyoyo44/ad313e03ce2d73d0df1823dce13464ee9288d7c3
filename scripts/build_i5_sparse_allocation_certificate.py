"""Build or resume the 880 i=5 allocation certificates.

Default: reuse completed records in the saved certificate. --fresh rebuilds
them using exact rational nullspaces; it may take many minutes. Generation
alone is not verification: run audit_i5_sparse_allocation.py afterwards.
"""
import argparse
from functools import reduce
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parent.parent
S, U = sp.symbols('S U')
N = 10**87
DESTINATION = ROOT/'data/certificates/i5_sparse_allocation_2026-10-03.json'


def normalize(expr):
    pp = sp.Poly(expr, S, U, domain=sp.QQ)
    _, pp = pp.clear_denoms()
    _, pp = pp.primitive()
    return (-pp if pp.LC() < 0 else pp).as_expr()


def terms(expr):
    return [[int(a), int(b), int(c)] for (a, b), c in sp.Poly(expr, S, U).terms()]


def make_record(active, degree, mults):
    monomials = [(t-b, b) for t in range(degree, -1, -1) for b in range(t+1)]
    entries = []
    for s, us, m in zip((2, 3, 4), active, mults):
        for u in us:
            for total in range(m):
                for i in range(total+1):
                    k = total-i
                    entries.append([comb(a, i)*comb(b, k)*s**(a-i)*u**(b-k)
                                    if a >= i and b >= k else 0 for a, b in monomials])
    null = DomainMatrix.from_Matrix(sp.Matrix(entries)).nullspace().to_Matrix()
    basis = [normalize(sum(c*S**a*U**b for c, (a, b) in zip(null.row(i), monomials)))
             for i in range(null.rows)]
    assert len(basis) >= 3
    common = normalize(reduce(sp.gcd, basis))
    reduced = [normalize(sp.cancel(f/common)) for f in basis]
    p = reduced[0]
    for t in range(1, 257):
        q = normalize(sum(t**i*f for i, f in enumerate(reduced[1:])))
        if sp.total_degree(sp.gcd(p, q)) == 0:
            break
    else:
        raise RuntimeError(('no relatively prime pair', active))
    pp, qq = normalize(common*p), normalize(common*q)
    resultant = sp.Poly(sp.resultant(sp.cancel(pp/common), sp.cancel(qq/common), U), S, domain=sp.QQ)
    assert not resultant.is_zero
    _, resultant = resultant.clear_denoms()
    _, resultant = resultant.primitive()
    if resultant.LC() < 0:
        resultant = -resultant
    coefficients = resultant.all_coeffs()
    bound = 1+max([int(sp.ceiling(abs(c/coefficients[0]))) for c in coefficients[1:]]+[0])
    normp = sum(abs(int(c)) for c in sp.Poly(pp, S, U).coeffs())
    normq = sum(abs(int(c)) for c in sp.Poly(qq, S, U).coeffs())
    capacity = 2*(normp**2+normq**2)*120**(2*max(mults))
    gap = 2*(sum(mults)-degree)
    assert gap > 0 and bound < N and capacity < N**gap
    return {'active': active, 'P': terms(pp), 'Q': terms(qq), 'common_factor': terms(common),
            'resultant': [str(c) for c in coefficients], 'resultant_root_bound': str(bound),
            'capacity_n_power_bound': str(capacity), 'row_multiplicities': mults,
            'degree': degree, 'n_power_gap': gap}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fresh', action='store_true', help='recompute all records instead of resuming')
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit('Assertions must be enabled: do not use python -O.')
    known = {}
    if DESTINATION.exists() and not args.fresh:
        for record in json.loads(DESTINATION.read_text(encoding='utf-8'))['records']:
            known[tuple(tuple(us) for us in record['active'])] = record
    all_keys = []
    for counts in product((2, 3), (2, 3, 4), (2, 3, 4, 5)):
        if sum(counts) > 8:
            continue
        # Three dimensions remain after imposing all homogeneous Taylor
        # constraints. We need two polynomials after removing their common part.
        degree, mults = min((sum(m)-1, m) for m in product(range(1, 9), repeat=3)
                            if sum(m)*(sum(m)+1)//2-sum(c*v*(v+1)//2 for c, v in zip(counts, m)) >= 3)
        for active in product(*[list(combinations(range(s+1), c)) for s, c in zip((2, 3, 4), counts)]):
            all_keys.append(active)
            if active in known:
                continue
            known[active] = make_record(active, degree, mults)
            if len(known) % 10 == 0:
                print(f'Generated {len(known)} records', flush=True)
                DESTINATION.write_text(json.dumps({'configuration_count': len(known), 'records': list(known.values())}, indent=2)+'\n', encoding='utf-8')
    assert len(all_keys) == 880 and len(set(all_keys)) == 880 and set(known) == set(all_keys)
    DESTINATION.write_text(json.dumps({'configuration_count': 880, 'records': list(known.values())}, indent=2)+'\n', encoding='utf-8')
    print('Saved 880 records. Run audit_i5_sparse_allocation.py for independent replay.')


if __name__ == '__main__':
    main()
