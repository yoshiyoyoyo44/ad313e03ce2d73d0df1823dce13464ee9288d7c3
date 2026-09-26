"""Construct circular-spacing certificates with outward-rounded log intervals.

Uses the frozen repository's 256-bit interval engine for discovery only.
verify_spacing.py independently replays the certificate with Fraction sums.
"""
import sys, json
from pathlib import Path
from math import gcd, isqrt
sys.path.insert(0, str(Path(__file__).resolve().parent/'frozen'))
from near_collision_arithmetic import SCALE, log, ratio, approximants

ROOT=Path(__file__).resolve().parent
M=10**16
A=1995
CUTOFF=128
PRIMES=[p for p in range(2,34) if all(p%d for d in range(2,isqrt(p)+1))]

def circle_gap(p,q,Q):
    points=[]
    for a in range(1,A+1):
        if gcd(a,p*q)!=1: continue
        lo,hi=ratio(log(a),log(q))
        lo*=Q; hi*=Q
        k=lo//SCALE
        if hi//SCALE!=k: return None
        points.append((lo-k*SCALE,hi-k*SCALE,a))
    points.sort()
    gaps=[(points[k+1][0]-points[k][1],points[k][2],points[k+1][2])
          for k in range(len(points)-1)]
    gaps.append((points[0][0]+SCALE-points[-1][1],points[-1][2],points[0][2]))
    return min(gaps),len(points)

def main():
    rows=[]
    for p in PRIMES:
        for q in PRIMES:
            if p>=q: continue
            alpha=ratio(log(p),log(q))
            for P,Q in approximants(alpha,6*M):
                error=max(abs(Q*alpha[0]-P*SCALE),abs(Q*alpha[1]-P*SCALE))
                if 2*M*error>=SCALE or p**CUTOFF<=800*Q: continue
                r=circle_gap(p,q,Q)
                if r is None: continue
                (gap,a,b),count=r
                epsilon=gap-M*error
                if epsilon>0 and epsilon*p**CUTOFF>400*Q*SCALE:
                    rows.append(dict(p=p,q=q,P=P,Q=Q,count=count,
                                     closest_coefficients=[a,b]))
                    break
            else: raise AssertionError(('no spacing certificate',p,q))
        print('generated',p,len(rows),flush=True)
    out=dict(schema=1,A=A,difference=33,M=M,cutoff=CUTOFF,primes=PRIMES,rows=rows)
    (ROOT/'spacing_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print('COMPLETE',len(rows),flush=True)

if __name__=='__main__': main()
