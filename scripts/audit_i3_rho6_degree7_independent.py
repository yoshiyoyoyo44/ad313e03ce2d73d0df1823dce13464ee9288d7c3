"""Exact finite audit of the standard-digit complete split rho=6,d=4,m=7.

The accompanying note proves the exhaustive parameterization.  This script
does not assert that a general numerical i=3 candidate has this split.
"""
from fractions import Fraction
from itertools import product
from math import isqrt, comb
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent

def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def mul(p, q):
    out = [0] * (len(p)+len(q)-1)
    for i, x in enumerate(p):
        for k, y in enumerate(q):
            out[i+k] += x*y
    return trim(out)

def divexact(p, b):
    p = trim(p)
    if len(p) < len(b):
        return None
    q = [0]*(len(p)-len(b)+1)
    for k in range(len(q)-1, -1, -1):
        v, rem = divmod(p[k+len(b)-1], b[-1])
        if rem:
            return None
        q[k] = v
        for i, c in enumerate(b):
            p[k+i] -= v*c
    return trim(q) if not any(p) else None

def value(p, x):
    out = 0
    for c in reversed(p):
        out = out*x+c
    return out

def fpoly(a, d):
    return [1]+[a*d[k-1]-d[k] for k in range(1, 7)]+[a*d[6]]

def eligible(a, d, j):
    if len(d) != 7 or d[0] != 1 or any(c <= 0 for c in d):
        return None
    f = fpoly(a, d)
    if f[1] < 1 or any(c < 0 for c in f) or any(j[k] > f[k] for k in range(5)):
        return None
    return f

def high_candidates():
    candidates = {}
    raw = {"pure": 0, "mixed": 0}
    for a in range(2, 14):
        for t in range(1, 13//a+1):
            for lead_e in range(1, 13//(a*t)+1):
                for h in (1, 2):
                    eps = 2-h
                    for ell in range(1, h*a):
                        for r in range(1, ell//h+1):
                            # E=B_0 or B_1, degree three. Its quotient has
                            # leading coefficient ell*t/lead_e.
                            if ell*t % lead_e == 0:
                                c = ell*t//lead_e
                                for s in range(1, ell*r//h+1):
                                    j = [eps, ell-h*r, ell*r-h*s,
                                         ell*s-h*t, ell*t]
                                    if min(j) < 0:
                                        continue
                                    for group in (0, 1):
                                        p = list(j)
                                        p[0] -= group
                                        e = divexact(p, [eps-group, c])
                                        if e is None or len(e) != 4 or e[0] != 1 or e[-1] != lead_e:
                                            continue
                                        d = mul(e, [1, r, s, t])
                                        f = eligible(a, d, j)
                                        if f is not None:
                                            raw["pure"] += 1
                                            candidates[(a, tuple(d), tuple(j))] = (f, "pure")
                            # E has a degree-one group 1+uX and a degree-two
                            # group 1+vX+wX^2.  The leading product is u*w.
                            for u in range(1, lead_e+1):
                                if lead_e % u:
                                    continue
                                w = lead_e//u
                                for line_group in (0, 1):
                                    numerator = (2-line_group)*u**4
                                    denominator = ell+h*u
                                    if numerator % denominator:
                                        continue
                                    n = numerator//denominator
                                    snum = n-u**3+r*u**2+t
                                    if snum % u:
                                        continue
                                    s = snum//u
                                    if not 1 <= s <= ell*r//h:
                                        continue
                                    j = [eps, ell-h*r, ell*r-h*s,
                                         ell*s-h*t, ell*t]
                                    if min(j) < 0:
                                        continue
                                    p = list(j)
                                    p[0] -= line_group
                                    assert divexact(p, [1, u]) is not None
                                    for v in range(1-r-u, a-r-u):
                                        other_group = 1-line_group
                                        other = list(j)
                                        other[0] -= other_group
                                        quadratic = [1, v, w]
                                        if divexact(other, quadratic) is None:
                                            continue
                                        e = mul([1, u], quadratic)
                                        d = mul(e, [1, r, s, t])
                                        f = eligible(a, d, j)
                                        if f is not None:
                                            raw["mixed"] += 1
                                            candidates[(a, tuple(d), tuple(j))] = (f, "mixed")
    return candidates, raw

def high_check(candidates):
    intervals = 0
    evaluations = 0
    survivors = []
    nonempty = []
    excluded = []
    for (a, dt, jt), (f, kind) in candidates.items():
        d, j = list(dt), list(jt)
        qlo = max(3, max(f)+1)
        ss = sum(v*v for v in j[1:])
        c = Fraction(3*(2*ss+1), 2*a*d[-1])
        qsquared = c*Fraction(qlo+1, qlo)**4
        qhi = isqrt(qsquared.numerator//qsquared.denominator)
        if qhi < qlo:
            excluded.append({"a": a, "D": d, "J": j,
                             "F": f, "q_min": qlo, "q_max": qhi,
                             "square_upper_bound": str(qsquared),
                             "strict_positive_gap": str(qlo*qlo-qsquared),
                             "kind": kind})
            continue
        intervals += 1
        nonempty.append({"a": a, "D": d, "J": j,
                         "q_min": qlo, "q_max": qhi, "kind": kind})
        for q in range(qlo, qhi+1):
            evaluations += 1
            n, jj = value(f, q), value(j, q)
            if (3*jj*(jj-1)) % (n-1) == 0:
                survivors.append({"a": a, "D": d, "J": j, "q": q,
                                  "n": n, "j": jj})
    return {"nonempty_intervals": intervals, "base_evaluations": evaluations,
            "intervals": nonempty, "excluded_candidates": excluded,
            "first_condition_survivors": survivors}

def high_candidates_secondary():
    """Direct coefficient loop, avoiding the negative-root formula.

    Enumerate s rather than deriving it. Divide both J-level polynomials
    directly, with separate pure and mixed constructions.
    """
    candidates = set()
    for a in range(2, 14):
        for t in range(1, 13//a+1):
            for lead_e in range(1, 13//(a*t)+1):
                for h in (1, 2):
                    eps = 2-h
                    for ell in range(1, h*a):
                        for r in range(1, ell//h+1):
                            for s in range(1, ell*r//h+1):
                                j = [eps, ell-h*r, ell*r-h*s,
                                     ell*s-h*t, ell*t]
                                if min(j) < 0:
                                    continue
                                b2 = [1, r, s, t]
                                for group in (0, 1):
                                    p = list(j)
                                    p[0] -= group
                                    if ell*t % lead_e == 0:
                                        e = divexact(p, [eps-group, ell*t//lead_e])
                                        if e is not None and len(e) == 4 and e[0] == 1:
                                            d = mul(e, b2)
                                            if eligible(a, d, j) is not None:
                                                candidates.add((a, tuple(d), tuple(j)))
                                    for u in range(1, lead_e+1):
                                        if lead_e % u or divexact(p, [1, u]) is None:
                                            continue
                                        w = lead_e//u
                                        other = list(j)
                                        other[0] -= 1-group
                                        for v in range(1-r-u, a-r-u):
                                            quadratic = [1, v, w]
                                            if divexact(other, quadratic) is None:
                                                continue
                                            d = mul(mul([1, u], quadratic), b2)
                                            if eligible(a, d, j) is not None:
                                                candidates.add((a, tuple(d), tuple(j)))
    return candidates

def small_check():
    rows = []
    survivors = []
    for q in range(3, 7):
        f_count = j_count = num_survivors = complete = 0
        reverse_set = set()
        for a in range(2, q):
            for lead in range(1, (q-1)//a+1):
                def recurse(k, ds):
                    if k == 0:
                        if ds[0] == 1:
                            yield list(ds)
                        return
                    for digit in range(q):
                        if k == 1 and digit == 0:
                            continue
                        numerator = ds[k]+digit
                        if numerator % a:
                            continue
                        prev = numerator//a
                        if prev <= 0:
                            continue
                        ds[k-1] = prev
                        yield from recurse(k-1, ds)
                for d in recurse(6, [0]*6+[lead]):
                    reverse_set.add((a, tuple(d)))
                    f = fpoly(a, d)
                    assert f[1] >= 1 and all(0 <= c < q for c in f)
                    f_count += 1
                    n = value(f, q)
                    for tail in product(*(range(f[k]+1) for k in range(1, 5))):
                        if tail[-1] == 0:
                            continue
                        for eps in (0, 1):
                            j = [eps]+list(tail)
                            j_count += 1
                            jj = value(j, q)
                            if (3*jj*(jj-1)) % (n-1):
                                continue
                            num_survivors += 1
                            pp = list(j)
                            p1, p2 = list(j), list(j)
                            p1[0] -= 1
                            p2[0] -= 2
                            if divexact(mul(mul(pp, p1), p2), d) is not None:
                                complete += 1
                                survivors.append({"q": q, "a": a, "D": d,
                                                  "J": j, "n": n, "j": jj})
        forward_set = set()
        for a in range(2, q):
            for digits in product(range(1, q), *(range(q) for _ in range(5))):
                ds = [1]
                for digit in digits:
                    ds.append(a*ds[-1]-digit)
                    if ds[-1] <= 0:
                        break
                if len(ds) == 7 and 0 < a*ds[-1] < q:
                    forward_set.add((a, tuple(ds)))
        assert forward_set == reverse_set
        rows.append({"q": q, "F_polynomials": f_count,
                     "J_polynomials": j_count,
                     "first_condition_survivors": num_survivors,
                     "complete_split_survivors": complete,
                     "forward_reverse_F_enumeration_agrees": True})
    return rows, survivors

def main():
    if not __debug__:
        raise SystemExit("Assertions must be enabled")
    # r_2>=2: 4*q^6 - 3*(8*(q-1)^2+1)*(q+1)^3 > 0 for q>=7.
    p = mul([9, -16, 8], [1, 3, 3, 1])
    p = [-3*c for c in p]+[4]
    shifted = [sum(p[k]*comb(k, i)*7**(k-i) for k in range(i, 7)) for i in range(7)]
    assert shifted == [26692, 89448, 55668, 15053, 2076, 144, 4]
    assert all(c > 0 for c in shifted)
    small_rows, small_survivors = small_check()
    candidates, raw = high_candidates()
    secondary = high_candidates_secondary()
    assert secondary == set(candidates)
    high = high_check(candidates)
    out = {"status": "passed" if not small_survivors and not high["first_condition_survivors"] else "survivors",
           "scope": "standard-digit complete split rho=6,d=4,m=7,F1>=1",
           "hypotheses": "integer polynomials; a is a positive integer; F0=1; F1>=1; deg(F)=7; deg(J)=4; 0<=Jk<=Fk<q; F-2=(aX-1)D; D=B0*B1*B2; Bs(0)=1; Bs divides J-s with all multiplicities; n=F(q); j=J(q); n-1 divides 3*j*(j-1)",
           "general_i3_solved": False,
           "r2_at_least_2_positive_shift_at_7": shifted,
           "small_base_rows": small_rows,
           "small_base_complete_survivors": small_survivors,
           "r2_equals_1_raw_candidates": raw,
           "r2_equals_1_unique_candidates": len(candidates),
           "r2_equals_1_secondary_enumeration_agrees": True,
           "r2_equals_1": high}
    target = ROOT/"data/results/verification_i3_rho6_degree7_independent.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    assert out["status"] == "passed", "The complete finite domain has surviving candidates"
    print(json.dumps({k: v for k, v in out.items() if k != "r2_equals_1"}, ensure_ascii=False))
    print(json.dumps({k: v for k, v in high.items() if k not in ("intervals", "excluded_candidates")}, ensure_ascii=False))

if __name__ == "__main__":
    main()
