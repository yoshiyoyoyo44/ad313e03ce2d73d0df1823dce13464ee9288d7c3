"""Integer interval arithmetic used to construct the near-collision certificate."""
from functools import lru_cache

BITS=256
SCALE=1<<BITS
TERMS=100


def ceiling(a,b):return -((-a)//b)


def log_ratio(a,b):
    assert b<=a<=2*b
    lo=SCALE*(a-b)//(a+b);hi=ceiling(SCALE*(a-b),a+b)
    lo2=lo*lo//SCALE;hi2=ceiling(hi*hi,SCALE)
    pl,pu=lo,hi;sl=su=0
    for k in range(TERMS):
        sl+=2*(pl//(2*k+1));su+=2*ceiling(pu,2*k+1)
        pl=pl*lo2//SCALE;pu=ceiling(pu*hi2,SCALE)
    assert 9*SCALE<4*(2*TERMS+1)*3**(2*TERMS+1)
    return sl,su+1


LOG2=log_ratio(2,1)


@lru_cache(None)
def log(n):
    assert n>0
    e=n.bit_length()-1
    lo,hi=log_ratio(n,1<<e)
    return lo+e*LOG2[0],hi+e*LOG2[1]


def ratio(numerator,denominator):
    lo,hi=numerator;dl,du=denominator
    assert dl>0
    return lo*SCALE//(dl if lo<0 else du),ceiling(hi*SCALE,du if hi<0 else dl)


def distance_lower(lo,hi):
    if ceiling(lo,SCALE)<=hi//SCALE:return 0
    return min(lo%SCALE,(-hi)%SCALE)


def approximants(alpha,minimum=0):
    # Candidates only. The replay proves every needed inequality without trusting
    # this continued-fraction construction or requiring convergent completeness.
    a,b=sum(alpha),2*SCALE
    h0,h1,k0,k1=0,1,1,0
    result=[]
    while b:
        quotient,a,b=a//b,b,a%b
        h0,h1=h1,quotient*h1+h0
        k0,k1=k1,quotient*k1+k0
        if k1>=10**35:break
        if k1>minimum:result.append((h1,k1))
    return result
