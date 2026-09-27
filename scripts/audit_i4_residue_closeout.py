"""Exact audits for the all-n i=4 residue classification and class 12.

The unrestricted arguments are in the accompanying research note. The small
normalization sample below diagnoses formulas; it is not a search for a bound
on n. Polynomial sign certificates cover all values of their variables.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb, gcd, prod
from pathlib import Path
import json

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
a, q, E, t = sp.symbols('a q E t', integer=True)


def quadratic_range(A, B, C, hi=F(1, 2)):
    values = [F(C), A*hi*hi+B*hi+C]
    if A:
        vertex = F(-B, 2*A)
        if 0 < vertex < hi:
            values.append(A*vertex*vertex+B*vertex+C)
    return min(values), max(values)


def residue_audit():
    # If v2(n)<=1 and v3(n)<=1, R0=n/d with d in this list.
    # d=2 is the excluded central case. d=3 uses row 2, d=6 row 1.
    assert [abs(x*(x-6)) for x in (1, 2, 3)] == [5, 8, 9]
    assert prod(2-3*x for x in range(3)) == 8
    assert prod(3-2*x for x in range(4)) == 9
    candidates = [r for r in range(36) if r % 4 == 0 or r % 9 == 0]
    groups = [([0, 24], [1, 2, 3], 16),
              ([4, 16], [3, 2, 1], 36),
              ([8, 32], [1, 6, 1], 16)]
    records = []
    for residues, denominators, threshold in groups:
        denominator = prod(d**w for d, w in zip(denominators, (6, 4, 3)))
        constant = F(3*denominator, 4096)
        endpoint = F((threshold-3)**13, threshold**12)
        assert endpoint > constant
        records.append({'residues': residues, 'R1_R2_R3_denominators': denominators,
                        'forced_f_n_less_than': str(constant),
                        'excluded_for_n_at_least': threshold,
                        'endpoint_f_n': str(endpoint)})
    # f'(n)/f(n)=(n+36)/(n(n-3))>0 for every n>3.
    n = sp.symbols('n')
    assert sp.factor(13/(n-3)-12/n) == (n+36)/(n*(n-3))
    boundaries = [{'n':16, 'j':j, 'common_prime':p}
                  for j, p in [(5,7), (6,7), (7,5), (8,5)]]
    for record in boundaries:
        assert comb(record['n'], 4) % record['common_prime'] == 0
        assert comb(record['n'], record['j']) % record['common_prime'] == 0
    remaining = sorted(set(candidates)-{r for rs, _, _ in groups for r in rs})
    assert remaining == [9, 12, 18, 20, 27, 28]
    return {'candidate_residues': candidates, 'exclusions': records,
            'small_boundary': boundaries, 'remaining_residues': remaining}


def equations(k, V):
    D = sp.prod(-2*a+q*(k-u) for u in (0, 1))
    G = sp.prod(-a+q*(k-v) for v in V)
    equation = sp.cancel(E*(2*G-D)+(4*G-D)/q-t*(q*E+2)*(q*E+1))
    r, s = D/(q*E+2), 2*G/(q*E+1)
    assert sp.cancel((s-r-t*q)*(q*E+2)*(q*E+1)/q-equation) == 0
    assert sp.Poly(equation, a, q, E, t).domain == sp.ZZ
    for u in (0, 1):
        assert sp.expand(q*(a*E+k-u)-(-2*a+q*(k-u))-a*(q*E+2)) == 0
    for v in V:
        assert sp.expand(q*(a*E+k-v)-(-a+q*(k-v))-a*(q*E+1)) == 0
    # The two quotients have the same residue 2a^2 modulo odd q.
    assert sp.expand(D).subs(q, 0) == 4*a*a
    assert sp.expand(2*G).subs(q, 0) == 2*a*a
    return equation, D, G


def class12_audit():
    A, B, C = sp.symbols('A B C')
    zero_records, nonzero_records = [], []
    strict, total = 0, 0
    # |t|<18/E: nonzero t forces E in these five values and |t|<=3.
    e_values = [e for e in range(5, 18) if gcd(e, 6) == 1]
    assert e_values == [5, 7, 11, 13, 17]
    assert F(18, 5) < 4
    assert 17*10**80+3 < 10**87
    for k in range(4):
        for V in combinations(range(3), 2):
            equation, D, G = equations(k, V)
            for polynomial in (D, G):
                P = sp.Poly(polynomial.subs(q, 1), a)
                low, high = quadratic_range(*(int(P.nth(i)) for i in (2, 1, 0)))
                assert max(abs(low), abs(high)) <= 6
            P = sp.Poly(equation.subs(t, 0).subs(
                {a:A+1, q:2*(A+1)+B+1, E:C+5}), A, B, C)
            sign = 1 if all(x > 0 for x in P.coeffs()) else -1
            assert all(sign*x > 0 for x in P.coeffs())
            assert sign*P.nth(0, 0, 0) > 0
            zero_records.append({'k':k, 'row2_columns':V, 'sign':sign,
                                 'polynomial_terms':[[list(m), int(c)] for m,c in P.terms()]})
            for e in e_values:
                for tv in [-3, -2, -1, 1, 2, 3]:
                    total += 1
                    P = sp.Poly(equation.subs({E:e, t:tv}), a, q)
                    mons = [a*a, a*q, q*q, a, q, 1]
                    cs = [int(P.coeff_monomial(m)) for m in mons]
                    assert sp.expand(sum(c*m for c,m in zip(cs, mons))-P.as_expr()) == 0
                    aa, bb, cc, dd, ee, ff = cs
                    low, high = quadratic_range(aa, bb, cc)
                    if low > 0 or high < 0:
                        delta = min(abs(low), abs(high))
                        assert delta*10**80 > F(abs(dd),2)+abs(ee)+abs(ff)
                        strict += 1
                    else:
                        assert (k,V,e,tv) == (0,(1,2),5,1)
                        assert cs == [-10,20,-5,10,-7,-2]
                        # qE==1 mod 4 and E=5 imply e_q even, q==1 mod 8.
                        values = [sum(c*m for c,m in zip(cs,(x*x,x,1,x,1,1))) % 8
                                  for x in range(8)]
                        assert 0 not in values
                        nonzero_records.append({'k':k, 'row2_columns':V, 'E':e, 't':tv,
                                                'coefficients':cs, 'modulus':8,
                                                'q_residue':1, 'polynomial_residues':values})
    assert len(zero_records) == 12 and total == 360 and strict == 359
    # Empty q-row: e even, n=3^e+3 and R0=n/12.
    assert max(abs(x*(x-12)) for x in range(1,7)) == 36
    assert 3**4+2 > 36
    for j in (5,6):
        assert comb(12,4) % 11 == 0 and comb(12,j) % 11 == 0
    return {'empty_q_row':{'tail_exponent_at_least':4, 'tail_divisibility_bound':36,
                          'boundary_n':12, 'boundary_j':[5,6], 'common_prime':11},
            't_zero_sign_certificates':zero_records, 'nonzero_cases':total,
            'nonzero_strict_sign_exclusions':strict, 'remaining_conics':nonzero_records}


def occupied_cell_identities():
    cells = [(s,u) for s in range(4) for u in range(s+1)]
    hexagon = {(1,0),(1,1),(2,0),(2,2),(3,1),(3,2)}
    records = []
    for s,u in cells:
        # C0 D0 H = R0^2 R1^2 R2^2 R3 / B21^2.
        left = int(u==0)+int(s-u==0)+int((s,u) in hexagon)
        right = [2,2,2,1][s]-2*int((s,u)==(2,1))
        assert left == right
        # C1 D1 H = R1^2 R2 B21 R3^2 / (B30 B33)^2.
        second = int(u==1)+int(s-u==1)+int((s,u) in hexagon)
        expected = [0,2,1,2][s]+int((s,u)==(2,1))-2*int((s,u) in {(3,0),(3,3)})
        assert second == expected
        records.append({'cell':[s,u], 'first_weight':left, 'second_weight':second})
    assert F(5,4)*F(7,10)**4 > F(3,16)  # classes 12,27, E>=5, n>=10
    assert F(5,9)*F(15,18)**4 > F(3,16)  # classes 18,20, E>=5, n>=18
    return {'cell_weights':records, 'mandatory_for_classes_12_27':'B21>1',
            'mandatory_for_classes_18_20':'B30*B33>1'}


def normalization_diagnostics():
    def part(n):
        for p in (2,3):
            while n % p == 0:
                n //= p
        return n
    counts = {r:0 for r in (0,4,8,12,16,24,32)}
    for n in range(10,10000):
        c = n % 36
        if c not in counts:
            continue
        R = [part(n-s) for s in range(4)]
        ds = {0:[1,2,3],24:[1,2,3],4:[3,2,1],16:[3,2,1],8:[1,6,1],32:[1,6,1]}
        if c in ds:
            assert R[1:] == [(n-s)//d for s,d in zip((1,2,3),ds[c])]
        else:
            Q = (n-3)//R[3]
            assert Q >= 9 and n == Q*R[3]+3
            assert R[1:3] == [n-1,(n-2)//2]
            assert Q*R[3] % 4 == 1
        counts[c] += 1
    return {'diagnostic_only_n_below':10000, 'class_counts':counts}


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    result = {'status':'passed', 'all_n_residue_classification':residue_audit(),
              'class12_five_cell_closeout':class12_audit(),
              'occupied_cell_identities':occupied_cell_identities(),
              'normalization_diagnostics':normalization_diagnostics(),
              'scope':['all n>=10: six possible residues and mandatory cells',
                       'n>=10^87: class12 has at least six occupied cells',
                       'with the previous five-class theorem: every i=4 counterexample '
                       'with n>=10^87 has at least six occupied cells in rows 1,2,3'],
              'not_claimed':'i=4 or any additional index completely solved'}
    path = ROOT/'data/results/verification_i4_residue_closeout.json'
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':result['status'], 'residues':[9,12,18,20,27,28],
                      'class12_zero_signs':12, 'class12_nonzero_cases':360,
                      'class12_strict_signs':359, 'class12_mod8_exclusion':1}))


if __name__ == '__main__':
    main()
