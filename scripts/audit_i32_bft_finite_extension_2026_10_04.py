"""Generate and independently replay the i=32 finite extension to 10^116.

The BFT 913/1000 tail is supplied by the companion pair-graph proof. This
script extends the genuinely finite certificate, and does not claim that an
unbounded CRT search is finite. Archive files are read only.
"""
from pathlib import Path
from importlib.util import module_from_spec,spec_from_file_location
from time import perf_counter
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/"archive/attachments/incoming_2026-09-27/erdos699_continuation"
BOUND=10**116
INDEX=32


def module(name,path):
    spec=spec_from_file_location(name,path)
    obj=module_from_spec(spec);spec.loader.exec_module(obj)
    return obj


def main():
    if not __debug__:
        raise RuntimeError("Assertions required.")
    hashes=json.loads((PACKAGE/"SHA256.json").read_text(encoding="utf-8"))
    for name,digest in hashes.items():
        assert hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest()==digest
    generator=module("i32_extension_generator",PACKAGE/"product_bootstrap.py")
    independent=module("i32_extension_independent",PACKAGE/"verify_product_bootstrap.py")
    m,d,S,D,c=generator.parameters(INDEX)
    assert (m,d,S,D,c)==(11,32,231,21,32)
    gap=913*d-1000*D
    assert gap==8216 and BOUND>2*31*32*d and BOUND>2*31*913*d
    assert 4**5>10**3 and 2**1001<10**302
    assert generator.factorial(32)//32 < 10**34
    tail_decimal_margin=116*gap+600*S-(302+1000*d*34)
    assert tail_decimal_margin==3354 and tail_decimal_margin>0
    rows=[];N=BOUND;start=perf_counter()
    for stage in range(80):
        row=generator.contract(INDEX,N)
        rows.append(row)
        cap=row["output_cap"]
        print(f"Generated i=32 stage {stage+1}: cap={cap}, "
              f"candidate n={row.get('candidate_n_count',0)}, "
              f"time={perf_counter()-start:.1f}s",flush=True)
        if cap*100>=N*99 or cap<generator.LOW:
            break
        N=cap
    else:
        raise AssertionError("Contraction budget exceeded")
    assert rows[-1]["output_cap"]<2_000_000,rows[-1]["output_cap"]
    certificate=dict(schema=1,i=INDEX,initial_cap=BOUND,
                     final_cap=rows[-1]["output_cap"],steps=rows)
    target=ROOT/"data/certificates/i32_bft_finite_extension_2026-10-04.json"
    target.write_text(json.dumps(certificate,indent=2)+"\n",encoding="utf-8")
    # Replay from the saved artifact, instead of from generator return values.
    saved=json.loads(target.read_text(encoding="utf-8"))
    assert saved["initial_cap"]==BOUND and saved["i"]==INDEX
    last=BOUND;count=0
    for stage,row in enumerate(saved["steps"],1):
        assert row["i"]==INDEX and row["input_cap"]==last
        count+=independent.verify_step(INDEX,row)
        last=row["output_cap"]
        print(f"Independently verified i=32 stage {stage}, "
              f"total binomial checks={count}",flush=True)
    assert last==saved["final_cap"]<2_000_000
    for name,digest in hashes.items():
        assert hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest()==digest
    out=dict(status="PASS",i=INDEX,finite_extension_lower=2_000_000,
             finite_extension_upper=BOUND,final_cap=last,
             bootstrap_steps=len(rows),exact_binomial_checks=count,
             independent_method="Opposite CRT coordinate and actual binomial large-prime part",
             archived_hashes_preserved=len(hashes),
             tail_from=BOUND,tail_product_exponent="913/1000",
             exact_tail_decimal_margin=tail_decimal_margin,
             tail_proof_dependency="research/general/bft_pair_graph_closeout_six_indices_2026-10-04.md",
             prefix_dependency="Existing i32 prefix certificate to 1999999; must replay separately",
             certificate=str(target.relative_to(ROOT)),
             unbounded_search_claimed=False)
    (ROOT/"data/results/verification_i32_bft_finite_extension_2026_10_04.json").write_text(
        json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS i32 finite extension through 10^116")


if __name__=="__main__":
    main()
