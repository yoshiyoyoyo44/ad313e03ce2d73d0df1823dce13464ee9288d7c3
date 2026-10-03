"""Exact replay of all six-cell certificates and the seven-cell obstruction."""
import itertools,json,math
from fractions import Fraction as F
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
CERTIFICATE = ROOT / 'data/certificates/i4_six_cell_capacity_2026-09-30.json'
RESULT = ROOT / 'data/results/verification_i4_six_cell_capacity.json'
D=json.loads(CERTIFICATE.read_text())
points=[tuple(p) for p in D['points']]
assert points==[(s,u) for s in range(1,4) for u in range(s+1)]
hexagon={tuple(p) for p in D['hexagon']}
assert hexagon=={(1,0),(1,1),(2,0),(2,2),(3,1),(3,2)}
expected=set()
for qrow in [1,2,3]:
 for supp in itertools.combinations(points,6):
  counts=[sum(s==r for s,u in supp) for r in [1,2,3]]
  if counts[qrow-1]>=1 and all(counts[r-1]>=2 for r in [1,2,3] if r!=qrow) and set(supp)!=hexagon:expected.add((qrow,tuple(supp)))
seen=set();counts={1:0,2:0,3:0};dist={1:{},2:{},3:{}}
for rec in D['records']:
 qrow=rec['qrow'];supp=tuple(tuple(p) for p in rec['support']);heavy=rec['heavy_rows'];mu=list(map(F,rec['mu']))
 key=(qrow,supp)
 assert key in expected and key not in seen
 seen.add(key);counts[qrow]+=1
 assert heavy==[r for r in [1,2,3] if r!=qrow]
 assert len(mu)==2 and all(-2<=v<=0 for v in mu)
 degree=F(0);weights={p:F(0) for p in supp}
 all_lines=[]
 for line in rec['lines']:
  a,b,c=line['abc'];w=F(line['weight'])
  assert w>0 and math.gcd(math.gcd(abs(a),abs(b)),abs(c))==1
  zeros=[p for p in points if b*p[1]-a*p[0]==c]
  assert len(zeros)>=2
  # Convexity in j: check both endpoints j=5 and j=n/2.
  # The affine bounds extend from n=10 by their nonnegative slopes.
  for alpha, beta in [(F(-a), F(5*b-c)), (F(b,2)-a, F(-c))]:
   for sign in [-1,1]:
    assert 3-sign*alpha >= 0
    assert 10*(3-sign*alpha)-9-sign*beta >= 0
  all_lines.append((a,b,c,w))
  degree+=w
  for p in supp:
   if p in zeros:weights[p]+=w
 assert degree<=4
 for p in supp:
  if p[0] in heavy:weights[p]+=mu[heavy.index(p[0])]
  assert weights[p]>=int(p[0]==qrow)
 gamma=degree+sum(mu)
 assert gamma==F(rec['gamma']) and 0<=gamma<=F(1,2)
 # Check an exact feasible primal and equality with the dual optimum.
 x=list(map(F,rec['primal']))
 assert len(x)==6 and all(v>=0 for v in x)
 assert all(sum(v for p,v in zip(supp,x) if p[0]==r)==1 for r in heavy)
 for p1,p2 in itertools.combinations(points,2):
  s,u=p1;t,v=p2;a=v-u;b=t-s;c=b*u-a*s
  assert sum(z for p,z in zip(supp,x) if b*p[1]-a*p[0]==c)<=1
 assert sum(v for p,v in zip(supp,x) if p[0]==qrow)==gamma
 gs=str(gamma);dist[qrow][gs]=dist[qrow].get(gs,0)+1
assert seen==expected and counts=={1:53,2:29,3:21}
# New necessary bounds use R_heavy >= (n-3)/d and line <= 3(n-3).
classes={9:(1,1,1,6,2),18:(2,1,1,3,2),20:(2,2,1,1,3),27:(3,3,2,1,2),28:(1,1,2,1,3),12:(3,1,1,2,3)}
tails={}
for residue,(qrow,c,d1,d2,p) in classes.items():
 K=81*(d1*d2)**2
 den=c*K
 exponent=1
 while den*den*p**(2*exponent)<=10**87-3:exponent+=1
 # q^2 >= (n-3)/den^2 forces q=p^e with e >= exponent.
 assert den*den*p**(2*(exponent-1))<10**87-3
 assert den*den*p**(2*exponent)>=10**87-3
 tails[residue]={'E_constant':K,'q_denominator':den,'prime':p,'exponent_at_least':exponent}
# Explicit seven-cell feasible exponent configuration. It is not an integer counterexample.
w=D['seven_cell_capacity_witness'];supp=list(map(tuple,w['support']));x=list(map(F,w['primal']))
assert len(supp)==7 and all(v>0 for v in x) and not hexagon.issubset(supp)
assert sum(v for p,v in zip(supp,x) if p[0]==2)==1
assert sum(v for p,v in zip(supp,x) if p[0]==3)==1
assert sum(v for p,v in zip(supp,x) if p[0]==1)==F(3,4)
for p1,p2 in itertools.combinations(points,2):
 s,u=p1;t,v=p2;a=v-u;b=t-s;c=b*u-a*s
 assert sum(z for p,z in zip(supp,x) if b*p[1]-a*p[0]==c)<=1
assert sum(v for p,v in zip(supp,x) if p in hexagon)<=2
result = {'status':'passed','certificates_verified':len(seen),'counts_by_qrow':counts,'optimal_exponent_distribution':dist,'six_cell_tail_bounds':tails,'seven_cell_positive_witness_verified':True,'scope':'Necessary conditions for exactly six occupied cells in rows 1,2,3, assuming an i=4 counterexample at n>=10^87; no index solved.'}
RESULT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
