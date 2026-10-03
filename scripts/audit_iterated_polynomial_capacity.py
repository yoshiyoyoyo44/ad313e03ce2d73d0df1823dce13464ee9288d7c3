"""Integer replay of an i27 exponent witness surviving new capacities.
Not a counterexample, nor feasibility for every polynomial capacity.
"""
from pathlib import Path
from itertools import combinations
from math import gcd
import json,hashlib
ROOT = Path(__file__).resolve().parent.parent
CERTIFICATES = ROOT / 'data/certificates'
RESULT = ROOT / 'data/results/verification_iterated_polynomial_capacity.json'

def main():
 raw=(CERTIFICATES/'iterated_polynomial_relaxation_i27_2026-09-30.json').read_bytes();c=json.loads(raw)
 i=27;den=c['denominator'];cells=[(s,u) for s in range(i) for u in range(s+1)]
 weights={p:0 for p in cells}
 for s,u,w in c['weighted_cells']:
  assert (s,u) in weights and weights[s,u]==0 and isinstance(w,int) and w>0
  weights[s,u]=w
 for s in range(i):assert sum(weights[s,u] for u in range(s+1))==(0 if s<9 else den)
 lines=set()
 for p,q in combinations(cells,2):
  a=q[1]-p[1];b=q[0]-p[0];g=gcd(a,b);a//=g;b//=g
  if b<0 or b==0 and a<0:a=-a;b=-b
  lines.add((a,b,b*p[1]-a*p[0]))
 line_slack=den
 for a,b,c0 in lines:
  mass=sum(w for (s,u),w in weights.items() if b*u-a*s==c0)
  assert mass<=den
  if b:line_slack=min(line_slack,den-mass)
 old=json.loads((ROOT/'data/certificates/quadratic_relaxation_i27_2026-09-27.json').read_bytes())
 qslack=2*den
 for A,B,C,D,E,F in old['positive_definite_quadratics']:
  mass=sum(w for (s,u),w in weights.items() if A*s*s+B*s*u+C*u*u+D*s+E*u+F==0)
  assert mass<=2*den;qslack=min(qslack,2*den-mass)
 masses=[];zero_sizes=[]
 for f in json.loads((CERTIFICATES/'polynomial_capacity_supports_2026-09-30.json').read_bytes())['certificates']+json.loads((CERTIFICATES/'iterated_polynomial_cuts_2026-09-30.json').read_bytes())['certificates']:
  if f['i']!=27:continue
  d=f['degree'];D=f['leading_coefficient'];terms=f['terms'];C=f['lower_coefficient_l1'];E=f['threshold_power_10'];N=10**E
  assert d>0 and D>0 and d<18
  assert {(a,b,t) for a,b,t in terms if a+b==d}=={(d,0,D),(0,d,D)}
  assert all(a>=0 and b>=0 and a+b<=d and isinstance(t,int) for a,b,t in terms)
  assert C==sum(abs(t) for a,b,t in terms if a+b<d)
  assert all(sum(t*s**a*u**b for a,b,t in terms)==0 for s,u in f['support'])
  assert N>2*27*26 and N*D>C and N**(18-d)*27>6*D*__import__('math').factorial(27)
  assert N<10**87
  mass=sum(w for (s,u),w in weights.items() if sum(t*s**a*u**b for a,b,t in f['terms'])==0)
  assert mass<=f['degree']*den
  masses.append({'name':f['name'],'capacity':f['degree'],'mass_numerator':mass,'denominator':den})
  zeros={(s,u) for s,u in cells if sum(t*s**a*u**b for a,b,t in f['terms'])==0}
  assert set(map(tuple,f['support'])).issubset(zeros)
  if f['name'].startswith('iterated_'):
   zero_sizes.append({'name':f['name'],'support_size':len(f['support']),'full_zero_set_size':len(zeros),'additional_zero_cells':len(zeros)-len(f['support'])})
 assert line_slack>0 and qslack>0
 result={'status':'passed','scope':'Exact exponent relaxation after adding '+str(len(masses))+' explicit high-degree capacities; no integer counterexample',
 'certificate_sha256':hashlib.sha256(raw).hexdigest(),'nonzero_cells':len(c['weighted_cells']),
 'total_mass_numerator':sum(weights.values()),'denominator':den,'line_count':len(lines),
 'quadratic_count':len(old['positive_definite_quadratics']),'minimum_nonhorizontal_line_slack_numerator':line_slack,
 'minimum_quadratic_slack_numerator':qslack,'higher_degree_capacities':masses,'iterated_curve_zero_set_sizes':zero_sizes,
 'minimum_higher_degree_capacity_slack_numerator':min(r['capacity']*r['denominator']-r['mass_numerator'] for r in masses),
 'iterated_polynomial_certificate_sha256':hashlib.sha256((CERTIFICATES/'iterated_polynomial_cuts_2026-09-30.json').read_bytes()).hexdigest(),
 'not_claimed':['feasibility for all higher-degree polynomials','integer realizability','any index solved']}
 RESULT.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
