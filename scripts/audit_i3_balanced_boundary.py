"""Replay the finite certificates and exact identities of the balanced boundary.

The all-degree classification, denominator lemmas, and analytic inequalities
are proved in the accompanying note. Finite diagnostics do not replace them.
Use --generate once to regenerate the transparent modular certificates.
"""
import argparse
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path

import sympy as S

ROOT = Path(__file__).resolve().parent.parent
CERT = ROOT / "data/certificates/i3_balanced_boundary_2026-10-01.json"
RESULT = ROOT / "data/results/verification_i3_balanced_boundary.json"
w, lam, y = S.symbols("w lam y")


def homogeneous_pair(q, a, b, modulus):
    """Return b**q*T_q(a/b), b**(q-1)*U_{q-1}(a/b)."""
    t0, t1 = 1, a % modulus
    for _ in range(2, q + 1):
        t0, t1 = t1, (2*a*t1 - b*b*t0) % modulus
    u0, u1 = 1, 2*a % modulus
    if q == 2:
        return t1, u1
    for _ in range(2, q):
        u0, u1 = u1, (2*a*u1 - b*b*u0) % modulus
    return t1, u1


def residue(kind, q, a, b, modulus):
    t, u = homogeneous_pair(q, a, b, modulus)
    if kind == "even":
        return (2*q*t + (a+b)*u) % modulus
    return (-4*q*t + ((1+3*q*q)*a+(1-3*q*q)*b)*u) % modulus


def candidates():
    result = []
    for q in range(2, 21):
        bound = 4*q + 2
        for b in S.divisors(bound):
            for a in range(-b+1, 0):
                if math.gcd(a, b) == 1:
                    result.append(("even", q, a, b))
    for q in range(2, 100):
        c = (3*q-1)*(q-1)
        for m in range(1, 36):
            result.append(("central", q, 2*c+m, 2*c))
    return result


def generate_certificate():
    rows = []
    for kind, q, a, b in candidates():
        prime = 1009
        while residue(kind, q, a, b, prime) == 0:
            prime = int(S.nextprime(prime))
            assert prime < 100000
        rows.append({"kind": kind, "q": q, "a": a, "b": b,
                     "modulus": prime, "nonzero_residue": residue(kind, q, a, b, prime)})
    payload = {"scope": "Finite exceptions after proved all-degree bounds; not a general i=3 solution.",
               "even_q_range": [2, 20], "central_q_range": [2, 99],
               "central_m_range": [1, 35], "rows": rows}
    CERT.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def replay_certificate():
    saved = json.loads(CERT.read_text(encoding="utf-8"))
    expected = candidates()
    assert len(saved["rows"]) == len(expected)
    prime_cache = set()
    coefficient_cache = {}
    maximum_bits = 0
    counts = {"even": 0, "central": 0}
    for row, expected_row in zip(saved["rows"], expected):
        actual = (row["kind"], row["q"], row["a"], row["b"])
        assert actual == expected_row
        p = row["modulus"]
        if p not in prime_cache:
            assert S.isprime(p)
            prime_cache.add(p)
        computed = residue(*actual, p)
        assert 0 < computed < p and computed == row["nonzero_residue"]
        # Independent full-integer homogeneous Horner evaluation. This uses
        # expanded coefficients, not the modular recurrence of the generator.
        kind, q, a, b = actual
        key = (kind, q)
        if key not in coefficient_cache:
            t, e = S.chebyshevt(q, w), S.chebyshevu(q-1, w)
            expr = 2*q*t+(w+1)*e if kind == "even" else -4*q*t+((1+3*q*q)*w+1-3*q*q)*e
            polynomial = S.Poly(expr, w, domain=S.ZZ)
            assert polynomial.degree() == q
            coefficient_cache[key] = [int(c) for c in polynomial.all_coeffs()]
        coefficients = coefficient_cache[key]
        integer_value, b_power = coefficients[0], b
        for coefficient in coefficients[1:]:
            integer_value = a*integer_value+coefficient*b_power
            b_power *= b
        assert integer_value and integer_value % p == computed
        maximum_bits = max(maximum_bits, abs(integer_value).bit_length())
        counts[actual[0]] += 1
    assert counts["central"] == 3430
    return {"counts": counts, "moduli": sorted(prime_cache),
            "independent_full_integer_Horner_evaluations": sum(counts.values()),
            "maximum_integer_bits": maximum_bits,
            "sha256": hashlib.sha256(CERT.read_bytes()).hexdigest()}


def term(kind, z, k):
    if kind == "G":
        return Q(2**k*(6*k*k-5*k-2), math.factorial(2*k+1))*z**k
    if kind == "S":
        return Q(2**k, math.factorial(2*k+1))*z**k
    end = k if kind == "ET" else k+1
    factorial = 2*k if kind == "ET" else 2*k+1
    return Q(2**k*sum(h*h for h in range(1, end)), math.factorial(factorial))*z**k


def series_bounds(kind, z):
    # The note proves that all subsequent ratios are <= 1/2, k >= 13.
    partial = sum((term(kind, z, k) for k in range(13)), Q(0))
    next_term = term(kind, z, 13)
    assert next_term > 0
    return partial, partial+2*next_term


def pack_fraction(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def audit_analytic_constants():
    bounds = {}
    for kind in ("S", "ET", "EU"):
        lo, hi = series_bounds(kind, Q(5, 2))
        assert 0 < lo <= hi < 3
        bounds[kind] = {"lower": pack_fraction(lo), "upper": pack_fraction(hi)}
    _, lower_endpoint_upper = series_bounds("G", Q(5000, 2277))
    upper_endpoint_lower, _ = series_bounds("G", Q(7, 3))
    assert lower_endpoint_upper < -Q(1, 20)
    assert upper_endpoint_lower > Q(1, 5)
    assert Q(48, 10000) < Q(1, 100)
    assert Q(13*100**2, 2*(3*100-1)*(100-1)) == Q(5000, 2277)
    assert Q(14*100**2, 2*(3*100-1)*(100-1)) < Q(5, 2)
    # Explicit ratio bounds used for the infinite positive tails.
    for k in range(3, 101):
        assert 5 < (2*k+2)*(2*k+3)/2
        assert 5 <= (k-1)*(2*k-1)
        assert 5*(k+2) <= k*(k+1)*(2*k+1)
        assert 20 <= (2*k+2)*(2*k+3)/2
        assert 4*(6*k*k-5*k-2)-(6*(k+1)**2-5*(k+1)-2) == 18*k*k-27*k-7 > 0
    bounds["G_at_5000_over_2277_upper"] = pack_fraction(lower_endpoint_upper)
    bounds["G_at_7_over_3_lower"] = pack_fraction(upper_endpoint_lower)
    return bounds


def zero(expression):
    assert S.cancel(expression) == 0


def core(q, kind):
    t, e = S.chebyshevt(q, w), S.chebyshevu(q-1, w)
    if kind == 1:
        f = 2+(w-1)*e*((w+1)*e-q*t)
        u, b, offset = t-q*(w-1)*e, -t+(w+1)*e/q, 0
    elif kind == 2:
        f = 2+(w-1)*e*((w+1)*e+2*q*t)
        u, b, offset = t, (w+1)*e/(2*q), 0
    else:
        r = -4*q*t+((1+3*q*q)*w+1-3*q*q)*e
        f = 2+(w-1)*e*r
        u, b, offset = t-3*q*(w-1)*e, -3*t/2+(w+1)*e/(2*q), S.Rational(1, 2)
    v = S.cancel((f-1)/u)
    assert S.denom(v) == 1
    j = S.expand(1+(f-1)*offset+v*b)
    return S.Poly(f, w, domain=S.QQ), S.Poly(j, w, domain=S.QQ)


def audit_identities():
    models = 0
    sparse = 0
    taylor = 0
    for q in range(2, 13):
        for kind in (1, 2, 3):
            f, j = core(q, kind)
            assert (j*(j-1)).rem(f-1).is_zero
            assert (j*(j-1)*(j-2)).rem(f-2).is_zero
            assert f.degree() == 2*q
            leading = (1-q) if kind == 1 else ((2*q+1) if kind == 2 else (3*q-1)*(q-1))
            assert f.LC() == leading*2**(2*q-2)
            if kind == 2:
                d = 2*q
                fd = (S.chebyshevt(d, w)+d*(w-1)*S.chebyshevu(d-1, w)+3)/2
                jd = (S.chebyshevt(d, w)+(w+1)*S.chebyshevu(d-1, w)/d+1)/2
                zero(f.as_expr()-fd)
                zero(j.as_expr()-jd)
            models += 1
        d = 2*q
        zz = (lam+1/lam)/2
        r_even = 2*q*S.chebyshevt(q, w)+(w+1)*S.chebyshevu(q-1, w)
        sparse_even = (d+1)*lam**(d+1)-(d-1)*lam**d+(d-1)*lam-(d+1)
        zero(sparse_even-2*(lam-1)*lam**q*r_even.subs(w, zz))
        r_central = -4*q*S.chebyshevt(q, w)+((1+3*q*q)*w+1-3*q*q)*S.chebyshevu(q-1, w)
        p = ((q-1)*lam-(q+1))*((3*q-1)*lam-(3*q+1))
        v = ((q+1)*lam-(q-1))*((3*q+1)*lam-(3*q-1))
        zero(p*lam**d-v-2*lam**(q+1)*(lam-1/lam)*r_central.subs(w, zz))
        sparse += 2
        tq = S.Poly(S.chebyshevt(q, 1+y/q**2), y)
        eq = S.Poly(S.chebyshevu(q-1, 1+y/q**2)/q, y)
        for k in range(q+1):
            prod_t = S.prod(1-S.Rational(h*h, q*q) for h in range(1, k))
            prod_e = S.prod(1-S.Rational(h*h, q*q) for h in range(1, k+1))
            assert tq.nth(k) == S.Rational(2**k, math.factorial(2*k))*prod_t
            assert eq.nth(k) == S.Rational(2**k, math.factorial(2*k+1))*prod_e
            taylor += 2
    return {"core_models": models, "sparse_identities": sparse, "Taylor_coefficients": taylor}


def mod_two(coefficient):
    coefficient = S.Rational(coefficient)
    assert coefficient.q % 2
    return int(coefficient.p) % 2


def audit_integer_edges():
    count = 0
    for d in range(2, 50, 2):
        f = S.Poly((S.chebyshevt(d, w)+d*(w-1)*S.chebyshevu(d-1, w)+3)/2, w)
        assert all(c.q == 1 for c in f.all_coeffs())
        shifted = S.Poly(f.as_expr().subs(w, 1+y), y)
        assert shifted.nth(1) == d*d
        assert shifted.LC() == (d+1)*2**(d-2)
        e = S.Poly(S.chebyshevu(d-1, w)/d, w)
        assert S.Poly(sum(mod_two(e.nth(k))*w**k for k in range(e.degree()+1)), w).as_expr() == w
        odd = S.Poly(f.as_expr().subs(w, 1+2*y)-2, y)
        assert all(c.q == 1 and int(c) % 4 == 0 for c in odd.all_coeffs())
        count += 1
    f2, j2 = core(2, 3)
    assert f2.as_expr() == 20*w**4-64*w**3+60*w**2-16*w+2
    assert j2.as_expr() == 15*w**4-43*w**3+S.Rational(63, 2)*w**2-S.Rational(5, 2)*w
    assert all(int(c) % 4 == 0 for c in S.Poly(f2.as_expr()-2, w).all_coeffs())
    f3, j3 = core(3, 3)
    mapped_f = S.Poly(f3.as_expr().subs(w, -(y+1)/2), y)
    mapped_j = S.Poly(j3.as_expr().subs(w, -(y+1)/2), y)
    assert mapped_f.as_expr() == 4*y**6+45*y**5+189*y**4+356*y**3+270*y**2+36*y+2
    assert S.Poly(3*mapped_j.as_expr(), y).LC() == 8
    sextic_f = mapped_f.as_expr().subs(y, 3*y).expand()
    sextic_j = (mapped_f.as_expr()-mapped_j.as_expr()).subs(y, 3*y).expand()
    assert sextic_f == 2916*y**6+10935*y**5+15309*y**4+9612*y**3+2430*y**2+108*y+2
    assert sextic_j == 972*y**6+3969*y**5+6102*y**4+4275*y**3+1263*y**2+94*y+2
    pp = 36*y**3+75*y**2+40*y+2
    kk = 324*y**4+1107*y**3+1296*y**2+561*y+47
    zero(sextic_f-2-27*y*(y+1)*(3*y+2)*pp)
    zero(sextic_j-(27*y**3+54*y**2+27*y+1)*pp)
    zero(sextic_j-1-(y+1)*(9*y**2+12*y+1)*(108*y**3+189*y**2+81*y+1))
    zero(sextic_j-2-y*(3*y+2)*kk)
    return {"even_core_integer_diagnostics": count, "central_exception_maps": [2, 3],
            "sextic_factorizations": 4}


def audit_global_bound():
    uu, hh, kk, cc = S.symbols("uu hh kk cc")
    vv = kk+cc*hh-S.Rational(3, 4)*cc*uu
    jj = 1+vv*(uu/2+hh)
    zero(jj-hh*kk-uu*(kk-S.Rational(3, 4)*cc*hh+vv/2)-(1+cc*hh**2-uu*kk))
    count = 0
    for u in range(1, 161):
        for v in range(u, 2*u):
            target = (8*u-v+11)//12
            for e in range(max(1, v-u), (u+v)//3+1):
                r = (v+e-1)//e
                assert r >= 2
                bound = u-e+(e*(r+1)-u+2*r-1)//(2*r)
                assert bound >= target
                # For the exceptional central group, ceil(u-e/2).
                assert (2*u-e+1)//2 >= target
                if u == v:
                    balanced_bound = (2*u-e+1)//2 if 3*e == 2*u else bound
                    assert balanced_bound >= (7*u)//12+1
                count += 1
    for q in range(3, 1001):
        assert 12*(q-1) >= 8*q-(q+1)
    return {"rounding_diagnostics": count, "empty_central_group_identity": 1,
            "delta_zero_unbalanced_diagnostics": 998,
            "paper_bound": "h >= ceil((8*u-v)/12), u <= v < 2*u",
            "balanced_strict_bound": "h > 7*u/12"}


def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    if args.generate:
        generate_certificate()
    result = {"scope": "All balanced minimum boundaries of lifted polynomials; general numerical i=3 remains open.",
              "finite_exception_certificates": replay_certificate(),
              "analytic_rational_bounds": audit_analytic_constants(),
              "identities": audit_identities(), "integer_edges": audit_integer_edges(),
              "all_partition_bound": audit_global_bound(),
              "does_not_prove": ["all higher difference degrees", "all odd five-power cores", "general numerical lifting"]}
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"certificate_counts": result["finite_exception_certificates"]["counts"],
                      "identities": result["identities"], "general_i3": "open"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
