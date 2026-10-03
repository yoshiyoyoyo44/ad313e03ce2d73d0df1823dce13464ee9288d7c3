"""Exact i=5 tail closeouts, cofactor bounds, and an all-degree capacity barrier.

No optimizer is used here. Polynomial orders are checked independently by
translation and by partial derivatives. This does not solve general i=5.
"""

import json
from fractions import Fraction
from math import comb, prod
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
S, U, X = sp.symbols("S U x")
CELLS = [(s, u) for s in range(5) for u in range(s + 1)]
THRESHOLD = 10**24
MONOMIALS = {
    3: [S, U, 1],
    6: [S**2, S*U, U**2, S, U, 1],
    10: [S**3, S**2*U, S*U**2, U**3, S**2, S*U, U**2, S, U, 1],
}
for _degree in (4, 6):
    MONOMIALS[(_degree+1)*(_degree+2)//2] = [
        S**(total-u)*U**u for total in range(_degree, -1, -1)
        for u in range(total+1)
    ]

# Each entry is (coefficient vector, integer exponent of the evaluation).
COLLISION = [
    ([0, 1, -2], 7), ([0, 1, -1], 13), ([0, 1, 0], 16),
    ([1, -1, -2], 4), ([1, -1, -1], 10), ([1, -1, 0], 14),
    ([1, 0, -4], 16), ([1, 0, -3], 13), ([1, 0, -2], 7),
    ([1, -2, 2, -3, 0, 2], 1),
    ([2, -2, 1, -8, 3, 6], 1),
    ([3, -4, 3, -9, 1, 6], 2),
]
SUPPORT_04 = [
    ([0, 1, -1], 2), ([0, 1, 0], 3),
    ([1, -1, -1], 2), ([1, -1, 0], 3),
    ([1, 0, -3], 3), ([1, 0, -2], 2),
    ([1, -1, 1, -3, 0, 2], 1),
]
SUPPORT_03 = [
    ([0, 1, -1], 2), ([0, 1, 0], 3),
    ([1, -1, 0], 3), ([1, -1, -1], 2),
    ([1, 0, -4], 9), ([1, 0, -2], 5),
    ([1, -2, 2, -3, 0, 2], 1),
    ([4, -12, 18, -9, -16, 18, -9, 20, -6, -8], 3),
    ([1, 3, -9, 9, -7, 0, -9, 14, 6, -8], 3),
]
BASE_01 = [
    ([0, 1, -2], 1), ([0, 1, -1], 2), ([0, 1, 0], 3),
    ([1, -1, -2], 1), ([1, -1, -1], 2), ([1, -1, 0], 3),
    ([1, 0, -4], 4), ([1, 0, -3], 3), ([1, 0, -2], 2),
]
BASE_02_LINES = [[0, 1, 0], [1, -1, 0], [1, 0, -1],
                 [1, -1, -1], [0, 1, -1], [1, 0, -3], [1, 0, -4]]
BASE_02_A = list(zip(BASE_02_LINES, [2, 2, 4, 1, 1, 7, 8])) + [
    ([1, -3, 3, -1, 0, 0], 2), ([1, -1, 1, -4, 0, 3], 1),
]
BASE_02_B = list(zip(BASE_02_LINES, [6, 6, 14, 4, 4, 23, 24])) + [
    ([1, -2, 3, -3, -1, 2], 2), ([2, -4, 3, -4, 1, 2], 2),
    ([2, -3, 6, -8, -3, 6], 1), ([5, -9, 6, -11, 3, 6], 1),
]
NEW_01 = [
    ([0, 1, -1], 1), ([0, 1, 0], 3), ([1, -2, 0], 3),
    ([1, -1, 0], 3), ([1, -1, -1], 1), ([1, 0, -4], 1),
    ([1, 2, -2, -9, 0, 14], 2),
]
NEW_02 = [
    ([0, 1, -1], 5), ([0, 1, 0], 8),
    ([1, -1, 0], 8), ([1, -1, -1], 5),
    ([1, -1, 1, -4, 0, 3], 1), ([3, -4, 3, -9, 1, 6], 1),
    ([1, -3, 3, -1, 0, 0], 4),
    ([2, -4, 3, -4, 1, 2], 1),
    ([1, -2, 3, -3, -1, 2], 1),
    ([2, -2, 3, -8, -1, 6], 1),
]
QUARTIC_02 = [10, -36, 63, -54, 27, -54, 117, -117, 0,
              90, -81, 81, -58, 0, 12]
SEXTIC_02 = [2, -2, -7, 45, -90, 81, -27, -24, 27, -45, 36, -18, 0,
             112, -72, 99, -54, 27, -260, 71, -71, 0, 318, -24, 24,
             -196, 0, 48]
FINAL_02 = [
    ([0, 1, 0], 3), ([0, 1, -1], 2),
    ([1, -1, 0], 3), ([1, -1, -1], 2),
    (QUARTIC_02, 1), (SEXTIC_02, 1),
]


def expression(coefficients):
    return sp.expand(sum(a*b for a, b in zip(coefficients, MONOMIALS[len(coefficients)])))


def valuation(value, prime):
    assert value > 0
    exponent = 0
    while value % prime == 0:
        exponent += 1
        value //= prime
    return exponent


def nonnegative_from_threshold(polynomial):
    shifted = sp.Poly(sp.expand(polynomial.subs(S, X + THRESHOLD)), X)
    assert all(a >= 0 for a in shifted.all_coeffs()), polynomial
    return shifted


def bernstein(homogeneous, degree):
    if degree == 0:
        return [sp.Rational(homogeneous)]
    f = sp.Poly(homogeneous.subs({S: 1, U: X}), X)
    return [sum(f.nth(k)*sp.Rational(comb(i, k), comb(degree, k))/2**k
                for k in range(i + 1)) for i in range(degree + 1)]


def polynomial_check(coefficients, heavy):
    polynomial = expression(coefficients)
    degree = sp.Poly(polynomial, S, U).total_degree()
    orders = []
    for s, u in CELLS:
        translated = sp.Poly(polynomial.subs({S: S+s, U: U+u}), S, U)
        order = min(sum(powers) for powers, coefficient in translated.terms() if coefficient)
        derivative_order = next(r for r in range(degree+1)
                                if any(sp.diff(polynomial, S, a, U, r-a).subs({S: s, U: u}) != 0
                                       for a in range(r+1)))
        assert order == derivative_order
        orders.append(int(order))

    zero_exclusion = None
    if degree == 1:
        a, b, c = coefficients
        missed = [s for s in heavy if all(a*s+b*u+c != 0 for u in range(s+1))]
        endpoints = [polynomial.subs(U, 6), polynomial.subs(U, S/2)]
        positive = all(all(v >= 0 for v in sp.Poly(e.subs(S, X+THRESHOLD), X).all_coeffs())
                       and e.subs(S, THRESHOLD) > 0 for e in endpoints)
        negative = all(all(v <= 0 for v in sp.Poly(e.subs(S, X+THRESHOLD), X).all_coeffs())
                       and e.subs(S, THRESHOLD) < 0 for e in endpoints)
        if not (positive or negative):
            assert missed, (coefficients, heavy)
            bounds = [(60*abs(prod(a*s+b*u+c for u in range(s+1)))+s, s) for s in missed]
            upper, row = min(bounds)
            assert upper < THRESHOLD
            zero_exclusion = {"missed_heavy_row": row, "n_upper_if_zero": upper}
        candidates = [sp.Rational(1, 2), sp.Rational(1), sp.Rational(sum(map(abs, coefficients)))]
        for upper in candidates:
            if all(all(v >= 0 for v in sp.Poly((upper*S+sign*e).subs(S, X+THRESHOLD), X).all_coeffs())
                   for e in endpoints for sign in (-1, 1)):
                break
        else:
            raise AssertionError(coefficients)
        leading_bounds = None
    else:
        homogeneous = [sum(coefficient*S**powers[0]*U**powers[1]
                           for powers, coefficient in sp.Poly(polynomial, S, U).terms()
                           if sum(powers) == r) for r in range(degree+1)]
        intervals = [(min(bernstein(part, r)), max(bernstein(part, r)))
                     for r, part in enumerate(homogeneous)]
        assert intervals[-1][0] > 0
        lower = sum(lo*S**r for r, (lo, _) in enumerate(intervals))
        shifted = nonnegative_from_threshold(lower)
        assert shifted.eval(0) > 0
        upper = intervals[-1][1]
        gap = upper*S**degree-sum(hi*S**r for r, (_, hi) in enumerate(intervals))
        if any(v < 0 for v in sp.Poly(gap.subs(S, X+THRESHOLD), X).all_coeffs()):
            upper = sp.ceiling(upper)+1
            gap = upper*S**degree-sum(hi*S**r for r, (_, hi) in enumerate(intervals))
        nonnegative_from_threshold(gap)
        leading_bounds = [str(v) for v in intervals[-1]]
    return {"expression": str(polynomial), "coefficients": coefficients, "degree": int(degree),
            "cell_orders": orders, "upper_multiplier": str(upper),
            "leading_bounds": leading_bounds, "zero_exclusion": zero_exclusion}


def audit_denominators():
    # A nonmaximal 2-part is at most 4, and a nonmaximal 3-part at most 3.
    # Maximal-row membership is decided by v2 capped at 3 and v3 capped at 2.
    # Nonmaximal valuations and denominator factors are therefore periodic mod 360.
    oriented = {}
    expected = {(0, 0): 120, (0, 1): 120, (1, 0): 30, (0, 2): 20,
                (2, 0): 30, (0, 3): 40, (3, 0): 10, (0, 4): 30, (4, 0): 30}
    for pair, maximum in expected.items():
        rows = []
        heavy = [s for s in range(5) if s not in pair]
        for n in range(360, 720):
            twos = [min(valuation(n-s, 2), 3) for s in range(5)]
            threes = [min(valuation(n-s, 3), 2) for s in range(5)]
            if twos[pair[0]] != max(twos) or threes[pair[1]] != max(threes):
                continue
            values = {s: 2**valuation(n-s, 2)*3**valuation(n-s, 3)
                      *(5 if (n-s) % 5 == 0 else 1) for s in heavy}
            assert all(60 % value == 0 for value in values.values())
            rows.append({"residue": n % 360, "denominators": values})
        assert rows and max(prod(r["denominators"].values()) for r in rows) == maximum
        oriented[pair] = rows
    return oriented


def audit_row_zero():
    upper = 60*240**5+4
    assert upper == 47775744000004 < THRESHOLD
    denominators = [b for b in range(2, 61) if 60 % b == 0]
    for b in denominators:
        multiples = [s for s in range(5) if s % b == 0]
        if len(multiples) >= 3:
            assert b == 2 and multiples == [0, 2, 4]
    return {"n_upper_when_row_0_not_maximal": upper,
            "proof": "j/n=a/b, b|60; missed nonmaximal row bounds its full factor; b=2 forces n both even and odd"}


def capacity(name, support, entries, targets, expected_degree, denominators, closure=False, paired=False):
    heavy = [s for s in range(5) if s not in support]
    checks = [polynomial_check(co, heavy) for co, _ in entries]
    cover = [sum(m*check["cell_orders"][i] for (_, m), check in zip(entries, checks))
             for i in range(len(CELLS))]
    assert all(cover[i] >= targets[s] for i, (s, _) in enumerate(CELLS))
    degree = sum(m*check["degree"] for (_, m), check in zip(entries, checks))
    assert degree == expected_degree
    evaluation_constant = prod(Fraction(check["upper_multiplier"])**m
                               for (_, m), check in zip(entries, checks))
    paired_line_factors = 0
    if paired:
        assert sp.expand(S**2/4-U*(S-U)-(U-S/2)**2) == 0
        for u in range(5):
            left = sum(m for co, m in entries if co == [0, 1, -u])
            right = sum(m for co, m in entries if co == [1, -1, -u])
            paired_line_factors += min(left, right)
        assert paired_line_factors > 0
        # A matched pair replaces (n/2)*n by n^2/4. All shifts are
        # nonnegative and their two evaluations are positive in the domain.
        evaluation_constant /= 2**paired_line_factors
    weights = {s: targets[s] for s in heavy}
    oriented_constants = {}
    for pair, residues in denominators.items():
        if set(pair) != set(support):
            continue
        worst = max(prod(r["denominators"][s]**weights[s] for s in heavy) for r in residues)
        oriented_constants[f"{pair[0]},{pair[1]}"] = worst
    assert oriented_constants
    denominator_constant = max(oriented_constants.values())
    heavy_degree = sum(weights.values())
    assert THRESHOLD > 8*heavy_degree  # Bernoulli bounds (n/(n-4))^heavy_degree < 2.
    constant = 2*evaluation_constant*denominator_constant
    excess = degree-heavy_degree
    if closure:
        assert excess < 0 and constant < THRESHOLD**(-excess)
    return {"name": name, "support": support, "row_targets": targets,
            "degree": degree, "heavy_degree": heavy_degree, "excess": excess,
            "constant": str(constant), "evaluation_constant": str(evaluation_constant),
            "oriented_denominator_constants": oriented_constants,
            "cell_coverage": cover, "polynomials": [dict(c, exponent=m) for c, (_, m) in zip(checks, entries)],
            "support_closed": closure, "paired_line_factors": paired_line_factors}


def audit_barrier():
    records = []
    for support in [(0, 1), (0, 2)]:
        heavy = [s for s in range(5) if s not in support]
        reciprocal_sum = sum(Fraction(1, s+1) for s in heavy)
        slack = 1-reciprocal_sum
        assert reciprocal_sum < 1 and slack > 0
        # Strip all heavy horizontal factors. Restriction to each remaining
        # heavy row is a nonzero univariate polynomial of degree <= residual d.
        weights = [Fraction(1, s+1) if s in heavy else slack/Fraction(2*(s+1)) for s, _ in CELLS]
        assert all(w > 0 for w in weights)
        assert all(sum(w for w, (s, _) in zip(weights, CELLS) if s == row) == 1 for row in heavy)
        # This positive vector is feasible for EVERY polynomial, not merely a
        # finite catalogue: h + (reciprocal_sum+slack)*residual_degree <= total degree.
        for coefficients, _ in COLLISION+SUPPORT_04+SUPPORT_03+BASE_01+BASE_02_A+BASE_02_B+NEW_01+NEW_02:
            polynomial = expression(coefficients)
            orders = [min(sum(powers) for powers, coefficient in
                          sp.Poly(polynomial.subs({S: S+s, U: U+u}), S, U).terms() if coefficient)
                      for s, u in CELLS]
            assert sum(w*r for w, r in zip(weights, orders)) <= sp.Poly(polynomial, S, U).total_degree()
        records.append({"support": list(support), "heavy_rows": heavy,
                        "reciprocal_sum": str(reciprocal_sum), "slack": str(slack),
                        "positive_all_degree_dual_weights": [str(w) for w in weights],
                        "minimum_degree_cost_for_heavy_coverage": 3,
                        "scope": "nonnegative combinations of fixed polynomial multiplicities with total-degree costs"})
    assert [r["slack"] for r in records] == ["13/60", "1/20"]
    return records


def audit_pure_powers():
    assert 2**79 < THRESHOLD <= 2**80
    assert 3**50 < THRESHOLD <= 3**51
    # Exact LTE identities underlying the paper argument, with a diagnostic
    # replay of initial exponents; universal identities are proved in the note.
    for exponent in range(2, 501):
        if exponent % 2 == 0:
            assert valuation(2**exponent-1, 3) == 1+valuation(exponent//2, 3)
            assert valuation(3**exponent-1, 2) == 2+valuation(exponent, 2)
        else:
            assert valuation(2**exponent-2, 3) == 1+valuation((exponent-1)//2, 3)
    assert 64*2**(2*80) > 120**6*(15*80)**5
    assert 2**80 > 7200*20**10*80**2
    assert 64*3**(2*51) > 30**6*(20*51)**5
    # Ratios increase thereafter: 4 and 9 beat (1+1/e)^5;
    # 2 beats (1+1/e)^2. No finite cutoff is inferred from sampled LTE checks.
    assert Fraction(81, 80)**5 < 4 and Fraction(81, 80)**2 < 2
    assert Fraction(52, 51)**5 < 9
    return {"tail_n_threshold": str(THRESHOLD), "two_power_exponents_at_least": 80,
            "three_power_exponents_at_least": 51, "tail_pure_two_and_three_powers_closed": True,
            "all_n_scope_requires_existing_finite_theorem": True}


def audit_congruence_frontier(certificates):
    by_name = {r["name"]: r for r in certificates}
    c1 = Fraction(by_name["support_01_baseline_tight_constants"]["constant"])
    c2 = Fraction(by_name["support_02_baseline_A_tight_constants"]["constant"])
    # If the maximal 3-exponent is <=1, the corresponding maximal-row
    # denominator is <=15 for support 01, and <=30 for support 02.
    assert THRESHOLD**2 > c1*30**5
    assert THRESHOLD**3 > c1*15**6
    assert THRESHOLD > c2*60**2
    assert THRESHOLD**5 > c2*30**6
    oriented = {
        "0,1": [n for n in range(72) if n % 8 == 0 and n % 9 == 1],
        "1,0": [n for n in range(72) if n % 4 == 1 and n % 9 == 0],
        "0,2": [n for n in range(72) if n % 8 == 0 and n % 9 == 2],
        "2,0": [n for n in range(72) if n % 4 == 2 and n % 9 == 0],
    }
    classes = sorted({n for values in oriented.values() for n in values})
    assert classes == [9, 18, 45, 54, 56, 64]
    return {"modulus": 72, "necessary_classes": classes,
            "oriented_classes": oriented, "maximal_3_exponent_at_least": 2,
            "scope": "necessary conditions, not an enumeration of counterexamples"}


def audit_bft_bridge(certificates):
    by_name = {r["name"]: r for r in certificates}
    baseline = Fraction(by_name["support_02_baseline_A_tight_constants"]["constant"])
    mixed = Fraction(by_name["support_02_new_mixed_bound"]["constant"])
    exponent = Fraction(57, 200)
    assert baseline < 200**6 and mixed < 50**10
    # Restore the possible denominator factor 5: A<=5R0<1000*n^(1/6).
    # The two adjacent prime-power multiples obtained after division by 2
    # are >=n/4. At n>=10^87, A is smaller than (n/4)^(57/200).
    assert exponent-Fraction(1, 6) == Fraction(71, 600)
    assert (10**87)**71 > 2000**600
    assert exponent < Fraction(1, 2)  # 4^exponent < 2.
    assert 10**87//4 > 1771561
    # BFT forces the other restored cofactor B to be larger; R2>=B/5.
    # R2>n^exponent/10 and R0^2*R2<50*n^(2/5) imply R0^2<500*n^(23/200).
    assert Fraction(2, 5)-exponent == Fraction(23, 200)
    assert 23**2 > 500
    return {
        "support": [0, 2], "n_threshold": str(10**87),
        "external_theorem": {
            "authors": "M. A. Bennett, M. Filaseta, O. Trifonov",
            "title": "On the factorization of consecutive integers",
            "publication": "J. Reine Angew. Math. 629 (2009), 171-200",
            "theorem": "2.1, prime pair (2,3)", "lambda": "57/200",
            "exceptional_maximum": 1771561,
            "primary_manuscript": "https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf",
            "status": "external published theorem; its hypergeometric proof is not replayed here",
        },
        "row2_lower": "R2 > n^(57/200)/10",
        "row0_upper": "R0 < 23*n^(23/400)",
        "scope": "earlier necessary condition; superseded by the explicit quartic-sextic support closeout",
    }


def audit_bft_closeout(certificates, denominators):
    certificate = next(r for r in certificates if r["name"] == "support_02_quartic_sextic")
    assert certificate["row_targets"] == [6, 10, 4, 5, 4]
    assert certificate["degree"] == 20 and certificate["heavy_degree"] == 19
    assert certificate["excess"] == 1
    assert Fraction(certificate["evaluation_constant"]) == Fraction(5, 256)
    t = U*(S-U)
    compact_quartic = (10*S**4-36*S*S*t+27*t*t-54*S**3+117*S*t
                       +90*S*S-81*t-58*S+12)
    compact_sextic = (2*S**6-2*S**4*t-9*S*S*t*t+27*t**3-24*S**5
                      +27*S**3*t-18*S*t*t+112*S**4-72*S*S*t+27*t*t
                      -260*S**3+71*S*t+318*S*S-24*t-196*S+48)
    for coefficients, compact in ((QUARTIC_02, compact_quartic), (SEXTIC_02, compact_sextic)):
        expanded = expression(coefficients)
        assert sp.expand(compact-expanded) == 0
        assert sp.expand(expanded-expanded.subs(U, S-U)) == 0
    # B=5^delta_2 R2. The restored factor cannot occur simultaneously with
    # any heavy-row factor 5. Enumerate their coupled period, not separate maxima.
    restored = {}
    for pair, rows in denominators.items():
        if set(pair) != {0, 2}:
            continue
        restored[f"{pair[0]},{pair[1]}"] = max(
            5**(4*int((row["residue"]-2) % 5 == 0))
            *prod(row["denominators"][s]**weight for s, weight in ((1, 10), (3, 5), (4, 4)))
            for row in rows)
    assert restored == {"0,2": 2500000000, "2,0": 37968750000}
    constant = 2*Fraction(certificate["evaluation_constant"])*max(restored.values())
    assert constant == Fraction(11865234375, 8) < 200**4
    threshold = 10**75
    assert threshold >= THRESHOLD and threshold//4 > 1771561
    exponent = Fraction(57, 200)
    assert exponent-Fraction(1, 4) == Fraction(7, 200)
    # B<200*n^(1/4)<n^(57/200)/2.
    assert threshold**7 > 400**200
    # The earlier baseline also gives A<=5R0<1000*n^(1/6)
    # <n^(57/200)/2. Both are below the BFT lower bound (n/4)^(57/200).
    assert threshold**71 > 2000**600
    assert exponent < Fraction(1, 2)
    return {
        "support": [0, 2], "n_threshold": str(threshold),
        "capacity_certificate": "support_02_quartic_sextic",
        "restored_cofactor": "B=5^delta_2*R2",
        "restored_denominator_constants": restored,
        "restored_constant": str(constant),
        "mixed_bound": "R0^6*B^4 < (11865234375/8)*n",
        "upper_bounds": ["A < 1000*n^(1/6)", "B < 200*n^(1/4)"],
        "contradiction": "max(A,B) < n^(57/200)/2 < (n/4)^(57/200), contrary to BFT Theorem 2.1",
        "external_theorem": "Bennett-Filaseta-Trifonov, Theorem 2.1, prime pair (2,3); proof not replayed",
        "support_closed_in_tail": True,
        "support_closed_all_n_using_existing_finite_theorem": True,
        "remaining_supports": [[0, 1]],
        "necessary_classes_mod72_after_closeout": [9, 45, 64],
        "i5_solved": False,
    }


def audit_high_multiplicity_diagnostic():
    z, a, c, e, f = sp.symbols("z a c e f")
    norm = sp.Rational(1, 2)+2*a*a+(z-2*a)**2+2*c*c+2*(sp.Rational(1, 2)-c)**2
    norm += 2*e*e+2*f*f+(1-2*e-2*f)**2
    constraints = [a+c+e-sp.Rational(1, 2), z-2*a-c+f]
    stationary = {a: (17*z-1)/31, c: (17-10*z)/62,
                  e: (8-12*z)/31, f: (13-4*z)/62}
    multipliers = [(160*z-24)/31, (120*z-18)/31]
    lagrangian = norm+sum(m*g for m, g in zip(multipliers, constraints))
    assert all(sp.simplify(sp.diff(lagrangian, variable).subs(stationary)) == 0
               for variable in (a, c, e, f))
    assert all(sp.simplify(g.subs(stationary)) == 0 for g in constraints)
    hessian = sp.hessian(norm, (a, c, e, f))
    assert all(hessian[:r, :r].det() > 0 for r in range(1, 5))
    value = sp.factor(norm.subs(stationary))
    assert sp.expand(value-(114*z*z-28*z+61)/62) == 0
    point = sp.Rational(57, 200)
    assert all(m.subs(z, point) > 0 for m in multipliers)
    a0, c0, e0, f0 = [stationary[v].subs(z, point) for v in (a, c, e, f)]
    assert all(v > 0 for v in (a0, point-2*a0, c0, sp.Rational(1, 2)-c0,
                               e0, f0, 1-2*e0-2*f0))
    optimum = sp.Rational(value.subs(z, point))
    assert optimum == sp.Rational(1245593, 1240000) > 1
    return {"support": [0, 2], "row2_mass": "57/200",
            "abstract_minimum_squared_norm": str(optimum),
            "formula": "(114*z^2-28*z+61)/62",
            "scope": "formal degree-capacity relaxation with four boundary lines, not a counterexample exclusion",
            "followup": "explicit positive quartic and sextic now close this support, using BFT; diagnostic alone remains a formal relaxation",
            "i5_support_closed_by_this_diagnostic": False}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    denominators = audit_denominators()
    specifications = [
        ("collision_at_0", [0], COLLISION, [0, 30, 30, 30, 30], 108, True, True),
        ("support_04", [0, 4], SUPPORT_04, [0, 6, 6, 6, 0], 17, True, True),
        ("support_03_nodal_cubics", [0, 3], SUPPORT_03, [0, 15, 15, 0, 15], 44, True, True),
        ("support_01_baseline_tight_constants", [0, 1], BASE_01, [6, 5, 6, 6, 6], 21, False, True),
        ("support_02_baseline_A_tight_constants", [0, 2], BASE_02_A, [6, 10, 2, 10, 10], 31, False, True),
        ("support_02_baseline_B_tight_constants", [0, 2], BASE_02_B, [12, 30, 8, 30, 30], 93, False, True),
        ("support_01_new_mixed_bound", [0, 1], NEW_01, [9, 4, 5, 3, 4], 16, False, True),
        ("support_02_new_mixed_bound", [0, 2], NEW_02, [20, 22, 10, 10, 8], 44, False, True),
        ("support_02_quartic_sextic", [0, 2], FINAL_02, [6, 10, 4, 5, 4], 20, False, True),
    ]
    certificates = [capacity(name, support, entries, targets, degree, denominators, closed, paired)
                    for name, support, entries, targets, degree, closed, paired in specifications]
    by_name = {r["name"]: r for r in certificates}
    assert by_name["support_03_nodal_cubics"]["constant"] == str(Fraction(27, 64)*40**15)
    assert by_name["support_01_baseline_tight_constants"]["constant"] == str(Fraction(120**6, 2048))
    assert by_name["support_02_baseline_A_tight_constants"]["constant"] == str(Fraction(30**10, 32))
    assert by_name["support_02_baseline_B_tight_constants"]["constant"] == str(Fraction(5*30**30, 65536))
    assert by_name["support_01_new_mixed_bound"]["constant"] == "36450000"
    result = {
        "status": "passed", "i": 5, "i5_solved": False,
        "tail_frontier_proved_without_supplied_terminal_scripts": [[0, 1], [0, 2]],
        "frontier_threshold": str(THRESHOLD), "row_zero": audit_row_zero(),
        "denominator_period": 360,
        "denominator_cases": {f"{p[0]},{p[1]}": r for p, r in denominators.items()},
        "certificates": certificates, "all_degree_barrier": audit_barrier(),
        "pure_powers": audit_pure_powers(),
        "congruence_frontier": audit_congruence_frontier(certificates),
        "bft_bridge": audit_bft_bridge(certificates),
        "bft_support_02_closeout": audit_bft_closeout(certificates, denominators),
        "tail_frontier_with_external_BFT": [[0, 1]],
        "BFT_frontier_threshold": str(10**75),
        "high_multiplicity_diagnostic": audit_high_multiplicity_diagnostic(),
        "universal_scope": "paper arguments and exact replay; explicit quartic and sextic plus external BFT close support 02 at n>=10^75; support 01 remains open; general i5 is not solved",
    }
    output = ROOT/"data/results/verification_i5_multiplicity_frontier.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "capacity_certificates": len(certificates),
                      "closed_cases": [r["name"] for r in certificates if r["support_closed"]],
                      "frontier_threshold": str(THRESHOLD),
                      "BFT_support_02_closeout_threshold": str(10**75),
                      "remaining_supports": [[0, 1]], "i5_solved": False}, indent=2))


if __name__ == "__main__":
    main()
