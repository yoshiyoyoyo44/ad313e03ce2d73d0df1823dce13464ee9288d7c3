"""Independent exact audit of the even-weight <=8 two-position exclusion.

The universal argument is in research/i5/i5_independent_attack_2026-10-03.md.
Finite symbolic checks supplement, and do not replace, that argument.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def audit() -> dict:
    x = sp.symbols("x")
    cases = []
    checked = 0
    constants_checked = 0
    units24 = (1, 5, 7, 11, 13, 17, 19, 23)
    odd_weight4 = [(q, odd_weight) for q in units24 for odd_weight in range(5)
                   if (4 + (q - 1) * odd_weight) % 24 == 6]
    even_weight4 = [(q, odd_weight) for q in units24 for odd_weight in range(5)
                    if (4 + (q - 1) * odd_weight) % 24 == 14]
    assert odd_weight4 == []
    assert even_weight4 == [(11, 1)]
    for q in (11, 23):
        assert all((6 + (q - 1) * odd_weight) % 24 != 6 for odd_weight in range(1, 7))
    all_minimal_even_patterns = [
        (denominator, parity) for denominator in (2, 10) for parity in (0, 1)
        if denominator * 11 ** parity % 24 == 14
    ]
    assert all_minimal_even_patterns == [(10, 1)]
    for weight, s in ((w, s) for w in (4, 6, 8) for s in (2, 3)):
        t = s + 1
        c0 = 5
        h_bound = weight ** 2 // 4
        k_bound = (weight - 1) * (t + 1)
        linear_factor_bound = h_bound + (5 * (weight - 1) + 6) // 7
        resultant_bound = (
            (weight - 1) * k_bound ** (t + 1)
            + (weight - 1) * k_bound * h_bound ** t
            + h_bound ** (t + 1)
        )
        low_bound = t + c0 * resultant_bound ** (t + 1)
        q_bound = 2 * c0 * linear_factor_bound ** (t + 1)
        high_bound = t + c0 * (linear_factor_bound * q_bound) ** (t + 1)
        linear_bound = t + c0 * (weight * t + weight - 1) ** (t + 1)
        resonance_bound = 60 * (8 * (weight - 1)) ** 4 + 3
        for a in range(1, weight):
            b = weight - a
            for c in range(a + 1):
                for d in range(b + 1):
                    if (c, d) in ((0, 0), (a, b)):
                        continue
                    h = b * c - a * d
                    assert abs(h) <= h_bound
                    for u in range(s + 1):
                        for v in range(t + 1):
                            k = d + b * (u - v)
                            assert abs(k) <= k_bound
                            for m in range(2, t + 2):
                                aa = b * x ** m + a * x - 1
                                jj = u + c * x + d * x ** m
                                ll = h * x + k
                                assert sp.expand(b * (jj - v) - d * aa - ll) == 0
                                if h == 0:
                                    assert 0 < d < b and k != 0
                                    constants_checked += 1
                                    continue
                                rr = b * (-k) ** m + a * (-k) * h ** (m - 1) - h ** m
                                actual = int(sp.resultant(aa, ll, x))
                                assert abs(actual) == abs(rr)
                                assert rr != 0
                                assert abs(rr) <= resultant_bound
                                # The resultant's elementary integral Bezout identity.
                                quotient, remainder = sp.div(
                                    h ** m * aa - rr, ll, domain=sp.ZZ
                                )
                                assert remainder == 0
                                assert sp.expand(h ** m * aa - quotient * ll - rr) == 0
                                checked += 1
        bound = max(low_bound, high_bound, linear_bound, resonance_bound)
        assert bound < 10 ** 87
        cases.append({
            "weight": weight,
            "s": s,
            "t": t,
            "neighbor_multiplier": c0,
            "K": k_bound,
            "H": h_bound,
            "linear_factor_bound": linear_factor_bound,
            "C": resultant_bound,
            "q_bound_high_degree": q_bound,
            "n_bound_low_degree": low_bound,
            "n_bound_high_degree": high_bound,
            "n_bound_one_position": linear_bound,
            "n_bound_resonance": resonance_bound,
            "n_bound_all_two_positions": bound,
            "below_existing_finite_certificate": True,
        })
    return {
        "status": "pass",
        "scope": "i=5 support 01; weights 4,6,8; at most two positive digit positions",
        "resultant_identities_checked": checked,
        "constant_transform_cases_checked": constants_checked,
        "all_digit_mod24": {
            "odd_row3_weight4_allowed": odd_weight4,
            "even_row2_weight4_allowed_q_and_odd_position_weight": even_weight4,
            "odd_row3_all_candidate_bases_digit_sum_at_least": 9,
            "odd_row3_q11_or23_mod24_digit_sum_at_least": 11,
            "even_row2_all_minimal_denominator_and_prime_count_parity": all_minimal_even_patterns,
        },
        "cases": cases,
        "general_i5_solved": False,
        "proof_dependencies": [
            "existing i=5 support-01 reduction",
            "existing n<=10^87 finite certificate",
            "existing affine zero-line lemma",
            "full Kummer digit dominance and prime-5 restoration",
        ],
    }


if __name__ == "__main__":
    result = audit()
    target = Path(__file__).resolve().parents[1] / "data/results/verification_i5_weight4_two_positions.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
