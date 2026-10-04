"""Exact finite theta-block part of a strengthened BFT G(3,2,n) bound.

For 50000 < m <= 4000000 this verifies G(3,2,2m-delta)>1.611^(2m)
for both deltas, using the disjoint prime intervals of BFT Lemma 5.2.
The imported lemma and the analytic tail are not re-proved by this script.
No floating point logarithms enter the verification.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from time import perf_counter
from bisect import bisect_right
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
SCALE=2**64
M0=50_000
END=4_000_000
K=32
L=F(1611,1000)


def ceil_div(a,b):
    return -((-a)//b)


def log_unit_bounds(a,b):
    """Scaled log(a/b), 1 <= a/b <= 2, using 32 atanh terms."""
    assert b<=a<=2*b and b>0
    zl=(a-b)*SCALE//(a+b)
    zh=ceil_div((a-b)*SCALE,a+b)
    z2l=zl*zl//SCALE
    z2h=ceil_div(zh*zh,SCALE)
    pl,ph=zl,zh
    low=high=0
    for k in range(32):
        low+=pl//(2*k+1)
        high+=ceil_div(ph,2*k+1)
        pl=pl*z2l//SCALE
        ph=ceil_div(ph*z2h,SCALE)
    # z <= 1/3: exact tail upper 9/(260*3^65).
    return 2*low,2*high+ceil_div(9*SCALE,260*3**65)


LOG2=log_unit_bounds(2,1)


def integer_log(p):
    assert p>=1
    k=p.bit_length()-1
    low,high=log_unit_bounds(p,1<<k)
    return low+k*LOG2[0],high+k*LOG2[1]


def primes_upto(cap):
    # Ordinary Eratosthenes sieve; every composite has a prime divisor
    # <= sqrt(cap). Bytearray slicing clears the entire multiple list.
    sieve=bytearray(b'\1')*(cap+1)
    sieve[:2]=b'\0\0'
    for p in range(2,isqrt(cap)+1):
        if sieve[p]:
            start=p*p
            sieve[start:cap+1:p]=b'\0'*((cap-start)//p+1)
    return [p for p in range(2,cap+1) if sieve[p]]


def main():
    if not __debug__:
        raise RuntimeError('Assertions required.')
    started=perf_counter()
    cap=(5*END-2)//2
    ps=primes_upto(cap)
    lo_prefix=[0]
    hi_prefix=[0]
    for j,p in enumerate(ps,1):
        low,high=integer_log(p)
        lo_prefix.append(lo_prefix[-1]+low)
        hi_prefix.append(hi_prefix[-1]+high)
        if j%100_000==0:
            print(f'Exact prime logarithms: {j}/{len(ps)}, {perf_counter()-started:.1f}s',flush=True)
    target_low,target_high=log_unit_bounds(L.numerator,L.denominator)
    assert M0+1>2*(5*(K-1)+4)
    lower=M0+1
    minimum=None
    worst=None
    count=0
    while lower<=END:
        upper=min(END,lower+max(1,lower//2000))
        bound=0
        for k in range(K):
            for t,numerator,denominator in ((5*k+2,2,2*k+1),(5*k+4,1,k+1)):
                x=(5*lower-2)//t
                y=numerator*upper//denominator
                if x>y:
                    right=bisect_right(ps,x)
                    left=bisect_right(ps,y)
                    # The lower prefix at the right endpoint and upper
                    # prefix at the left give a valid lower enclosure.
                    value=lo_prefix[right]-hi_prefix[left]
                    bound+=max(0,value)
        margin=bound-2*upper*target_high
        assert margin>0,(lower,upper,margin)
        normalized=F(margin,2*upper*SCALE)
        if minimum is None or normalized<minimum:
            minimum=normalized
            worst=[lower,upper]
        count+=1
        lower=upper+1
    assert lower==END+1
    out=dict(status='PASS',c=3,d=2,L1=str(L),m0=M0,
             scope='Finite part only: 50000 < m <= 4000000, both delta=0 and delta=1',
             analytic_tail_required=True,finite_blocks=count,last_m=END,
             primes_sieved=len(ps),sieve_cap=cap,K=K,
             exact_log_scale_bits=64,atanh_terms=32,
             logarithm_error_tail='9/(260*3^65)',
             minimum_normalized_margin_lower=str(minimum),worst_block=worst,
             target_log_interval=[target_low,target_high,SCALE],
             external_input='BFT Lemma 5.2 and disjointness of its prime intervals',
             source_url='https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf',
             delta_safe_endpoints='U=(5m-2)/t, V=2m/(2k+1) for t=5k+2; V=m/(k+1) for t=5k+4',
             finite_block_rule='upper=min(4000000, lower+max(1,lower//2000)); next lower=upper+1',
             script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    dest=ROOT/'data/results/verification_bft_gcd_3_2_finite_blocks_2026_10_04.json'
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {count} exact finite blocks, minimum={minimum}, {perf_counter()-started:.1f}s',flush=True)


if __name__=='__main__':
    main()
