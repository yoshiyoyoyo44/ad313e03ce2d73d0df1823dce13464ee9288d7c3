"""Exact replay for the all-index adjacent-row digit-descent note.

Universal arguments are in the paper. This does not solve any new index.
"""
from fractions import Fraction
from itertools import product
from math import comb, lcm, prod
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
X = sp.symbols('X')
N = 10**87


def digits(n, base):
    answer = []
    while n:
        answer.append(n % base)
        n //= base
    return answer or [0]


def dominated(a, b):
    return all(c <= (b[k] if k < len(b) else 0) for k, c in enumerate(a))


def valuation(n, p):
    assert n > 0
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def pp(coeffs):
    return sp.Poly(sum(c*X**k for k, c in enumerate(coeffs)), X, domain=sp.ZZ)


def norm(poly):
    return sum(abs(int(c)) for c in poly.all_coeffs())


def reciprocal(poly, degree=None):
    degree = poly.degree() if degree is None else degree
    return pp([int(poly.nth(degree-k)) for k in range(degree+1)])


def audit_full_power_lift():
    count = 0
    for n in range(8, 121):
        row = [comb(n, j) for j in range(n//2+1)]
        for i in range(3, min(15, n//2)+1):
            for p, exponent in sp.factorint(comb(n, i)).items():
                p = int(p)
                if p < i:
                    continue
                s = n % p
                assert s < i
                e = valuation(n-s, p)
                assert exponent == e-(p == i)
                q = p**e
                for j in range(i+1, n//2+1):
                    if row[j] % p == 0:
                        continue
                    assert j % q <= s
                    assert dominated(digits(j, q), digits(n, q))
                    assert digits(n, q)[1] % p != 0
                    count += 1
    assert count > 0
    # Grouped base-q dominance is only a necessary implication.
    assert dominated(digits(18, 9), digits(64, 9))
    assert not dominated(digits(18, 3), digits(64, 3))
    return {'local_no_shared_prime_samples': count,
            'full_power_rule': 'v_p((n)_i)=v_p(C(n,i)) + 1 if p=i is prime; otherwise equal',
            'grouped_digit_converse_valid': False}


def audit_positive_root_and_transfer():
    cases = 0
    for s in (0, 1, 2, 3):
        t = s+1
        for upper in ((1, 1), (1, 2), (2, 1), (2, 2), (1, 0, 1)):
            f = pp([s, *upper])
            a = f-t
            m = f.degree()
            for u in range(s+1):
                for lower in product(*[range(c+1) for c in upper]):
                    jpoly = pp([u, *lower])
                    if jpoly == pp([u]) or jpoly == f-s+u:
                        continue
                    b = sp.Poly(6*prod(jpoly.as_expr()-v for v in range(t+1)), X, domain=sp.ZZ)
                    # Other roots can be shared. The positive root rules out
                    # complete divisibility, not every common factor.
                    assert not b.rem(a).is_zero
                    if b.degree() < m:
                        rem = reciprocal(b)
                        iterations = 0
                        original = rem
                        divisor = -reciprocal(a)
                    else:
                        divisor = -reciprocal(a)
                        original = reciprocal(b)
                        # Independent descending monic integer division.
                        work = original
                        iterations = 0
                        while not work.is_zero and work.degree() >= m:
                            before = norm(work)
                            work -= sp.Poly(work.LC()*X**(work.degree()-m), X)*divisor
                            assert norm(work) <= (f.eval(1)-s)*before
                            iterations += 1
                        rem = work
                        assert rem == original.rem(divisor)
                    d = max(m, b.degree())
                    # The d<m branch can directly use B, so the larger
                    # formula remains a safe uniform coefficient bound.
                    bound = 6*prod(int(f.eval(1))+v for v in range(t+1))*(int(f.eval(1))-s)**(t*m+1)
                    assert norm(rem) <= bound
                    assert iterations <= t*m+1
                    cases += 1
    return {'exact_polynomial_samples': cases,
            'monic_reciprocal_transfer_constant': '2*c*product(H+v, v=0..t)*(H-s)^(t*m+1)',
            'universal_scope': 'paper proof for all degrees; finite resultant and division diagnostics do not replace it'}


def sparse_bound(i, s, c):
    t = s+1
    assert 0 <= s <= i-2
    return t+c*max((2*t+1)**t, (t**t+t+1)**t, (c*2**t+t)**t)


def audit_two_mass_class():
    count = 0
    for s in range(0, 9):
        t = s+1
        for u in range(s+1):
            b = sp.Poly(prod(X+u-v for v in range(t+1) if v != u), X)
            r = prod(1+2*(u-v) for v in range(t+1) if v != u)
            assert r != 0 and abs(r) <= (2*t+1)**t
            assert abs(int(sp.resultant(2*X-1, b))) == abs(r)
            for m in range(2, t+1):
                a = X**m+X-1
                r = prod((v-u)**m+(v-u)-1 for v in range(t+1) if v != u)
                assert r != 0 and abs(r) <= (t**t+t+1)**t
                assert abs(int(sp.resultant(a, b))) == abs(r)
                count += 1
    all_index_bounds = []
    for i in range(3, 34):
        c = lcm(*range(1, i+1))
        largest = max(sparse_bound(i, s, c) for s in range(i-1))
        all_index_bounds.append({'i': i, 'uniform_denominator': str(c),
                                 'explicit_n_upper': str(largest),
                                 'upper_below_10_power87': largest < N})
    i5 = []
    for s, c, orientation in ((2, 5, 'even64'), (3, 5, 'odd9')):
        t = s+1
        # Conservative q bound; x^(t+1)/(x+t)^t increases for x>0.
        q = 7
        while q**(t+1) < c*(q+t)**t:
            q += 1
        maximum_q = q-1
        large_degree_n = t+c*(maximum_q+t)**t
        small_degree_n = t+c*max(abs(prod((v-u)**m+(v-u)-1
                                               for v in range(t+1) if v != u))
                                    for u in range(s+1) for m in range(2, t+1))
        linear_n = t+c*max(abs(prod(1+2*(u-v) for v in range(t+1) if v != u))
                           for u in range(s+1))
        bound = max(large_degree_n, small_degree_n, linear_n)
        assert bound < N
        i5.append({'row': s, 'adjacent_row': t, 'orientation': orientation, 'c': c,
                   'q_upper_for_m_at_least_t_plus_1': maximum_q,
                   'low_mass_n_upper': bound,
                   'large_degree_n_upper': large_degree_n,
                   'small_degree_n_upper': small_degree_n,
                   'linear_n_upper': linear_n})
    assert [r['low_mass_n_upper'] for r in i5] == [10988, 1827249]
    return {'resultant_samples': count, 'all_index_bounds': all_index_bounds,
            'i5_low_digit_mass_closeout': i5,
            'i5_odd_necessary_block_digit_sums': {'row2_at_least': 5, 'row3_at_least': 7},
            'i5_even_necessary_block_digit_sums': {'row2_at_least': 6, 'row3_at_least': 6},
            'scope': 'all exponents and radix prime powers in this digit-mass class; general height remains open'}


def budget(d, c, s, k, h):
    t = s+1
    return (2*d)**2*(2*c)**k*(h+t)**((t+1)*k)*(h-s)**(k+t*k*k)


def three_mass_bound(s, c):
    """Safe all-degree bound for at most two positive-degree positions.

    Requires q>2*t-1. The low-degree branch uses the reciprocal transfer,
    so common factors and zero full resultants are allowed.
    """
    t = s+1
    qlow = 2*c*(s+3+t)**(t+1)*3**(t*t+1)
    nlow = (s+3)*qlow**t
    # J=u+2X leaves a factor2 after cancelling q. Keep it uniformly.
    nhigh = t+2*c*(4*c*4**t+2*t+1)**t
    return max(nlow, nhigh), qlow, nlow, nhigh


def audit_three_mass_positions():
    eliminations = 0
    zero_resultants = 0
    for s in range(1, 5):
        t = s+1
        for u in range(s+1):
            for m in range(2, t+2):
                for f, jpoly, scale, transformed in (
                    (s+2*X+X**m, u+X, 1, X+u),
                    (s+2*X+X**m, u+2*X, 1, 2*X+u),
                    (s+X+2*X**m, u+X, 1, X+u),
                    (s+X+2*X**m, u+X**m, 2, 1-X+2*u),
                ):
                    a = sp.Poly(f-t, X, domain=sp.ZZ)
                    reduced = sp.Poly(prod(jpoly-v for v in range(t+1) if v != u), X)
                    g = sp.Poly(prod(transformed-scale*v for v in range(t+1) if v != u), X)
                    assert (scale**t*reduced-g).rem(a).is_zero
                    assert g.degree() == t
                    assert not sp.Poly(prod(jpoly-v for v in range(t+1)), X).rem(a).is_zero
                    if sp.resultant(a, g) == 0:
                        zero_resultants += 1
                    for q in (max(2*t, 7), max(2*t, 7)+1, max(2*t, 7)+5):
                        assert g.eval(q) != 0
                        assert abs(g.eval(q)) <= (2*q+2*t+1)**t
                    eliminations += 1
    assert zero_resultants > 0
    # q=5 is a real resonance of the local adjacent-row condition. It is
    # not a counterexample to Problem699, and is not covered by q>2*t-1.
    for m in range(2, 12):
        n, j, s, t, q = 7+2*5**m, 2+5**m, 2, 3, 5
        assert valuation(n-s, 5) == 1
        assert dominated(digits(j, q), digits(n, q))
        assert 2*j == n-t
        assert (2*prod(j-v for v in range(t+1))) % (n-t) == 0
    i5 = []
    for orientation, s, c in (('odd9', 2, 30), ('even64', 3, 60)):
        bound, qlow, nlow, nhigh = three_mass_bound(s, c)
        assert bound < N
        i5.append({'orientation': orientation, 'row': s, 'c': c,
                   'two_positive_positions_mass3_n_upper': str(bound),
                   'q_upper_in_low_degree_branch': str(qlow),
                   'low_degree_n_upper': str(nlow), 'high_degree_n_upper': str(nhigh),
                   'q_resonance_excluded': 'q>=7>5' if s == 2 else 'q=7 contradicts n=1 mod3; all other candidate q>7'})
    # Exhaust the residue and exponent periods; no finite exponent cutoff
    # is imposed by this CRT calculation.
    residue_records = []
    for orientation, s, target in (('odd9', 2, 9), ('even64', 3, 64)):
        triples = []
        for q in range(1, 72):
            if q % 2 == 0 or q % 3 == 0:
                continue
            for a in range(24):
                for b in range(24):
                    value = s+q+pow(q, a, 72)+pow(q, b, 72)
                    if value % 72 != target or value % 9 != (0 if s == 2 else 1):
                        continue
                    triples.append((q, a, b))
        assert triples
        assert all(a % 2 == b % 2 == 0 for _, a, b in triples)
        allowed = sorted({q for q, _, _ in triples})
        assert allowed == ([5, 29] if s == 2 else [11, 59])
        for q, _, _ in triples:
            assert q % 9 in (2, 5)
        # Unit powers modulo72 have exponent dividing6. Thus a q of order6
        # must come from a prime p with e coprime to6 and p in these classes.
        pairs = [(p, e) for p in range(1, 72) if p % 2 and p % 3
                 for e in range(6) if pow(p, e, 72) in allowed]
        assert all(e in (1, 5) and p in allowed for p, e in pairs)
        residue_records.append({'orientation': orientation, 'row': s,
                                'q_mod72': allowed, 'prime_p_mod72': allowed,
                                'full_valuation_e_mod6': [1, 5],
                                'a_b_both_even': True, 'CRT_periodic_samples': len(triples)})
    return {'elimination_identity_samples': eliminations,
            'zero_resultants_allowed': zero_resultants,
            'general_condition': 'i>=3, q>=i, q>2*(s+1)-1; at most two positive-degree positions and mass3',
            'local_resonance_model_is_global_counterexample': False,
            'i5_two_position_closeout': i5,
            'i5_minimal_height_remaining_shape': 'F=s+X+X^a+X^b, 2<=a<b; J=u+X^a or u+X+X^a',
            'minimal_height_residues': residue_records,
            'scope': 'two-position mass3 is closed in i5; the surviving three-position, two-exponent family is not closed'}


def residue_subgroup(modulus, generators):
    subgroup = {1}
    while True:
        expanded = subgroup | {(a*b) % modulus for a in subgroup for b in generators}
        if expanded == subgroup:
            return subgroup
        subgroup = expanded


def audit_multiplicative_separator():
    results = []
    for orientation, s, generator, target, height in (
        ('odd9', 2, 5, 7, 5), ('even64', 3, 11, 13, 6)
    ):
        group = residue_subgroup(24, [generator])
        denominator_residues = {1, 5}
        possible_row_residues = {(d*g) % 24 for d in denominator_residues for g in group}
        assert target not in possible_row_residues
        assert group == ({1, 5} if s == 2 else {1, 11})
        # Compare closure with the complete cyclic-power description.
        assert group == {pow(generator, k, 24) for k in range(8)}
        results.append({'orientation': orientation, 'row': s, 'modulus': 24,
                        'candidate_prime_power_residue': generator,
                        'generated_subgroup': sorted(group),
                        'denominator_residues': sorted(denominator_residues),
                        'all_product_row_residues': sorted(possible_row_residues),
                        'required_actual_row_residue': target,
                        'all_primes_minimal_height_at_most': height,
                        'uniform_minimal_height_impossible': True,
                        'at_least_one_prime_power_digit_sum_at_least': height+2})
    return {'all_index_principle': 'if all candidate q residues lie in a subgroup G modulo m, n-s must lie in D*G; a disjoint row residue excludes the whole family without a prime-count bound',
            'i5_uniform_minimal_height_closeout': results,
            'general_i5_solved': False}


def audit_height_budget():
    denominators = {}
    for orientation, residue in (('odd9', 9), ('even64', 64)):
        maxima = [0, 0, 0]
        for n in range(residue, 1800, 72):
            r = n % 5
            e5 = valuation(n-r, 5)
            for k, s in enumerate((2, 3, 4)):
                d = 2**valuation(n-s, 2)*3**valuation(n-s, 3)
                d *= 5 if e5 == 1 and r == s else 1
                maxima[k] = max(maxima[k], d)
        denominators[orientation] = maxima
    assert denominators == {'odd9': [5, 30, 5], 'even64': [10, 5, 60]}
    results = []
    for orientation, s, d, c, h in (('odd9', 2, 5, 30, 5), ('odd9', 3, 30, 5, 7),
                                   ('even64', 2, 10, 5, 6), ('even64', 3, 5, 60, 6)):
        first = next(k for k in range(1, 100) if budget(d, c, s, k, h) >= N)
        assert budget(d, c, s, first-1, h) < N
        results.append({'orientation': orientation, 'row': s, 'H_star_at_most': h, 'necessary_distinct_primes': first,
                        'uniform_height_later_excluded_by_multiplicative_separator': (orientation, s) in (('odd9', 2), ('even64', 3)),
                        'excluded_previous_k_upper': str(budget(d, c, s, first-1, h))})
    assert [r['necessary_distinct_primes'] for r in results[:2]] == [6, 5]
    # Cauchy reduction: (C+d)^2-C(C+d)-k^2*b*d=d*(k*a+d)>0.
    a, b, d, k = sp.symbols('a b d k', positive=True)
    ctotal = k*a+k*k*b
    assert sp.expand((ctotal+d)**2-ctotal*(ctotal+d)-k*k*b*d-d*(k*a+d)) == 0
    return {'full_candidate_denominator_maxima_rows234': denominators,
            'bounded_height_i5_consequences': results,
            'general_formula': 'n<(2*d)^2*(2*c)^k*(H_star+t)^((t+1)*k)*(H_star-s)^(k+t*k^2)',
            'scope': 'effective finite bound when k and block digit height are bounded; neither bound is proved in the general case'}


def audit_adjacent_existence():
    samples = []
    for i in range(10, 120):
        m = int(sp.primepi(i-1))
        assert i-m > (i+1)//2
        samples.append({'i': i, 'small_primes': m, 'at_least_nonmaximal_rows': i-m})
    return {'universal_range': 'i>=10',
            'argument': 'the odd composite9 gives pi(i-1)<=floor(i/2)-1; a path with i vertices has independent sets of size at most ceil(i/2)',
            'samples': samples,
            'scope': 'guarantees one pair of consecutive nonmaximal rows, not a bound on its digit height or number of prime factors'}


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled: do not use python -O.')
    result = {'status': 'passed', 'problem699_solved': False, 'general_i5_solved': False,
              'new_completely_solved_indices': 0, 'unresolved_indices': 28,
              'full_power_lift': audit_full_power_lift(),
              'adjacent_positive_root': audit_positive_root_and_transfer(),
              'low_digit_mass': audit_two_mass_class(),
              'three_mass_positions': audit_three_mass_positions(),
              'multiplicative_separator': audit_multiplicative_separator(),
              'height_budget': audit_height_budget(),
              'adjacent_row_existence': audit_adjacent_existence(),
              'dependencies': ['Kummer no-carry theorem and its block implication',
                               'prior i5 support01 reduction',
                               'prior i5 odd class9 and even class64 necessary residues',
                               'existing finite i>=5 theorem through n=10^87'],
              'novelty_claimed': False,
              'universal_scope': 'paper proof plus exact replay; all-index conditional lemmas and a new i5 digit class, not an all-index solution'}
    out = ROOT/'data/results/verification_adjacent_digit_descent.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': 'passed', 'polynomial_diagnostics': result['adjacent_positive_root']['exact_polynomial_samples'],
                      'i5_low_mass_n_upper': [r['low_mass_n_upper'] for r in result['low_digit_mass']['i5_low_digit_mass_closeout']],
                      'necessary_prime_counts_for_bounded_height': [r['necessary_distinct_primes'] for r in result['height_budget']['bounded_height_i5_consequences']],
                      'uniform_minimal_height_classes_closed': len(result['multiplicative_separator']['i5_uniform_minimal_height_closeout']),
                      'general_i5_solved': False}, indent=2))


if __name__ == '__main__':
    main()
