"""Exact rational intervals for three BFT 2.4 applications and i22/i25.

Only the standard library is used. Outward rounding, integer roots, a
positive atanh log series, and exact polynomial integrals replace the
exploratory floating point calculation. External BFT and the finite input
are explicitly retained; they are not re-proved by this checker.
"""
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path
from functools import lru_cache
import json

ROOT = Path(__file__).resolve().parents[1]
SCALE = 2**128


def floor_scaled(x):
    return (x.numerator*SCALE)//x.denominator


def ceil_scaled(x):
    return -((-x.numerator*SCALE)//x.denominator)


class I:
    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = self.lo if hi is None else F(hi)
        assert self.lo <= self.hi

    @staticmethod
    def rounded(lo, hi):
        return I(F(floor_scaled(F(lo)), SCALE), F(ceil_scaled(F(hi)), SCALE))

    @staticmethod
    def cast(x):
        return x if isinstance(x,I) else I(x)

    def __add__(self, other):
        other = I.cast(other)
        return I.rounded(self.lo+other.lo,self.hi+other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi,-self.lo)

    def __sub__(self, other):
        return self+(-I.cast(other))

    def __rsub__(self, other):
        return I.cast(other)+(-self)

    def __mul__(self, other):
        other = I.cast(other)
        vals=[x*y for x in (self.lo,self.hi) for y in (other.lo,other.hi)]
        return I.rounded(min(vals),max(vals))

    __rmul__ = __mul__

    def reciprocal(self):
        assert not self.lo <= 0 <= self.hi
        return I.rounded(1/self.hi,1/self.lo)

    def __truediv__(self, other):
        return self*I.cast(other).reciprocal()

    def __rtruediv__(self, other):
        return I.cast(other)*self.reciprocal()

    def __pow__(self,n):
        assert isinstance(n,int)
        if n<0:
            return (self**(-n)).reciprocal()
        out=I(1);base=self
        while n:
            if n&1:out=out*base
            n//=2
            if n:base=base*base
        return out

    def root(self,d):
        assert self.lo>=0 and d>=1
        def bound(x):
            target=(x.numerator*SCALE**d)//x.denominator
            if d==2:return isqrt(target)
            left=0;right=1<<((target.bit_length()+d-1)//d+1)
            while left+1<right:
                middle=(left+right)//2
                if middle**d<=target:left=middle
                else:right=middle
            return left
        low=bound(self.lo);high=bound(self.hi)+1
        return I(F(low,SCALE),F(high,SCALE))

    def rational_power(self,exponent):
        exponent=F(exponent)
        assert self.lo>0
        if exponent<0:return self.rational_power(-exponent).reciprocal()
        return (self**exponent.numerator).root(exponent.denominator)

    def record(self):
        # Integer decimal enclosures are readable and remain exact.
        decimal_scale=10**12
        low=(self.lo.numerator*decimal_scale)//self.lo.denominator
        high=-((-self.hi.numerator*decimal_scale)//self.hi.denominator)
        return dict(lower_numerator=low,upper_numerator=high,denominator=decimal_scale)


def log_unit(t):
    assert 1<=t<=2
    z=I(t-1)/I(t+1)
    power=z;z2=z*z;total=I(0)
    for k in range(80):
        total=total+power/F(2*k+1)
        power=power*z2
    # With 0<=z<=1/3, the positive tail is bounded geometrically.
    tail=2*F(1,3)**161/(161*(1-F(1,9)))
    return I.rounded(2*total.lo,2*total.hi+tail)


@lru_cache(None)
def log_fraction(x):
    x=F(x)
    assert x>0
    k=x.numerator.bit_length()-x.denominator.bit_length()
    t=x/F(2)**k
    while t<1:t*=2;k-=1
    while t>=2:t/=2;k+=1
    return log_unit(t)+k*log_unit(F(2))


def logarithm(x):
    x=I.cast(x)
    assert x.lo>0
    low=log_fraction(x.lo);high=log_fraction(x.hi)
    return I(low.lo,high.hi)


def interval_max(values):
    return I(max(v.lo for v in values),max(v.hi for v in values))


def interval_min(values):
    return I(min(v.lo for v in values),min(v.hi for v in values))


def polynomial_integral(A,B,C,t):
    """Integral u^A (1-u)^B (1-t*u)^C du, computed exactly."""
    value=F(0)
    for j in range(B+1):
        for k in range(C+1):
            value+=F((-1)**(j+k)*comb(B,j)*comb(C,k),A+j+k+1)*t**k
    assert value>0
    return value


ANCHORS = (
    dict(pair=[2,17],p=17,k0=1,a=1,q=2,l0=4,b=1,c=7,d=5,
         L1=F(14135,10000),m0=74,target=F(337,1000),epsilon=F(9,10000)),
    dict(pair=[11,19],p=11,k0=2,a=3,q=19,l0=2,b=1,c=25,d=17,
         L1=F(15540,10000),m0=582,target=F(196,1000),epsilon=F(15,10000)),
    dict(pair=[17,19],p=17,k0=2,a=5,q=19,l0=2,b=4,c=2,d=1,
         L1=F(19377,10000),m0=150,target=F(191,1000),epsilon=F(15,10000)),
)


def certify(row, upper_log_threshold=500000):
    p,k0,a,q,l0,b,c,d=(row[k] for k in ('p','k0','a','q','l0','b','c','d'))
    A=p**k0;B=q**l0;D0=a*A-b*B
    assert D0>0
    s=F(c,d);z=F(D0,a*A);L1=row['L1']
    assert 1<s<1/z
    M1=min(A,B);M2=max(A,B)
    radicand=s*s*z*z+4-4*z
    radical=I(radicand).root(2)
    u1=(s*(2-z)-radical)/(2*(1-z)*(s+1))
    u2=(s*z+2-radical)/(2*z*(s+1))
    assert 0<u1.lo<u1.hi<1 and 0<u2.lo<u2.hi<1
    alpha=I(s+1).rational_power(s+1)/I(s-1).rational_power(s-1)
    Q=alpha*u1.rational_power(s-1)*(1-u1)*(1-u1+z*u1)
    E=alpha*u2*(1-u2)*(1-z*u2).rational_power(s-1)
    Omega3=I(A).rational_power(s-1)*L1/(a*I(b).rational_power(s)*Q)
    Omega4=I(M1).rational_power(s)*L1/(I(a*A).rational_power(s-1)*D0**2*E)
    assert Omega3.lo>1 and Omega4.lo>1
    denominator=logarithm(I(M2).rational_power(s)*Omega4)
    lam=logarithm(Omega4)/denominator
    epsilon=row['epsilon'];target=row['target']
    assert lam.lo-epsilon>target
    # 3<pi<4 suffices. This coarse elementary enclosure avoids relying
    # on any decimal approximation of pi for a strict certificate.
    pi=I(3,4)
    Cs=[]
    for delta in (0,1):
        # The source exponent is (-1)^delta/2: +1/2 for delta=0,
        # -1/2 for delta=1. This corrects the preliminary diagnostic.
        root_factor=I(s*s-1).rational_power(F((-1)**delta,2))
        common=(alpha**d)*root_factor/(2*pi)
        # (1-u+z*u)=(1-(1-z)u).
        I1=polynomial_integral(c-d-1+delta,d-delta,d-delta,1-z)
        I2=polynomial_integral(d-delta,d-delta,c-d-1+delta,z)
        Cs.append((common*I1/(Q**d),common*I2/(E**d)))
    kappa1=interval_max([200*C1/F((a*A)**delta)
                         for delta,(C1,C2) in enumerate(Cs)])
    kappa2=interval_min([F((a*A)**(1-delta),2)*F(D0)**(2*delta-1)/C2
                         for delta,(C1,C2) in enumerate(Cs)])
    terms=[logarithm(kappa1)/(d*logarithm(Omega3)),
           (1+lam)*logarithm(I(M2)**c/kappa2)/(epsilon*d*denominator),
           (1+lam)*logarithm(kappa2)/(epsilon*d*denominator),I(row['m0'])]
    big_M=interval_max(terms)
    log_x0=c*(big_M+1)/(1-lam)*logarithm(M2)
    assert log_x0.hi<upper_log_threshold
    return dict(pair=row['pair'],p=p,k0=k0,a=a,q=q,l0=l0,b=b,c=c,d=d,
                D0=D0,L1=str(L1),m0=row['m0'],target=str(target),epsilon=str(epsilon),
                Omega3=Omega3.record(),Omega4=Omega4.record(),
                lambda3=lam.record(),log_x0=log_x0.record(),
                upper_log_threshold=upper_log_threshold,positive_D_final=100,
                corrected_delta0_prefactor=True)


def tail_comparison(i):
    h=i-1;ps=[p for p in range(2,i) if all(p%k for k in range(2,isqrt(p)+1))]
    b=(2*h+2)//3;d=3*b-h;S=b*(b+1)//2;D=3*S-d*(i-len(ps))
    assert D==d and i in (22,25)
    # P>Z^(561/500); both Bernoulli losses are <2.
    gap=561*d-500*D
    assert gap>0
    A=factorial(i)//i
    e=0
    while A>=10**e:e+=1
    assert A<10**e and 2**501<10**151 and 4**5>10**3
    # It suffices to use n>=10^1000, far below exp(10^6).
    margin=1000*gap+300*S-151-500*d*e
    assert margin>0
    assert 10**1000>2*h*561*d and 10**1000>2*h*i*d
    # Prop6.1 P>Z^(5/3) gives intermediate comparison.
    prop_gap=5*d-3*D
    assert 4**(3*S)*(10**87)**prop_gap>16*A**(3*d)
    assert 10**87>2*h*5*d and 10**87>2*h*i*d
    return dict(i=i,h=h,m=len(ps),d=d,S=S,D=D,
                tail_product_exponent='561/500',tail_numeric_cutoff_power=1000,
                tail_decimal_margin=margin,
                intermediate_product_exponent='5/3',intermediate_cutoff=10**87,
                intermediate_integer_comparison=True)


def main():
    if not __debug__:
        raise RuntimeError('Assertions required.')
    anchors=[certify(r) for r in ANCHORS]
    branch_bounds=(913+337,337+329+265+191,
                   337+329+227+98+196,337+329+227+199+191)
    assert branch_bounds==(1250,1122,1187,1283)
    comparisons=[tail_comparison(i) for i in (22,25)]
    finite_path=ROOT/'data/results/verification_bft_i22_i25_finite_dependency_2026_10_04.json'
    finite=json.loads(finite_path.read_text(encoding='utf-8'))
    assert finite['status']=='PASS' and finite['indices']==[22,25]
    assert finite['finite_bound']==10**87
    assert finite['exhaustive_targeted_replay']
    assert finite['archived_hashes_preserved']==40
    for r in finite['rows']:
        assert r['initial_cap']==10**87 and r['final_cap']<2_000_000
        assert r['prefix']['upper']==1_999_999
    output=dict(status='passed',scope='Exact BFT tail and intermediate interval for i22/i25; combine with separately replayed n<=10^87 input',
                indices=[22,25],pair_graph_exponent='561/500',analytic_branch_bounds=list(branch_bounds),
                exact_rational_interval_bits=128,anchors=anchors,comparisons=comparisons,
                source_url='https://people.math.sc.edu/filaseta/papers/BFTpaper0207.pdf',
                external_dependencies=['BFT Proposition 5.1','BFT Theorem 2.4 and Section 7 proof','BFT Proposition 6.1'],
                source_typo='Last display of Theorem 2.4 repeats x1; Section 7 explicitly defines x=min(p^k*x1,q^l*x2) and proves the bound for it',
                external_theorems_reproved=False,finite_dependency_replay_pending=False,
                finite_dependency_replay_result=str(finite_path.relative_to(ROOT)),
                exact_all_n_indices_added=[22,25])
    dest=ROOT/'data/results/verification_bft_newvertex_i22_i25_2026_10_04.json'
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
