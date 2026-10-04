"""Exact analytic completion of the new G(4,3,n) lower bound.

Requires the finite theta-block checker for 30000<m<=4000000. The two
unbounded estimates below are derived from BFT Lemma 5.4, not sampled.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_bft_newvertex_i22_i25_2026_10_04 import I, logarithm

ROOT=Path(__file__).resolve().parents[1]
M1=4_000_000
M2=20_000_000_000
K=20
L=F(1444,1000)
R=((2,1),(4,2),(6,3))


def main():
    if not __debug__:
        raise RuntimeError("Assertions required.")
    finite=json.loads((ROOT/"data/results/verification_bft_gcd_4_3_finite_blocks_2026_10_04.json").read_text())
    assert finite["status"]=="PASS" and finite["c"]==4 and finite["d"]==3
    assert finite["L1"]==str(L) and finite["m0"]==30000 and finite["last_m"]==M1
    coefficients=[(F(7,7*w+r),F(3,3*w+a),F(2,7*w+r))
                  for w in range(K) for r,a in R]
    target=logarithm(L)
    asymptotic=sum((alpha-beta for alpha,beta,shift in coefficients),F(0))/3
    shift=sum((v for alpha,beta,v in coefficients),F(0))
    roots=sum((I(alpha).root(2) for alpha,beta,v in coefficients),I(0))
    # Every upper theta endpoint on [M1,M2] is <=10^11; every lower
    # endpoint is >=1. Monotonic 1/m and 1/sqrt(m) losses are largest at M1.
    assert M1>2*(7*(K-1)+6)
    for alpha,beta,v in coefficients:
        assert alpha*M2 < 10**11 and beta*M2 < 10**11
        assert alpha*M1-v > 1 and beta*M1 > 1
        assert alpha>beta
    first=I(asymptotic)-F(shift,3*M1)-F(259,125)*roots/(3*I(M1).root(2))
    assert first.lo>target.hi
    # All endpoints on the second domain are >=10^8, so the relative
    # theta estimate applies and remains valid without an upper cutoff.
    for alpha,beta,v in coefficients:
        assert alpha*M2-v>=10**8 and beta*M2>=10**8
    epsilon=F(213,1_000_000)
    second_const=sum(((1-epsilon)*alpha-(1+epsilon)*beta
                      for alpha,beta,v in coefficients),F(0))/3
    second=I(second_const-F((1-epsilon)*shift,3*M2))
    assert second.lo>target.hi
    out=dict(status="PASS",c=4,d=3,L1=str(L),m0=30000,
             scope="Universal G(4,3,3m-delta)>L1^(3m), every integer m>30000, delta=0,1",
             finite_part=finite,
             analytic_K=K,first_domain=[M1,M2],
             first_lower_log_G_per_3m=first.record(),
             first_positive_margin=(first-target).record(),
             second_domain_lower=M2,
             second_lower_log_G_per_3m=second.record(),
             second_positive_margin=(second-target).record(),
             target_log_interval=target.record(),
             external_inputs=["BFT Proposition 5.3","BFT Lemma 5.4"],
             no_finite_m_sampling_used_for_analytic_tail=True,
             source_url="https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf")
    (ROOT/"data/results/verification_bft_gcd_4_3_universal_2026_10_04.json").write_text(
        json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS universal G(4,3,n) bound with L1=1.444,m0=30000")
    print("first margin",(first-target).record(),"second margin",(second-target).record())


if __name__=="__main__":
    main()
