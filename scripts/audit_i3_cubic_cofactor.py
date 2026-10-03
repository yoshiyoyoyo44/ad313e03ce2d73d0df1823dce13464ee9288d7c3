"""Replay the cubic-cofactor partial-sharing theorem.

Universal bounds and their scope are in the companion note. The finite tail
is derived from those bounds, not a diagnostic box. Two directions generate
the factor profiles; quotient enumeration and CRT independently test the
first necessary condition. Assertions must remain enabled.
"""

import json
import math
from fractions import Fraction
from pathlib import Path

import sympy as sp

from audit_i3_quadratic_cofactor import (
    backward_profiles, forward_profiles, horner,
)

ROOT = Path(__file__).resolve().parent.parent


def equal(left, right=0):
    assert sp.expand(left-right) == 0


def symbolic():
    q, A, P, h, e = sp.symbols("q A P h e")
    B = (q*A-1)/P
    results = []
    for s in (0, 1, 2):
        j = s+h*B
        U, V = s*P-h, (s-1)*P-h
        C = U*V/q
        equal(sp.cancel(P*P*j*(j-1)/q-C
                        - A*(h*(U+V)+q*h*h*A)))
        # Constant terms at q=0: P(0)=-1, h(0)=e-s.
        equal((U*V).subs({P:-1, h:e-s}), e*(e-1))
        results.append(s)
    return {"all_three_compression_identities": results,
            "constant_term": "e*(e-1), zero for e=0,1",
            "requires_no_polynomial_divisibility_of_F_minus_1": True}


def inequalities():
    q, y = sp.symbols("q y", nonnegative=True)
    gaps = {
        "m8_q_ge_9": (q**6-6*(q-1)*(q+1)**4, 9),
        "m9_q_ge_4": (q**7-6*(q-1)*(q+1)**4, 4),
        "m_ge_10_q_ge_3": (q**8-6*(q-1)*(q+1)**4, 3),
        "s1_m7_q_ge_10": (4*q**5-3*(q-1)*(q+1)**4, 10),
    }
    certificates = {}
    for name, (gap, start) in gaps.items():
        shifted = sp.Poly(sp.expand(gap.subs(q, start+y)), y)
        assert all(value > 0 for value in shifted.all_coeffs())
        certificates[name] = [int(value) for value in shifted.all_coeffs()]
    # General root-disk bound: (1+1/q)^(2k) < 2 for q>=4k.
    # Every positive-degree binomial coefficient is <=(2k)^r; the
    # geometric series has further positive terms. This is universal,
    # and the following exact cases only check its arithmetic.
    for k in range(1, 65):
        qv = max(12, 4*k)
        assert Fraction(qv+1, qv)**(2*k) < 2
        assert 12*Fraction(qv-1, qv*qv) < 1
    return {"positive_shift_certificates": certificates,
            "general_root_disk_threshold": "m>=2*k+2, q>=max(12,4*k)",
            "linear_factor_ratio": "<6*(q-1)*(q+1)**4/q**(m-2)",
            "central_ratio": "<3*(q-1)*(q+1)**4/(4*q**(m-2))"}


def divide_linear(coefficients, c):
    R = [coefficients[0]]
    for value in coefficients[1:-1]:
        R.append(value-c*R[-1])
    return tuple(R) if c*R[-1] == coefficients[-1] else None


def profiles(q, m, direction):
    base, terminal = (forward_profiles if direction == "forward"
                      else backward_profiles)(q, m=m)
    result = set()
    for a, b, D, first_B, F in base:
        for c in range(b, a+1):
            if a*b*c >= q:
                continue
            if direction == "backward":
                # Independent root and repeated-root tests on D itself.
                if b != c:
                    root = sum(v*(-1)**i*c**(m-1-i)
                               for i, v in enumerate(D))
                else:
                    root = sum(i*v*(-1)**(i-1)*b**(m-1-i)
                               for i, v in enumerate(D) if i)
                if root:
                    continue
            B = divide_linear(first_B, c)
            if direction == "backward":
                assert B is not None
            if B is None:
                continue
            assert B[0] == 1 and B[-1] > 0
            rebuilt = [0]*m
            for i, v in enumerate(B):
                for k, w in enumerate((1, b+c, b*c)):
                    rebuilt[i+k] += v*w
            assert tuple(rebuilt) == D
            result.add((a, b, c, D, B, F))
    return result, terminal


def polynomial_divides(values, divisor):
    """Exact Z[X] long division; constant-one divisor is primitive."""
    R = list(values)
    for k in range(len(R)-1, len(divisor)-2, -1):
        if R[k] % divisor[-1]:
            return False
        coefficient = R[k]//divisor[-1]
        start = k-(len(divisor)-1)
        for i, value in enumerate(divisor):
            R[start+i] -= coefficient*value
    return not any(R)


def quotient_cases(q, profile, allowed_s):
    a, b, c, D, B, F = profile
    m, Z = len(F)-1, a*b*c
    n = horner(F, q)
    A, P = (n-1)//q, (a*q-1)*(b*q+1)*(c*q+1)
    BV = horner(B, q)
    assert n == 2+P*BV and BV > 0
    cases, first_hits = 0, set()
    for e in (0, 1):
        for s in allowed_s:
            r0 = e-s
            for x in range(F[1]+1):
                r1 = x-r0*B[1]
                for y in range(F[2]+1):
                    r2 = y-r1*B[1]-r0*B[2]
                    for r3 in range(Z+1):
                        R = (r0, r1, r2, r3)
                        J = [0]*(m+1)
                        J[0] = s
                        for i, v in enumerate(B):
                            for k, w in enumerate(R):
                                J[i+k] += v*w
                        if any(not 0 <= v <= f for v, f in zip(J, F)):
                            continue
                        j = horner(J, q)
                        if not 4 <= j <= n//2:
                            continue
                        cases += 1
                        assert sum(v*q**i for i, v in enumerate(J)) == j
                        assert sum(v*q**i for i, v in enumerate(F)) == n
                        h = horner(R, q)
                        U, V = s*P-h, (s-1)*P-h
                        assert U*V % q == 0
                        C = U*V//q
                        assert P*P*(j*(j-1)//q)-C == (
                            A*(h*(U+V)+q*h*h*A))
                        assert 0 < abs(C)*q < 2*P*P
                        if s == 1:
                            assert 0 < -4*C*q <= P*P
                        if 3*j*(j-1) % (n-1) == 0:
                            first_hits.add((tuple(J), s))
    return cases, first_hits


def crt_first_cases(q, profile, allowed_s):
    """Generate ALL j satisfying the first condition, then test sharing."""
    _, _, _, _, B, F = profile
    n = horner(F, q)
    modulus = (n-1)//math.gcd(n-1, 3)
    factors = {int(p):int(exponent) for p, exponent in sp.factorint(modulus).items()}
    assert math.prod(p**exponent for p, exponent in factors.items()) == modulus
    assert all(sp.isprime(p) for p in factors)
    residues, current = [0], 1
    for p, exponent in sorted(factors.items()):
        power = p**exponent
        inverse = pow(current, -1, power)
        residues = [r+current*((endpoint-r)*inverse % power)
                    for r in residues for endpoint in (0, 1)]
        current *= power
    assert current == modulus and len(set(residues)) == len(residues)
    hits, dominated, numeric = set(), 0, 0
    for residue in residues:
        j = residue
        if j < 4:
            j += ((4-j+modulus-1)//modulus)*modulus
        while j <= n//2:
            numeric += 1
            assert 3*j*(j-1) % (n-1) == 0
            digits, v = [], j
            for _ in F:
                v, digit = divmod(v, q)
                digits.append(digit)
            assert not v
            if all(v <= f for v, f in zip(digits, F)):
                dominated += 1
                for s in allowed_s:
                    values = list(digits)
                    values[0] -= s
                    if polynomial_divides(values, B):
                        hits.add((tuple(digits), s))
            j += modulus
    return hits, dominated, numeric, len(residues)


def finite_tail():
    expected = {
        (8,3):(0,0), (8,4):(2,24), (8,5):(4,36), (8,6):(13,218),
        (8,7):(25,278), (8,8):(53,1174), (9,3):(0,0),
        (7,3):(0,0), (7,4):(2,9), (7,5):(4,11), (7,6):(11,67),
        (7,7):(16,77), (7,8):(32,287), (7,9):(44,367),
    }
    rows = []
    for (m, q), counts in expected.items():
        allowed_s = (1,) if m == 7 else (0, 1, 2)
        forward, ft = profiles(q, m, "forward")
        backward, bt = profiles(q, m, "backward")
        assert forward == backward and ft == bt
        cases = dominated = numeric = residues = 0
        for profile in sorted(forward):
            count, quotient_hits = quotient_cases(q, profile, allowed_s)
            crt_hits, dom, num, res = crt_first_cases(q, profile, allowed_s)
            assert quotient_hits == crt_hits == set()
            cases += count
            dominated += dom
            numeric += num
            residues += res
        assert (len(forward), cases) == counts
        rows.append({"m":m, "q":q, "s":list(allowed_s),
                     "profiles":len(forward), "quotients":cases,
                     "negative_B_profiles":sum(any(v < 0 for v in row[4])
                                               for row in forward),
                     "terminal_D_sequences":ft,
                     "CRT_residues":residues, "CRT_numeric_j":numeric,
                     "CRT_dominated_j":dominated, "first_hits":0})
    assert sum(row["profiles"] for row in rows) == 206
    assert sum(row["quotients"] for row in rows) == 2548
    assert sum(row["negative_B_profiles"] for row in rows) == 104
    return {"derived_domain":"m8:q3..8; m9:q3; m7,s1:q3..9",
            "independent_profile_enumerators":2,
            "independent_numeric_methods":["all quotients", "all CRT roots"],
            "profiles":206, "quotients":2548, "negative_B_profiles":104,
            "first_hits":0, "rows":rows}


def split_example():
    X = sp.symbols("X")
    B = 1+2*X+2*X**2+X**3+3*X**4+2*X**5
    P = (20*X-1)*(X+1)*(2*X+1)
    F, J = sp.expand(2+P*B), sp.expand(1+(17*X**2+18*X**3)*B)
    assert sp.rem(J-1, B, X) == 0
    assert sp.rem(J, X+1, X) == 0
    assert sp.rem(J-2, 2*X+1, X) == 0
    # No possible choice of one omitted negative linear factor makes
    # the old quadratic-cofactor single-allocation theorem applicable.
    for cofactor in ((X+1)*B, (2*X+1)*B):
        assert all(sp.rem(J-s, cofactor, X) != 0 for s in (0, 1, 2))
    q = 257
    assert sp.isprime(q)
    fc = [int(sp.Poly(F,X).nth(i)) for i in range(9)]
    jc = [int(sp.Poly(J,X).nth(i)) for i in range(9)]
    assert all(0 <= v <= f < q for v, f in zip(jc, fc))
    n, j = horner(fc,q), horner(jc,q)
    assert 4 <= j <= n//2 and n % 8 == 0
    assert (n-1) % q == 0 and (n-1) % (q*q) != 0
    remainder = 3*j*(j-1) % (n-1)
    assert remainder != 0
    # Deep 2-adic digit examples are possible too; sharing and even n
    # alone are insufficient. Lift the odd root with F'(q) odd.
    lift = 1
    for exponent in range(1, 51):
        modulus = 1 << (exponent+1)
        if horner(fc,lift) % modulus:
            lift += 1 << exponent
        assert horner(fc,lift) % modulus == 0
        assert sum(i*fc[i]*lift**(i-1) for i in range(1,9)) % 2 == 1
    if lift <= max(fc):
        lift += 1 << 51
    deep_n, deep_j = horner(fc,lift), horner(jc,lift)
    assert deep_n % (1 << 51) == 0 and 4 <= deep_j <= deep_n//2
    assert 3*deep_j*(deep_j-1) % (deep_n-1) != 0
    return {"F":fc, "J":jc, "B": [int(sp.Poly(B,X).nth(i)) for i in range(6)],
            "a":20, "b":1, "c":2, "q":q, "n":n, "j":j,
            "assignments":{"X+1":0,"B":1,"2X+1":2},
            "n_mod8":0, "full_q_in_n_minus_1":True,
            "first_remainder":remainder, "true_counterexample":False,
            "deep_2adic_example":{"q":lift, "v2_n_at_least":51,
                                  "q_prime_power_not_asserted":True,
                                  "true_counterexample":False}}


def degree7_small_zero_allocation():
    # j<=n/2 and n>=32 imply h<=8P/15, so t<3 for q>=32.
    bound = Fraction(184,75)*Fraction(33,32)**4
    assert bound < 3
    odd_B_t = set()
    for P in (2,6):
        for h in range(8):
            t = -3*h*(h+P) % 8
            if t in (1,2):
                odd_B_t.add(t)
    assert not odd_B_t
    assert all(h*(h+P) % 2 == 0 for P in (1,3,5,7) for h in range(8))
    # Universal structural gap for P=(aX-1)(2X+1)^2, deg B=4.
    # Assuming q<=5f forces L=1, t3 in {0,1}, r2>=-t3.
    # The only negative r2 is (-1,1), forcing B1>=1; F3>5a.
    a, y, e = sp.symbols("a y e", nonnegative=True)
    gap = (7*a-1)-5*a
    assert all(v > 0 for v in sp.Poly(gap.subs(a,y+2),y).coeffs())
    # Nonnegative r2>=2, or r2=t3=1, also exceed q<5a.
    for gap in (9*a-4-5*a, 9*a-8-5*a, 12*a-4-5*a):
        assert all(v >= 0 for v in sp.Poly(gap.subs(a,y+2),y).all_coeffs())
    pairs = ((0,0),(0,1),(1,0))
    for r, t3 in pairs:
        F3 = 4*a+(a-4)*r+(4*a-4)*e-t3
        gap = sp.Poly(sp.expand((F3-5*a).subs({a:y+2,e:1})),y)
        assert all(v >= 0 for v in gap.all_coeffs())
    # Thus e<=0. D2>0 gives e>=0 for r=0 and e>=-1 for r=1.
    e, r, t3, X = sp.symbols("e r t3 X")
    BX = 1+e*X+r*X**2+t3*X**3+X**4
    DX = sp.Poly(sp.expand((1+2*X)**2*BX),X)
    FX = sp.Poly(sp.expand(2+(a*X-1)*(1+2*X)**2*BX),X)
    equal(FX.nth(4).subs({e:-1,r:1,t3:0}), -5)
    # e=0 => f=a-4; either remaining nonzero pair has F5>5f.
    equal(FX.nth(5).subs({e:0,r:1,t3:0})-5*(a-4),16)
    equal(FX.nth(5).subs({e:0,r:0,t3:1})-5*(a-4),12)
    equal(DX.nth(3).subs({e:0,r:0,t3:0}),0)
    # The two low-digit congruences for s=0.
    x, f, p1, B1, r1, ev, q = sp.symbols("x f p1 B1 r1 ev q")
    PV = -1+p1*q
    hv = ev+r1*q
    constant_C = sp.Poly(sp.expand(hv*(hv+PV)),q).nth(1)
    equal(constant_C.subs(ev,0),-r1)
    equal(constant_C.subs(ev,1),r1+p1)
    return {"scope":"m7,s0,j<=n/2,q odd>=32,n>=32,8|n,F1>=1",
            "strict_t_upper_bound":str(bound), "t_equals_2":True,
            "two_low_digit_congruences":True,
            "b_c_equal_2_structural_gap":"q>5*F1",
            "uses_T_or_other_odd_Kummer":False}


def degree7_remaining_endpoint():
    R = 6*Fraction(33,32)**4
    assert R < 7 and R/4 < 2
    allowed = set()
    for P in (2,6):
        for W in range(8):
            t = -3*W*(W-P) % 8
            if 1 <= t <= 6:
                allowed.add(t)
    assert allowed == {3}
    supports = [(t,T) for t in (2,3,4,6) for T in range(1,t+1,2)
                if t % T == 0 and not (T % 3 == 0 and T % 9 != 0)]
    assert all(T == 1 for _,T in supports)
    # The inherited elementary LTE identity gives u>=2*3^(e-1).
    # Degree seven gives u<13e, and these bounds contradict u>=51.
    assert 3**8 < 2**13 and 2*3**3 > 13*4
    assert 3*13*4 > 13*(4+1)
    q, ev, r1, p1 = sp.symbols("q ev r1 p1")
    h, P = ev-2+r1*q, -1+p1*q
    low = sp.Poly(sp.expand((h-P)*(h-2*P)),q).nth(1)
    equal(low.subs(ev,0),2*p1-r1)
    equal(low.subs(ev,1),r1-p1)
    assert all((h-P)*(h-2*P) % 3 in (0,2)
               for P in (1,2) for h in range(3))
    return {"scope":"true counters, m7, B|J-2, small j",
            "R":str(R), "T":1, "M":[1,3], "3_does_not_divide_q":True,
            "B_leading_coefficient":1, "remaining_t":[3,4,6],
            "t2_excluded_by_low_digit_and_q_gt_5F1":True,
            "t3_requires_J0_J1":[0,"F1"],
            "t4_t6_require_a_b_c_even":True,
            "t4_t6_require_M_1":True, "t4_requires_even_u":True,
            "q_band":"abc<q<7*abc/3",
            "endpoint_not_closed":True}


def main():
    assert __debug__, "Do not run with python -O."
    result = {
        "scope":"cubic cofactor: all m>=8; central allocation m>=7; first condition only; general i=3 open",
        "symbolic":symbolic(), "inequalities":inequalities(),
        "finite_tail":finite_tail(), "genuine_split_example":split_example(),
        "degree7_small_zero_allocation":degree7_small_zero_allocation(),
        "degree7_remaining_endpoint":degree7_remaining_endpoint(),
    }
    target = ROOT/"data/results/verification_i3_cubic_cofactor.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"symbolic":True, "finite_tail":result["finite_tail"]["profiles"],
                      "quotients":2548, "first_hits":0,
                      "independent_numeric_methods":2, "general_i3_open":True}))


if __name__ == "__main__":
    main()
