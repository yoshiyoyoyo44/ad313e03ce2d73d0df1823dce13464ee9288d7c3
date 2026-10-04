"""Exact analytic tail of a strengthened BFT G(3,2,n) lower bound.

The external BFT Lemmas 5.2--5.4 are explicit dependencies.
This script proves all m>=4,000,000, both n=2m and n=2m-1.
The finite interval 50,001<=m<4,000,000 is a separate obligation.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rational_interval_kernel',
    ROOT/'scripts/audit_bft_newvertex_i22_i25_2026_10_04.py')
kernel=importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)
I=kernel.I


def main():
    K=32
    intervals=[]
    for k in range(K+1):
        for r in (2,4):
            t=5*k+r
            v=F(2,2*k+1) if r==2 else F(1,k+1)
            u=F(5,t)
            assert u>v
            # For m>=2t, the floor identities in BFT (5.8) give these
            # two actual lower endpoints. The chosen v*m dominates both.
            for delta in (0,1):
                # Compare affine polynomials at m=2t, where all relevant
                # floors are fixed. They then keep their slope ordering.
                first_slope=F(2,2*k+1 if r==2 else 2*k+2)
                first_constant=F(-delta,2*k+1 if r==2 else 2*k+2)
                second_slope=F(1,k+1)
                second_constant=F(delta-1,k+1)
                assert v>=first_slope and v>=second_slope
                assert (v-first_slope)*(2*t)>=first_constant
                assert (v-second_slope)*(2*t)>=second_constant
            intervals.append((t,u,v))
    H=sum(u-v for t,u,v in intervals)/2
    A=sum(F(1,t) for t,u,v in intervals)
    C=sum(u+v for t,u,v in intervals)/2
    B=I(F(2072,1000))/2*sum((I(F(5,t)).root(2) for t,u,v in intervals),I(0))
    log_target=kernel.logarithm(F(1611,1000))
    first_m=4000000
    switch_m=20000000000
    # First range: all upper/lower endpoints <=1e11, so no relative loss.
    assert first_m>=2*max(t for t,u,v in intervals)
    assert max(u for t,u,v in intervals)*switch_m<=10**11
    assert max(v for t,u,v in intervals)*switch_m<=10**11
    first_lower=I(H)-I(A)/first_m-B/I(first_m).root(2)
    assert first_lower.lo>log_target.hi
    # Second range: all endpoints >=1e8, so no square-root loss.
    eta=F(213,1000000)
    assert min(v for t,u,v in intervals)*switch_m>10**8
    assert min(u for t,u,v in intervals)*switch_m-2>10**8
    second_lower=I(H-eta*C)-I((1-eta)*A)/switch_m
    assert second_lower.lo>log_target.hi
    output=dict(status='passed',reviewer='global_audit',
        theorem='G(3,2,2m-delta)>=(1611/1000)^(2m), delta=0,1, every m>=4000000',
        K=K,number_of_disjoint_prime_intervals=len(intervals),
        first_m=first_m,switch_m=switch_m,
        H=I(H).record(),constant_remainder_A=I(A).record(),
        sqrt_remainder_B=B.record(),relative_error_coefficient_C=I(C).record(),
        log_target=log_target.record(),first_range_lower=first_lower.record(),
        second_range_lower=second_lower.record(),
        external_dependencies=['BFT Lemma5.2 and floor identities5.8',
                               'BFT Lemma5.4'],
        finite_range_50001_to_3999999_closed_here=False,
        claim_all_m_above_50000=False)
    dest=ROOT/'data/results/verification_bft_G_3_2_analytic_tail_2026-10-04.json'
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
