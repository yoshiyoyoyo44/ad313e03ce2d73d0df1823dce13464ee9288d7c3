"""Exact finite audits for the five-cell theorem (see the accompanying proof).

SymPy is used only for integer-polynomial identities and expansions. All
congruence sieves, quadratic ranges, and Pell seed/orbit checks are exact.
The infinite descent and growth arguments are proved in the research note;
finite sample checks here are not a substitute for those arguments.
"""
from fractions import Fraction as F
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path
import json

import sympy as sp

from audit_handoff_integration_2026_09_26 import support_covers

ROOT = Path(__file__).resolve().parents[1]
MODULI = [8, 16, 32, 64, 128, 256, 512, 1024, 3, 9, 27, 81, 243,
          5, 25, 125, 7, 49, 11, 121, 13, 169, 17, 19, 23, 29, 31,
          37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
CLASSES = [9, 18, 20, 27, 28]
a, L, E, t = sp.symbols('a L E t', integer=True)


def normalization_checks():
    def vp(n,p):
        e=0
        while n%p==0:
            n//=p
            e+=1
        return e
    counts={c:0 for c in CLASSES}
    exponent_parities={0:0,1:0}
    for n in range(10,10000):
        c=n%36
        if c not in CLASSES:
            continue
        R=[(n-s)//(2**vp(n-s,2)*3**vp(n-s,3)) for s in range(4)]
        if c==9:
            l=2**(vp(n-1,2)-1);e=R[1]
            assert l>=2 and n==2*l*e+1 and l*e%9==4
            assert R[2:]==[2*l*e-1,(l*e-1)//3]
        elif c in (18,20):
            l=2**vp(n-2,2) if c==18 else 2*3**vp(n-2,3)
            e=R[2];d=3 if c==18 else 1
            assert n==l*e+2 and R[1]==l*e+1 and R[3]==(l*e-1)//d
            if c==18:
                assert l>=4 and l*e%9==7
            else:
                assert l>=18
        elif c==27:
            f=vp(n-3,2)-1;l=3*2**f;e=R[3]
            assert f>=1 and n==2*l*e+3 and e*2**f%3==1
            assert R[1:3]==[l*e+1,2*l*e+1]
        else:
            exponent=vp(n-1,3);l=3**exponent;e=R[1]
            assert exponent>=2 and n==l*e+1
            assert R[2:]==[(l*e-1)//2,l*e-2]
            assert e%4==(1 if exponent%2 else 3)
            exponent_parities[exponent%2]+=1
        assert gcd(e,6)==1
        counts[c]+=1
    assert all(exponent_parities.values())
    # These are diagnostics of the normalization, not counterexample searches.
    return {'n_below':10000,'class_counts':counts,'class28_both_exponent_parities':exponent_parities}


def supports(c):
    if c in (9, 28):
        for k in range(2):
            for u in combinations(range(3), 2):
                for v in combinations(range(4), 2):
                    yield k, u, v
    elif c in (18, 20):
        for k in range(3):
            for v in combinations(range(4), 2):
                yield k, (0, 1), v
    else:
        for k in range(4):
            for v in combinations(range(3), 2):
                yield k, (0, 1), v


def equations(c, k, u, v):
    """Return the quotient numerator, and its t=0 normalization.

    Construct the factors from M(j-col) modulo the actual heavy-row value.
    In particular BOTH factors for class 27 have -a, not +a.
    """
    j = a*E + k
    if c == 9:
        D = sp.prod(a + 2*L*(k-x) for x in u)
        G = sp.prod(a + L*(k-x) for x in v)
        M1, M2, R1, R2 = 2*L, L, 2*L*E-1, (L*E-1)/3
        factors1 = [a+2*L*(k-x) for x in u]
        factors2 = [a+L*(k-x) for x in v]
        r, s, multiple = D/R1, G/R2, 3
        raw = (s-3*r-t*L)*(L*E-1)*(2*L*E-1)/L
        zero = E*(2*G-D)+(D-G)/L
        formula = 3*zero-t*(L*E-1)*(2*L*E-1)
    elif c == 28:
        D = sp.prod(a+L*(k-x) for x in u)
        G = sp.prod(2*a+L*(k-x) for x in v)
        M1, M2, R1, R2 = L, L, (L*E-1)/2, L*E-2
        factors1 = [a+L*(k-x) for x in u]
        factors2 = [2*a+L*(k-x) for x in v]
        r, s, multiple = D/R1, G/R2, 1
        raw = (s-r-t*L)*(L*E-1)*(L*E-2)/L
        zero = E*(G-2*D)+(4*D-G)/L
        formula = zero-t*(L*E-1)*(L*E-2)
    elif c in (18, 20):
        d = 3 if c == 18 else 1
        D = sp.prod(-a+L*(k-x) for x in u)
        G = sp.prod(a+L*(k-x) for x in v)
        M1, M2, R1, R2 = L, L, L*E+1, (L*E-1)/d
        factors1 = [-a+L*(k-x) for x in u]
        factors2 = [a+L*(k-x) for x in v]
        r, s, multiple = D/R1, G/R2, -d
        raw = (s+d*r-t*L)*(L*E+1)*(L*E-1)/L
        zero = E*(G+D)+(G-D)/L
        formula = d*zero-t*((L*E)**2-1)
    else:
        D = sp.prod(-a+L*(k-x) for x in u)
        G = sp.prod(-a+2*L*(k-x) for x in v)
        M1, M2, R1, R2 = L, 2*L, L*E+1, 2*L*E+1
        factors1 = [-a+L*(k-x) for x in u]
        factors2 = [-a+2*L*(k-x) for x in v]
        r, s, multiple = D/R1, G/R2, 1
        raw = (s-r-t*L)*(L*E+1)*(2*L*E+1)/L
        zero = E*(G-2*D)+(G-D)/L
        formula = zero-t*(L*E+1)*(2*L*E+1)
    # The displayed reduced factors are congruent to M(j-col) modulo R.
    for M, R, cols, factors in ((M1, R1, u, factors1), (M2, R2, v, factors2)):
        for col, factor in zip(cols, factors):
            quotient = sp.cancel((M*(j-col)-factor)/R)
            assert sp.Poly(quotient, a, L, E).domain == sp.ZZ
    assert sp.cancel(raw-formula) == 0
    # Integer quotients r,s have the stated residues modulo L.
    assert sp.cancel((s-multiple*r).subs(L, 0)) == 0
    return sp.cancel(formula), sp.cancel(zero), sp.expand(D), sp.expand(G)


def quadratic_range(A, B, C, hi):
    values = [F(C), A*hi*hi+B*hi+C]
    if A and 0 <= F(-B, 2*A) <= hi:
        x = F(-B, 2*A)
        values.append(A*x*x+B*x+C)
    return min(values), max(values)


def parameter_orbit(c, e, modulus):
    if c in (9, 18):
        target = 4 if c == 9 else 7
        e0 = next(x for x in range(6) if e*pow(2, x, 9) % 9 == target)
        prime, scale, start, step = 2, 1, e0+24, 6
    elif c == 20:
        prime, scale, start, step = 3, 2, 20, 1
    elif c == 27:
        prime, scale, start, step = 2, 3, 20+int(e % 3 == 2), 2
    else:
        prime, scale, start, step = 3, 1, 20+int(e % 4 == 1), 2
    # Every actual exponent exceeds start since L >= 10^80. The p-primary
    # part of modulus has vanished by start; the remaining orbit is cyclic.
    assert scale*prime**(start+step) < 10**80
    rem, power = modulus, 0
    while rem % prime == 0:
        rem //= prime
        power += 1
    assert start >= power
    x = scale*pow(prime, start, modulus) % modulus
    seen, orbit = set(), []
    while x not in seen:
        seen.add(x)
        orbit.append(x)
        x = x*pow(prime, step, modulus) % modulus
    assert x == orbit[0]
    return orbit


def bound_checks():
    hi = {9: F(1), 18: F(1, 2), 20: F(1, 2), 27: F(1), 28: F(1, 2)}
    bounds = {9: (8, 6), 18: (2, 6), 20: (2, 6), 27: (6, 24), 28: (2, 6)}
    for c in CLASSES:
        for k, u, v in supports(c):
            _, _, D, G = equations(c, k, u, v)
            for P, bound in zip((D, G), bounds[c]):
                P = sp.Poly(P.subs(L, 1), a)
                cs = [int(P.nth(x)) for x in (2, 1, 0)]
                low, high = quadratic_range(*cs, hi[c])
                assert max(abs(low), abs(high)) <= bound
    # Decreasing in E; L/(LE-1) decreases with L, and L/(LE+1)<1/E.
    assert F(36, 2*31-1)+F(48, 4*31-1) < 1
    assert F(36, 9)+F(48, 19) < 7
    assert F(18*4, 4*25-1)+F(6, 25) < 1
    assert F(18*4, 19)+F(6, 5) < 5
    assert F(6*18, 18*9-1)+F(2, 9) < 1
    assert F(6*18, 18*5-1)+F(2, 5) < 2
    assert F(18, 18) == 1 and F(18, 5) < 4  # strict bound for class 27
    assert F(6*9, 9*11-2)+F(4*9, 9*11-1) < 1
    assert F(6*9, 9*5-2)+F(4*9, 9*5-1) < 3
    assert 60*10**80+3 < 10**87
    return {'D_G_bounds': bounds, 'E_max': {9:29,18:23,20:7,27:17,28:7},
            'abs_t_max': {9:6,18:4,20:1,27:3,28:2}, 'L_min_nonzero_t': str(10**80)}


def zero_t_checks():
    A, B, C = sp.symbols('A B C')
    out = {}
    for c in CLASSES:
        records = []
        for k, u, v in supports(c):
            _, zero, _, _ = equations(c, k, u, v)
            av = A+1
            lv = (av+B+k if c == 9 else 2*av+B+1 if c == 28
                  else 2*av+B+int(k == 2) if c in (18, 20)
                  else av+B+int(k >= 2))
            P = sp.Poly(zero.subs({a: av, L: lv, E: C+5}), A, B, C)
            cs = P.coeffs()
            sign = 1 if all(x > 0 for x in cs) else -1 if all(x < 0 for x in cs) else 0
            if sign:
                assert sign*P.nth(0, 0, 0) > 0
            else:
                assert c in (9, 28) and k == 1
                assert (u, v) in (((0, 1), (2, 3)), ((1, 2), (0, 2)))
            records.append({'k':k, 'first_heavy_columns':u, 'second_heavy_columns':v,
                            'sign':sign, 'expanded_coefficients':
                            [[list(mon), int(co)] for mon, co in P.terms()]})
        out[c] = records
    return out


def nonzero_t_checks(bounds):
    covers = support_covers()['residue_classes']
    out = {}
    terminal = {
        (9,0,(0,2),(2,3),7,2): 'norm_minus32_D57',
        (9,0,(1,2),(0,1),5,-2): 'norm_one_D3_mod5',
        (18,0,(0,1),(1,3),7,1): 'norm_minus128_D33',
    }
    seen_terminal = set()
    for c in CLASSES:
        sign_count, records, total = 0, [], 0
        for k, u, v in supports(c):
            if c in (9, 28):
                cells = sorted([(1,k)]+[(2,x) for x in u]+[(3,x) for x in v])
                match = next(x for x in covers[c]['supports'] if x['cells'] == cells)
                if match['excluded_by'] is not None:
                    continue
            equation, _, _, _ = equations(c, k, u, v)
            for e in range(5, bounds['E_max'][c]+1):
                if gcd(e, 6) != 1:
                    continue
                for tv in range(-bounds['abs_t_max'][c], bounds['abs_t_max'][c]+1):
                    if not tv:
                        continue
                    total += 1
                    P = sp.Poly(equation.subs({E:e, t:tv}), a, L)
                    cs = [int(P.coeff_monomial(mon)) for mon in (a*a, a*L, L*L, a, L, 1)]
                    assert sp.expand(sum(x*mon for x,mon in zip(cs,(a*a,a*L,L*L,a,L,1)))-P.as_expr()) == 0
                    A,B,C,D,G,H = cs
                    hi = F(1) if c in (9, 27) else F(1,2)
                    low, high = quadratic_range(A, B, C, hi)
                    if low > 0 or high < 0:
                        delta = min(abs(low), abs(high))
                        # For all L >= L0, delta*L^2 dominates lower terms.
                        assert delta*10**80 > abs(D)*hi+abs(G)+abs(H)
                        sign_count += 1
                        continue
                    record = {'k':k, 'first_heavy_columns':u, 'second_heavy_columns':v,
                              'E':e, 't':tv, 'coefficients':cs}
                    for modulus in MODULI:
                        orbit = parameter_orbit(c, e, modulus)
                        if not any((A*x*x+B*x*l+C*l*l+D*x+G*l+H) % modulus == 0
                                   for l in orbit for x in range(modulus)):
                            record.update({'excluded_modulus':modulus, 'L_orbit':orbit})
                            break
                    else:
                        key = (c,k,u,v,e,tv)
                        assert key in terminal, key
                        seen_terminal.add(key)
                        record['pell_terminal'] = terminal[key]
                    records.append(record)
        out[c] = {'total_nonzero_cases':total, 'strict_sign_exclusions':sign_count,
                  'conics':records, 'modular_exclusions':sum('excluded_modulus' in x for x in records),
                  'pell_terminals':sum('pell_terminal' in x for x in records)}
    assert seen_terminal == set(terminal)
    assert [len(out[c]['conics']) for c in CLASSES] == [43,10,1,1,2]
    return out


def pell_orbit(seed, unit, D, modulus):
    x, y = (z % modulus for z in seed)
    start = (x,y)
    orbit = []
    while (x,y) not in orbit:
        orbit.append((x,y))
        x,y = (unit[0]*x+D*unit[1]*y) % modulus, (unit[1]*x+unit[0]*y) % modulus
    assert (x,y) == start
    return orbit


def pell_checks():
    x,z = sp.symbols('x z')
    # Discriminants of the three terminal conics.
    assert sp.expand((60*L-15)**2-60*(-20*L*L-6*L+2)-3*((40*L-6)**2-1)) == 0
    d57 = (-126*L+3)**2-84*(56*L*L+24*L-2)
    assert sp.expand((266*L-33)**2-sp.Rational(19,3)*d57+32) == 0
    d33 = (-63*L-15)**2-168*(14*L*L+9*L+1)
    assert sp.expand((77*L+9)**2-sp.Rational(11,3)*d33+128) == 0
    assert {p[0] for p in pell_orbit((1,0),(2,1),3,5)} == {1,2}
    assert {p[0] for p in pell_orbit((3,1),(2,1),3,24)} == {3,9}
    result = []
    for D,norm,cut,unit,mod,residue in [(57,-32,114,(151,20),152,119),
                                       (33,-128,46,(23,4),4928,9)]:
        # Inverse-unit descent for y>=cut: x'>0, 0<y'<y.
        U,V = unit
        assert U*U-D*V*V == 1
        assert D*cut*cut+U*U*norm > 0
        assert (D*V*V-(U-1)**2)*cut*cut+V*V*norm > 0
        seeds=[]
        for y in range(1,cut):
            sq = D*y*y+norm
            if sq>=0 and isqrt(sq)**2==sq:
                seeds.append((isqrt(sq),y))
        if D==57:
            assert seeds==[(5,1),(14,2),(166,22),(385,51)]
            # X=266L-33 gives X=5 mod 19 and X=7 mod 8, i.e.119 mod152.
            assert residue % 19 == 5 and residue % 8 == 7
        else:
            assert seeds==[(2,2),(13,3),(20,4),(68,12),(97,17),(218,38)]
            # L=2^e, e=0 mod6, gives X=77L+9=9 mod(64*77).
        orbits=[]
        for seed in seeds:
            orbit=pell_orbit(seed,unit,D,mod)
            assert all(xx != residue for xx,yy in orbit)
            orbits.append({'seed':seed,'period':len(orbit),'orbit':orbit})
        result.append({'D':D,'norm':norm,'descent_y_cutoff':cut,'unit':unit,
                       'modulus':mod,'forbidden_x_residue':residue,'orbits':orbits})
    # Symbolic discriminants for the four t=0 exceptions.
    assert sp.expand((5-8*z)**2-4*(4*z*z-2*z)-((12*z-9)**2-6)/3) == 0
    assert sp.expand((2*z-2)**2-4*(-2*z*z+z)-4*(3*z*z-3*z+1)) == 0
    assert sp.expand((5-4*z)**2-4*(z*z-z)-(3*(2*z-3)**2-2)) == 0
    assert sp.expand((2*z-4)**2-8*(-z*z+z)-4*(3*(z-1)**2+1)) == 0
    # Both exponential growth contradictions start at q=27 and improve.
    # In an occupied five-cell branch E<=18q, n=qE+1<=18q^2+1.
    assert 10**87>18*27**2+1
    assert 2**25 > 36*27**2 and 2**27 > 18*27**2
    assert 2*27**2 > 28**2
    return result


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    normalization=normalization_checks()
    bounds=bound_checks()
    zero=zero_t_checks()
    nonzero=nonzero_t_checks(bounds)
    pell=pell_checks()
    report={'status':'passed', 'scope':'five occupied cells in rows 1,2,3; n>=10^87; residues 9,18,20,27,28 mod36',
            'not_claimed':['all n for i=4','exclusion of all six-or-more-cell supports','complete solution of any new index'],
            'normalization_diagnostics':normalization,
            'bounds':bounds,'zero_t':zero,'nonzero_t':nonzero,'pell_descent_certificates':pell}
    path=ROOT/'data/results/verification_i4_five_cell_closeout.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'passed','raw_supports':{c:len(zero[c]) for c in CLASSES},
                      'zero_t_sign_exclusions':{c:sum(bool(r['sign']) for r in zero[c]) for c in CLASSES},
                      'nonzero_t':{c:{k:v for k,v in nonzero[c].items() if k!='conics'} for c in CLASSES},
                      'output':path.relative_to(ROOT).as_posix()},indent=2))


if __name__=='__main__':
    main()
