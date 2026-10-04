"""Exact BFT 2.4 application of the separately proved new G(4,3) bound.

This proves a pair estimate, not Erdős 699 or the whole i16 case.
"""
from fractions import Fraction as F
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_bft_newvertex_i22_i25_2026_10_04 import certify


def main():
    if not __debug__:
        raise RuntimeError("Assertions required.")
    dependency=ROOT/"data/results/verification_bft_gcd_4_3_universal_2026_10_04.json"
    proof=json.loads(dependency.read_text(encoding="utf-8"))
    assert proof["status"]=="PASS" and proof["c"]==4 and proof["d"]==3
    assert proof["L1"]=="361/250" and proof["m0"]==30000
    row=dict(pair=[7,13],p=7,k0=3,a=1,q=13,l0=2,b=2,c=4,d=3,
             L1=F(361,250),m0=30000,target=F(49,400),epsilon=F(1,10000))
    result=certify(row,999999)
    out=dict(status="PASS",
             scope="For nonnegative exponents k,l and positive integer cofactors x1,x2, |7^k*x1-13^l*x2|<=100 and min(values)>=exp(999999) imply max(x1,x2)>min(values)^(49/400)",
             all_n_problem_claim=False,
             universal_G_dependency=str(dependency.relative_to(ROOT)),
             anchor=result,
             exact_rational_interval_bits=128,
             external_inputs=["BFT Theorem 2.4 and its Section 7 proof",
                              "BFT Proposition 5.3","BFT Lemma 5.4"],
             source_url="https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf")
    dest=ROOT/"data/results/verification_bft_gcd_4_3_anchor_7_13_2026_10_04.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
