"""Exact certificates for the i=5 product, affine strips, and valuation frontier.

Universal scope comes from the accompanying paper proof and its stated prior
dependencies. Small arithmetic and CRT samples are independent diagnostics.
"""
import json
from fractions import Fraction
from math import comb, gcd, prod
from pathlib import Path

from audit_i5_multiplicity_frontier import audit_denominators

ROOT = Path(__file__).resolve().parent.parent
CELLS = [(s, u) for s in range(5) for u in range(s + 1)]
N0 = 10**87
LAMBDA = Fraction(57, 200)
C6, C9 = 1458000000, 36450000


def valuation(number, prime):
    assert number > 0
    exponent = 0
    while number % prime == 0:
        number //= prime
        exponent += 1
    return exponent


def rough_part(number):
    for prime in (2, 3):
        while number % prime == 0:
            number //= prime
    return number


def audit_binomial_identity():
    cases = nontrivial_quotients = 0
    for n in range(12, 241):
        q = rough_part(comb(n, 5))
        rows = []
        for s in range(5):
            value = n - s
            denominator = 2**valuation(value, 2) * 3**valuation(value, 3)
            denominator *= 5 if value % 5 == 0 else 1
            rows.append(value // denominator)
        assert prod(rows) == q
        assert all(gcd(rows[s], rows[t]) == 1 for s in range(5) for t in range(s))
        for j in range(6, n // 2 + 1):
            left = comb(n, 5) * comb(n - 5, j - 5)
            right = comb(n, j) * comb(j, 5)
            assert left == right
            remaining = q // gcd(q, comb(n, j))
            assert comb(j, 5) % remaining == 0
            nontrivial_quotients += remaining > 1
            cases += 1
    return {'diagnostic_cases': cases, 'nontrivial_quotients': nontrivial_quotients,
            'scope': 'identity and exact row decomposition diagnostics; universal identity proved in the note'}


def audit_coupled_denominators():
    source = audit_denominators()
    maxima = {}
    restored_mixed_constants = {}
    for pair in ((0, 1), (1, 0)):
        records = source[pair]
        values = [5**sum((r['residue'] - s) % 5 == 0 for s in (0, 1))
                  * prod(r['denominators'][s] for s in (2, 3, 4)) for r in records]
        maxima[f'{pair[0]},{pair[1]}'] = max(values)
        for r, actual in zip(records, values):
            n = 1080 + r['residue']
            small = prod(2**valuation(n - s, 2) * 3**valuation(n - s, 3)
                         for s in (2, 3, 4))
            # Exactly one of the five consecutive rows contains a factor 5.
            assert actual == 5 * small
        restored = max(5**(6*int(r['residue'] % 5 == 0) + 5*int((r['residue'] - 1) % 5 == 0))
                       * prod(r['denominators'][s]**6 for s in (2, 3, 4)) for r in records)
        constant = Fraction(restored, 2048)
        assert constant == Fraction(maxima[f'{pair[0]},{pair[1]}']**6, 2048)
        restored_mixed_constants[f'{pair[0]},{pair[1]}'] = str(constant)
    assert maxima == {'0,1': 120, '1,0': 30}
    saved = json.loads((ROOT / 'data/results/verification_i5_multiplicity_frontier.json').read_text(encoding='utf-8'))
    baseline = next(c for c in saved['certificates'] if c['name'] == 'support_01_baseline_tight_constants')
    assert baseline['row_targets'] == [6, 5, 6, 6, 6]
    assert Fraction(baseline['evaluation_constant']) == Fraction(1, 4096)
    assert restored_mixed_constants == {'0,1': '1458000000', '1,0': '11390625/32'}
    return {'period': 360, 'restored_joint_denominator_maxima': maxima,
            'restored_A6_B5_constants': restored_mixed_constants,
            'tail_lower': 'Q5(n) > (n-4)^3*(n-1)^(57/200)/C',
            'external_dependency': 'Bennett-Filaseta-Trifonov Theorem 2.1, prime pair (2,3)'}


def audit_affine_geometry():
    records = []
    for a, b, expected in ((0, 1, 5), (1, 2, 9), (1, 3, 12), (1, 4, 14), (2, 5, 15)):
        offsets = sorted({a*s - b*u for s, u in CELLS})
        assert len(offsets) == expected
        records.append({'a': a, 'b': b, 'offsets': offsets, 'factor_count': len(offsets)})
    for b in range(2, 101):
        for a in range(1, b // 2 + 1):
            if gcd(a, b) != 1:
                continue
            offsets = {a*s - b*u for s, u in CELLS}
            assert len(offsets) <= 15
            assert all(abs(v) <= 4*b for v in offsets)
            if b >= 5:
                assert len(offsets) == 15
            for delta in {-v for v in offsets}:
                missed = [s for s in (2, 3) if all(delta + a*s - b*u != 0 for u in range(s + 1))]
                assert missed  # Coprimality makes intersected row indices congruent mod b.
                s = missed[0]
                assert abs(prod(delta + a*s - b*u for u in range(s + 1))) <= (8*b)**4
    central_zeros = []
    for delta in range(5):
        possibilities = [(60*abs(prod(delta - s + 2*u for u in range(s + 1))) + s, s)
                         for s in (2, 3, 4) if all(delta - s + 2*u for u in range(s + 1))]
        bound, row = min(possibilities)
        central_zeros.append({'gap': delta, 'missed_row': row, 'n_upper': bound})
    assert [r['n_upper'] for r in central_zeros] == [543, 182, 903, 902, 2882]
    return {'selected_slopes': records, 'central_zero_lines': central_zeros,
            'general_zero_line_bound': 'n <= 60*(8*b)^4+3',
            'scope': 'finite geometry replay; general b proof uses b|(s-t), not a finite denominator cutoff'}


def audit_formal_prime_power_cells():
    primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
    checks = 0
    for shift in range(3):
        moduli = [p**(1 + (index + shift) % 3) for index, p in enumerate(primes)]
        modulus = prod(moduli)
        def crt(residues):
            return sum(value*(modulus//q)*pow(modulus//q, -1, q)
                       for value, q in zip(residues, moduli)) % modulus
        n = crt([s for s, u in CELLS]) + 2*modulus
        j = crt([u for s, u in CELLS])
        for a, b in ((0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (3, 7)):
            delta = b*j - a*n
            offsets = {a*s - b*u for s, u in CELLS}
            for q, (s, u) in zip(moduli, CELLS):
                assert (n - s) % q == (j - u) % q == 0
                assert (delta + a*s - b*u) % q == 0
            assert prod(delta + v for v in offsets) % modulus == 0
            checks += 1
    return {'crt_diagnostics': checks, 'prime_power_exponents': [1, 2, 3],
            'scope': 'formal coprime cell examples, not counterexamples or a proof by sampling'}


def audit_thresholds():
    rhs = (N0 - 4)**600 * (N0 - 1)**57
    inequalities = {
        'j_at_most_1p4e57': (14*10**56)**1000 < rhs,
        'odd_n_j_at_most_1p9e57': (19*10**56)**1000 < 4**200*rhs,
        'central_gap_at_most_3e31': 120**200*(3*10**31)**1800 < rhs,
        'one_third_error_at_most_4e23': (120*(4*10**23 + 8)**12)**200 < rhs,
        'one_quarter_error_at_most_1e20': (120*(10**20 + 12)**14)**200 < rhs,
        'uniform_height_error_at_most_1e18': (120*(5*10**18)**15)**200 < rhs,
        'uniform_zero_line_b_at_most_1e18': 60*(8*10**18)**4 + 3 < N0,
    }
    assert all(inequalities.values())
    assert (3 + LAMBDA)/5 == Fraction(657, 1000)
    assert (3 + LAMBDA)/9 == Fraction(73, 200)
    assert (3 + LAMBDA)/12 == Fraction(219, 800)
    assert (3 + LAMBDA)/15 == Fraction(219, 1000)
    return {'tail_threshold': str(N0), 'integer_inequalities': inequalities,
            'j_exponent': '657/1000', 'central_gap_exponent': '73/200',
            'all_n_extension_dependency': 'existing finite theorem for i>=5, n<=10^87'}


def audit_valuation_frontier():
    bounds = {}
    for row, prime, expected in ((0, 2, 156), (0, 3, 99), (1, 2, 108), (1, 3, 68)):
        exponent = 0
        def allowed(e):
            if row == 0:
                return N0**5 < C9*5**9*prime**(9*e)
            return (N0 - 1)**5 < C6*5**5*prime**(5*e)*N0**3
        while not allowed(exponent):
            exponent += 1
        assert exponent == expected and not allowed(exponent - 1)
        bounds[f'row{row}_p{prime}'] = exponent
    progressions = []
    for pair, p0, e0, p1, e1, mod72 in (((0, 1), 2, 156, 3, 68, 64), ((1, 0), 3, 99, 2, 108, 9)):
        m0, m1 = p0**e0, p1**e1
        modulus = m0*m1
        residue = m0*pow(m0, -1, m1) % modulus
        assert residue % m0 == 0 and residue % m1 == 1
        assert modulus % 72 == 0 and residue % 72 == mod72
        progressions.append({'orientation': list(pair), 'row0_prime': p0, 'row0_exponent_min': e0,
                             'row1_prime': p1, 'row1_exponent_min': e1,
                             'residue': str(residue), 'modulus': str(modulus), 'class_mod72': mod72})
    for f in range(2, 40):
        for t in range(20):
            assert 3**f*5**(2*t + 1) % 8 in (5, 7)
    return {'prime_power_exponent_lower_bounds': bounds, 'necessary_progressions': progressions,
            'remaining_classes_mod72': [9, 64], 'class_45_closed': True,
            'family_closed_all_n': 'n=3^f*5^(2t+1), f,t>=0',
            'scope': 'necessary congruences are infinite and do not prove general i=5'}


def audit_cofactor_imbalance_and_ineffective_finiteness():
    odd_constant = Fraction(30**6, 2048)
    assert 70**5 > C6 and 13**5 > odd_constant
    tests = {}
    for name, constant, ratio, exponent in (
        ('A_over_B_gt_3', C6, 3, 5), ('B_over_A_gt_2', C6, 2, 6),
        ('odd_A_over_B_gt_17', odd_constant, 17, 5), ('odd_B_over_A_gt_10', odd_constant, 10, 6),
    ):
        tests[name] = (N0 - 1)**627 > (ratio**exponent*constant*N0**3)**200
    assert all(tests.values())
    assert (11*LAMBDA - 3)/5 == Fraction(27, 1000)
    assert (11*LAMBDA - 3)/6 == Fraction(9, 400)
    assert Fraction(3, 4) - Fraction(3, 5) == Fraction(3, 20)
    assert N0**3 > 140**20  # n^(3/4)/2 > 70*n^(3/5) throughout this tail.
    return {'restored_product_upper': 'A*B < 70*n^(3/5); odd n: A*B < 13*n^(3/5)',
            'integer_ratio_tests': tests,
            'necessary_unbalanced_alternatives': 'A>3B or B>2A; odd n: A>17B or B>10A',
            'A_max_ratio_growth_exponent': '27/1000', 'B_max_ratio_growth_exponent': '9/400',
            'ineffective_finiteness': {
                'external_theorem': 'Mahler/Ridout: x*(x+1)=2^k*3^l*y implies y>x^(1-epsilon) for sufficiently large x',
                'source': 'Bennett-Filaseta-Trifonov, introduction, page 2; cites Mahler, Lectures on Diophantine Approximations I (1961)',
                'source_url': 'https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf',
                'epsilon': '1/4', 'substitution': 'x=n-1, y=A*B',
                'consequence': 'Only finitely many i=5 counterexamples, using the stated external theorem and prior support reduction',
                'numerical_cutoff_known': False, 'theorem_proof_replayed': False,
                'scope': 'non-effective finiteness; cannot justify scanning to an invented upper bound or claiming general i=5 solved',
            }}


def audit_perfect_power_closeout():
    """Replay constants and LTE identities; the note proves all roots/exponents."""
    root_floor = 10**43
    square_constant = 4**5*C6
    assert square_constant == 1492992000000
    assert root_floor**2 < N0 and root_floor > 1771561
    restored_9_4_constant = C9*5**9
    assert 5*LAMBDA - 1 == Fraction(17, 40)
    assert 12*LAMBDA - 1 == Fraction(121, 50)
    tests = {
        'square_D_upper_below_BFT_lower': (32*square_constant)**40 < root_floor**17,
        'square_C_upper_below_BFT_lower': (4096*square_constant)**50 < root_floor**121,
        'log2_N_below_290': N0 < 2**290,
        'odd_exponent_uniform_threshold': 10**29 > C6*290**5,
        'monotonicity_log_N_above_15': N0 > 3**15,
        'n_minus_1_odd_power_threshold': N0 > 512*C6*290**6,
        'n_plus_1_square_threshold': N0 > (4**9*restored_9_4_constant)**2,
        'n_plus_1_odd_power_threshold': N0**2 > restored_9_4_constant*290**9,
    }
    assert all(tests.values())
    square_cases = odd_power_cases = 0
    for p, q in ((2, 3), (3, 2)):
        for root in range(2, 241):
            if root % p or root % q == 0:
                continue
            a = root // p**valuation(root, p)
            n = root**2
            exponent = valuation(n - 1, q)
            if not exponent:
                continue
            sign = max((-1, 1), key=lambda s: valuation(root + s, q))
            root_exponent = valuation(root + sign, q)
            d = (root + sign) // q**root_exponent
            h = (root - sign) // q**valuation(root - sign, q)
            b = (n - 1) // q**exponent
            assert n == p**(2*valuation(root, p))*a**2
            assert b == d*h and 4*h > root
            assert abs(p**valuation(root, p)*a - q**root_exponent*d) == 1
            assert root_exponent == exponent - (1 if q == 2 else 0)
            square_cases += 1
            for k in range(3, 32, 2):
                # For odd k, root**k == 1 mod q requires root == 1 mod q.
                if root % q != 1:
                    continue
                n = root**k
                h = (n - 1) // (root - 1)
                qk = q**valuation(k, q)
                d = (root - 1) // q**valuation(root - 1, q)
                b = (n - 1) // q**valuation(n - 1, q)
                assert valuation(h, q) == valuation(k, q)
                assert h % qk == 0 and b == d*(h // qk)
                assert qk <= k and b*k > root**(k - 1)
                assert Fraction(2*k - 5, k) >= Fraction(1, 3)
                assert n >= 2**k
                odd_power_cases += 1
    assert all((root**2 + 1) % 72 not in (9, 64) for root in range(72))
    for f in (0, 1):
        for d in (0, 1):
            assert (3**f*5**d % 8 == 1) == (f == d == 0)
    assert all((2**e*5**d % 9 == 1) == ((e-d) % 6 == 0)
               for e in range(1, 7) for d in range(6))
    adjacent_minus_cases = adjacent_plus_cases = adjacent_plus_square_cases = 0
    for p in (2, 3):
        for root in range(2, 241):
            if root % p == 0:
                continue
            exponent = valuation(root**2 - 1, p)
            sign = max((-1, 1), key=lambda s: valuation(root + s, p))
            d = (root + sign) // p**valuation(root + sign, p)
            h = (root - sign) // p**valuation(root - sign, p)
            a = (root**2 - 1) // p**exponent
            assert a == d*h and 4*h > root
            adjacent_plus_square_cases += 1
            for k in range(3, 32, 2):
                pk = p**valuation(k, p)
                assert pk <= k
                if (root + 1) % p == 0:
                    x = root**k
                    h = (x + 1) // (root + 1)
                    d = (root + 1) // p**valuation(root + 1, p)
                    a = (x + 1) // p**valuation(x + 1, p)
                    assert valuation(h, p) == valuation(k, p)
                    assert a == d*(h // pk) and 2*a*k > root**(k - 1)
                    assert 6 - Fraction(6, k) >= 4
                    adjacent_minus_cases += 1
                if (root - 1) % p == 0:
                    x = root**k
                    h = (x - 1) // (root - 1)
                    d = (root - 1) // p**valuation(root - 1, p)
                    a = (x - 1) // p**valuation(x - 1, p)
                    assert valuation(h, p) == valuation(k, p)
                    assert a == d*(h // pk) and a*k > root**(k - 1)
                    assert 9 - Fraction(9, k) >= 6
                    adjacent_plus_cases += 1
    return {
        'family_closed_all_n': 'at least one of n-1,n,n+1 is z^k, integers z>=2,k>=2; every allowable j, i=5',
        'square_diagnostic_cases': square_cases,
        'odd_exponent_LTE_diagnostic_cases': odd_power_cases,
        'adjacent_n_minus_1_LTE_cases': adjacent_minus_cases,
        'adjacent_n_plus_1_LTE_cases': adjacent_plus_cases,
        'adjacent_n_plus_1_square_cases': adjacent_plus_square_cases,
        'restored_9_4_constant': restored_9_4_constant,
        'square_constant': square_constant,
        'square_root_floor': str(root_floor),
        'integer_threshold_tests': tests,
        'square_reduction': 'A=C^2, B=D*H, H>z/4, C^12*D^5 < (4^5*C6)*z',
        'odd_exponent_reduction': 'n^(2-5/k) < C6*k^5; k<=log2(n), k>=3',
        'n_minus_1_reduction': 'squares excluded mod72; odd k: x < 512*C6*k^6, x=n-1',
        'n_plus_1_reduction': 'squares: sqrt(n)<4^9*C9*5^9; odd k: x^2<C9*5^9*k^9, x=n+1',
        'all_odd_5_smooth_n_closed': 'n=3^f*5^d for every f,d>=0 and every allowable j, i=5',
        'remaining_5_smooth_necessary_form': 'n=2^e*5^d with e,d positive odd and e=d mod6; not actual counterexamples',
        'dependencies': ['prior support reduction to 01',
                         'Bennett-Filaseta-Trifonov Theorem 2.1 at the square root',
                         'existing finite theorem for i>=5, n<=10^87'],
        'scope': 'universal proof in the note; diagnostic roots/exponents are not a finite coverage proof',
    }


def audit_effective_exponent_gap():
    x, y = Fraction(1, 3), Fraction(1, 10)
    assert 6*x + 5*y < 3 and 9*x + 4*y < 4
    assert x + y < Fraction(3, 5)
    assert max(x, y) > Fraction(2921, 10000) > LAMBDA
    assert x - y > Fraction(27, 1000)
    return {'formal_exponents': {'log_n_A': str(x), 'log_n_B': str(y)},
            'mixed_6_5_exponent': str(6*x + 5*y),
            'mixed_9_4_exponent': str(9*x + 4*y),
            'BFT_Corollary_2_3_max_exponent': '2921/10000',
            'scope': 'exponent relaxation only, not integers, a Kummer model, or a counterexample',
            'consequence': 'the presently recorded effective exponent bounds alone do not give a tail contradiction'}


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled: do not use python -O.')
    result = {'status': 'passed', 'i': 5, 'general_i5_solved': False,
              'new_completely_solved_indices': 0, 'unresolved_indices': 28,
              'binomial_identity': audit_binomial_identity(),
              'coupled_denominators': audit_coupled_denominators(),
              'affine_geometry': audit_affine_geometry(),
              'formal_cells': audit_formal_prime_power_cells(),
              'thresholds': audit_thresholds(), 'valuation_frontier': audit_valuation_frontier(),
              'cofactor_imbalance': audit_cofactor_imbalance_and_ineffective_finiteness(),
              'perfect_power_closeout': audit_perfect_power_closeout(),
              'effective_exponent_gap': audit_effective_exponent_gap()}
    output = ROOT / 'data/results/verification_i5_global_product_and_affine.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'passed', 'remaining_classes_mod72': [9, 64],
                      'closed_class_mod72': 45, 'j_all_n_bound': str(14*10**56),
                      'central_gap_all_n_bound': str(3*10**31),
                      'perfect_power_n_and_adjacent_closed': True,
                      'general_i5_solved': False}, indent=2))


if __name__ == '__main__':
    main()
