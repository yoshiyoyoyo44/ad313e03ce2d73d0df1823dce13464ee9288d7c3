"""Exact theta-block proof for G(4,3,3m-delta) >= 1.444^(3m).

Finite part only: 30000 < m <= 4000000, both deltas. The disjoint prime
intervals come from BFT Proposition 5.3; the analytic tail is separate.
A 4096-point mantissa table plus three exact correction terms speeds logs.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from time import perf_counter
from bisect import bisect_right
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
SCALE=2**64
M0=30_000
END=4_000_000
K=64
L=F(1444,1000)


def ceil_div(a,b):
    return -((-a)//b)


def atanh_bounds(a,b,terms,tail_upper_units):
    assert b<=a<=2*b and b>0
    zl=(a-b)*SCALE//(a+b);zh=ceil_div((a-b)*SCALE,a+b)
    z2l=zl*zl//SCALE;z2h=ceil_div(zh*zh,SCALE)
    pl,ph=zl,zh;low=high=0
    for k in range(terms):
        low+=pl//(2*k+1);high+=ceil_div(ph,2*k+1)
        pl=pl*z2l//SCALE;ph=ceil_div(ph*z2h,SCALE)
    return 2*low,2*high+tail_upper_units


def log_unit_bounds(a,b):
    return atanh_bounds(a,b,32,ceil_div(9*SCALE,260*3**65))


def log_table():
    return [log_unit_bounds(j,4096) for j in range(4096,8193)]


def integer_log(p,table):
    k=p.bit_length()-1
    j=(p*4096)//(1<<k)
    assert 4096<=j<8192
    a=p*4096;b=j*(1<<k)
    assert 1<=F(a,b)<1+F(1,4096)
    # z <= 1/8192: 2*z^7/(7*(1-z^2)) < 1/SCALE.
    assert 2*SCALE*8192**2 < 7*8192**7*(8192**2-1)
    low,high=atanh_bounds(a,b,3,1)
    core=table[j-4096];log2=table[-1]
    return core[0]+low+k*log2[0],core[1]+high+k*log2[1]


def primes_upto(cap):
    sieve=bytearray(b'\1')*(cap+1);sieve[:2]=b'\0\0'
    for p in range(2,isqrt(cap)+1):
        if sieve[p]:
            start=p*p
            sieve[start:cap+1:p]=b'\0'*((cap-start)//p+1)
    return [p for p in range(2,cap+1) if sieve[p]]


def main():
    if not __debug__:
        raise RuntimeError("Assertions required.")
    started=perf_counter();cap=(7*END-2)//2
    ps=primes_upto(cap);table=log_table()
    lo_prefix=[0];hi_prefix=[0]
    for j,p in enumerate(ps,1):
        low,high=integer_log(p,table)
        lo_prefix.append(lo_prefix[-1]+low);hi_prefix.append(hi_prefix[-1]+high)
        if j%200_000==0:
            print(f"Exact prime logarithms: {j}/{len(ps)}, {perf_counter()-started:.1f}s",flush=True)
    target_low,target_high=log_unit_bounds(L.numerator,L.denominator)
    assert M0+1>2*(7*(K-1)+6)
    lower=M0+1;minimum=None;worst=None;count=0
    while lower<=END:
        upper=min(END,lower+max(1,lower//2000))
        bound=0
        for w in range(K):
            for r,a in ((2,1),(4,2),(6,3)):
                x=(7*lower-2)//(7*w+r)
                y=(3*upper)//(3*w+a)
                if x>y:
                    right=bisect_right(ps,x);left=bisect_right(ps,y)
                    bound+=max(0,lo_prefix[right]-hi_prefix[left])
        margin=bound-3*upper*target_high
        assert margin>0,(lower,upper,margin)
        normalized=F(margin,3*upper*SCALE)
        if minimum is None or normalized<minimum:
            minimum=normalized;worst=[lower,upper]
        count+=1;lower=upper+1
    assert lower==END+1
    out=dict(status="PASS",c=4,d=3,L1=str(L),m0=M0,last_m=END,
        scope="Finite part only: 30000 < m <= 4000000, both delta=0 and delta=1",
        analytic_tail_required=True,finite_blocks=count,K=K,
        primes_sieved=len(ps),sieve_cap=cap,
        exact_log_scale_bits=64,core_atanh_terms=32,correction_atanh_terms=3,
        core_table_denominator=4096,correction_error_tail_units=1,
        minimum_normalized_margin_lower=str(minimum),worst_block=worst,
        target_log_interval=[target_low,target_high,SCALE],
        external_input="BFT Proposition 5.3 and disjointness of its prime intervals",
        source_url="https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf",
        delta_safe_endpoints="U=(7m-2)/(7w+r), V=3m/(3w+a), (r,a)=(2,1),(4,2),(6,3)",
        finite_block_rule="upper=min(4000000,lower+max(1,lower//2000)); next lower=upper+1",
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/"data/results/verification_bft_gcd_4_3_finite_blocks_2026_10_04.json").write_text(
        json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(f"PASS {count} exact blocks, worst={worst}, minimum={minimum}, {perf_counter()-started:.1f}s",flush=True)


if __name__=="__main__":
    main()
