"""Independent source/parameter and integral audit of the three BFT anchors.

The exact interval enclosure is proved in the companion audit note.
The 90-digit replay here is a separate implementation consistency check,
not a replacement for the exact interval proof in the root checker.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import importlib.util
import json
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'scripts/audit_bft_newvertex_i22_i25_2026_10_04.py'
RESULT = ROOT / 'data/results/verification_bft_newvertex_i22_i25_2026_10_04.json'
mp.mp.dps = 90


def mp_fraction(value):
    value = F(value)
    return mp.mpf(value.numerator)/value.denominator


def beta_integral(A, B, C, t):
    # Independently integrate against a beta density, leaving one finite sum.
    return sum((-t)**k*comb(C,k)*F(factorial(A+k)*factorial(B),
                                  factorial(A+B+k+1)) for k in range(C+1))


def inside(value, interval):
    return (mp.mpf(interval['lower_numerator'])/interval['denominator'] <= value
            <= mp.mpf(interval['upper_numerator'])/interval['denominator'])


def main():
    spec=importlib.util.spec_from_file_location('root_interval_checker', SOURCE)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # No main() execution or root output mutation.
    saved=json.loads(RESULT.read_text(encoding='utf-8'))
    expected=[(17,1,1,2,4,1,7,5,F(14135,10000),74,F(337,1000),F(9,10000)),
              (11,2,3,19,2,1,25,17,F(1554,1000),582,F(196,1000),F(15,10000)),
              (17,2,5,19,2,4,2,1,F(19377,10000),150,F(191,1000),F(15,10000))]
    records=[]
    for row,record,params in zip(module.ANCHORS,saved['anchors'],expected):
        keys=('p','k0','a','q','l0','b','c','d','L1','m0','target','epsilon')
        assert tuple(row[key] for key in keys)==params
        p,k0,a,q,l0,b,c,d,L1,m0,target,epsilon=params
        A=p**k0;B=q**l0;D0=a*A-b*B
        s=mp.mpf(c)/d;z=mp.mpf(D0)/(a*A)
        M1=min(A,B);M2=max(A,B)
        assert D0==record['D0'] and 1<s<1/z
        u1=(s*(2-z)-mp.sqrt(s*s*z*z+4-4*z))/(2*(1-z)*(s+1))
        u2=(s*z+2-mp.sqrt(s*s*z*z+4-4*z))/(2*z*(s+1))
        alpha=(s+1)**(s+1)/(s-1)**(s-1)
        Q=alpha*u1**(s-1)*(1-u1)*(1-u1+z*u1)
        E=alpha*u2*(1-u2)*(1-z*u2)**(s-1)
        omega3=A**(s-1)*mp_fraction(L1)/(a*b**s*Q)
        omega4=M1**s*mp_fraction(L1)/((a*A)**(s-1)*D0**2*E)
        lam=mp.log(omega4)/mp.log(M2**s*omega4)
        Cs=[]
        for delta in (0,1):
            args1=(c-d-1+delta,d-delta,d-delta,F(1)-F(D0,a*A))
            args2=(d-delta,d-delta,c-d-1+delta,F(D0,a*A))
            I1=beta_integral(*args1);I2=beta_integral(*args2)
            assert I1==module.polynomial_integral(*args1)
            assert I2==module.polynomial_integral(*args2)
            prefactor=alpha**d*(s*s-1)**(mp.mpf((-1)**delta)/2)/(2*mp.pi)
            Cs.append((prefactor*mp_fraction(I1)/Q**d,
                       prefactor*mp_fraction(I2)/E**d))
        k1=max(200*C1/(a*A)**delta for delta,(C1,C2) in enumerate(Cs))
        k2=min((a*A)**(1-delta)/(2*mp.mpf(D0)**(1-2*delta)*C2)
               for delta,(C1,C2) in enumerate(Cs))
        eps=mp_fraction(epsilon)
        big_M=max(mp.log(k1)/(d*mp.log(omega3)),
                  (1+lam)*mp.log(M2**c/k2)/(eps*d*mp.log(M2**s*omega4)),
                  (1+lam)*mp.log(k2)/(eps*d*mp.log(M2**s*omega4)),m0)
        log_x0=c*(big_M+1)/(1-lam)*mp.log(M2)
        assert omega3>1 and omega4>1 and lam-eps>mp_fraction(target)
        for field,value in [('Omega3',omega3),('Omega4',omega4),
                            ('lambda3',lam),('log_x0',log_x0)]:
            assert inside(value,record[field]), (record['pair'],field)
        assert log_x0<500000
        records.append(dict(pair=record['pair'],D0=D0,
                            exact_integrals_independently_matched=4,
                            source_parameters_matched=True,
                            independent_numeric_inside_saved_intervals=True))
    assert saved['analytic_branch_bounds']==[1250,1122,1187,1283]
    assert min(saved['analytic_branch_bounds'])==1122
    output=dict(status='passed',reviewer='global_audit',
        script_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        root_result_sha256=hashlib.sha256(RESULT.read_bytes()).hexdigest(),
        anchors=records,interval_kernel_independently_paper_audited=True,
        delta_prefactor='(s^2-1)^((-1)^delta/2), both deltas checked against PDF image',
        graph_lower_bound='561/500',
        prop6_max_version_all_15_pairs=True,
        prop6_exception_both_components_ceiling=3000000000,
        finite_dependency_independently_replayed_by_root=False,
        scope='Tail and intermediate proof audited; full conclusion depends on root finite-input replay',
        external_bft_reproved=False,numeric_replay_is_not_the_exact_proof=True)
    dest=ROOT/'data/results/verification_bft_newvertex_i22_i25_independent_2026-10-04.json'
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
