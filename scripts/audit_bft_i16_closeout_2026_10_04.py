"""Exact all-n closure of i16: six updated edges and complete range join.

The G bounds and the original finite range have their own full verifiers.
This checker pins those inputs, recertifies every new BFT anchor, enumerates
all graph orientations, and checks the capacity and boundary comparisons.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial, isqrt
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dependency(name):
    path = ROOT / 'data/results' / name
    value = json.loads(path.read_text(encoding='utf-8'))
    assert value['status'].lower() in ('pass', 'passed')
    return value, dict(path=str(path.relative_to(ROOT)), sha256=digest(path))


def main():
    if not __debug__:
        raise RuntimeError('Assertions required.')
    names = [
        'verification_bft_gcd_3_2_finite_blocks_2026_10_04.json',
        'verification_bft_G_3_2_analytic_tail_2026-10-04.json',
        'verification_bft_gcd_4_3_finite_blocks_2026_10_04.json',
        'verification_bft_gcd_4_3_universal_2026_10_04.json',
        'verification_bft_gcd_19_14_finite_blocks_2026_10_04.json',
        'verification_bft_gcd_19_14_universal_2026_10_04.json',
        'verification_bft_gcd_19_14_independent_2026_10_04.json',
        'verification_bft_gcd_10_7_and_two_anchors_2026_10_04.json',
        'verification_bft_gcd_10_7_independent_2026-10-04.json',
        'verification_bft_i16_finite_dependency_2026_10_04.json',
    ]
    inputs = [dependency(name) for name in names]
    g32f, g32t, g43f, g43, g1914f, g1914, audit1914, g107, audit107, finite = [x[0] for x in inputs]
    assert g32f['m0'] == 50000 and g32f['last_m'] == 4000000
    assert g32f['L1'] == '1611/1000' and g32f['finite_blocks'] == 8727
    assert g32t['first_m'] == 4000000 and g32t['switch_m'] == 20000000000
    assert (g43['c'], g43['d'], g43['L1'], g43['m0']) == (4, 3, '361/250', 30000)
    assert g43['finite_part'] == g43f
    assert g43f['last_m'] == 4000000 and g43f['finite_blocks'] == 9723
    assert g43['first_domain'] == [4000000, 20000000000]
    assert g43['second_domain_lower'] == 20000000000
    assert (g1914['c'], g1914['d'], g1914['L1'], g1914['m0']) == (19, 14, '361/250', 6000)
    assert g1914['finite_part'] == g1914f
    assert g1914f['last_m'] == 4000000 and g1914f['finite_blocks'] == 12693
    assert g1914['first_domain'] == [4000000, 2000000000]
    assert g1914['second_domain_start'] == 2000000000
    assert audit1914['finite_full_replay_performed'] and audit1914['mathematical_source_audit_passed']
    assert audit1914['finite_result_sha256'] == inputs[4][1]['sha256']
    assert (g107['c'], g107['d'], g107['L1'], g107['m0']) == (10, 7, '149/100', 12000)
    assert g107['finite_range'] == [12001, 2000000] and g107['finite_blocks'] == 19840
    assert g107['first_domain'] == [2000000, 10000000000]
    assert g107['second_domain_lower'] == 10000000000
    assert audit107['finite_blocks_independently_rerun'] == 19840
    assert audit107['result_sha256'] == inputs[7][1]['sha256']
    assert audit107['delta_safe_generic_intervals_audited']
    assert audit107['integer_mantissa_log_enclosure_audited']
    assert audit107['analytic_two_domain_tail_audited']
    assert finite['indices'] == [16] and finite['finite_bound'] == 10**87
    assert finite['archived_hashes_preserved'] == 40 and finite['exhaustive_targeted_replay']
    row = finite['rows'][0]
    assert (row['i'], row['bootstrap_steps'], row['final_cap']) == (16, 4, 927728)
    assert row['exact_binomial_checks'] == 4675
    assert row['prefix']['intervals'] == 5861 and row['prefix']['singletons'] == 1116
    assert row['prefix']['upper'] == 1999999
    spec = importlib.util.spec_from_file_location('i16_interval_kernel',
        ROOT / 'scripts/audit_bft_newvertex_i22_i25_2026_10_04.py')
    kernel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kernel)
    seeds = [
        dict(pair=[2, 7], p=2, k0=3, a=1, q=7, l0=1, b=1, c=25, d=17,
             L1=F(777, 500), m0=582, target=F(273, 1000), epsilon=F(1, 2500)),
        dict(pair=[3, 11], p=3, k0=5, a=1, q=11, l0=2, b=2, c=19, d=14,
             L1=F(361, 250), m0=6000, target=F(43, 125), epsilon=F(3, 20000)),
        dict(pair=[5, 7], p=5, k0=2, a=2, q=7, l0=2, b=1, c=3, d=2,
             L1=F(1611, 1000), m0=50000, target=F(33, 125), epsilon=F(1, 1250)),
        dict(pair=[7, 13], p=7, k0=3, a=1, q=13, l0=2, b=2, c=4, d=3,
             L1=F(361, 250), m0=30000, target=F(49, 400), epsilon=F(1, 10000)),
        dict(pair=[2, 13], p=2, k0=9, a=1, q=13, l0=2, b=3, c=10, d=7,
             L1=F(149, 100), m0=12000, target=F(73, 1000), epsilon=F(3, 10000)),
        dict(pair=[11, 13], p=13, k0=1, a=1, q=11, l0=1, b=1, c=10, d=7,
             L1=F(149, 100), m0=12000, target=F(61, 1000), epsilon=F(3, 10000)),
    ]
    anchors = [kernel.certify(seed, 999999) for seed in seeds]
    assert anchors[1] == g1914['new_3_11_anchor'] == audit1914['new_3_11_anchor']
    assert anchors[4:] == g107['anchors']
    edges = [(2, 3, 570), (2, 5, 516), (2, 7, 546), (2, 11, 118), (2, 13, 146),
             (3, 5, 432), (3, 7, 76), (3, 11, 688), (3, 13, 462), (5, 7, 528),
             (5, 11, 398), (5, 13, 326), (7, 13, 245), (11, 13, 122)]
    vertices = [2, 3, 5, 7, 11, 13]
    assert all(F(w, 2000) < F(1, 2) for p, q, w in edges)
    best = 10**9
    vectors = set()
    for choices in product((0, 1), repeat=len(edges)):
        lower = dict.fromkeys(vertices, 0)
        for (p, q, weight), side in zip(edges, choices):
            endpoint = (p, q)[side]
            lower[endpoint] = max(lower[endpoint], weight)
        total = sum(lower.values())
        if total < best:
            best, vectors = total, set()
        if total == best:
            vectors.add(tuple(lower[p] for p in vertices))
    assert best == 2007 and vectors == {(546, 688, 528, 0, 0, 245)}
    # Six analytic branches. A triangle lower bound is largest+smallest:
    # the endpoint selected for a largest edge is disjoint from the opposite
    # edge, whose weight is at least the smallest triangle weight.
    triangle235 = max(570, 516, 432) + min(570, 516, 432)
    triangle2_11_13 = max(118, 146, 122) + min(118, 146, 122)
    branches = [688+528+triangle235, 688+528+570+245,
                688+546+528+245, 688+546+528+398,
                688+516+546+398, 688+546+516+triangle2_11_13]
    assert branches == [2218, 2031, 2007, 2160, 2148, 2014]
    i, h = 16, 15
    small = [p for p in range(2, i) if all(p % k for k in range(2, isqrt(p)+1))]
    assert small == vertices
    m = len(small)
    b = (2*h+2)//3
    d = 3*b-h
    S = b*(b+1)//2
    D = 3*S-d*(i-m)
    c_i = i
    A = factorial(i)//c_i
    assert (m, b, d, S, D) == (6, 10, 15, 55, 15)
    assert A == factorial(15)
    assert all(max(0, s-(h-b))+max(0, b-u)+max(0, b-s+u) >= d
               for s in range(i) for u in range(s+1))
    assert sum(max(0, s-(h-b)) for s in range(i)) == S
    assert sum(max(0, b-u) for u in range(i)) == S
    gap = 2007*d-2000*D
    cutoff = 3100
    assert gap == 105
    assert A < 10**13 and 2**2001 < 10**603 and 4**5 > 10**3
    margin = cutoff*gap+1200*S-603-2000*d*13
    assert margin == 897
    assert 10**cutoff > 2*h*i*d and 10**cutoff > 2*h*2007*d
    N = 10**87
    prop_gap = 5*d-3*D
    assert prop_gap == 30 and 4**(3*S)*N**prop_gap > 16*A**(3*d)
    prop_margin = 87*prop_gap+3*(3*S)//5-2-3*d*13
    assert prop_margin == 2122
    assert N > 2*h*i*d and N > 2*h*5*d
    assert h <= 100 and N-h > 3_000_000_000
    # Strict boundaries: exp(10^6)-h>exp(999999), and the tail capacity
    # threshold is below exp(10^6)>2^1000000>10^300000.
    assert 2**999999 > h and 2**10 > 10**3 and cutoff < 300000
    output = dict(status='passed', exact_all_n_indices_added=[16],
        scope='Every integer 16<j<=n/2 satisfies the original common-prime conclusion p>=16',
        dependencies=[x[1] for x in inputs],
        six_exact_anchors=anchors, graph_edges_scale2000=edges,
        graph_exponent='2007/2000', orientations_checked=16384,
        minimum_vectors=[list(v) for v in sorted(vectors)],
        analytic_branches_scale2000=branches,
        i=i, h=h, m=m, b=b, d=d, S=S, D=D, c_i=c_i, A='15!',
        tail_integer_gap=gap, tail_cutoff_power=cutoff, tail_decimal_margin=margin,
        intermediate_integer_gap=prop_gap, intermediate_decimal_margin=prop_margin,
        finite_interval='n<=10^87', intermediate_interval='10^87<=n<exp(1000000)',
        infinite_interval='n>=exp(1000000)',
        finite_replay_independently_repeated_by='i3_attack, 2026-10-04: 4675 binomial checks, 6977 prefix tiles, 40 unchanged archive hashes',
        same_row_argument='max(a_p,a_q)>=sqrt(n-r)>(n-h)^lambda; every lambda<1/2',
        source_url='https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf',
        source_typo='Theorem2.4 final display repeats x1; Section7 proves the two-component minimum formulation',
        external_dependencies=['BFT Theorem2.1', 'BFT Proposition5.1',
            'BFT Theorem2.4 and Section7', 'BFT Lemmas5.2,5.4',
            'BFT Proposition5.3', 'BFT Proposition6.1'],
        external_theorems_reproved=False, problem699_fully_solved=False)
    dest = ROOT / 'data/results/verification_bft_i16_closeout_2026-10-04.json'
    dest.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('PASS i16 all n/all j: six exact anchors, 16384 orientations, six analytic branches, all three ranges')
    print(dict(graph='2007/2000', tail_cutoff_power=cutoff, tail_margin=margin,
               intermediate_margin=prop_margin))


if __name__ == '__main__':
    main()
