"""Replay October 4 proof dependencies and conditional lemmas in order.

Imported BFT theorems are dependencies of the paper proofs, not reproved
by this runner. Passing these checks does not settle the full problem.
"""
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    "audit_bft_six_finite_dependency_2026_10_04.py",
    "audit_bft_pair_graph_closeout_independent_2026_10_04.py",
    "audit_i32_bft_finite_extension_2026_10_04.py",
    "audit_i32_bft_prefix_dependency_2026_10_04.py",
    "audit_bft_i22_i25_finite_dependency_2026_10_04.py",
    "audit_bft_newvertex_i22_i25_2026_10_04.py",
    "audit_bft_newvertex_i22_i25_independent_2026_10_04.py",
    "audit_bft_proposition61_intermediate_bridge_2026_10_04.py",
    "audit_bft_gcd_3_2_finite_blocks_2026_10_04.py",
    "audit_bft_G_3_2_analytic_tail_2026_10_04.py",
    "audit_bft_i19_finite_dependency_2026_10_04.py",
    "audit_bft_strengthened_gcd_i19_2026_10_04.py",
    "audit_bft_i24_finite_dependency_2026_10_04.py",
    "audit_bft_i24_closeout_2026_10_04.py",
    "audit_bft_gcd_4_3_finite_blocks_2026_10_04.py",
    "audit_bft_gcd_4_3_universal_2026_10_04.py",
    "audit_bft_gcd_4_3_anchor_7_13_2026_10_04.py",
    "audit_bft_gcd_19_14_finite_blocks_2026_10_04.py",
    "audit_bft_gcd_19_14_universal_2026_10_04.py",
    "audit_bft_gcd_19_14_independent_2026_10_04.py",
    "audit_bft_gcd_10_7_and_two_anchors_2026_10_04.py",
    "audit_bft_i16_finite_dependency_2026_10_04.py",
    "audit_bft_i16_closeout_2026_10_04.py",
    "audit_largest_base_adjacent_shared_degree_2026_10_04.py",
    "audit_nonmaximum_row_zero_rational_closeout_2026_10_04.py",
    "audit_i3_largest_base_general_shared_degree_2026_10_04.py",
    "audit_i3_largest_base_endpoint_balance_2026_10_04.py",
    "audit_i3_linear_J2_quotient_degree1_bge2_all_degrees.py",
    "audit_i3_linear_J2_quotient_degree1_independent.py",
    "audit_i3_linear_J2_quotient_degree_ge2_all_degrees.py",
    "audit_i3_quadratic_J2_Elinear_high_degree_2026_10_04.py",
    "audit_i3_quadratic_J2_Elinear_high_degree_independent.py",
    "audit_i3_quadratic_group_linear_residual_all_degrees.py",
    "audit_i3_nrow_dyadic_strip_2026_10_04.py",
    "audit_i3_three_linear_above_2026_10_04.py",
    "audit_i3_three_linear_b_c_t_2026_10_04.py",
    "audit_i3_three_linear_congruence_2026_10_04.py",
    "audit_i3_three_linear_order_2026_10_04.py",
    "audit_i5_pell_primitive_unit_reduction.py",
    "check_repository.py",
)


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled: do not use python -O.")
    destination = ROOT / "data/results/verification_october04_publication_2026-10-04.json"
    log_path = ROOT / "data/results/verification_october04_publication_2026-10-04.log"
    output_blocks = []
    record = dict(status="running", python=sys.version, platform=platform.platform(),
                  exact_all_n_indices_added=[16, 17, 19, 22, 23, 24, 25, 26, 27, 30, 32, 33],
                  unresolved_indices=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 20, 21],
                  external_theorems_reproved=False, problem699_fully_solved=False,
                  checks=[])
    # Create both paths before the final navigation check resolves their links.
    destination.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    with log_path.open("w", encoding="utf-8") as log:
        for script in CHECKS:
            path = ROOT / "scripts" / script
            started = time.monotonic()
            result = subprocess.run(
                [sys.executable, "-X", "utf8", str(path)], cwd=ROOT,
                capture_output=True, text=True, encoding="utf-8",
            )
            elapsed = round(time.monotonic() - started, 3)
            record["checks"].append(dict(script=script, exit_code=result.returncode,
                elapsed_seconds=elapsed, script_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
            block = f"{script}\n{result.stdout.rstrip()}\n{result.stderr.rstrip()}".rstrip()
            output_blocks.append(block)
            log.write(block + "\n\n")
            log.flush()
            if result.returncode:
                record["status"] = "failed"
                destination.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                print(f"FAIL {script}", flush=True)
                print(result.stdout[-4000:])
                print(result.stderr[-4000:], file=sys.stderr)
                return result.returncode
            print(f"PASS {script} ({elapsed:.1f}s)", flush=True)
        record["status"] = "passed"
        record["checks_passed"] = len(CHECKS)
        destination.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    log_path.write_text("\n\n".join(output_blocks) + "\n", encoding="utf-8")
    print(f"Passed {len(CHECKS)} October 4 checks. The full problem remains open.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
