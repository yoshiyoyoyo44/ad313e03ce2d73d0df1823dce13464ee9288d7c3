"""Preserve October 3 sources and reconstruct selected supplied certificates.

This does not replay unprovided Matveev/continued-fraction closeout scripts,
nor certify that the two source-reported i=5 supports are the full frontier.
"""

import hashlib
import json
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
from zipfile import ZipFile

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT/"archive/attachments/incoming_2026-10-03"
BUNDLE = SOURCE/"erdos699_conversation_progress_bundle_2026-10-03"
S, U, T, N, Y = sp.symbols("S U t n y")


def check_source_hashes():
    manifest = json.loads((SOURCE/"import_manifest.json").read_text(encoding="utf-8"))
    for record in manifest["source_files"]:
        path = SOURCE/record["path"]
        assert path.stat().st_size == record["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
    outer = SOURCE/manifest["source_files"][1]["path"]
    with ZipFile(outer) as archive:
        assert archive.testzip() is None
        assert len(archive.infolist()) == manifest["zip_entry_count"] == 19
        files = {entry.filename for entry in archive.infolist() if not entry.is_dir()}
        assert files == set(manifest["extracted_files"])
        for name, expected in manifest["extracted_files"].items():
            assert hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() == expected
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected
    assert not list(BUNDLE.rglob("*.py")), "Reassess replay status if actual scripts are supplied."
    return {"original_files": 2, "zip_entries": 19, "extracted_files": 12,
            "source_bytes_preserved": True, "source_replay_scripts_provided": False}


def bounded_subset_count(size, cardinality, limit):
    counts = {(0, 0): 1}
    for position in range(size):
        updated = dict(counts)
        for (number, total), count in counts.items():
            if number < cardinality and total+position <= limit:
                key = (number+1, total+position)
                updated[key] = updated.get(key, 0)+count
        counts = updated
    return sum(value for (number, _), value in counts.items() if number == cardinality)


def audit_collision_moments():
    threshold = 10**87
    supplied_lines = (BUNDLE/"data/results/collision_aware_maximal_row_moment_2026-10-02.log").read_text().splitlines()
    supplied = {int(line.split()[0]): [int(value) for value in line.split()]
                for line in supplied_lines[1:] if line and line[0].isdigit()}
    rows = []
    for index in [value for value in range(5, 34) if value not in (28, 29, 31)]:
        h = index-1
        m = int(sp.primepi(h))
        k = index-m
        b0 = (2*h+2)//3
        d0 = 3*b0-h
        s0 = b0*(b0+1)//2
        power = 3*s0-d0*k
        assert 2*d0 > power >= 0
        assert 2*factorial(h)**d0*threshold**power < 4**s0*(threshold-h)**(2*d0)
        b = k-1 if 2*(k-1) >= h else k
        denominator = 2*b
        triangular = b*(b+1)//2
        H = index*h//2-k*(k-1)
        assert denominator >= h
        C = Fraction(2*factorial(h)**denominator, 4**triangular)
        logarithmic_quotient = 0
        while C >= threshold**(logarithmic_quotient+1):
            logarithmic_quotient += 1
        assert threshold**logarithmic_quotient <= C < threshold**(logarithmic_quotient+1)
        maximum_sum = H+logarithmic_quotient
        distinct = bounded_subset_count(index, m, maximum_sum)
        one_collision = bounded_subset_count(index, m-1, maximum_sum)
        row = [index, m, b, denominator, H, logarithmic_quotient, maximum_sum,
               distinct, one_collision, distinct+one_collision, comb(index, m)+comb(index, m-1)]
        assert row == supplied[index], (index, row, supplied[index])
        rows.append(row)
    assert len(rows) == 26
    return {"role": "exact numerical bounds and support counts under the stated cofactor/moment inequalities",
            "indices": 26, "rows_match_supplied_log": True, "rows": rows}


def conic_bounds(expression, multiplier):
    leading = sum(
        coefficient*S**powers[0]*U**powers[1]
        for powers, coefficient in sp.Poly(expression, S, U).terms() if sum(powers) == 2
    )
    f = sp.Poly(leading.subs({S: 1, U: T}), T)
    quadratic, linear, constant = f.all_coeffs()
    assert quadratic > 0 and constant > 0 and 4*quadratic*constant-linear**2 > 0
    endpoints = [sp.Rational(0), sp.Rational(1, 2)]
    vertex = -linear/(2*quadratic)
    candidates = endpoints+[vertex] if 0 <= vertex <= sp.Rational(1, 2) else endpoints
    minimum = min(f.eval(value) for value in candidates)
    maximum = max(f.eval(value) for value in endpoints)
    assert 0 < minimum <= maximum <= multiplier
    lower = expression-leading
    degree_one = sp.expand(lower).coeff(S, 1)*S+sp.expand(lower).coeff(U, 1)*U
    constant_term = lower.subs({S: 0, U: 0})
    linear_values = [degree_one.subs({S: 1, U: value}) for value in endpoints]
    low_linear, high_linear = min(linear_values), max(linear_values)
    lower_bound = minimum*N**2+low_linear*N+constant_term
    upper_gap = -high_linear*N-constant_term
    for bound in (lower_bound, upper_gap):
        shifted = sp.Poly(bound.subs(N, Y+16), Y)
        assert all(value >= 0 for value in shifted.all_coeffs())
        assert shifted.eval(0) > 0
    return {"expression": str(expression), "multiplier": multiplier,
            "normalized_quadratic_minimum": str(minimum),
            "valid_for": "n>=16, 0<=j<=n/2"}


def capacity_certificate(lines, line_multiplicities, conics, conic_multiplicities, multipliers, targets):
    polynomials = lines+conics
    multiplicities = line_multiplicities+conic_multiplicities
    coverage = {}
    for row in range(5):
        for column in range(row+1):
            covered = sum(multiplicity for polynomial, multiplicity in zip(polynomials, multiplicities)
                          if polynomial.subs({S: row, U: column}) == 0)
            assert covered >= targets[row]
            coverage[f"{row},{column}"] = int(covered)
    degree = sum(sp.Poly(polynomial, S, U).total_degree()*multiplicity
                 for polynomial, multiplicity in zip(polynomials, multiplicities))
    conic_checks = [conic_bounds(expression, multiplier) for expression, multiplier in zip(conics, multipliers)]
    constant = 1
    for multiplier, multiplicity in zip(multipliers, conic_multiplicities):
        constant *= multiplier**multiplicity
    return {"degree": degree, "coverage": coverage, "conics": conic_checks,
            "evaluation_constant": constant}


def audit_i5_two_certificates():
    lines = [U, U-S, S-1, U-S+1, U-1, S-3, S-4]
    conics_A = [S**2-3*S*U+3*U**2-S, S**2-S*U+U**2-4*S+3]
    conics_B = [S**2-2*S*U+3*U**2-3*S-U+2,
                2*S**2-4*S*U+3*U**2-4*S+U+2,
                2*S**2-3*S*U+6*U**2-8*S-3*U+6,
                5*S**2-9*S*U+6*U**2-11*S+3*U+6]
    A = capacity_certificate(lines, [2, 2, 4, 1, 1, 7, 8], conics_A, [2, 1], [1, 1], [6, 10, 2, 10, 10])
    B = capacity_certificate(lines, [6, 6, 14, 4, 4, 23, 24], conics_B, [2, 2, 1, 1], [1, 2, 2, 5], [12, 30, 8, 30, 30])
    assert A["degree"] == 31 and A["evaluation_constant"] == 1
    assert B["degree"] == 93 and B["evaluation_constant"] == 40
    supplied = json.loads((BUNDLE/"data/results/i5_last_two_capacity_frontier_2026-10-02.json").read_text())
    constant_A, constant_B = 2*60**30, 80*60**90
    assert int(supplied["support_0_2"]["constant"]) == constant_A
    assert int(supplied["support_0_2"]["constant_B"]) == constant_B
    # Bernoulli: (1-4/n)^r >=1-4r/n>1/2 for n>=10^87, r=30,90.
    assert 10**87 > 8*90
    return {"support": [0, 2], "certificate_A": A, "certificate_B": B,
            "constant_A": str(constant_A), "constant_B": str(constant_B),
            "scope": "capacity bounds reconstructed; support not excluded",
            "i5_solved": False, "other_support_closeouts_replayed": False}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    result = {"status": "passed", "preservation": check_source_hashes(),
              "collision_moments": audit_collision_moments(),
              "i5_capacity": audit_i5_two_certificates(),
              "general_i3_solved": False, "i5_solved": False}
    output = ROOT/"data/results/verification_october03_integration.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "preservation": result["preservation"],
                      "collision_moment_rows": 26, "i5_capacity_certificates": 2,
                      "closeout_scripts_replayed": False}, indent=2))


if __name__ == "__main__":
    main()
