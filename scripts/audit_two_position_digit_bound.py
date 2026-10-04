"""Exact diagnostics for the all-index bounded-weight two-position lemma."""

import json
from math import gcd, lcm
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent


def bounds(i, s, weight, multiplier=None, denominator=None):
    t, h = s + 1, i - 1
    default = lcm(*range(1, i + 1))
    multiplier = default if multiplier is None else multiplier
    denominator = default if denominator is None else denominator
    q0 = 2 * multiplier * (s + weight + t) ** (t + 1) * weight ** (t * (t + 1) + 1)
    e = weight * (weight + t + 1)
    k = multiplier * e ** (t + 1)
    values = {
        "low_degree": s + weight * q0 ** (t + 1),
        "high_degree": t + k ** (t + 2),
        "resonance": h + denominator * (weight * (t + h)) ** i,
    }
    return {"i": i, "s": s, "weight": weight, "C": multiplier,
            "D": denominator, "bounds": values, "n_upper": max(values.values())}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    x, a, b, c, d, u, v, s, z = sp.symbols("x a b c d u v s z")
    # z stands for X**m: the equality holds for every exponent m.
    aa = b * z + a * x - 1
    jj = u + c * x + d * z
    ll = (b * c - a * d) * x + d + b * (u - v)
    assert sp.expand(b * (jj - v) - d * aa - ll) == 0

    resonance_checks = 0
    for i in range(3, 16):
        h = i - 1
        for ss in range(i - 1):
            t = ss + 1
            for bb in range(2, 9):
                for dd in range(1, bb):
                    g = gcd(bb, dd)
                    big_b, big_a = bb // g, dd // g
                    assert big_b >= 2 and gcd(big_a, big_b) == 1
                    for vv in range(t + 1):
                        delta = big_b * vv - big_a * t
                        assert abs(delta) <= big_b * t
                        zero_rows = set()
                        for rr in range(i):
                            values = [delta + big_a * rr - big_b * ww for ww in range(rr + 1)]
                            assert max(map(abs, values)) <= bb * (t + h)
                            if 0 in values:
                                zero_rows.add(rr)
                                assert (delta + big_a * rr) % big_b == 0
                        assert all(not ({rr, rr + 1} <= zero_rows) for rr in range(i - 1))
                        resonance_checks += 1

    integer_checks = 0
    for ss in (1, 2, 3):
        t = ss + 1
        for weight in range(2, 8):
            for aa in range(1, weight):
                bb = weight - aa
                for cc in range(aa + 1):
                    for dd in range(bb + 1):
                        if (cc, dd) in ((0, 0), (aa, bb)):
                            continue
                        for uu in range(ss + 1):
                            for m in (2, t + 1, t + 2, t + 5):
                                q = 11
                                n = ss + aa * q + bb * q ** m
                                j = uu + cc * q + dd * q ** m
                                aval = n - t
                                kval = bb * cc - aa * dd
                                for vv in range(t + 1):
                                    lv = kval * q + dd + bb * (uu - vv)
                                    assert bb * (j - vv) == dd * aval + lv
                                    assert abs(lv) <= weight * (weight + t + 1) * q
                                    integer_checks += 1
                                assert aval >= q ** m

    # A shared negative root exists in the general coefficient range.
    # It is deliberately covered by low-degree integer division.
    assert 2 * (-1) ** 2 + (-1) - 1 == 0
    result = {
        "status": "passed", "general_problem_solved": False,
        "scope": "at most two positive digit positions, bounded weight, adjacent nonmaximal rows",
        "universal_compression_identity": True,
        "resonance_configurations": resonance_checks,
        "integer_compression_diagnostics": integer_checks,
        "sample_bounds": [bounds(5, 2, 4, 30, 60), bounds(5, 3, 4, 5, 60),
                          bounds(10, 1, 4), bounds(27, 1, 4)],
    }
    target = ROOT / "data/results/verification_two_position_digit_bound.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
