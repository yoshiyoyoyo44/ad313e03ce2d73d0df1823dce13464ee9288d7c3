#!/usr/bin/env python3
from array import array
from math import isqrt
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
INDICES=[95,99,103,107,119]
LIMIT=2_000_100

def candidate_count(q,r,low,high):
    def count(end):
        if end<0:return 0
        k,t=divmod(end,q)
        return k*(r+1)+min(t,r)+1
    return count(high)-count(low-1)

def candidates(q,r,low,high):
    return [j for k in range(low//q,high//q+1)
            for j in range(max(low,k*q),min(high,k*q+r)+1)]

def main():
    spf=array('I',range(LIMIT+1))
    for p in range(2,isqrt(LIMIT)+1):
        if spf[p]==p:
            for k in range(p*p,LIMIT+1,p):
                if spf[k]==k:spf[k]=p
    primes=[p for p in range(2,LIMIT+1) if spf[p]==p]
    gaps=[(a,b) for a,b in zip(primes,primes[1:]) if b-a>min(INDICES)]
    records=[]
    for i in INDICES:
        needed=sorted(n for a,b in gaps for n in range(a+i,b)
                      if 2*i+2<=n<2_000_000)
        for n in needed:
            constraints=[]
            for r in range(i):
                z=n-r
                while z>1:
                    p=spf[z];q=1;e=0
                    while z%p==0:z//=p;q*=p;e+=1
                    if p>i:constraints.append(dict(p=p,e=e,r=r))
            constraints.sort(key=lambda c:candidate_count(c['p']**c['e'],c['r'],i+1,n//2))
            assert constraints
            anchor=constraints[0];left=candidates(anchor['p']**anchor['e'],anchor['r'],i+1,n//2)
            initial=len(left);used=[]
            while left:
                options=[]
                for c in constraints[1:]:
                    q=c['p']**c['e'];rem=c['r']
                    kept=[j for j in left if j%q<=rem]
                    options.append((len(kept),c,kept))
                size,c,kept=min(options,key=lambda x:x[0])
                assert size<len(left),(i,n,left)
                used.append(dict(**c,eliminated=len(left)-size));left=kept
            records.append(dict(i=i,n=n,anchor=anchor,initial_count=initial,constraints=used))
        print(json.dumps(dict(i=i,exceptions=len(needed))),flush=True)
    obj=dict(schema=1,limit=LIMIT,covered_upper=1_999_999,
        prime_count=len(primes),last_prime=primes[-1],long_gaps=gaps,
        exceptions=records)
    (ROOT/'small_certificate.json').write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(dict(total=len(records),max_initial=max(r['initial_count'] for r in records))))

if __name__=='__main__':main()
