"""Independently verify full prefix coverage and every Kummer singleton."""
from pathlib import Path
from math import isqrt
from functools import lru_cache
from fractions import Fraction
import json,gzip,sys,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'frozen'))
import verify as arithmetic

@lru_cache(None)
def prime(p):return p>=2 and all(p%d for d in range(2,isqrt(p)+1))

def vfac(n,p):
    total=0
    power=p
    while power<=n:total+=n//power;power*=p
    return total

def check_single(i,row):
    n=row['n'];conditions=[]
    for p,e in row['powers']:
        assert prime(p) and p>=i and e>=1 and p**e<=n
        assert vfac(n,p)>vfac(i,p)+vfac(n-i,p)
        q=p**e;conditions.append((q,n%q))
    assert conditions
    q,r=conditions[0]
    allowed=[]
    for start in range(0,n//2+1,q):
        a=max(start,i+1);b=min(start+r,n//2)
        if a<=b:allowed.extend(range(a,b+1))
    assert len(allowed)==row['initial']
    for q,r in conditions[1:]:allowed=[j for j in allowed if j%q<=r]
    assert not allowed,(i,n,allowed[:20])

def main():
    if not __debug__:raise RuntimeError('Assertions required.')
    cert=json.loads(gzip.decompress((ROOT/'prefix_certificate.json.gz').read_bytes()))
    bootstrap=json.loads((ROOT/'product_bootstrap.json').read_text())
    expected=[r['i'] for r in bootstrap['rows']]
    caps={r['i']:max(1_999_999,r['final_cap']) for r in bootstrap['rows']}
    assert cert['schema']==1 and [r['i'] for r in cert['rows']]==expected
    results=[]
    for row in cert['rows']:
        i=row['i'];upper=row['upper'];assert upper==caps[i]
        h=i-1;b=(2*h+2)//3;a=h-b;d=3*b-h;S=b*(b+1)//2
        for s in range(i):
            for u in range(s+1):
                assert max(0,s-a)+max(0,b-u)+max(0,b-s+u)>=d
        assert sum(max(0,s-a) for s in range(i))==S
        assert sum(max(0,b-u) for u in range(i))==S
        ps=[p for p in range(2,i) if prime(p)];data=[]
        for p in ps:
            q=p;qs=[]
            while q<=upper:qs.append((q,i%q));q*=p
            data.append((arithmetic.log_interval(p)[1],qs))
        fact=sum(arithmetic.log_interval(k)[1] for k in range(1,i+1))
        tiles=[(lo,hi,None) for lo,hi in row['intervals']]
        tiles.extend((c['n'],c['n'],c) for c in row['exceptions']);tiles.sort()
        expected_n=2*i+2;minimum=None;start=time.time()
        for lo,hi,c in tiles:
            assert lo==expected_n and lo<=hi<=upper
            expected_n=hi+1
            if c is not None:
                check_single(i,c);continue
            part=0
            for lp,qs in data:
                e=0
                for q,r in qs:
                    if q>hi:break
                    e+=int(r>0 and -((-(lo-r+1))//q)<=hi//q)
                part+=e*lp
            margin=(2*S*arithmetic.L2+i*d*arithmetic.log_interval(lo-h)[0]
                    -d*fact-d*part-3*S*arithmetic.log_interval(hi)[1])
            assert margin>0,(i,lo,hi)
            minimum=margin if minimum is None else min(minimum,margin)
        assert expected_n==upper+1
        item=dict(i=i,upper=upper,intervals=len(row['intervals']),singletons=len(row['exceptions']),
                  minimum_log_margin_lower=str(Fraction(minimum,arithmetic.SCALE)))
        results.append(item)
        arithmetic.log_interval.cache_clear()
        print(json.dumps(dict(i=i,intervals=item['intervals'],singletons=item['singletons'],seconds=round(time.time()-start,2))),flush=True)
    out=dict(status='EXHAUSTIVE-COMPUTATION',rows=results,
             interval_count=sum(r['intervals'] for r in results),
             singleton_count=sum(r['singletons'] for r in results))
    (ROOT/'prefix_verification.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
