"""Independent symbolic diagnostics for the coefficient-unbounded proof.
Finite numeric cases are diagnostics, not completeness evidence.
"""
import json
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
import sympy as S

if not __debug__:
 raise RuntimeError('Run without -O.')

Y,X,h,a,b,c,k,l=S.symbols('Y X h a b c k l')
reports=[]
for t in map(S.Rational,[S.Rational(1,5),S.Rational(2,5),S.Rational(3,5)]):
 z=1-3*t
 U=a*Y**2+b*Y+c
 kval=(a*c-b*b)/a**2
 lval=-b*c/a**2
 D=Y/a-b/a**2
 assert S.expand(Y**3+kval*Y+lval-U*D)==0
 U0=a*Y**2-Y/z-1/(a*z*z)
 k0=-2/(a*a*z*z);l0=-1/(a**3*z**3)
 assert S.expand(Y**3+k0*Y+l0-U0*(Y/a+1/(a*a*z)))==0
 assert S.rem(Y/a+1/(a*a*z)-z*Y**2,U0,Y)==0
 discriminants=[]
 for s in range(3):
  r=s-1-t; disc=S.factor((1+z/r)**2+4)
  discriminants.append(str(disc))
  num,den=map(int,S.fraction(disc));sq=isqrt(num)**2==num and isqrt(den)**2==den
  assert sq==(s==3-5*t)
 U0=S.expand(U0.subs(a,1/z**2));k0=k0.subs(a,1/z**2);l0=l0.subs(a,1/z**2)
 P=S.prod(Y-(s-1-t)*U0 for s in range(3))
 C=S.cancel((Y*P/(k0*Y+l0)+U0+Y)/U0**2)
 assert S.denom(C)==1 or S.denom(C).is_number
 assert S.degree(C,Y)==2
 V=S.cancel((U0*C-1)/Y)
 F=S.expand(1+U0*V);J=S.expand(1+V*(t*U0+Y))
 assert S.expand(Y*P-(k0*Y+l0)*(U0**2*C-U0-Y))==0
 assert S.cancel(J*(J-1)/(F-1)).is_polynomial(Y)
 assert S.cancel(J*(J-1)*(J-2)/(F-2)).is_polynomial(Y)
 Fw=S.expand(F.subs(Y,z*(2+X)));Jw=S.expand(J.subs(Y,z*(2+X)))
 reports.append({'t':str(t),'discriminants':discriminants,'F':str(Fw),'J':str(Jw)})
 if t==S.Rational(1,5):
  f=S.expand(Fw.subs(X,10*h));j=S.expand(Jw.subs(X,10*h))

assert f==150000*h**5+125000*h**4+35000*h**3+3750*h**2+125*h+2
assert j==30000*h**5+31000*h**4+11400*h**3+1770*h**2+105*h+2
factors={
 'f-1':(100*h**2+30*h+1)*(1500*h**3+800*h**2+95*h+1),
 'f-2':125*h*(20*h**2+10*h+1)*(60*h**2+20*h+1),
 'j':(5*h+2)*(100*h**2+30*h+1)*(60*h**2+20*h+1),
 'j-1':(20*h**2+10*h+1)*(1500*h**3+800*h**2+95*h+1),
 'j-2':5*h*(6000*h**4+6200*h**3+2280*h**2+354*h+21),
}
for name,fac in factors.items():
 target={'f-1':f-1,'f-2':f-2,'j':j,'j-1':j-1,'j-2':j-2}[name]
 assert S.expand(target-fac)==0
A=210000*h**4+169000*h**3+42200*h**2+3550*h+107
B=-1050000*h**4-635000*h**3-105000*h**2-5250*h-95
assert S.expand(A*f+B*j)==24
assert f.subs(h, -S.Rational(1,4)) == S.Rational(3,64)
assert j.subs(h, -S.Rational(1,4)) == S.Rational(3,64)
assert S.expand(64*f-3-125*(4*h+1)*(19200*h**4+11200*h**3+1680*h**2+60*h+1)) == 0
assert all(int(coef)%2==0 for coef in S.Poly(S.diff(f,h)-1,h).all_coeffs())
K=6000*h**4+6200*h**3+2280*h**2+354*h+21
assert [r for r in range(25) if int(K.subs(h,r))%25==0]==[6]
assert all(int(coef)%3125==0 for coef in S.Poly(f-(625*(h**3+h**2)+125*h+2),h).all_coeffs())
assert [int(f.subs(h,6+25*r))%3125 for r in range(125)]==[2002]*125
assert pow(2,601,3125)==2002 and 3*pow(2,2494,3125)%3125==2002
assert pow(2,2500,3125)==1 and all(pow(2,2500//q,3125)!=1 for q in [2,5])
assert [r for r in range(3) if int(f.subs(h,r))%3==0]==[2]
assert all(int(coef)%27==0 for coef in S.Poly(S.expand(f.subs(h,2+3*X)-3),X).all_coeffs())
assert [r for r in range(7500) if r%2500==2494 and r%6==0]==[7494]
assert pow(2,6,9)==1 and all(pow(2,r,9)!=1 for r in range(1,6))
q1=S.cancel(j*(j-1)/(f-1))
q2=S.cancel(6*j*(j-1)*(j-2)/(f-2))
assert q1.is_polynomial(h)
assert S.expand(q2-6*(5*h+2)*(100*h**2+30*h+1)*(1500*h**3+800*h**2+95*h+1)*K/25)==0

def v(n,p):
 e=0
 while n and n%p==0:n//=p;e+=1
 return e

def kummer(n,j,p):
 total=0;pk=p
 while pk<=n:
  total+=int(j%pk>n%pk);pk*=p
 return total

numeric=10000;exceptional=[]
for r in range(1,numeric+1):
 n=150000*r**5+125000*r**4+35000*r**3+3750*r**2+125*r+2
 jj=30000*r**5+31000*r**4+11400*r**3+1770*r**2+105*r+2
 assert gcd(n,jj) in (1,2,3,4,6,8,12,24)
 assert v(n-2,5)==3+v(r,5)
 assert (6*jj*(jj-1)*(jj-2)%(n-2)==0)==(r%25==6)
 if r%25!=6:assert kummer(n,jj,5)>0
 elif kummer(n,jj,5)==0:exceptional.append(r)

result={'status':'passed','branches':reports,'factorizations':len(factors),'numeric_evaluations':numeric,
 'denominator25_exception_modulus':25,'denominator25_exception_residue':6,
 'no_base5_carry_exceptions_in_numeric_range':exceptional,
 'pure_power_exponent_modulus':2500,'pure_power_exponent_residues':{'M1':601,'M3':2494},'M3_refined_exponent_modulus':7500,'M3_refined_exponent_residue':7494,
 'gcd_bound':24,'M3_rational_local_point':['-1/4','3/64'],
 'finite_congruence_obstruction_proved_in_note':True,'complete_solution_claimed':False}
path=Path(__file__).resolve().parent.parent/'data/results/verification_i3_quintic_digit_classification.json';path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
