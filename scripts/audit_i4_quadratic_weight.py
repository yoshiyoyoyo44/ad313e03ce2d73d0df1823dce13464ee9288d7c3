"""Audit the all-n quadratic weighted-product inequality, using exact integers.

This is a necessary-condition theorem, not a proof that i=4 is solved.
No bound on n, exponent search, or optimization solver is used in the proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]


def curve(s,u):
    return s*s-s*u+u*u-3*s+2


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    cells=[(s,u) for s in range(4) for u in range(s+1)]
    zeros=[p for p in cells if curve(*p)==0]
    assert zeros==[(1,0),(1,1),(2,0),(2,2),(3,1),(3,2)]
    row_weights=[6,6,4,3]
    records=[]
    for s,u in cells:
        weight=3*int(u==0)+2*int(u==1)+3*int(s-u==0)+2*int(s-u==1)+int((s,u) in zeros)
        assert weight==row_weights[s]
        records.append({'cell':[s,u],'multiplicity':weight})
    # F(n,j)>=3n^2/4-3n+2. At n=10+x this is 3x^2/4+12x+47.
    assert [F(3,4),F(12),F(47)]==[F(3,4),2*F(3,4)*10-3,F(3,4)*100-30+2]
    # With z=jy/n^2 in [0,1/4], z^5(1-z) increases:
    # its derivative is z^4(5-6z), with 5-6z>=7/2>0.
    assert 5-6*F(1,4)==F(7,2)
    assert F(1,4)**5*(1-F(1,4))==F(3,4096)
    # Explicit large-n cofactor bounds. 9,18,20,27,28 are direct residue
    # assumptions; a classification of all n is not an input to this audit.
    # Rows outside {0,qrow} have R_s=(n-s)/d_s.
    normalization={9:(1,{2:1,3:6}),28:(1,{2:2,3:1}),
                   18:(2,{1:1,3:3}),20:(2,{1:1,3:1}),27:(3,{1:2,2:1})}
    bounds={}
    N=10**87
    for cl,(qrow,ds) in normalization.items():
        C=F(3,4096)
        heavy_weight=0
        for s,d in ds.items():
            C*=d**row_weights[s]
            heavy_weight+=row_weights[s]
        # (n/(n-3))^heavy_weight < 2 for all n>=N by Bernoulli.
        assert N>6*heavy_weight
        bounds[cl]={'qrow':qrow,'R0_power':6,'Rq_power':row_weights[qrow],
                    'n_power':12-heavy_weight,'constant_before_correction':str(C),
                    'constant_valid_for_n_ge_1e87':str(2*C)}
    result={'status':'passed','scope':'all n>=10: weighted inequality necessary for an i=4 counterexample',
            'inequality':'4096*R0^6*R1^6*R2^4*R3^3 < 3*n^12',
            'hexagon':zeros,'cell_weights':records,'large_n_cofactor_bounds':bounds,
            'not_claimed':['all i=4 counterexamples excluded','any new index completely solved']}
    path=ROOT/'data/results/verification_i4_quadratic_weight.json'
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
