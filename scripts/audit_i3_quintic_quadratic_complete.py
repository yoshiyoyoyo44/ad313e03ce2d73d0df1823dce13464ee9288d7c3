"""Audit the complete degree-five single-allocation exclusion.

The universal argument is in the companion note. This checks its algebra,
finite residue certificates, exact rational gaps, and an independent small
numeric diagnostic. The diagnostic does not prove the infinite theorem.
"""

import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

from audit_i3_quadratic_cofactor import forward_profiles, horner

ROOT = Path(__file__).resolve().parent.parent


def equal(left, right=0):
    assert sp.expand(left-right) == 0


def symbolic():
    X, q, a, b, c, d, B = sp.symbols("X q a b c d B")
    e, r, L, z, f, Delta = sp.symbols("e r L z f Delta")
    G = (a*q-1)*(b*q+1)
    for theta in (-1, 1):
        H = c*q+d*q*q-theta
        V = c+d*q-theta*(a*b*q+a-b)
        C = V*(q*V-G)
        if theta == -1:
            equal(q*C, H*(H+G))
            equal(q*V, H+G)
        else:
            equal(q*C, (H-G)*(H-2*G))
            equal(q*V, H-G)
    BX = 1+e*X+r*X**2+L*X**3
    DX = sp.Poly(sp.expand((1+b*X)*BX), X)
    FX = sp.Poly(sp.expand(2+(a*X-1)*(1+b*X)*BX), X)
    equal(DX.nth(1), b+e)
    equal(DX.nth(2), b*e+r)
    equal(DX.nth(3), L+b*r)
    equal(FX.nth(3).subs(L, 1), a*b*e+(a-b)*r-1)
    equal(FX.nth(4).subs(L, 1), a-b+a*b*r)
    # Exact A-C lower bound for the t=3,x=0 branch.
    gap = z*q**4+f*q**3-(2*z*q+f)*(z*q*q+1)
    equal(gap, z*q**3*(q-2*z)+f*q*q*(q-z)-2*z*q-f)
    # Final t=3 cubic, with B=1+X^2+X^3.
    A = f+(z-1)*q+(f-1)*q**2+(z+f)*q**3+z*q**4
    C = ((z+d)*q+f)*(d*q*q+1)
    cubic = -z*q**3+(d*(z+d)-z-f)*q*q+(f*(d-1)+1)*q+d+1
    equal(C-A, q*cubic)
    equal(sp.Poly(cubic, q).nth(0), d+1)
    # LTE is proved by a unit factor; no external theorem is used.
    k = sp.symbols("k")
    equal((1+3*k)**3-1, 9*k*(1+3*k+3*k*k))
    assert all((1+3*kv+3*kv*kv) % 3 == 1 for kv in range(3))
    assert pow(4, 3, 9) == 1
    assert all((pow(4, v, 9)-1) % 9 in (3, 6) for v in (1, 2))
    return {"two_endpoint_identities": True, "coefficient_formulas": True,
            "t3_gap_and_terminal_cubic": True, "elementary_LTE_identity": True}


def constants_and_residues():
    R = 6*Fraction(33, 32)*(1+Fraction(2, 32)+Fraction(1, 2*32**2))
    assert R == Fraction(215523, 32768) < 7
    assert R/4 < 2 and R/2 < 4
    assert 6*Fraction(33, 32)**2 < R
    residues = []
    for sign in (-1, 1):
        allowed = set()
        for G in (2, 6):
            for W in range(8):
                t = (-3*W*(W+sign*G)) % 8
                residues.append([sign, G, W, t])
                if 1 <= t <= 6:
                    allowed.add(t)
        assert allowed == {3}
    # With even B and odd G the product is always even.
    for G in (1, 3, 5, 7):
        for W in range(8):
            assert W*(W+G) % 2 == 0
    # T is odd, divides t, and never has exactly one factor of 3.
    supports = [(t, T) for t in (2, 3, 4, 6)
                for T in range(1, t+1, 2)
                if t % T == 0 and not (T % 3 == 0 and T % 9 != 0)]
    assert all(T == 1 for _, T in supports)
    assert 3**6 < 2**10 and 2*3**3 > 10*4
    # Induction: a margin >0 at e is still positive at e+1, e>=4.
    assert 3*10*4 > 10*(4+1)
    return {"R": str(R), "32_odd_B_residue_cases": residues,
            "odd_B_allowed_t": [3], "all_allowed_t": [2, 3, 4, 6],
            "T_equals_1": True, "radix_3_degree_contradiction": True}


def finite_shapes():
    # Negative e with r<=3 and positive D1,D2 has exactly one profile.
    negative = []
    for b in range(1, 10):
        for e in range(-5, 0):
            for r in range(4):
                if b+e > 0 and b*e+r > 0:
                    negative.append([b, e, r])
    assert negative == [[2, -1, 3]]
    assert all((1-q+3*q*q+q**3) % 4 == 0 for q in (1, 3))
    small = [(e, r) for e in range(2) for r in range(2) if (e, r) != (0, 0)]
    assert small == [(0, 1), (1, 0), (1, 1)]
    even_shapes = [(e, r) for e in range(4) for r in range(4)
                   if (e+r) % 2 == 0 and (e, r) != (0, 0)]
    invalid = [(e, r) for e, r in even_shapes if all(
        (1+e*q+r*q*q+q**3) % 4 == 0 for q in (1, 3))]
    assert invalid == [(1, 1), (3, 3)]
    survivors = [pair for pair in even_shapes if pair not in invalid]
    assert survivors == [(0, 2), (1, 3), (2, 0), (2, 2), (3, 1)]
    a, y = sp.symbols("a y")
    chosen = {(0, 2): 5*a-2, (2, 0): 4*a-1,
              (2, 2): 5*a-2, (1, 3): 7*a-2, (3, 1): 7*a-3}
    for e, r in survivors:
        f = a-2-e
        # a>=3+e follows from f>=1; positive coefficient certificate.
        p = sp.Poly(sp.expand((chosen[e, r]-4*f).subs(a, 3+e+y)), y)
        assert all(value > 0 for value in p.all_coeffs())
        if (e, r) != (2, 0):
            p = sp.Poly(sp.expand((chosen[e, r]-5*f).subs(a, 3+e+y)), y)
            assert all(value > 0 for value in p.all_coeffs())
    final_mod3 = []
    for a in range(3):
        q = 2*(a-1) % 3
        if not q:
            continue
        n = (2+(a*q-1)*(2*q+1)*(1+2*q+q**3)) % 3
        final_mod3.append([a, q, n])
        assert n == 2
    assert final_mod3 == [[0, 1, 2], [2, 2, 2]]
    return {"negative_coefficient_case": negative,
            "q_less_than_2z_shapes": small, "even_B_terminal_shapes": survivors,
            "digit_gaps_verified": True, "final_mod3": final_mod3}


def numeric_diagnostic():
    profiles = cases = 0
    for q in (35, 37, 41, 43):
        rows, _ = forward_profiles(q, m=5)
        for a, b, D, B, F in rows:
            n, f = horner(F, q), F[1]
            if n % 8 or f < 1:
                continue
            profiles += 1
            for theta in (-1, 1):
                for d in range(a*b+1):
                    for x in range(f+1):
                        c = x+theta*B[1]
                        J = [1]+[
                            c*(B[e-1] if e-1 < len(B) else 0)
                            +d*(B[e-2] if 0 <= e-2 < len(B) else 0)
                            -theta*(B[e] if e < len(B) else 0)
                            for e in range(1, 6)]
                        if any(not 0 <= v <= w for v, w in zip(J, F)):
                            continue
                        j = horner(J, q)
                        if min(j, n-j) < 4:
                            continue
                        cases += 1
                        # Direct first divisibility, independent of C/t formula.
                        assert (3*j*(j-1)) % (n-1) != 0
    return {"radices": [35, 37, 41, 43], "profiles": profiles, "cases": cases,
            "first_hits": 0, "diagnostic_only": True}


def main():
    assert __debug__, "Do not run with python -O."
    result = {"scope": "all degree-five quadratic-cofactor single allocations excluded for true i=3 counters; general i=3 open",
              "symbolic": symbolic(), "residues": constants_and_residues(),
              "finite_shapes": finite_shapes(), "numeric": numeric_diagnostic()}
    target = ROOT/"data/results/verification_i3_quintic_quadratic_complete.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"symbolic": True, "finite_shapes": True,
                      "numeric": result["numeric"], "general_i3_open": True}))


if __name__ == "__main__":
    main()
