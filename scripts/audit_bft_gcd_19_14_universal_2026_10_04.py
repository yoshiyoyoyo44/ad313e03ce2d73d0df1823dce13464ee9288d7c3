"""Exact universal new G(19,14,n) bound and the 3,11 BFT anchor.

Connects all finite m>6000 through 4e6 to an analytic two-domain tail.
No finite sample extrapolation is used.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_bft_newvertex_i22_i25_2026_10_04 import I,logarithm,certify

ROOT=Path(__file__).resolve().parents[1]
C,D=19,14
L=F(1444,1000)
M0=6000
FIRST=4_000_000
SWITCH=2_000_000_000
T=128


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    finite_path=ROOT/'data/results/verification_bft_gcd_19_14_finite_blocks_2026_10_04.json'
    finite=json.loads(finite_path.read_text(encoding='utf-8'))
    assert finite['status']=='PASS' and finite['c']==C and finite['d']==D
    assert finite['L1']==str(L) and finite['m0']==M0 and finite['last_m']==FIRST
    terms=[]
    for t in range(1,T+1):
        if 2*((D*t)%(C+D))<=C+D:continue
        alpha=F(C+D,t)
        beta=max(F(D,D*t//(C+D)+1),F(C-D,(C-D)*t//(C+D)+1))
        assert alpha>beta
        terms.append((t,alpha,beta))
    H=sum(alpha-beta for t,alpha,beta in terms)/D
    A=sum(F(2,t) for t,alpha,beta in terms)/D
    B=F(259,125)/D*sum((I(alpha).root(2) for t,alpha,beta in terms),I(0))
    R=sum(alpha+beta for t,alpha,beta in terms)/D
    target=logarithm(L)
    assert FIRST>2*T
    for t,alpha,beta in terms:
        assert alpha*SWITCH<10**11 and beta*SWITCH<10**11
        assert alpha*FIRST-F(2,t)>1 and beta*FIRST>1
    first=I(H)-I(A)/FIRST-B/I(FIRST).root(2)
    assert first.lo>target.hi
    eta=F(213,1000000)
    for t,alpha,beta in terms:
        assert alpha*SWITCH-F(2,t)>=10**8 and beta*SWITCH>=10**8
    second=I(H-eta*R)-I((1-eta)*A)/SWITCH
    assert second.lo>target.hi
    # Both deltas covered: upper ((c+d)m-delta-1)/t is at least
    # ((c+d)m-2)/t; each actual lower endpoint is at most beta*m.
    seed=dict(pair=[3,11],p=3,k0=5,a=1,q=11,l0=2,b=2,c=C,d=D,
              L1=L,m0=M0,target=F(344,1000),epsilon=F(15,100000))
    anchor=certify(seed,999999)
    out=dict(status='PASS',c=C,d=D,L1=str(L),m0=M0,
        theorem='G(19,14,14m-delta)>(361/250)^(14m), delta=0,1, every integer m>6000',
        finite_part_file=str(finite_path.relative_to(ROOT)),
        finite_part_sha256=hashlib.sha256(finite_path.read_bytes()).hexdigest(),
        finite_part=finite,analytic_valid_t_max=T,
        number_of_analytic_prime_intervals=len(terms),
        first_domain=[FIRST,SWITCH],second_domain_start=SWITCH,
        H=I(H).record(),sqrt_error_B=B.record(),relative_error_R=I(R).record(),
        log_target=target.record(),first_lower=first.record(),second_lower=second.record(),
        first_margin=(first-target).record(),second_margin=(second-target).record(),
        new_3_11_anchor=anchor,
        external_dependencies=['BFT Lemma5.2 and floor identities5.8',
                               'BFT Lemma5.4','BFT Theorem2.4 and Section7'],
        independent_parent_review_pending=True,all_original_problem_indices_added_here=[],
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    dest=ROOT/'data/results/verification_bft_gcd_19_14_universal_2026_10_04.json'
    dest.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
