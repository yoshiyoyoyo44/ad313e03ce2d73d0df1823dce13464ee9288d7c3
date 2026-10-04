"""New universal G(10,7,n) bound and explicit (2,13)/(11,13) edges.

Uses BFT Lemma 5.2, floor identities (5.8), interval disjointness, and
Lemma 5.4 as external inputs. Finite blocks and analytic tails are exact.
This script does not itself close an index of the original problem.
"""
from fractions import Fraction as F
from bisect import bisect_right
from pathlib import Path
from time import perf_counter
import hashlib,json
from audit_bft_gcd_4_3_finite_blocks_2026_10_04 import (
    primes_upto,log_table,integer_log,log_unit_bounds,SCALE)
from audit_bft_newvertex_i22_i25_2026_10_04 import I,logarithm,certify

ROOT=Path(__file__).resolve().parents[1]
C,D=10,7
L=F(149,100)
M0=12000
END=2000000
SWITCH=10000000000


def intervals(T):
    out=[]
    for t in range(1,T+1):
        if 2*((D*t)%(C+D))<=C+D:
            continue
        v=max(F(D,(D*t)//(C+D)+1),F(C-D,((C-D)*t)//(C+D)+1))
        u=F(C+D,t)
        assert u>v
        out.append((t,u,v))
    return out


def main():
    if not __debug__:
        raise RuntimeError('Assertions required.')
    started=perf_counter()
    finite_T=512
    parts=intervals(finite_T)
    assert M0+1>2*finite_T and len(parts)==241
    cap=((C+D)*END-2)//min(t for t,u,v in parts)
    ps=primes_upto(cap)
    table=log_table()
    lop=[0];hip=[0]
    for j,p in enumerate(ps,1):
        low,high=integer_log(p,table)
        lop.append(lop[-1]+low);hip.append(hip[-1]+high)
        if j%200000==0:
            print(f'Exact prime logs {j}/{len(ps)}, {perf_counter()-started:.1f}s',flush=True)
    log_low,log_high=log_unit_bounds(L.numerator,L.denominator)
    a=M0+1;minimum=None;worst=None;blocks=0
    while a<=END:
        b=min(END,a+max(1,a//4000))
        bound=0
        for t,u,v in parts:
            x=((C+D)*a-2)//t
            y=b*v.numerator//v.denominator
            if x>y:
                right=bisect_right(ps,x);left=bisect_right(ps,y)
                bound+=max(0,lop[right]-hip[left])
        margin=bound-D*b*log_high
        assert margin>0,(a,b,margin)
        normalized=F(margin,D*b*SCALE)
        if minimum is None or normalized<minimum:
            minimum=normalized;worst=[a,b]
        a=b+1;blocks+=1
    assert a==END+1 and blocks==19840
    # Analytic first domain uses theta(x)>x-2.072sqrt(x), theta(x)<x.
    tail_T=128
    parts=intervals(tail_T)
    H=sum((u-v for t,u,v in parts),F(0))/D
    A=sum((F(2,t) for t,u,v in parts),F(0))/D
    B=F(259,125*D)*sum((I(u).root(2) for t,u,v in parts),I(0))
    target=logarithm(L)
    assert END>2*tail_T
    for t,u,v in parts:
        assert u*SWITCH<=10**11 and v*SWITCH<=10**11
        assert u*END-F(2,t)>1 and v*END>1
    first=I(H)-A/END-B/I(END).root(2)
    assert first.lo>target.hi
    # The unbounded second domain uses only the relative theta bound.
    eta=F(213,1000000)
    V=sum((u+v for t,u,v in parts),F(0))/D
    for t,u,v in parts:
        assert u*SWITCH-F(2,t)>=10**8 and v*SWITCH>=10**8
    second=I(H-eta*V-(1-eta)*A/SWITCH)
    assert second.lo>target.hi
    seeds=[
        dict(pair=[2,13],p=2,k0=9,a=1,q=13,l0=2,b=3,c=C,d=D,
             L1=L,m0=M0,target=F(73,1000),epsilon=F(3,10000)),
        dict(pair=[11,13],p=13,k0=1,a=1,q=11,l0=1,b=1,c=C,d=D,
             L1=L,m0=M0,target=F(61,1000),epsilon=F(3,10000)),
    ]
    anchors=[certify(seed,999999) for seed in seeds]
    output=dict(status='PASS',c=C,d=D,L1=str(L),m0=M0,
        universal_G_statement='G(10,7,7m-delta)>(149/100)^(7m), every integer m>12000, delta=0,1',
        finite_range=[M0+1,END],finite_T=finite_T,
        finite_blocks=blocks,prime_count=len(ps),sieve_cap=cap,
        exact_log_scale_bits=64,
        minimum_normalized_margin_lower=str(minimum),worst_block=worst,
        analytic_T=tail_T,first_domain=[END,SWITCH],second_domain_lower=SWITCH,
        first_lower=first.record(),second_lower=second.record(),log_target=target.record(),
        anchors=anchors,original_problem_all_n_indices_added=[],
        delta_safe_endpoints='U=((c+d)m-2)/t; V=m*max(d/(floor(dt/(c+d))+1),(c-d)/(floor((c-d)t/(c+d))+1))',
        external_dependencies=['BFT Lemma5.2 and floor identities5.8','BFT prime interval disjointness',
                               'BFT Lemma5.4','BFT Theorem2.4 and Section7 proof'],
        source_url='https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    dest=ROOT/'data/results/verification_bft_gcd_10_7_and_two_anchors_2026_10_04.json'
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS universal G10/7 and two exact anchors, {blocks} blocks, {perf_counter()-started:.1f}s',flush=True)
    print(dict(first=first.record(),second=second.record(),minimum=str(minimum)))


if __name__=='__main__':main()
