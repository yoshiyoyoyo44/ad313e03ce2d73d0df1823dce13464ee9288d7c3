"""Exact closure of i19 with a newly certified G(3,2,n) bound."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from math import factorial
import importlib.util
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]


def read_result(name):
    p=ROOT/'data/results'/name
    obj=json.loads(p.read_text(encoding='utf-8'))
    assert obj['status'].lower()=='pass' or obj['status']=='passed'
    return obj,dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())


def main():
    if not __debug__:
        raise RuntimeError('Assertions required.')
    finite,finite_dep=read_result('verification_bft_gcd_3_2_finite_blocks_2026_10_04.json')
    tail,tail_dep=read_result('verification_bft_G_3_2_analytic_tail_2026-10-04.json')
    old,old_dep=read_result('verification_bft_i19_finite_dependency_2026_10_04.json')
    assert finite['m0']==50000 and finite['last_m']==4000000
    assert finite['L1']=='1611/1000' and finite['finite_blocks']==8727
    assert tail['first_m']==4000000 and tail['switch_m']==20000000000
    assert old['indices']==[19] and old['finite_bound']==10**87
    assert old['archived_hashes_preserved']==40 and old['exhaustive_targeted_replay']
    spec=importlib.util.spec_from_file_location('interval_kernel',
        ROOT/'scripts/audit_bft_newvertex_i22_i25_2026_10_04.py')
    kernel=importlib.util.module_from_spec(spec);spec.loader.exec_module(kernel)
    seed=dict(pair=[5,7],p=5,k0=2,a=2,q=7,l0=2,b=1,c=3,d=2,
              L1=F(1611,1000),m0=50000,target=F(264,1000),epsilon=F(8,10000))
    new_anchor=kernel.certify(seed,999999)
    old_anchor=kernel.certify(kernel.ANCHORS[0])
    # These six old edges and two new edges already suffice.
    edges=[(2,7,259),(3,11,329),(5,13,163),(3,13,231),
           (7,13,98),(5,11,199),(5,7,264),(2,17,337)]
    vertices=[2,3,5,7,11,13,17]
    best=10**9;vectors=set()
    for choices in product((0,1),repeat=len(edges)):
        v={p:0 for p in vertices}
        for (p,q,weight),choice in zip(edges,choices):
            endpoint=(p,q)[choice]
            v[endpoint]=max(v[endpoint],weight)
        total=sum(v.values())
        if total<best:best=total;vectors=set()
        if total==best:vectors.add(tuple(v[p] for p in vertices))
    assert best==1028 and vectors=={(337,329,264,0,0,98,0),
                                  (337,329,264,98,0,0,0)}
    branches=[337+259+329+163,337+329+264+231,
              337+329+264+98,337+329+264+199]
    assert branches==[1088,1161,1028,1129]
    i=19;h=18;m=7;d=18;S=78;D=18
    A=factorial(i)  # i19 is prime, so c_i=1.
    assert D==3*S-d*(i-m)
    assert all(max(0,s-(h-12))+max(0,12-u)+max(0,12-s+u)>=d
               for s in range(i) for u in range(s+1))
    exponent=F(257,250);gap=257*d-250*D
    e=18
    assert A<10**e and 2**251<10**76 and 4**5>10**3
    margin=1000*gap+150*S-76-250*d*e
    assert gap==126 and margin==56624
    assert 10**1000>2*h*257*d and 10**1000>2*h*i*d
    assert 4**(3*S)*(10**87)**(5*d-3*D)>16*A**(3*d)
    assert 10**87>2*h*5*d and 10**87>2*h*i*d
    out=dict(status='passed',exact_all_n_indices_added=[19],
             new_G_lower_bound='G(3,2,2m-delta)>(1611/1000)^(2m), delta=0,1, every m>50000',
             G_bound_dependencies=[finite_dep,tail_dep],
             finite_original_problem_dependency=old_dep,
             anchors=[old_anchor,new_anchor],graph_edges=edges,
             graph_exponent=str(exponent),minimum_vectors=[list(v) for v in sorted(vectors)],
             orientations_checked=2**len(edges),analytic_branches=branches,
             i=i,h=h,m=m,d=d,S=S,D=D,c_i=1,
             tail_integer_gap=gap,tail_decimal_margin=margin,
             intermediate_interval='10^87 <= n < exp(1000000)',
             infinite_interval='n >= exp(1000000)',
             source_url='https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf',
             external_dependencies=['BFT Theorem2.1','BFT Theorem2.4 and Section7 proof',
                                    'BFT Lemmas5.2,5.4','BFT Proposition6.1'],
             external_theorems_reproved=False)
    dest=ROOT/'data/results/verification_bft_strengthened_gcd_i19_2026_10_04.json'
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS i19 all n/all j; new G lower bound, exact anchors, graph, all three ranges connected')
    print(dict(graph=str(exponent),log_x0=new_anchor['log_x0'],margin=margin))


if __name__=='__main__':main()
