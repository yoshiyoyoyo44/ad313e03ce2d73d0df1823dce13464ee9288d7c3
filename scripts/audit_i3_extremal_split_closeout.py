"""Check the all-degree extremal split proof and its cubic numerical obstruction."""
import json
from itertools import permutations
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent.parent


def valuation(n, p):
    assert n != 0
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def main():
    U, H, lam, z, k, x = s.symbols('U H lam z k x')
    P = H**3+H**2*U-s.Rational(2, 3)*H*U**2-s.Rational(8, 27)*U**3
    assert s.expand(H*P+lam*(H+U)-(H+U)*(H**3+lam)
                    +s.Rational(2, 3)*H**2*U**2+s.Rational(8, 27)*H*U**3) == 0
    Fz = 2+s.Rational(9, 2)*z+s.Rational(9, 2)*z**2+z**3
    Jz = 2+s.Rational(23, 6)*z+s.Rational(13, 6)*z**2+s.Rational(1, 3)*z**3
    f = 216*k**3+162*k**2+27*k+2
    j = 72*k**3+78*k**2+23*k+2
    assert s.expand(Fz.subs(z, 6*k)-f) == 0
    assert s.expand(Jz.subs(z, 6*k)-j) == 0
    assert s.expand(f-1-(6*k+1)*(36*k**2+21*k+1)) == 0
    assert s.expand(f-2-27*k*(2*k+1)*(4*k+1)) == 0
    assert s.expand(j-(3*k+2)*(4*k+1)*(6*k+1)) == 0
    assert s.expand(j-1-(2*k+1)*(36*k**2+21*k+1)) == 0
    assert s.expand(j-2-k*(72*k**2+78*k+23)) == 0
    assert s.rem(j*(j-1), f-1, k) == 0
    assert s.rem(j*(j-1)*(j-2), f-2, k) == 0
    compositions = []
    for d in range(1, 9):
        K = x**d+x
        F, J = s.Poly(f.subs(k, K), x), s.Poly(j.subs(k, K), x)
        a, b = s.Poly(6*K+1, x), s.Poly(36*K**2+21*K+1, x)
        assert F.degree() == 3*d and a.degree() == d and b.degree() == 2*d
        assert s.rem(J, a) == 0 and s.rem(J-1, b) == 0
        assert all(F.nth(i) >= J.nth(i) >= 0 for i in range(3*d+1))
        compositions.append({'d': d, 'F_degree': 3*d, 'split': [d, 2*d]})
    for n in range(1, 1001):
        N, J = int(f.subs(k, n)), int(j.subs(k, n))
        e = valuation(N-2, 3)
        assert e >= 3
        assert valuation(J*(J-1)*(J-2), 3) == e-3
        assert J % (3**e) not in [0, 1, 2]
        assert N % (3**e) == 2
    degrees = set(permutations((3, 3, 0))) | set(permutations((3, 2, 1))) | {(2, 2, 2)}
    remaining = set()
    for ds in degrees:
        t = s.Rational(ds[1]+2*ds[2]-3, 6)
        if not 0 < t < 1:
            continue
        if t == s.Rational(1, 2) and ds[0]+ds[2] > 4:
            continue
        if t > s.Rational(1, 2):
            t = 1-t
            ds = tuple(reversed(ds))
        remaining.add((str(t), ds))
    assert remaining == {('1/6', (3, 2, 1)), ('1/3', (3, 1, 2)),
                         ('1/3', (2, 3, 1)), ('1/2', (2, 2, 2))}
    result = {'status': 'passed',
              'scope': 'Coefficient-unbounded all-degree extremal split is a cubic composition, excluded numerically by prime 3; general i=3 remains open.',
              'compositions_checked': compositions, 'numeric_parameter_checks': 1000,
              'sextic_split_excluded': [2, 4], 'sextic_split_remaining': [3, 3],
              'sextic_H_C_degrees_remaining': [2, 2],
              'sextic_F2_degree_cases_remaining': [{'t': t, 'degrees': list(ds)} for t, ds in sorted(remaining)],
              'general_counterexample_degree_interval': 'm/3 < deg U, deg V < 2m/3',
              'finite_examples_used_as_general_proof': False,
              'complete_problem_solution': False, 'remaining_indices': 28}
    (ROOT/'data/results/verification_i3_extremal_split_closeout.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
