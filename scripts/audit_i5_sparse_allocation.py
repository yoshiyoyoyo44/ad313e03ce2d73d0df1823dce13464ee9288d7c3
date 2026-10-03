"""Replay exact i=5 certificates for sparse allocations and a method barrier.

The paper proof states all universal dependencies. This does not solve i=5.
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb, prod
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
S, U = sp.symbols('S U')
N = 10**87
CERTIFICATE = ROOT / 'data/certificates/i5_sparse_allocation_2026-10-03.json'


def polynomial(terms):
    assert len({(a, b) for a, b, c in terms}) == len(terms)
    assert all(a >= 0 and b >= 0 and c != 0 for a, b, c in terms)
    return sp.Poly(sum(int(c)*S**a*U**b for a, b, c in terms), S, U, domain=sp.QQ)


def coefficient_at_cell(terms, s, u, i, k):
    return sum(c*comb(a, i)*comb(b, k)*s**(a-i)*u**(b-k)
               for a, b, c in terms if a >= i and b >= k)


def leading_bernstein(terms, degree):
    values = {b: Fraction(c) for a, b, c in terms if a+b == degree}
    return [sum(values.get(k, 0)*Fraction(comb(i, k), comb(degree, k)*2**k)
                for k in range(i+1)) for i in range(degree+1)]


def certify_factor_nonzero(factor):
    pp = sp.Poly(factor, S, U, domain=sp.QQ)
    _, pp = pp.clear_denoms()
    _, pp = pp.primitive()
    if pp.LC() < 0:
        pp = -pp
    terms = [(int(a), int(b), int(c)) for (a, b), c in pp.terms()]
    degree = pp.total_degree()
    if degree == 1:
        a, b, c = pp.coeff_monomial(S), pp.coeff_monomial(U), pp.coeff_monomial(1)
        endpoints = [(a, 6*b+c), (a+b/2, c)]
        signs = [sign for sign in (1, -1)
                 if all(sign*slope >= 0 and sign*(slope*N+intercept) > 0
                        for slope, intercept in endpoints)]
        assert signs, pp
        return {'polynomial': str(pp.as_expr()), 'degree': 1,
                'method': 'linear endpoints on 6<=j<=n/2, n>=10^87'}
    assert degree in (2, 3), ('unhandled common component', pp)
    bs = leading_bernstein(terms, degree)
    sign = 1 if min(bs) > 0 else -1
    assert min(sign*x for x in bs) > 0, pp
    signed_terms = [(a, b, sign*c) for a, b, c in terms]
    lower = [min(leading_bernstein(signed_terms, r)) for r in range(degree+1)]
    shifted = [sum(lower[r]*comb(r, k)*N**(r-k) for r in range(k, degree+1))
               for k in range(degree+1)]
    assert lower[-1] > 0 and min(shifted) >= 0 and shifted[0] > 0
    return {'polynomial': str(pp.as_expr()), 'degree': degree,
            'leading_bernstein': [str(x) for x in bs],
            'signed_lower': [str(x) for x in lower],
            'method': 'positive coefficients after n=10^87+x'}


def normalize_univariate(pp):
    _, pp = pp.clear_denoms()
    _, pp = pp.primitive()
    return pp if pp.LC() > 0 else -pp


def expected_configurations():
    expected = set()
    for counts in product((2, 3), (2, 3, 4), (2, 3, 4, 5)):
        if sum(counts) <= 8:
            expected.update(product(*[list(combinations(range(s+1), count))
                                      for s, count in zip((2, 3, 4), counts)]))
    assert len(expected) == 880
    return expected


def audit_allocation_certificate():
    data = json.loads(CERTIFICATE.read_text(encoding='utf-8'))
    expected = expected_configurations()
    seen = set()
    factors = {}
    max_root_bound = max_capacity = 0
    two_cell_odd_max = 0
    for index, record in enumerate(data['records'], 1):
        active = tuple(tuple(us) for us in record['active'])
        assert active in expected and active not in seen
        seen.add(active)
        mults, degree = record['row_multiplicities'], record['degree']
        assert len(mults) == 3 and min(mults) > 0
        assert N > 4*sum(s*m for s, m in zip((2, 3, 4), mults))
        gap = 2*(sum(mults)-degree)
        assert gap > 0
        p, q, f = (polynomial(record[name]) for name in ('P', 'Q', 'common_factor'))
        assert p.total_degree() <= degree and q.total_degree() <= degree
        for s, us, m in zip((2, 3, 4), active, mults):
            for u in us:
                for total in range(m):
                    for i in range(total+1):
                        k = total-i
                        assert coefficient_at_cell(record['P'], s, u, i, k) == 0
                        assert coefficient_at_cell(record['Q'], s, u, i, k) == 0
        reduced_p, reduced_q = p.exquo(f), q.exquo(f)
        actual = normalize_univariate(sp.Poly(sp.resultant(reduced_p.as_expr(), reduced_q.as_expr(), U), S, domain=sp.QQ))
        supplied = sp.Poly.from_list([int(c) for c in record['resultant']], S, domain=sp.QQ)
        assert actual == supplied and not actual.is_zero
        coeffs = actual.all_coeffs()
        root_bound = 1+max([int(sp.ceiling(abs(c/coeffs[0]))) for c in coeffs[1:]]+[0])
        assert str(root_bound) == record['resultant_root_bound'] and root_bound < N
        for factor, exponent in sp.factor_list(f.as_expr())[1]:
            key = str(sp.Poly(factor, S, U).monic().as_expr())
            if key not in factors:
                factors[key] = certify_factor_nonzero(factor)
        normp = sum(abs(int(c)) for c in p.coeffs())
        normq = sum(abs(int(c)) for c in q.coeffs())
        capacity = 2*(normp**2+normq**2)*120**(2*max(mults))
        supplied_capacity = record.get('capacity_n_power_bound', record.get('capacity_n2_bound'))
        assert str(capacity) == supplied_capacity and capacity < N**gap
        max_root_bound = max(max_root_bound, root_bound)
        max_capacity = max(max_capacity, capacity)
        if all(len(us) == 2 for us in active):
            assert mults == [2, 2, 2] and degree == 5
            two_cell_odd_max = max(two_cell_odd_max, 2*(normp**2+normq**2)*30**4)
        if index % 100 == 0:
            print(f'Replayed {index} allocation certificates', flush=True)
    assert seen == expected and data['configuration_count'] == len(expected)
    assert two_cell_odd_max*10**152 < N**2
    # A single occupied cell gives a small rational zero line, already closed.
    single_cell_upper = 60*(8*60)**4+3
    assert single_cell_upper < N
    return {'configurations': len(seen), 'coverage': 'all t2,t3,t4>=2 with t2+t3+t4<=8',
            'degree_range': sorted({r['degree'] for r in data['records']}),
            'max_resultant_root_bound': str(max_root_bound),
            'max_capacity_constant': str(max_capacity),
            'common_components': list(factors.values()),
            'single_cell_n_upper': single_cell_upper,
            'necessary_active_cell_count': 't2+t3+t4>=9; each tr>=2',
            'odd_universal_omitted_product_lower': 'For every choice of two cells in each heavy row, M2*M3*M4>10^38',
            'odd_two_cell_max_constant': str(two_cell_odd_max),
            'scope': 'paper proof plus exact certificate replay, not a search over counterexamples'}


def audit_all_degree_barrier():
    per_cell = [Fraction(1, 100), Fraction(1, 5), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5)]
    row_sums = [(s+1)*weight for s, weight in enumerate(per_cell)]
    assert row_sums == [Fraction(1, 100), Fraction(2, 5), Fraction(1), Fraction(1), Fraction(1)]
    assert sum(per_cell) == Fraction(149, 150)
    assert all(0 < x <= 1 for x in row_sums)
    x, y = row_sums[:2]
    assert max(x, y) > Fraction(2921, 10000)
    assert x+y > Fraction(1, 3) and x+y < Fraction(3, 5)
    assert 6*x+5*y == Fraction(103, 50) < 3
    assert 9*x+4*y == Fraction(169, 100) < 4
    assert y-x > Fraction(9, 400)
    return {'per_cell_weights_by_row': [str(x) for x in per_cell],
            'row_exponents': [str(x) for x in row_sums],
            'restriction_degree_multiplier': '149/150',
            'universal_formula': 'weighted local orders <= d - (99/100)h0 - (3/5)h1 - dG/150',
            'compatible_max_lower_exponent': '2921/10000',
            'compatible_product_lower_exponent': '1/3',
            'scope': 'formal exponent weights for all fixed polynomials using total-degree capacity; no integer or full-Kummer counterexample is constructed'}


def valuation(n, p):
    assert n > 0
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def minimum_exponent(lhs, constant, base, multiplier):
    # The excluded exponents are checked by integer cross multiplication.
    assert constant > 0
    numerator, denominator = constant.numerator, constant.denominator
    e = 0
    while lhs*denominator >= numerator*base**(multiplier*e):
        e += 1
    assert lhs*denominator >= numerator*base**(multiplier*(e-1))
    assert lhs*denominator < numerator*base**(multiplier*e)
    return e


def audit_prime5_lift():
    parent = json.loads((ROOT/'data/results/verification_i5_multiplicity_frontier.json').read_text(encoding='utf-8'))
    records = {r['name']: r for r in parent['certificates']}
    baseline = records['support_01_baseline_tight_constants']
    mixed = records['support_01_new_mixed_bound']
    assert baseline['row_targets'] == [6, 5, 6, 6, 6]
    assert mixed['row_targets'] == [9, 4, 5, 3, 4]
    assert Fraction(baseline['evaluation_constant']) == Fraction(1, 4096)
    assert Fraction(mixed['evaluation_constant']) == Fraction(9, 1024)
    # The odd surviving class has full small-prime denominators (1,6,1)
    # on rows 2,3,4. The period 1800 covers 72 and 25 jointly.
    for n in range(9, 1800, 72):
        small_parts = [2**valuation(n-s, 2)*3**valuation(n-s, 3) for s in (2, 3, 4)]
        assert small_parts == [1, 6, 1]
    k6 = 2*Fraction(baseline['evaluation_constant'])*6**6
    k9 = 2*Fraction(mixed['evaluation_constant'])*6**3
    assert k6 == Fraction(729, 32) and k9 == Fraction(243, 64)
    # A direct diagnostic of the higher base-5 digit implication. The paper
    # gives its universal no-carry proof; these cases do not replace it.
    samples = 0
    for n in range(12, 401):
        r = n % 5
        e = valuation(n-r, 5)
        assert valuation(comb(n, 5), 5) == e-1
        if e < 2:
            continue
        for j in range(6, n//2+1):
            if comb(n, j) % 5:
                assert j % 5**e <= r
                samples += 1
    assert samples > 0
    cases = []
    for r in range(5):
        c6 = k6*5**baseline['row_targets'][r]
        c9 = k9*5**mixed['row_targets'][r]
        # n^5 < c9*3^(9F), (n-1)^5 < c6*2^(5E)*n^3.
        f = minimum_exponent(N**5, c9, 3, 9)
        e = minimum_exponent((N-1)**5, c6*N**3, 2, 5)
        cases.append({'row': r, 'K6': str(c6), 'K9': str(c9),
                      'v3_n_lower': f, 'v2_n_minus_1_lower': e})
    assert [(r['v3_n_lower'], r['v2_n_minus_1_lower']) for r in cases] == [(100, 112), (101, 113), (101, 112), (101, 112), (101, 112)]
    f = minimum_exponent(N**5, k9, 3, 9)
    e = minimum_exponent((N-1)**5, k6*N**3, 2, 5)
    assert (f, e) == (102, 115)
    assert 2**5 > k6
    assert (N-1)**627 > (119**5*k6*N**3)**200
    assert (N-1)**627 > (53**6*k6*N**3)**200
    return {'conditional_full5_lift': 'if e=v5(n-(n mod5))>=2, no shared5 implies j mod5^e<=n mod5, so the complete 5^e is allocated',
            'odd_class': '9 mod72', 'full_small_prime_denominators': [1, 6, 1],
            'lifted_K6': str(k6), 'lifted_K9': str(k9),
            'first_power5_cases': cases,
            'all_odd_necessary_valuations': {'v3_n_at_least': 100, 'v2_n_minus_1_at_least': 112},
            'higher_power5_necessary_valuations': {'v3_n_at_least': f, 'v2_n_minus_1_at_least': e},
            'higher_power5_product_upper': 'A*B<2*n^(3/5)',
            'higher_power5_necessary_imbalance_with_external_BFT': 'A>119*B or B>53*A',
            'diagnostic_nonzero_binomial_samples': samples,
            'scope': 'universal no-carry argument, reused exact parent certificates, and exact thresholds; general odd class remains open'}


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled: do not use python -O.')
    result = {'status': 'passed', 'i': 5, 'general_i5_solved': False,
              'odd_class_9_solved': False, 'problem699_solved': False,
              'new_completely_solved_indices': 0, 'unresolved_indices': 28,
              'allocation': audit_allocation_certificate(),
              'all_degree_barrier': audit_all_degree_barrier(),
              'prime5_lift': audit_prime5_lift(),
              'dependencies': ['prior reduction to support01; odd n uses its elementary part',
                               'exact nonmaximal denominator bounds',
                               'existing finite theorem for i>=5, n<=10^87',
                               'prior support01 polynomial identities and evaluation bounds',
                               'external BFT Theorem 2.1 only for the new imbalance bound'],
              'high_Kummer_digits_used_in_sparse_allocation_closeout': False,
              'high_Kummer_digits_used_in_conditional_prime5_lift': True}
    out = ROOT/'data/results/verification_i5_sparse_allocation.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': 'passed', 'configurations': result['allocation']['configurations'],
                      'necessary_active_cell_count': 'at least 9',
                      'odd_class_9_solved': False, 'general_i5_solved': False}, indent=2))


if __name__ == '__main__':
    main()
