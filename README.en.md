# Erdős Problem 699

**Research notes and reproducible certificates on common prime divisors of binomial coefficients. The full problem remains open.**

[日本語](README.md) · [Current status](docs/STATUS.md) · [Proof guide](docs/READING_GUIDE.md) · [Verification](docs/VERIFICATION.md)

## The question

For every $`1\le i<j\le n/2`$, must $`\binom ni`$ and $`\binom nj`$ share a prime divisor $`p\ge i`$?
For example, $`\binom{10}{2}=45`$ and $`\binom{10}{3}=120`$ share the prime 3.

[Original problem](https://www.erdosproblems.com/699) · [Upstream Lean statement](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/699.lean)

## Status as of October 3, 2026

These are the ranges covered by the saved paper proofs and finite certificates in this repository.

| Range | Status |
|---|---|
| $`i=1,2,28,29,31,34`$ and $`i\ge35`$ | Covered for all admissible $`n,j`$ |
| $`i\ge5`$ and $`n\le10^{87}`$ | Covered for all admissible $`j`$ |
| $`i=3,4`$ | General cases remain open |
| $`5\le i\le33`$, excluding 28,29,31 | The tail $`n>10^{87}`$ remains open |

**28 indices remain unresolved.** Excluding a special family does not resolve an entire index.
Independent peer review and a Lean formalization of the full argument have not been completed.

## Research map

Most proof notes are in Japanese. Each topic has a curated guide and a complete note index.

| Topic | Main progress | Remaining boundary |
|---|---|---|
| [General methods](research/general/README.md) | Weighted coverings; adjacent-row digit descent; effective bounds with bounded digit sums and prime counts | Uniform bounds for the general branch |
| [i=5](research/i5/README.md) | Support {0,1}; residues 9,64 modulo 72; sparse-cell and small-digit-family exclusions | The general tail beyond $`10^{87}`$ |
| [i=3](research/i3/README.md) | Conditional polynomial classifications and numerical exclusions of particular families | Unbounded degree and the general numerical regime |
| [i=4](research/i4/README.md) | All $`n`$ for $`5\le j\le1000`$; restrictions on occupied cells | General $`j`$ and cell configurations |
| [i=119](research/i119/README.md) | Earlier finite/Hankel work | Now covered by the general $`i\ge35`$ result |

See the [status page](docs/STATUS.md) for precise hypotheses and dependencies, and the [results catalog](docs/RESULTS_CATALOG.md) for individual lemmas.

## Reproduce checks

Python 3.12 or newer; SymPy 1.14.0 is pinned. Run from the repository root, with assertions enabled:

```console
python -m pip install -r requirements-verification.txt
python -X utf8 scripts/check_repository.py
python -X utf8 scripts/verify_latest.py
```

The first script checks navigation, syntax and preserved source hashes. The second replays 35 checks associated with the recent research updates; it is not a verifier for the full conjecture.
Auditors may overwrite their corresponding output JSON files. The saved [35-check log](data/results/verification_github_publish_2026-10-03.log) and [run record](data/results/verification_adjacent_digit_continuation_2026-10-03.json) document the preceding mathematical update.

## Repository map

- [Documentation](docs/README.md): overview, status, glossary, reading guide, verification, history.
- [Proof notes](research/README.md), [scripts](scripts/README.md), [certificates and outputs](data/README.md).
- [External sources](sources/README.md), [original attachments and snapshots](archive/README.md).
- [Lean](formal/README.md): three algebraic identities only. [Magma](magma/README.md): saved inputs and responses.
- [Contribution conventions](CONTRIBUTING.md): preserve scope, provenance and reproducibility.
