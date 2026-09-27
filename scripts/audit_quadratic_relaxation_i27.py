"""Replay an exact exponent-relaxation witness with no optimization package.

This does not construct integers n,j or a counterexample to Problem 699.
It shows that the explicitly tested geometric capacity inequalities still
admit a rational exponent allocation with all cofactor exponents zero.
"""
from itertools import combinations
from math import gcd
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    path=ROOT/'data/certificates/quadratic_relaxation_i27_2026-09-27.json'
    raw=path.read_bytes()
    data=json.loads(raw)
    i=data['i'];den=data['denominator'];bad=set(data['maximal_rows'])
    assert i==27 and bad==set(range(9)) and den==10**6
    cells=[(s,u) for s in range(i) for u in range(s+1)]
    weights={p:0 for p in cells}
    seen=set()
    for s,u,w in data['weighted_cells']:
        assert (s,u) in weights and (s,u) not in seen and isinstance(w,int) and w>0
        seen.add((s,u));weights[s,u]=w
    for s in range(i):
        assert sum(weights[s,u] for u in range(s+1))==(0 if s in bad else den)
    lines=set()
    for p,q in combinations(cells,2):
        a=q[1]-p[1];b=q[0]-p[0];g=gcd(a,b);a//=g;b//=g
        if b<0 or b==0 and a<0:
            a=-a;b=-b
        lines.add((a,b,b*p[1]-a*p[0]))
    smallest_line_slack=den
    for a,b,c in lines:
        mass=sum(w for (s,u),w in weights.items() if b*u-a*s==c)
        assert mass<=den
        if b:
            smallest_line_slack=min(smallest_line_slack,den-mass)
    curves=data['positive_definite_quadratics']
    assert len({tuple(c) for c in curves})==len(curves)==666
    smallest_quadratic_slack=2*den
    for A,B,C,D,E,F in curves:
        assert all(isinstance(x,int) for x in (A,B,C,D,E,F))
        assert A>0 and C>0 and 4*A*C-B*B>0
        mass=sum(w for (s,u),w in weights.items()
                 if A*s*s+B*s*u+C*u*u+D*s+E*u+F==0)
        assert mass<=2*den
        smallest_quadratic_slack=min(smallest_quadratic_slack,2*den-mass)
    assert len(lines)==data['line_count'] and len(curves)==data['quadratic_count']
    assert smallest_line_slack>0 and smallest_quadratic_slack>0
    result={'status':'passed','scope':'feasible rational exponent relaxation, not integer counterexamples',
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'i':i,'maximal_rows':sorted(bad),'nonzero_cells':len(seen),'denominator':den,
            'all_pair_determined_lines':len(lines),'positive_definite_quadratics':len(curves),
            'minimum_nonhorizontal_line_slack_numerator':smallest_line_slack,
            'minimum_quadratic_slack_numerator':smallest_quadratic_slack,
            'not_claimed':['feasibility for all quadratic curves','integer realizability',
                           'impossibility of another proof method','any index solved']}
    output=ROOT/'data/results/verification_quadratic_relaxation_i27.json'
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
