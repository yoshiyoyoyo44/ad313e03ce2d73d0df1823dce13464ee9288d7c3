# Erdős 699 — 2026-09-27 research package

Read `REPORT.md` for complete statements, proofs, dependencies, limitations,
and next research steps.

Verified in this session:

- All admissible n,j for i=28,31,34.
- All admissible n,j with n<=10^87 for
  i=5..33 excluding i=28,29,31 (26 indices).

Combined with the frozen repository baseline, all i>=5 are covered for
n<=10^87. The whole problem remains open; i=3,4 and the large-n tails of
the 26 indices remain.

Python 3 standard library only. Keep assertions enabled. To replay:

```sh
python run_verification.py
```

The two-prime tail proof uses Matveev's published theorem, as specified in
REPORT.md. The bounded product bootstrap does not use that theorem.
These are mathematical arguments with exact computational certificates;
they are not Lean proofs or external peer review.

`frozen/` contains unchanged generator/arithmetic sources from the frozen
GitHub commit. `sources/` preserves the two user attachments and relevant
repository notes. `provenance.json` records checked Git blob hashes.
`exploratory/` is not an input to either theorem.
