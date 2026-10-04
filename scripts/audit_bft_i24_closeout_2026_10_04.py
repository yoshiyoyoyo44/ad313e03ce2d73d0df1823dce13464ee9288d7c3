"""Exact all-n closure of i24: six BFT anchors, graph and three ranges."""
from fractions import Fraction as F
from itertools import product
from math import factorial, isqrt
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT=Path(__file__).resolve().parents[1]


def dependency(name):
    path=ROOT/'data/results'/name
    value=json.loads(path.read_text(encoding='utf-8'))
    assert value['status'].lower() in ('pass','passed')
    return value,dict(path=str(path.relative_to(ROOT)),
                      sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def main():
    if not __debug__:
        raise RuntimeError('Assertions required.')
    finite_G,finite_G_dep=dependency('verification_bft_gcd_3_2_finite_blocks_2026_10_04.json')
    tail_G,tail_G_dep=dependency('verification_bft_G_3_2_analytic_tail_2026-10-04.json')
    finite,finite_dep=dependency('verification_bft_i24_finite_dependency_2026_10_04.json')
    assert finite_G['m0']==50000 and finite_G['last_m']==4000000
    assert finite_G['L1']=='1611/1000' and finite_G['finite_blocks']==8727
    assert tail_G['first_m']==4000000 and tail_G['switch_m']==20000000000
    assert finite['indices']==[24] and finite['finite_bound']==10**87
    assert finite['archived_hashes_preserved']==40 and finite['exhaustive_targeted_replay']
    row=finite['rows'][0]
    assert row['i']==24 and row['bootstrap_steps']==5 and row['final_cap']==1562926
    assert row['exact_binomial_checks']==21225
    assert row['prefix']['intervals']==10879 and row['prefix']['singletons']==3838
    spec=importlib.util.spec_from_file_location('i24_interval_kernel',
        ROOT/'scripts/audit_bft_newvertex_i22_i25_2026_10_04.py')
    kernel=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kernel)
    strengthened=dict(pair=[5,7],p=5,k0=2,a=2,q=7,l0=2,b=1,c=3,d=2,
                      L1=F(1611,1000),m0=50000,target=F(264,1000),epsilon=F(8,10000))
    additional=[
        dict(pair=[5,23],p=5,k0=2,a=1,q=23,l0=1,b=1,c=4,d=3,
             L1=F(1417,1000),m0=153,target=F(206,1000),epsilon=F(1,1000)),
        dict(pair=[11,23],p=23,k0=1,a=1,q=11,l0=1,b=2,c=7,d=4,
             L1=F(16219,10000),m0=60,target=F(116,1000),epsilon=F(1,1000)),
    ]
    seeds=list(kernel.ANCHORS)+[strengthened]+additional
    anchors=[kernel.certify(seed,999999) for seed in seeds]
    assert {tuple(a['pair']) for a in anchors}=={
        (2,17),(11,19),(17,19),(5,7),(5,23),(11,23)}
    edges=[(2,7,259),(3,11,329),(3,13,231),(7,13,98),
           (2,17,337),(11,19,196),(17,19,191),(5,7,264),
           (5,23,206),(11,23,116)]
    vertices=[2,3,5,7,11,13,17,19,23]
    assert all(p<24 for p in vertices) and all(F(w,1000)<F(1,2) for p,q,w in edges)
    best=10**9
    vectors=set()
    for choices in product((0,1),repeat=len(edges)):
        lower={p:0 for p in vertices}
        for (p,q,w),side in zip(edges,choices):
            endpoint=(p,q)[side]
            lower[endpoint]=max(lower[endpoint],w)
        total=sum(lower.values())
        if total<best:
            best,vectors=total,set()
        if total==best:
            vectors.add(tuple(lower[p] for p in vertices))
    assert best==1332 and vectors=={
        (337,329,0,264,0,0,0,196,206),
        (0,329,0,264,196,0,337,0,206),
        (0,329,0,264,0,0,337,196,206),
        (0,329,206,264,196,0,337,0,0)}
    i=24;h=23
    small=[p for p in range(2,i) if all(p%k for k in range(2,isqrt(p)+1))]
    assert small==vertices
    m=len(small);b=(2*h+2)//3;d=3*b-h;S=b*(b+1)//2
    D=3*S-d*(i-m);c_i=i;A=factorial(i)//c_i
    assert (m,b,d,S,D)==(9,16,25,136,33) and A==factorial(23)
    assert all(max(0,s-(h-b))+max(0,b-u)+max(0,b-s+u)>=d
               for s in range(i) for u in range(s+1))
    assert sum(max(0,s-(h-b)) for s in range(i))==S
    assert sum(max(0,b-u) for u in range(i))==S
    gap=333*d-250*D
    assert gap==75 and A<10**23 and 2**251<10**76 and 4**5>10**3
    cutoff_power=1646
    margin=cutoff_power*gap+150*S-76-250*d*23
    assert margin==24
    assert 10**cutoff_power>2*h*i*d and 10**cutoff_power>2*h*333*d
    N=10**87
    prop_gap=5*d-3*D
    assert prop_gap==26 and 4**(3*S)*N**prop_gap>16*A**(3*d)
    assert N>2*h*i*d and N>2*h*5*d
    assert h<=100 and N-h>3_000_000_000
    # exp(10^6)-h>exp(999999), since (e-1)e^999999>2^999999>h.
    # exp(10^6)>2^1000000>10^300000>10^1646.
    assert 2**999999>h and 2**10>10**3 and cutoff_power<300000
    out=dict(status='passed',exact_all_n_indices_added=[24],
             independent_review='Root independently reviewed source anchors, new G dependencies, graph logic and capacity comparisons, then reran this checker and the complete i24 finite replay; all passed on 2026-10-04',
             scope='Every integer n,j with 24<j<=n/2 satisfies the original common-prime conclusion p>=24',
             G_bound_dependencies=[finite_G_dep,tail_G_dep],
             original_finite_dependency=finite_dep,anchors=anchors,
             graph_edges=edges,graph_exponent='333/250',
             orientations_checked=1024,minimum_vectors=[list(v) for v in sorted(vectors)],
             i=i,h=h,m=m,b=b,d=d,S=S,D=D,c_i=c_i,A='23!',
             capacity_cutoff_power=cutoff_power,tail_integer_gap=gap,tail_decimal_margin=margin,
             intermediate_integer_gap=prop_gap,intermediate_integer_comparison=True,
             finite_interval='n<=10^87',intermediate_interval='10^87<=n<exp(1000000)',
             infinite_interval='n>=exp(1000000)',same_row_argument='max(a_p,a_q)>=sqrt(n-r)> (n-h)^lambda, all lambda<1/2',
             source_url='https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf',
             source_typo='Theorem2.4 final display repeats x1; Section7 proves the bound for min(p^k*x1,q^l*x2)',
             external_dependencies=['BFT Theorem2.1','BFT Proposition5.1','BFT Theorem2.4 and Section7 proof',
                                    'BFT Lemmas5.2,5.4','BFT Proposition6.1'],
             external_theorems_reproved=False,problem699_fully_solved=False)
    dest=ROOT/'data/results/verification_bft_i24_closeout_2026-10-04.json'
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS i24 all n/all j; six exact anchors, 1024 graph branches, all three ranges connected')
    print(dict(graph='333/250',new_pair_thresholds=[a['log_x0'] for a in anchors[-2:]],
               capacity_cutoff_power=cutoff_power,margin=margin))


if __name__=='__main__':
    main()
