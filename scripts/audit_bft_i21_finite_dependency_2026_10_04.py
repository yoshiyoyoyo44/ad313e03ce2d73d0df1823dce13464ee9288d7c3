"""Targeted exhaustive replay of the finite input for i21 all-n index.

Uses the archived independent opposite-CRT verifier and rational-interval
prefix arithmetic without calling archive mains or changing archived files.
"""
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location
from fractions import Fraction
from time import perf_counter
import gzip, hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/"archive/attachments/incoming_2026-09-27/erdos699_continuation"
INDICES=[21]


def module(name,path):
    spec=spec_from_file_location(name,path)
    obj=module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def main():
    if not __debug__:
        raise RuntimeError("Assertions required.")
    hashes=json.loads((PACKAGE/"SHA256.json").read_text(encoding="utf-8"))
    for name,digest in hashes.items():
        assert hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest()==digest
    bootstrap=module("i21_finite_bootstrap",PACKAGE/"verify_product_bootstrap.py")
    prefix=module("i21_finite_prefix",PACKAGE/"verify_prefix.py")
    arithmetic=prefix.arithmetic
    cert=json.loads((PACKAGE/"product_bootstrap.json").read_text(encoding="utf-8"))
    pc=json.loads(gzip.decompress((PACKAGE/"prefix_certificate.json.gz").read_bytes()))
    saved_b=json.loads((PACKAGE/"product_bootstrap_verification.json").read_text(encoding="utf-8"))
    saved_p=json.loads((PACKAGE/"prefix_verification.json").read_text(encoding="utf-8"))
    expected=[i for i in range(5,34) if i not in (28,29,31)]
    assert [r["i"] for r in cert["rows"]]==expected
    assert [r["i"] for r in pc["rows"]]==expected
    result=[]
    for i in INDICES:
        start=perf_counter()
        row=next(r for r in cert["rows"] if r["i"]==i)
        last=10**87
        assert row["initial_cap"]==last
        count=0
        for step in row["steps"]:
            assert step["i"]==i and step["input_cap"]==last
            count+=bootstrap.verify_step(i,step)
            last=step["output_cap"]
        assert last==row["final_cap"]<2_000_000
        saved=next(r for r in saved_b["rows"] if r["i"]==i)
        assert dict(i=i,steps=len(row["steps"]),final_cap=last,
                    exact_binomial_checks=count)==saved
        r=next(r for r in pc["rows"] if r["i"]==i)
        upper=r["upper"]
        assert upper==max(1_999_999,last)==1_999_999
        ps,m,d,S,D,c=bootstrap.parameters(i)
        h=i-1
        data=[]
        for p in ps:
            q=p;qs=[]
            while q<=upper:
                qs.append((q,i%q));q*=p
            data.append((arithmetic.log_interval(p)[1],qs))
        fact=sum(arithmetic.log_interval(k)[1] for k in range(1,i+1))
        tiles=[(lo,hi,None) for lo,hi in r["intervals"]]
        tiles.extend((e["n"],e["n"],e) for e in r["exceptions"])
        tiles.sort()
        needed=2*i+2
        minimum=None
        for lo,hi,exception in tiles:
            assert lo==needed and lo<=hi<=upper
            needed=hi+1
            if exception is not None:
                prefix.check_single(i,exception)
                continue
            part=0
            for lp,qs in data:
                e=0
                for q,residue in qs:
                    if q>hi:
                        break
                    e+=int(residue>0 and
                           -((-(lo-residue+1))//q)<=hi//q)
                part+=e*lp
            margin=(2*S*arithmetic.L2+
                    i*d*arithmetic.log_interval(lo-h)[0]-
                    d*fact-d*part-
                    3*S*arithmetic.log_interval(hi)[1])
            assert margin>0,(i,lo,hi)
            minimum=margin if minimum is None else min(minimum,margin)
        assert needed==upper+1
        reproduced=dict(i=i,upper=upper,intervals=len(r["intervals"]),
                        singletons=len(r["exceptions"]),
                        minimum_log_margin_lower=str(Fraction(minimum,arithmetic.SCALE)))
        assert reproduced==next(x for x in saved_p["rows"] if x["i"]==i)
        result.append(dict(i=i,initial_cap=10**87,final_cap=last,
                           bootstrap_steps=len(row["steps"]),
                           exact_binomial_checks=count,prefix=reproduced))
        arithmetic.log_interval.cache_clear()
        print(f"i={i}: PASS full finite input, "
              f"{count} binomial checks, {len(tiles)} prefix tiles, "
              f"{perf_counter()-start:.1f}s",flush=True)
    for name,digest in hashes.items():
        assert hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest()==digest
    out=dict(status="PASS",indices=INDICES,finite_bound=10**87,
             archived_hashes_preserved=len(hashes),
             exhaustive_targeted_replay=True,rows=result,
             external_matveev_not_used=True,
             scope="Finite input only; combine with BFT pair-graph tail proof")
    (ROOT/"data/results/verification_bft_i21_finite_dependency_2026_10_04.json").write_text(
        json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS i21 finite dependency; originals preserved")


if __name__=="__main__":
    main()
