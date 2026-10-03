"""Integer-only replay of high-degree geometric capacity certificates.

No optimizer, SymPy, floating point, or imported repository code is used.
The program verifies a support-specific exclusion; it does not solve any
remaining index of Erdos Problem 699.
"""
from pathlib import Path
from math import factorial,isqrt
import hashlib,json
ROOT = Path(__file__).resolve().parent.parent
CERTIFICATE = ROOT / 'data/certificates/polynomial_capacity_supports_2026-09-30.json'
RESULT = ROOT / 'data/results/verification_polynomial_capacity_supports.json'

def small_primes(i):
 return [p for p in range(2,i) if all(p%q for q in range(2,isqrt(p)+1))]

def eval_poly(terms,s,u):
 return sum(c*s**a*u**b for a,b,c in terms)

def main():
 raw=CERTIFICATE.read_bytes()
 data=json.loads(raw); out=[]
 quad=json.loads((ROOT/'data/certificates/quadratic_relaxation_i27_2026-09-27.json').read_bytes())
 halves=json.loads((ROOT/'data/certificates/maximal_row_relaxation_2026-09-27.json').read_bytes())
 originals={'quadratic_i27':{(s,u):w for s,u,w in quad['weighted_cells']}}
 for r in halves['rows']:
  originals['half_i'+str(r['i'])]={(s,u):1 for s,u in r['occupied_cells']}
 for c in data['certificates']:
  i=c['i'];d=c['degree'];D=c['leading_coefficient'];terms=c['terms'];support={tuple(p) for p in c['support']}
  assert d>0 and D>0
  assert len(terms)==len({(a,b) for a,b,t in terms})
  assert all(isinstance(a,int) and isinstance(b,int) and isinstance(t,int) and a>=0 and b>=0 and a+b<=d for a,b,t in terms)
  assert {(a,b,t) for a,b,t in terms if a+b==d}=={(d,0,D),(0,d,D)}
  assert all(0<=u<=s<i for s,u in support)
  assert all(eval_poly(terms,s,u)==0 for s,u in support)
  zeros={(s,u) for s in range(i) for u in range(s+1) if eval_poly(terms,s,u)==0}
  assert support==set(originals[c['name']])
  assert zeros == support
  C=sum(abs(t) for a,b,t in terms if a+b<d)
  assert C==c['lower_coefficient_l1']
  primes=small_primes(i);m=len(primes);k=i-m
  ci=i if i not in small_primes(i+1) else 1
  # Alternative exact definition of ci from the p<i part of i.
  ci2=1
  for p in primes:
   z=i
   while z%p==0:ci2*=p;z//=p
  assert ci==ci2
  assert m==c['cofactor_count'] and k-d==c['gap_degree']>0
  E=c['threshold_power_10'];N=10**E
  assert N>2*i*(i-1) and N*D>C
  assert N**(k-d)*ci>6*D*factorial(i)
  assert 10**87>=N
  # Each inequality extends to all n>=N by elementary monotonicity.
  den=10**6 if c['name']=='quadratic_i27' else 2
  mass=sum(originals[c['name']].values())
  assert mass==k*den
  assert mass>d*den
  out.append({'name':c['name'],'i':i,'support_size':len(support),'full_zero_set_size':len(zeros),'degree':d,
   'total_certificate_exponent':k,'polynomial_capacity_exponent':d,'degree_gap':k-d,
   'threshold_power_10':E,'threshold_below_existing_finite_range':True,
   'leading_coefficient_digits':len(str(D)),'lower_coefficient_l1_digits':len(str(C)),
   'coefficient_terms':len(terms)})
 result={'status':'passed','certificate_sha256':hashlib.sha256(raw).hexdigest(),
  'scope':'Four explicitly listed supports excluded for all n after combining with the existing finite-domain theorem; no index solved.',
  'certificates':out,
  'not_claimed':['all-support exclusion','newly solved index','an integer counterexample from any relaxation witness']}
 RESULT.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
