"""Independent lambda-first replay of the degree-one linear-quotient certificate."""
from math import isqrt
import json
from pathlib import Path


def main():
    root_rows = parameter_rows = 0
    candidates = []
    for b in range(2,7):
        for N in range(1,4):
            for h in (1,2):
                for g in (0,1):
                    d = 2-g
                    target = d*b**(N+1)
                    divisors = []
                    for t in range(1,isqrt(target)+1):
                        if target % t == 0:
                            divisors.append(t)
                            if t*t != target:
                                divisors.append(target//t)
                    for t in divisors:
                        v = t-h*b
                        if v < h:
                            continue
                        root_rows += 1
                        a_min = max(b+2,v//h+1)
                        ell_max = (3*h*v-1)//b
                        # This replay enumerates lambda and q, then solves ell.
                        for lam in range(1,(6*v-1)//b+1):
                            denominator = 6*v-b*lam
                            q_max = (lam+6*h+d*ell_max)//denominator
                            q_min = a_min*b+1
                            q_min += 1-q_min%2
                            for q in range(q_min,q_max+1,2):
                                numerator = denominator*q-lam-6*h
                                if numerator % d:
                                    continue
                                ell = numerator//d
                                if not (1 <= ell <= ell_max):
                                    continue
                                a_max = min((q-1)//b,(3*v*v-1)//(b*ell))
                                for a in range(a_min,a_max+1):
                                    parameter_rows += 1
                                    E = 1+b*q
                                    assert lam*E == 6*v*q-6*h-d*ell
                                    P = (a*q-1)*E
                                    R = v*q-h
                                    T = 3*R*R-ell*P
                                    V = 6*P+ell-9*R
                                    assert V > 0
                                    if T == 0 or V % T:
                                        continue
                                    Q = V//T
                                    if Q > q and Q % q == 1:
                                        candidates.append((b,N,h,g,v,lam,q,ell,a,Q))
    assert root_rows == 297
    assert parameter_rows == 596
    assert not candidates
    result = dict(status='passed',method='lambda-first independent replay',
                  root_parameter_rows=root_rows,integer_parameter_rows=parameter_rows,
                  admissible_integer_Q_values=0,
                  scope='Conditional degree-one E linear J-2 quotient finite certificate; not general i=3.')
    output = Path(__file__).resolve().parents[1]/'data/results/verification_i3_linear_J2_quotient_degree1_independent.json'
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
