"""Exact finite prime-interval certificate for G(19,14,n), L1=1.444.

Only BFT Lemma5.2 / its floor identities are imported mathematics.
Grid logarithms and a two-term Taylor enclosure use integers only.
--quick checks feasibility up to m=20000 and writes no theorem result.
"""
from array import array
from bisect import bisect_right
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from time import perf_counter
import hashlib,json,sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_bft_gcd_3_2_finite_blocks_2026_10_04 import log_unit_bounds

ROOT=Path(__file__).resolve().parents[1]
C,D=19,14
L=F(1444,1000)
M0=6000
END=4_000_000
T=512
SCALE=2**32
SHIFT=2**32


def ceil_div(a,b):return -((-a)//b)


def grid_log_bounds():
    grid=[]
    for g in range(1024,2049):
        low,high=log_unit_bounds(g,1024)
        grid.append((low//SHIFT,ceil_div(high,SHIFT)))
    return grid


def integer_log_grid(p,grid):
    k=p.bit_length()-1
    norm=1<<k
    g=(p<<10)//norm
    # p/2^k = (g/1024)*(1+t), 0<=t<1/1024.
    numerator=(p<<10)-norm*g
    denominator=norm*g
    tl=numerator*SCALE//denominator
    th=ceil_div(numerator*SCALE,denominator)
    # Alternating Taylor series: t-t^2/2 <= log(1+t)
    # <= t-t^2/2+t^3/3. SCALE/(3*1024^3) < 2.
    lower=tl-ceil_div(th*th,2*SCALE)
    upper=th-(tl*tl)//(2*SCALE)+2
    gl,gh=grid[g-1024]
    l2,h2=grid[-1]
    return k*l2+gl+lower,k*h2+gh+upper


def primes_upto(cap):
    sieve=bytearray(b'\1')*(cap+1)
    sieve[:2]=b'\0\0'
    for p in range(2,isqrt(cap)+1):
        if sieve[p]:
            start=p*p
            sieve[start:cap+1:p]=b'\0'*((cap-start)//p+1)
    ps=array('I',(p for p in range(2,cap+1) if sieve[p]))
    assert ps.itemsize==4
    return ps


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    quick='--quick' in sys.argv
    end=20000 if quick else END
    started=perf_counter()
    # Integer residues with {d*t/(c+d)}>1/2 are precisely the valid t.
    coeffs=[]
    for t in range(1,T+1):
        if 2*((D*t)%(C+D))<=C+D:continue
        assert (2*(D*t//(C+D))+(C-D)*t//(C+D))==t-2
        beta=max(F(D,D*t//(C+D)+1),F(C-D,(C-D)*t//(C+D)+1))
        assert F(C+D,t)>beta
        coeffs.append((t,beta.numerator,beta.denominator))
    assert M0+1>2*T
    cap=((C+D)*end-2)//min(t for t,_,_ in coeffs)
    ps=primes_upto(cap)
    print(f'Sieve: {len(ps)} primes <= {cap}, {perf_counter()-started:.1f}s',flush=True)
    grid=grid_log_bounds()
    lo=array('Q',[0]);hi=array('Q',[0])
    assert lo.itemsize==8
    for j,p in enumerate(ps,1):
        low,high=integer_log_grid(p,grid)
        lo.append(lo[-1]+low);hi.append(hi[-1]+high)
        if j%500000==0:print(f'Exact grid logarithms: {j}/{len(ps)}, {perf_counter()-started:.1f}s',flush=True)
    target_low64,target_high64=log_unit_bounds(L.numerator,L.denominator)
    target_high=ceil_div(target_high64,SHIFT)
    lower=M0+1;minimum=None;worst=None;count=0;failed=[]
    while lower<=end:
        upper=min(end,lower+max(1,lower//2000))
        bound=0
        for t,a,b in coeffs:
            x=((C+D)*lower-2)//t
            y=a*upper//b
            if x>y:
                value=lo[bisect_right(ps,x)]-hi[bisect_right(ps,y)]
                bound+=max(0,value)
        margin=bound-D*upper*target_high
        if not quick:assert margin>0,(lower,upper,margin)
        elif margin<=0:failed.append([lower,upper])
        normalized=F(margin,D*upper*SCALE)
        if minimum is None or normalized<minimum:minimum=normalized;worst=[lower,upper]
        count+=1;lower=upper+1
    assert lower==end+1
    print(f'{"DIAGNOSTIC" if quick else "PASS"} {count} blocks; min={minimum}, worst={worst}, {perf_counter()-started:.1f}s',flush=True)
    if quick:
        print('failed blocks',failed[:20],'total',len(failed),'last',failed[-1:] if failed else [])
        return
    out=dict(status='PASS',c=C,d=D,L1=str(L),m0=M0,last_m=END,
             scope='Finite part only, m0<m<=4000000, delta=0,1',analytic_tail_required=True,
             valid_t_max=T,number_of_disjoint_prime_intervals=len(coeffs),finite_blocks=count,
             primes_sieved=len(ps),sieve_cap=cap,exact_log_scale_bits=32,
             grid_scale=1024,grid_logs_64bit_atanh_terms=32,
             small_log_taylor='t-t^2/2 <= log(1+t) <= t-t^2/2+t^3/3, 0<=t<1/1024',
             minimum_normalized_margin_lower=str(minimum),worst_block=worst,
             delta_safe_endpoints='U=((c+d)m-2)/t, V=m*max(d/(floor(dt/(c+d))+1),(c-d)/(floor((c-d)t/(c+d))+1))',
             finite_block_rule='upper=min(4000000,lower+max(1,lower//2000)); next lower=upper+1',
             external_input='BFT Lemma5.2 and floor identities5.8',
             script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    dest=ROOT/'data/results/verification_bft_gcd_19_14_finite_blocks_2026_10_04.json'
    dest.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
