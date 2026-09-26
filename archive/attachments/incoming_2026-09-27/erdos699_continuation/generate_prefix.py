"""Certify the remaining bounded prefixes using intervals and Kummer singletons."""
from pathlib import Path
from math import isqrt
import sys,json,gzip,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'frozen'))
import generate as gen
from generate_small import candidate_count,candidates

def trial_primes(limit):
    flags=bytearray(b'\1')*(limit+1);flags[:2]=b'\0\0'
    for p in range(2,isqrt(limit)+1):
        if flags[p]:flags[p*p::p]=b'\0'*((limit-p*p)//p+1)
    return [p for p in range(2,limit+1) if flags[p]]

def vp_factorial(n,p):
    v=0
    while n:n//=p;v+=n
    return v

def kummer(i,n,ps):
    good=set()
    for s in range(i):
        z=n-s
        for p in ps:
            if p*p>z:break
            if z%p==0:
                while z%p==0:z//=p
                if p>=i:good.add(p)
        if z>=i:good.add(z)
    constraints=[]
    for p in good:
        v=vp_factorial(n,p)-vp_factorial(i,p)-vp_factorial(n-i,p)
        if v<=0:continue
        q=p;e=1
        while q<=n:
            r=n%q
            count=candidate_count(q,r,i+1,n//2)
            constraints.append((count,p,e,q,r))
            q*=p;e+=1
    assert constraints,('no common-prime candidates',i,n)
    constraints.sort()
    count,p,e,q,r=constraints[0]
    left=candidates(q,r,i+1,n//2)
    assert len(left)==count
    used=[[p,e]]
    while left:
        choice=min((([j for j in left if j%q<=r],p,e) for _,p,e,q,r in constraints),
                   key=lambda item:len(item[0]))
        kept,p,e=choice
        assert len(kept)<len(left),('unresolved singleton',i,n,left[:20])
        used.append([p,e]);left=kept
    return dict(n=n,powers=used,initial=count)

def certify(i,upper):
    h=i-1;b=(2*h+2)//3;a=h-b;d=3*b-h;S=b*(b+1)//2
    data=[]
    for p in gen.primes(i):
        qs=[];q=p
        while q<=upper:qs.append((q,i%q));q*=p
        data.append((gen.logs(p)[1],qs))
    constant=2*S*gen.LOG2[0]-d*sum(gen.logs(k)[1] for k in range(1,i+1))
    todo=[(2*i+2,upper)];leaves=[];exceptions=[];nodes=0
    ps=trial_primes(isqrt(upper)+1)
    while todo:
        lo,hi=todo.pop();nodes+=1
        vu=0
        for lp,qs in data:
            e=sum(int(r>0 and (lo%q<r or lo//q<hi//q)) for q,r in qs if q<=hi)
            vu+=lp*e
        margin=constant+i*d*gen.logs(lo-h)[0]-d*vu-3*S*gen.logs(hi)[1]
        if margin>0:leaves.append([lo,hi])
        elif lo==hi:exceptions.append(kummer(i,lo,ps))
        else:
            mid=(lo+hi)//2;todo.append((mid+1,hi));todo.append((lo,mid))
        if nodes>2_000_000:raise RuntimeError(('prefix budget',i,nodes))
    return dict(i=i,upper=upper,intervals=leaves,exceptions=exceptions,nodes=nodes)

def main():
    if not __debug__:raise RuntimeError('Assertions required.')
    root=json.loads((ROOT/'product_bootstrap.json').read_text())
    rows=[]
    for row in root['rows']:
        i=row['i'];upper=max(1_999_999,row['final_cap']);start=time.time()
        result=certify(i,upper);rows.append(result)
        gen.logs.cache_clear()
        print(json.dumps(dict(i=i,upper=upper,intervals=len(result['intervals']),
                              exceptions=len(result['exceptions']),seconds=round(time.time()-start,2))),flush=True)
        payload=json.dumps(dict(schema=1,rows=rows),separators=(',',':')).encode()
        (ROOT/'prefix_certificate.json.gz').write_bytes(gzip.compress(payload,mtime=0))

if __name__=='__main__':main()
