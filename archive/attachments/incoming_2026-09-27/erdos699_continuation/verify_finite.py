"""Independent replay of all n<=4,209,368,355 for i=28,31,34.

Uses the frozen separate verifier's direct rational logarithm implementation.
The interval coverage checker below is adapted for a finite, not asymptotic, cap.
"""
from pathlib import Path
import sys,json,gzip
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'frozen'))
import verify as arithmetic
from fractions import Fraction
from math import isqrt

INDICES=[28,31,34]

def check_middle(cert):
    assert cert['schema']==1 and cert['upper']==4_209_368_355
    assert [r['i'] for r in cert['rows']]==INDICES
    results=[]
    for row in cert['rows']:
        i,a,b,d,S=(row[k] for k in ('i','a','b','d','S'))
        assert a==i-1-b and d==3*b-i+1>0 and S==b*(b+1)//2
        for s in range(i):
            for u in range(s+1):
                assert max(0,s-a)+max(0,b-u)+max(0,b-s+u)>=d
        assert sum(max(0,s-a) for s in range(i))==S
        assert sum(max(0,b-u) for u in range(i))==S
        pdata=[]
        for p in range(2,i):
            if not arithmetic.prime(p): continue
            qs=[]; q=p
            while q<=cert['upper']:
                qs.append((q,i%q));q*=p
            pdata.append((arithmetic.log_interval(p)[1],qs))
        fact=sum(arithmetic.log_interval(k)[1] for k in range(1,i+1))
        expected=2_000_000; minimum=None
        for lo,hi in row['intervals']['leaves']:
            assert lo==expected and lo<=hi<=cert['upper']
            expected=hi+1
            upper=0
            for lp,qs in pdata:
                count=0
                for q,r in qs:
                    if q>hi: break
                    count+=int(r>0 and -((-(lo-r+1))//q)<=hi//q)
                upper+=lp*count
            margin=(2*S*arithmetic.L2+d*i*arithmetic.log_interval(lo-i+1)[0]
                    -d*fact-d*upper-3*S*arithmetic.log_interval(hi)[1])
            assert margin>0,(i,lo,hi)
            minimum=margin if minimum is None else min(minimum,margin)
        assert expected==cert['upper']+1
        results.append(dict(i=i,intervals=len(row['intervals']['leaves']),
                            minimum_log_margin_lower=str(Fraction(minimum,arithmetic.SCALE))))
        print('middle verified',results[-1],flush=True)
    return results

def main():
    if not __debug__: raise RuntimeError('Assertions are required.')
    middle=check_middle(json.loads((ROOT/'finite_intervals.json').read_text()))
    arithmetic.INDICES=INDICES
    plain=ROOT/'small_certificate.json'
    path=ROOT/'small_certificate.json.gz'
    small=json.loads(plain.read_text()) if plain.exists() else json.loads(gzip.decompress(path.read_bytes()))
    check=arithmetic.check_small(small)
    formula=arithmetic.check_formula()
    result=dict(status='EXHAUSTIVE-COMPUTATION',indices=INDICES,upper=4_209_368_355,
                middle=middle,small=check,formula=formula)
    (ROOT/'finite_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__': main()
