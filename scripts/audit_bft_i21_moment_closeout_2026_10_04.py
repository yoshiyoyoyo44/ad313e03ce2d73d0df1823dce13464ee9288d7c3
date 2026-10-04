"""Exact i21 closeout using distinct maximum rows and a position moment.

The published G and BFT anchor inputs are read without rewriting them.
All 17-edge orientations and all 28 possible maximum-row collisions are
checked with integers.  The finite i21 input has its own fresh replay.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
VERTICES = [2, 3, 5, 7, 11, 13, 17, 19]
SCALE = 2000
EDGES = [(2,3,570),(2,5,516),(2,7,546),(2,11,118),(2,13,146),
         (3,5,432),(3,7,76),(3,11,688),(3,13,462),(5,7,528),
         (5,11,398),(5,13,326),(7,13,245),(11,13,122),
         (2,17,674),(11,19,392),(17,19,382)]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dependency(name):
    path = ROOT / 'data/results' / name
    value = json.loads(path.read_text(encoding='utf-8'))
    assert value['status'].lower() in ('pass', 'passed')
    return value, dict(path=path.relative_to(ROOT).as_posix(), sha256=digest(path))


def verify_graph():
    assert all(0 < w < SCALE//2 for p,q,w in EDGES)
    assert len(EDGES) == 17
    index = {p:k for k,p in enumerate(VERTICES)}
    indexed = [(index[p],index[q],w) for p,q,w in EDGES]
    pairs = list(combinations(range(8),2))
    collision = {pq:10**9 for pq in pairs}
    vectors = set()
    for choices in product((0,1), repeat=17):
        v = [0]*8
        for (p,q,w),side in zip(indexed,choices):
            k = (p,q)[side]
            v[k] = max(v[k],w)
        vectors.add(tuple(v))
    total_min = min(map(sum,vectors))
    moment_min = 10**9
    best_moment = set()
    for v in vectors:
        total = sum(v)
        for p,q in pairs:
            collision[p,q] = min(collision[p,q],
                total + max(0,SCALE-v[p]-v[q]))
        score = sum((28-k)*w for k,w in enumerate(sorted(v))) + SCALE*28
        if score < moment_min:
            moment_min, best_moment = score, {v}
        elif score == moment_min:
            best_moment.add(v)
    assert len(vectors) == 2631
    assert total_min == 2527
    assert min(collision.values()) == 3165
    assert all(value >= 3000 for value in collision.values())
    assert moment_min == 112953
    assert best_moment == {(674,688,528,0,0,245,0,392)}
    # Rearrangement requires 1-lambda>0, and d-r>0 for every actual row.
    assert all(max(v) < SCALE for v in vectors)
    assert 28 > 20
    return dict(orientations=2**17, distinct_lower_vectors=len(vectors),
        product_minimum=str(F(total_min,SCALE)),
        collision_minimum=str(F(min(collision.values()),SCALE)),
        collision_pair_minima={f'{VERTICES[p]},{VERTICES[q]}':str(F(value,SCALE))
                              for (p,q),value in collision.items()},
        moment_minimum=str(F(moment_min,SCALE)),
        unique_minimum_vector_scale2000=list(next(iter(best_moment))))


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled.')
    published, published_dep = dependency('verification_bft_i16_closeout_2026-10-04.json')
    assert published['exact_all_n_indices_added'] == [16]
    assert published['orientations_checked'] == 16384
    assert published['graph_exponent'] == '2007/2000'
    # Pin every G input and independent audit recorded by the published proof.
    for entry in published['dependencies']:
        path = ROOT / entry['path']
        assert digest(path) == entry['sha256'], entry['path']
        record = json.loads(path.read_text(encoding='utf-8'))
        assert record['status'].lower() in ('pass','passed')
    kernel_path = ROOT/'scripts/audit_bft_newvertex_i22_i25_2026_10_04.py'
    spec = importlib.util.spec_from_file_location('i21_bft_interval_kernel',kernel_path)
    kernel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kernel)
    seeds = [
        dict(pair=[2,7],p=2,k0=3,a=1,q=7,l0=1,b=1,c=25,d=17,
             L1=F(777,500),m0=582,target=F(273,1000),epsilon=F(1,2500)),
        dict(pair=[3,11],p=3,k0=5,a=1,q=11,l0=2,b=2,c=19,d=14,
             L1=F(361,250),m0=6000,target=F(43,125),epsilon=F(3,20000)),
        dict(pair=[5,7],p=5,k0=2,a=2,q=7,l0=2,b=1,c=3,d=2,
             L1=F(1611,1000),m0=50000,target=F(33,125),epsilon=F(1,1250)),
        dict(pair=[7,13],p=7,k0=3,a=1,q=13,l0=2,b=2,c=4,d=3,
             L1=F(361,250),m0=30000,target=F(49,400),epsilon=F(1,10000)),
        dict(pair=[2,13],p=2,k0=9,a=1,q=13,l0=2,b=3,c=10,d=7,
             L1=F(149,100),m0=12000,target=F(73,1000),epsilon=F(3,10000)),
        dict(pair=[11,13],p=13,k0=1,a=1,q=11,l0=1,b=1,c=10,d=7,
             L1=F(149,100),m0=12000,target=F(61,1000),epsilon=F(3,10000)),
    ]
    anchors = [kernel.certify(seed,999999) for seed in seeds]
    assert anchors == published['six_exact_anchors']
    newvertex, newvertex_dep = dependency('verification_bft_newvertex_i22_i25_2026_10_04.json')
    vertex_anchors = [kernel.certify(seed,999999) for seed in kernel.ANCHORS]
    # Only the requested safe-threshold label changes. Compare all actual
    # interval certificates to the independently audited published input.
    for current, saved in zip(vertex_anchors,newvertex['anchors']):
        assert current['upper_log_threshold'] == 999999
        assert saved['upper_log_threshold'] == 500000
        assert {k:v for k,v in current.items() if k!='upper_log_threshold'} == {
            k:v for k,v in saved.items() if k!='upper_log_threshold'}
    assert {tuple(v['pair']) for v in vertex_anchors} == {(2,17),(11,19),(17,19)}
    anchors.extend(vertex_anchors)
    finite, finite_dep = dependency('verification_bft_i21_finite_dependency_2026_10_04.json')
    assert finite['indices'] == [21] and finite['finite_bound'] == 10**87
    assert finite['archived_hashes_preserved'] == 40
    assert finite['exhaustive_targeted_replay']
    row = finite['rows'][0]
    assert (row['i'],row['bootstrap_steps'],row['final_cap']) == (21,5,1259176)
    assert row['exact_binomial_checks'] == 14755
    assert row['prefix']['intervals'] == 9427 and row['prefix']['singletons'] == 2604
    assert row['prefix']['upper'] == 1999999
    graph = verify_graph()
    i,h,m,b,d,S,D = 21,20,8,14,22,105,29
    A = factorial(20)
    assert factorial(i)//i == A and A < 10**19
    assert 3*b-h == d and b*(b+1)//2 == S
    assert 3*S-d*(i-m) == D
    assert all(max(0,s-(h-b))+max(0,b-u)+max(0,b-s+u) >= d
               for s in range(i) for u in range(s+1))
    assert sum(max(0,s-(h-b)) for s in range(i)) == S
    moment_d = 28
    H = i*h//2 + 2*S - moment_d*(i-m)
    assert H == 56 and moment_d == 2*b
    assert all(s+max(0,b-u)+max(0,b-s+u) >= moment_d
               for s in range(i) for u in range(s+1))
    assert sum(range(i)) == 210
    assert sum(max(0,b-u) for u in range(i)) == S
    # Integer decimal certificates, with a single Bernoulli loss after raising.
    assert 4**5 > 10**3
    collision_power, collision_gap = 100, 2*d*F(3,2)-2*D
    assert collision_gap == 8
    collision_bernoulli = 3*d + 2*i*d
    collision_margin = collision_power*8 + (2*S//5)*3 - 1 - 2*d*19
    assert collision_bernoulli == 990 and collision_margin == 89
    assert 10**collision_power > 2*h*collision_bernoulli
    moment_power = 1000
    moment_gap = 112953 - SCALE*H
    moment_bernoulli = 112953 + SCALE*i*moment_d
    moment_margin = moment_power*moment_gap + (SCALE*S//5)*3 - 1 - SCALE*moment_d*19
    assert moment_gap == 953 and moment_bernoulli == 1288953
    assert moment_margin == 14999
    assert 10**moment_power > 2*h*moment_bernoulli
    intermediate_gap = 5*d-3*D
    intermediate_bernoulli = 5*d+3*i*d
    intermediate_margin = 87*intermediate_gap+(3*S//5)*3-1-3*d*19
    assert intermediate_gap == 23 and intermediate_bernoulli == 1496
    assert intermediate_margin == 935
    assert 10**87 > 2*h*intermediate_bernoulli
    assert h <= 100 and 10**87-h > 3_000_000_000
    assert 2**999999 > h and 2**10 > 10**3 and moment_power < 300000
    out = dict(status='passed', exact_all_n_indices_added=[21],
        independent_review='Root independently reviewed the numerical Kummer argument, all collision and rearrangement bounds, exact constants and strict range joins, and replayed this checker and finite input; i3_attack independently replayed the finite input and separately audited the graph and position-moment proof before source completion',
        scope='Every integer 21<j<=n/2 satisfies the original common-prime conclusion p>=21',
        dependencies=[published_dep,newvertex_dep,finite_dep],
        recertified_nine_anchors=anchors, graph_edges_scale2000=EDGES,
        graph=graph, i=i,h=h,m=m,c_i=21,A='20!',
        uniform_capacity=dict(b=b,d=d,S=S,D=D,beta='29/22'),
        moment_capacity=dict(b=b,d=moment_d,S=S,H=H,
            lower_exponent='112953/2000',integer_gap=moment_gap,
            bernoulli_exponent=moment_bernoulli,cutoff_power=moment_power,
            decimal_margin=moment_margin),
        collision_capacity=dict(lower_exponent_used='3/2',cutoff_power=collision_power,
            integer_gap=8,bernoulli_exponent=collision_bernoulli,decimal_margin=collision_margin),
        intermediate_capacity=dict(product_exponent='5/3',integer_gap=intermediate_gap,
            bernoulli_exponent=intermediate_bernoulli,decimal_margin=intermediate_margin),
        finite_interval='n<=10^87',intermediate_interval='10^87<=n<exp(1000000)',
        infinite_interval='n>=exp(1000000)',
        rearrangement='All orientation lower levels are <1; among distinct rows the minimum is rows 0..7 assigned ascending levels. Actual log(a_p)/log(Z) need not be <=1.',
        numerical_Kummer_used=True, complete_polynomial_allocation_assumed=False,
        source_url='https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf',
        problem699_fully_solved=False)
    dest = ROOT/'data/results/verification_bft_i21_moment_closeout_2026-10-04.json'
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS i21: 131072 graph directions, all 28 collisions, position moment and all three ranges')
    print(dict(moment='112953/2000 > 56', gap='953/2000', finite_binomial_checks=14755,
               tail_decimal_margin=moment_margin, intermediate_decimal_margin=intermediate_margin))


if __name__ == '__main__':
    main()
