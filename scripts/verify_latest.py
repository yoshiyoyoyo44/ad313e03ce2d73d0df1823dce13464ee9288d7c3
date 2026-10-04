"""Replay the October 3 independent research and prior checks."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKS = (
    "audit_i3_rho6_degree7_independent.py",
    "audit_i5_weight4_two_positions.py",
    "audit_two_position_digit_bound.py",
    "audit_global_independent_2026_10_03.py",
    "audit_adjacent_digit_descent.py",
    "audit_i5_sparse_allocation.py",
    "audit_i5_global_product_and_affine.py",
    "audit_i5_multiplicity_frontier.py",
    "audit_i3_quintic_split_allocation.py",
    "audit_i3_split_mahler_frontier.py",
    "audit_october03_integration.py",
    "audit_i3_quadratic_cofactor.py",
    "audit_i3_quintic_quadratic_endpoint.py",
    "audit_i3_quintic_quadratic_complete.py",
    "audit_i3_cubic_cofactor.py",
    "audit_i3_sextic_partial_sharing.py",
    "audit_i3_even_multiplier.py",
    "audit_i3_split_geometric.py",
    "audit_i3_arbitrary_cofactor.py",
    "audit_i3_adjacent_resultants.py",
    "audit_i3_central_square_descent.py",
    "audit_i3_half_ratio_central_bounds.py",
    "audit_i3_balanced_boundary.py",
    "audit_i3_five_power_composition.py",
    "audit_i3_five_power_low_degree_closeout.py",
    "audit_i3_half_degree_composition.py",
    "audit_i3_prime_power_resultants.py",
    "audit_i3_septic_and_saturation.py",
    "audit_i3_sextic_closeout.py",
    "audit_i3_quintic_digit_classification.py",
    "audit_i3_quintic_closeout.py",
    "audit_i3_extremal_split_closeout.py",
    "audit_i3_sextic_working_models.py",
    "audit_i4_six_cell_capacity.py",
    "audit_polynomial_capacity_supports.py",
    "audit_iterated_polynomial_capacity.py",
    "audit_known_bridge_and_i4_fixed_j.py",
    "replay_i4_fixed_j.py",
    "check_repository.py",
)


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled: do not use python -O.")
    for script in CHECKS:
        started = time.monotonic()
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(ROOT / "scripts" / script)],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )
        if result.returncode:
            print(f"FAIL {script}", flush=True)
            print(result.stdout[-4000:])
            print(result.stderr[-4000:], file=sys.stderr)
            return result.returncode
        print(f"PASS {script} ({time.monotonic() - started:.1f}s)", flush=True)
    print(f"Passed {len(CHECKS)} checks. Problem 699 remains open.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
