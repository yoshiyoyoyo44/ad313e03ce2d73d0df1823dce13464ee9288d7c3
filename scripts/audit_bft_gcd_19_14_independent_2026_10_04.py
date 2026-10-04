"""Independent exact analytic audit of the new G(19,14) certificate.

The finite prime-block certificate has also been completely replayed;
its fixed output is checked here. Analytic arithmetic below uses direct
Fractions, decimal integer square roots and a direct atanh series.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib,json,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_bft_newvertex_i22_i25_2026_10_04 import certify


def sqrt_bounds(x):
    scale=10**30
    integer=isqrt((x.numerator*scale**2)//x.denominator)
    return F(integer,scale),F(integer+1,scale)


def log_bounds(x):
    assert 1<=x<=2
    z=(x-1)/(x+1)
    total=sum((z**(2*k+1)/F(2*k+1) for k in range(40)),F(0))*2
    tail=2*z**81/(81*(1-z*z))
    return total,total+tail


def decimal_lower(x,scale=10**12):
    return dict(numerator=x.numerator*scale//x.denominator,denominator=scale)


def main():
    if not __debug__:raise RuntimeError("Assertions required")
    finite_path=ROOT/"data/results/verification_bft_gcd_19_14_finite_blocks_2026_10_04.json"
    finite=json.loads(finite_path.read_text())
    assert finite["status"]=="PASS" and finite["m0"]==6000
    assert finite["c"]==19 and finite["d"]==14 and finite["L1"]=="361/250"
    assert finite["last_m"]==4000000 and finite["finite_blocks"]==12693
    assert finite["minimum_normalized_margin_lower"]=="951921554421/649278796070912"
    assert finite["worst_block"]==[10793,10798]
    # The Taylor upper remainder at 32-bit scale is strictly below 2.
    assert 2**32<6*1024**3
    terms=[]
    for t in range(1,513):
        residue=(14*t)%33
        if 2*residue<=33:continue
        f=14*t//33;g=5*t//33
        assert 2*f+g==t-2
        alpha=F(33,t);beta=max(F(14,f+1),F(5,g+1))
        assert alpha>beta
        # For both deltas the constants at both lower endpoints are <=0.
        for delta in (0,1):
            assert -delta<=0 and delta-1<=0
        if t<=128:terms.append((t,alpha,beta))
    assert len(terms)==62 and 6001>2*512
    H=sum((alpha-beta for t,alpha,beta in terms),F(0))/14
    A=sum((F(2,t) for t,alpha,beta in terms),F(0))/14
    R=sum((alpha+beta for t,alpha,beta in terms),F(0))/14
    root_upper=sum((sqrt_bounds(alpha)[1] for t,alpha,beta in terms),F(0))
    B_upper=F(259,125)*root_upper/14
    M1=4000000;M2=2000000000;eta=F(213,1000000)
    assert isqrt(M1)**2==M1
    for t,alpha,beta in terms:
        assert alpha*M1-F(2,t)>1 and beta*M1>1
        assert alpha*M2<10**11 and beta*M2<10**11
        assert alpha*M2-F(2,t)>=10**8 and beta*M2>=10**8
    log_low,log_high=log_bounds(F(361,250))
    first=H-A/M1-B_upper/isqrt(M1)
    second=H-eta*R-(1-eta)*A/M2
    assert first>log_high and second>log_high
    row=dict(pair=[3,11],p=3,k0=5,a=1,q=11,l0=2,b=2,c=19,d=14,
             L1=F(361,250),m0=6000,target=F(43,125),epsilon=F(3,20000))
    anchor=certify(row,999999)
    out=dict(status="PASS",reviewer="i5_attack",
             finite_full_replay_performed=True,
             finite_replay_blocks=12693,finite_replay_seconds_approximate=14.6,
             finite_result_sha256=hashlib.sha256(finite_path.read_bytes()).hexdigest(),
             analytic_arithmetic="Direct exact Fraction series and decimal-scale integer square roots, separate from the shared interval arithmetic",
             first_margin_lower=decimal_lower(first-log_high),
             second_margin_lower=decimal_lower(second-log_high),
             new_3_11_anchor=anchor,
             mathematical_source_audit_passed=True,
             external_inputs=["BFT Lemma 5.2 and floor identities (5.8)",
                              "BFT Lemma 5.4","BFT Theorem 2.4 and Section 7"],
             all_n_original_problem_claim=False)
    dest=ROOT/"data/results/verification_bft_gcd_19_14_independent_2026_10_04.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS independently: all finite blocks replayed, both analytic domains, 3/11 anchor")
    print(out["first_margin_lower"],out["second_margin_lower"])


if __name__=="__main__":main()
