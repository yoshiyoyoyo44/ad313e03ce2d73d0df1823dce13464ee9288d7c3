"""Exact certificates for the quintic, degree-three complete allocation.

The paper covers unbounded parameters, both constant digits, and all 14
residual degree triples. The small-base CRT replay is a separate diagnostic.
General i=3 in Erdos problem 699 remains unresolved.
"""

import json
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
X = sp.symbols("X")
a, q, c, d, h, k, ell, r, s, u, v, beta, gamma = sp.symbols(
    "a q c d h k ell r s u v beta gamma"
)


def equal(left, right=0):
    assert sp.cancel(left - right) == 0, sp.factor(left - right)


def coeffs(expression):
    return [sp.expand(expression).coeff(X, i) for i in range(4)]


def audit_degree_coverage():
    rows = {}
    for epsilon in (0, 1):
        triples = sorted(
            row for row in product(range(4), repeat=3)
            if sum(row) == 5 and row[1] >= 1 and row[2] >= 1
            and (epsilon == 1 or row[0] >= 1)
        )
        rows[str(epsilon)] = [list(row) for row in triples]
    assert len(rows["0"]) == 6 and len(rows["1"]) == 8
    return rows


def audit_cancellation_and_second_condition():
    D1, D2, D3, D4 = sp.symbols("D1 D2 D3 D4")
    DP = 1 + D1*X + D2*X**2 + D3*X**3 + D4*X**4
    FP = 2 + (a*X-1)*DP
    AP = sp.cancel((FP-1)/X)
    equal(X*AP - (a*X-1)*DP, 1)
    equal(AP.subs(X, 0), a-D1)
    equal(sp.expand(AP).coeff(X, 4), a*D4)

    # First-condition cancellation after the known zero constant digit.
    B0, B1, B2, H0, H1 = sp.symbols("B0 B1 B2 H0 H1")
    for epsilon in (0, 1):
        L0 = X*H0 if epsilon == 0 else H0
        L1 = H1 if epsilon == 0 else X*H1
        K = sp.cancel(L0*L1/X)
        equal((B0*L0)*(B1*L1)/X, B0*B1*K)
        equal(B2*(B0*L0)*(B1*L1)/X, B0*B1*B2*K)

    # Literal cancellation of D(q), with no coprimality requirement:
    # (a*q-1)*D(q) | 6*D(q)*W(q) iff a*q-1 | 6*W(q).
    W0, W1, W2, W3 = sp.symbols("W0 W1 W2 W3")
    WP = W0 + W1*X + W2*X**2 + W3*X**3
    remainder = sp.cancel(a**3*(WP.subs(X, q)-WP.subs(X, 1/a))/(a*q-1))
    assert sp.Poly(remainder, a, q, W0, W1, W2, W3).domain.is_ZZ
    equal(a**3*WP.subs(X, q) - a**3*WP.subs(X, 1/a), (a*q-1)*remainder)
    # The same termwise geometric identity works for every residual degree.
    for degree in range(1, 15):
        quotient = sum((a*q)**j for j in range(degree))
        equal((a*q)**degree-1, (a*q-1)*quotient)

    z = sp.symbols("z")
    equal(4-27*z*(1-z)**2, (1-3*z)**2*(4-3*z))
    assert Fraction(4, 27) < Fraction(1, 4)
    return {"second_condition": "a*q-1 divides 6*L0(q)*L1(q)*L2(q)",
            "nonzero_integer_bound": "0 < |6*a^rho*W(1/a)| < 3*a^rho/D(1/a)",
            "termwise_degree_checks": 14}


def audit_endpoint_coefficients():
    certificates = {}
    # epsilon=0, residual degrees (3,1,1).
    JP = 1+(h*X-1)*(1+r*X+beta*X**2)
    KP = 2+(ell*X-2)*(1+s*X+gamma*X**2)
    difference = sp.expand(JP-KP).subs(r, h-ell+2*s)
    equal(difference.coeff(X, 1), 0)
    equal(difference.coeff(X, 2), h*(h-ell)+(2*h-ell)*s+2*gamma-beta)
    equal(difference.coeff(X, 3), h*beta-ell*gamma)
    rows = []
    for bb, gg in ((1, 1), (1, 2), (2, 1)):
        expression = sp.factor(difference.coeff(X, 2).subs(
            {beta: bb, gamma: gg, ell: h*sp.Rational(bb, gg)}))
        rows.append({"beta": bb, "gamma": gg, "residual": str(expression)})
    assert rows[0]["residual"] == "h*s + 1"
    equal(sp.sympify(rows[1]["residual"]), 3*h*s/2+h**2/2+3)
    equal(sp.sympify(rows[2]["residual"]), -h**2)
    certificates["epsilon0_311"] = rows

    # epsilon=0, residual degrees (1,3,1).
    JP = c*X*(1+r*X+beta*X**2)
    KP = 2+(ell*X-2)*(1+s*X+gamma*X**2)
    difference = sp.expand(JP-KP).subs({beta: 2, gamma: 1, ell: 2*c, s: c/2})
    equal(difference.coeff(X, 1), 0)
    equal(difference.coeff(X, 2), c*r-c**2+2)
    equal(difference.coeff(X, 3), 0)
    integer_candidates = [cc for cc in sp.divisors(2) if cc % 2 == 0]
    assert integer_candidates == [2]
    equal(difference.subs({c: 2, r: 1}), 0)
    certificates["epsilon0_131"] = {"c": 2, "r": 1, "s": 1,
                                   "J": [0, 2, 2, 4], "minimum_a": 4}

    # epsilon=1, residual degrees (1,3,1).
    r0 = sp.symbols("r0")
    JP = (1+c*X)*(1+r0*X+beta*X**2)
    KP = 2+(ell*X-1)*(1+r*X+gamma*X**2)
    difference = sp.expand(JP-KP).subs({beta: 2, gamma: 1, ell: 2*c, r0: c-r})
    equal(difference.coeff(X, 1), 0)
    equal(difference.coeff(X, 2), c**2-3*c*r+3)
    equal(difference.coeff(X, 3), 0)
    divisors = sp.divisors(3)
    values = [(int(cc), Fraction(int(cc)**2+3, 3*int(cc))) for cc in divisors]
    assert all(value.denominator != 1 for _, value in values)
    certificates["epsilon1_131"] = {"c_divides": 3,
                                   "r_values": [[cc, str(value)] for cc, value in values]}

    # epsilon=1, residual degrees (3,1,1).
    r1 = sp.symbols("r1")
    JP = 1+d*X*(1+r1*X+beta*X**2)
    KP = 2+(ell*X-1)*(1+r*X+gamma*X**2)
    difference = sp.expand(JP-KP).subs({beta: 2, gamma: 1, ell: 2*d, r: d})
    equal(difference.coeff(X, 1), 0)
    equal(difference.coeff(X, 2), d*r1-2*d**2+1)
    equal(difference.coeff(X, 3), 0)
    assert sp.divisors(1) == [1]
    equal(difference.subs({d: 1, r1: 1}), 0)
    certificates["epsilon1_311"] = {"d": 1, "r1": 1, "r": 1,
                                   "J": [1, 1, 1, 2], "minimum_a": 3}
    return certificates


def audit_epsilon0_221():
    JP = X*(c*X+d)*(1+u*X)
    KP = 1+(h*X**2+k*X-1)*(1+v*X)
    difference = sp.expand(JP-KP).subs({k: d+v, h: c+(u-v)*d-v**2})
    equal(difference.coeff(X, 1), 0)
    equal(difference.coeff(X, 2), 0)
    equal(difference.coeff(X, 3), v**3-(u-v)*(v*d-c))
    # Reduction u^2*v^2*s<=11 is proved in the paper, not inferred from a scan.
    parameter_rows = []
    for uu, vv, ss in product(range(1, 4), range(1, 4), range(1, 12)):
        if (uu*vv)**2*ss > 11 or uu == vv:
            continue
        if vv**3 % (uu-vv):
            continue
        parameter_rows.append((uu, vv, ss))
    assert parameter_rows == [(1, 2, 1), (1, 2, 2), (2, 1, 1), (2, 1, 2)]
    rows = []
    for uu, vv, ss in parameter_rows:
        cc = vv*d-sp.Rational(vv**3, uu-vv)
        hp = cc*sp.Rational(uu, vv)
        kp = d+vv
        jq = sp.expand(JP.subs({u: uu, c: cc}))
        equal(jq, sp.expand(KP.subs({v: vv, h: hp, k: kp})))
        lp = sp.cancel(jq.coeff(X, 3)/ss)
        rp = sp.cancel((lp-d)/2)
        second_difference = sp.expand(jq-(2+(lp*X-2)*(1+rp*X+ss*X**2)))
        equal(second_difference.coeff(X, 1), 0)
        equal(second_difference.coeff(X, 3), 0)
        residual = sp.factor(second_difference.coeff(X, 2))
        rows.append({"u": uu, "v": vv, "s": ss, "c": str(cc),
                     "ell": str(lp), "r": str(rp), "residual": str(residual)})
        if (uu, vv, ss) == (2, 1, 1):
            equal(residual, -(d**2-6*d+1))
            assert all((dd**2-6*dd+1) % 3 != 0 for dd in range(3))
        elif (uu, vv, ss) == (2, 1, 2):
            equal(rp, sp.Rational(-1, 2))
        elif (uu, vv, ss) == (1, 2, 1):
            equal(residual, -(d**2+9*d+22))  # Strictly negative for d>=0.
        else:
            equal(residual, d+4)  # Cannot vanish for d>=0.
    return rows


def audit_size_certificates():
    # epsilon=1, (2,2,1): no low-congruence normalization or complement used.
    constant = 1+Fraction(1, 2)+Fraction(1, 25)+Fraction(1, 250)
    assert constant == Fraction(193, 125)
    ratio = 3*constant**2/8
    assert ratio == Fraction(111747, 125000) < 1
    certificates = {"epsilon1_221": {"j_over_a_beta_q3_bound": str(constant),
                                      "3K_over_A_bound": str(ratio)}}
    # Other easy cases reduce to these positive/nonnegative polynomials at q>=3.
    y = sp.symbols("y")
    for name, expression in {
        "quadratic_gap": q**2-3,
        "zero_r0_gap": 2*q-3,
        "cubic_gap_strict_input": q-3,
    }.items():
        shifted = sp.Poly(expression.subs(q, y+3), y)
        assert all(cc >= 0 for cc in shifted.all_coeffs())
        certificates[name] = [int(cc) for cc in reversed(shifted.all_coeffs())]
    return certificates


def digits(n, base):
    result = []
    while n:
        result.append(n % base)
        n //= base
    return result or [0]


def forward_profiles(base, aa):
    def descend(ds):
        if len(ds) == 5:
            if aa*ds[-1] < base:
                yield tuple(ds)
            return
        maximum = aa*ds[-1]
        for current in range(max(1, maximum-base+1), maximum+1):
            yield from descend(ds+[current])
    for first in range(1, aa):  # F1>=1 is an explicit theorem hypothesis.
        yield from descend([1, first])


def backward_profiles(base, aa):
    def descend(ds):
        if len(ds) == 4:
            if 1 <= ds[-1] < aa:
                yield tuple([1]+list(reversed(ds)))
            return
        current = ds[-1]
        for previous in range(max(1, (current+aa-1)//aa), (current+base-1)//aa+1):
            yield from descend(ds+[previous])
    for leading in range(1, (base-1)//aa+1):
        yield from descend([leading])


def crt_first_residues(n):
    modulus = (n-1)//gcd(n-1, 3)
    residues, accumulated = [0], 1
    for prime, exponent in sorted(sp.factorint(modulus).items()):
        prime_power = int(prime)**int(exponent)
        inverse = pow(accumulated, -1, prime_power)
        residues = sorted({value+accumulated*((target-value)*inverse % prime_power)
                           for value in residues for target in (0, 1)})
        accumulated *= prime_power
    assert accumulated == modulus
    return residues, modulus


def diagnostic_small_bases():
    totals = {"profiles": 0, "range_degree3_first_hits": 0,
              "digit_dominated_hits": 0, "complete_allocation_hits": 0}
    witnesses = []
    for base in range(3, 11):
        for aa in range(2, base):
            profiles = set(forward_profiles(base, aa))
            assert profiles == set(backward_profiles(base, aa))
            for ds in sorted(profiles):
                totals["profiles"] += 1
                fc = [1]+[aa*ds[t-1]-ds[t] for t in range(1, 5)]+[aa*ds[4]]
                assert fc[1] >= 1 and all(0 <= ff < base for ff in fc)
                n = sum(ff*base**t for t, ff in enumerate(fc))
                residues, modulus = crt_first_residues(n)
                for residue in residues:
                    first = max(0, (base**3-residue+modulus-1)//modulus)
                    last = (min(base**4-1, n//2)-residue)//modulus
                    for offset in range(first, last+1):
                        j = residue+offset*modulus
                        assert 4 <= j <= n//2 and len(digits(j, base)) == 4
                        assert 3*j*(j-1) % (n-1) == 0
                        totals["range_degree3_first_hits"] += 1
                        jc = digits(j, base)
                        if any(jj > ff for jj, ff in zip(jc, fc)):
                            continue
                        totals["digit_dominated_hits"] += 1
                        DP = sp.Poly(sum(dd*X**t for t, dd in enumerate(ds)), X, domain=sp.QQ)
                        JP = sp.Poly(sum(jj*X**t for t, jj in enumerate(jc)), X, domain=sp.QQ)
                        remainder = (JP*(JP-1)*(JP-2)).rem(DP)
                        if remainder.is_zero:
                            totals["complete_allocation_hits"] += 1
                        if len(witnesses) < 12:
                            witnesses.append({"q": base, "a": aa, "D": list(ds),
                                              "J": jc, "remainder": str(remainder.as_expr())})
    assert totals["complete_allocation_hits"] == 0
    return {"role": "diagnostic; universal proof is the 14-case paper",
            "bases_inclusive": [3, 10], **totals, "first_hits_examples": witnesses}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    result = {
        "status": "passed", "general_i3_solved": False,
        "scope": "deg F=5, deg J=3, F1>=1, complete D allocation, first numerical condition",
        "degree_coverage": audit_degree_coverage(),
        "cancellation": audit_cancellation_and_second_condition(),
        "endpoint_coefficients": audit_endpoint_coefficients(),
        "epsilon0_221_finite_shapes": audit_epsilon0_221(),
        "size_certificates": audit_size_certificates(),
        "small_base_diagnostic": diagnostic_small_bases(),
    }
    output = ROOT/"data/results/verification_i3_quintic_split_allocation.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "residual_cases": 14,
                      "diagnostic": result["small_base_diagnostic"],
                      "general_i3_solved": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
