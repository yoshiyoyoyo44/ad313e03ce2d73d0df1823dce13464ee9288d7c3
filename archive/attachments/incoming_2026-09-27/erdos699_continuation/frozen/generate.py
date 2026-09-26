#!/usr/bin/env python3
from functools import lru_cache
from math import factorial,isqrt,log
from pathlib import Path
import json,time

INDICES=[95,99,103,107,119]
ROOT=Path(__file__).resolve().parent
BITS=192; SCALE=1<<BITS; TERMS=72

def ceildiv(a,b):return -((-a)//b)

def atanh(a,b):
    assert b<=a<=2*b
    low=SCALE*(a-b)//(a+b); high=ceildiv(SCALE*(a-b),a+b)
    ql=low*low//SCALE;qu=ceildiv(high*high,SCALE)
    pl,pu=low,high;rl=ru=0
    for k in range(TERMS):
        rl+=2*(pl//(2*k+1));ru+=2*ceildiv(pu,2*k+1)
        pl=pl*ql//SCALE;pu=ceildiv(pu*qu,SCALE)
    assert 9*SCALE<4*(2*TERMS+1)*3**(2*TERMS+1)
    return rl,ru+1

LOG2=atanh(2,1)
@lru_cache(None)
def logs(n):
    e=n.bit_length()-1;l,u=atanh(n,1<<e)
    return l+e*LOG2[0],u+e*LOG2[1]

def primes(n):
    return [p for p in range(2,n) if all(p%d for d in range(2,isqrt(p)+1))]

def parameters(i):
    h=i-1
    # Compare rational exponents exactly.
    from fractions import Fraction
    b=min(range(h//3+1,h+1),key=lambda b:Fraction(3*b*(b+1),2*(3*b-h)))
    a=h-b;d=2*b-a;S=b*(b+1)//2
    return a,b,d,S

def tail(i,d,S,ps):
    hsmall=1 if i in primes(i+1) else i
    pi=len(ps);delta=d*(i-pi)-3*S
    assert delta>0
    for E in range(1,100):
        n=10**E
        if n<2*i+2:continue
        if 4**S*hsmall**d*(n-i+1)**(i*d)>factorial(i)**d*n**(pi*d+3*S):
            return dict(n_power=E,small_part_correction=hsmall,degree_gap=delta)
    raise AssertionError('No tail cutoff found')

def generate_intervals(i,low,cap,d,S,ps):
    data=[]
    for p in ps:
        qs=[];q=p
        while q<cap:qs.append((q,i%q));q*=p
        data.append((logs(p)[1],qs))
    fac=sum(logs(k)[1] for k in range(1,i+1))
    constant=2*S*LOG2[0]-d*fac
    todo=[(low,cap-1)];leaves=[];nodes=0;st=time.time()
    while todo:
        lo,hi=todo.pop();nodes+=1
        upper=0
        for lp,qs in data:
            e=0
            for q,r in qs:
                if q>hi:break
                e+=int(r>0 and (lo%q<r or lo//q<hi//q))
            upper+=e*lp
        margin=constant+d*i*logs(lo-i+1)[0]-d*upper-3*S*logs(hi)[1]
        if margin>0:leaves.append([lo,hi])
        elif lo==hi:
            print(json.dumps(dict(failed_singleton=i,n=lo)),flush=True)
            return None
        else:
            mid=(lo+hi)//2;todo.append((mid+1,hi));todo.append((lo,mid))
        if nodes%20000==0:print(json.dumps(dict(i=i,nodes=nodes,leaves=len(leaves),seconds=round(time.time()-st,2))),flush=True)
        if nodes>1000000:raise RuntimeError('Concrete budget exceeded')
    print(json.dumps(dict(i=i,nodes=nodes,leaves=len(leaves),seconds=round(time.time()-st,2))),flush=True)
    return dict(leaves=leaves,tested_nodes=nodes)

def main():
    rows=[]
    for i in INDICES:
        a,b,d,S=parameters(i);ps=primes(i);t=tail(i,d,S,ps)
        print(json.dumps(dict(i=i,weights=[a,b,d,S],tail=t)),flush=True)
        intervals=generate_intervals(i,2_000_000,10**t['n_power'],d,S,ps)
        assert intervals is not None
        rows.append(dict(i=i,pi=len(ps),a=a,b=b,d=d,S=S,tail=t,intervals=intervals))
        (ROOT/'interval_certificate.json').write_text(json.dumps(dict(schema=1,rows=rows),indent=2)+'\n')

if __name__=='__main__':main()
