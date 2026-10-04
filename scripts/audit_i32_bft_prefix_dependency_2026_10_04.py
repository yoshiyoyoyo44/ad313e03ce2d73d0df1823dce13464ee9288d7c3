"""Replay the existing i32 prefix against the new finite-extension endpoint."""
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
import gzip,hashlib,json,shutil,tempfile

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/"archive/attachments/incoming_2026-09-27/erdos699_continuation"


def main():
    if not __debug__:
        raise RuntimeError("Assertions required.")
    hashes=json.loads((PACKAGE/"SHA256.json").read_text(encoding="utf-8"))
    for name,digest in hashes.items():
        assert hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest()==digest
    extension=json.loads((ROOT/"data/certificates/i32_bft_finite_extension_2026-10-04.json").read_text(encoding="utf-8"))
    assert extension["i"]==32 and extension["initial_cap"]==10**116
    assert extension["final_cap"]<2_000_000
    original=json.loads(gzip.decompress((PACKAGE/"prefix_certificate.json.gz").read_bytes()))
    selected=[r for r in original["rows"] if r["i"]==32]
    assert len(selected)==1 and selected[0]["upper"]==1_999_999
    spec=spec_from_file_location("i32_original_independent_prefix",PACKAGE/"verify_prefix.py")
    verifier=module_from_spec(spec);spec.loader.exec_module(verifier)
    dist=ROOT/"dist";dist.mkdir(exist_ok=True)
    work=Path(tempfile.mkdtemp(prefix="i32-prefix-independent-",dir=dist)).resolve()
    try:
        (work/"prefix_certificate.json.gz").write_bytes(gzip.compress(
            json.dumps(dict(schema=1,rows=selected)).encode(),mtime=0))
        (work/"product_bootstrap.json").write_text(
            json.dumps(dict(schema=1,rows=[extension])),encoding="utf-8")
        verifier.ROOT=work
        verifier.main()
        reproduced=json.loads((work/"prefix_verification.json").read_text(encoding="utf-8"))
        saved=json.loads((PACKAGE/"prefix_verification.json").read_text(encoding="utf-8"))
        expected=next(r for r in saved["rows"] if r["i"]==32)
        assert reproduced["rows"]==[expected]
        assert expected["upper"]==1_999_999
        out=dict(status="PASS",i=32,start=66,end=1_999_999,
                 matches_archived_independent_result=True,
                 finite_extension_endpoint=extension["final_cap"],
                 finite_extension_upper=10**116,
                 no_gap_to_extension=True,
                 prefix=expected,archived_hashes_preserved=len(hashes))
        (ROOT/"data/results/verification_i32_bft_prefix_dependency_2026_10_04.json").write_text(
            json.dumps(out,indent=2)+"\n",encoding="utf-8")
    finally:
        # Verified absolute target is a newly created directory inside dist.
        assert work.parent==dist.resolve()
        assert work.name.startswith("i32-prefix-independent-")
        shutil.rmtree(work)
    for name,digest in hashes.items():
        assert hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest()==digest
    print("PASS i32 prefix through 1999999; overlaps finite extension")


if __name__=="__main__":
    main()
