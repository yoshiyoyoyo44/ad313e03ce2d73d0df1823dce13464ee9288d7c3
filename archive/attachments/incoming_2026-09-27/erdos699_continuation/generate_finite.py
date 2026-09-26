"""Reuse the frozen interval and Kummer generators on the three new indices."""
from pathlib import Path
import sys, json, gzip
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'frozen'))
import generate as intervals
import generate_small as small

INDICES=[28,31,34]
UPPER=4_209_368_355

def main():
    rows=[]
    for i in INDICES:
        a,b,d,S=intervals.parameters(i)
        out=intervals.generate_intervals(i,2_000_000,UPPER+1,d,S,intervals.primes(i))
        assert out is not None
        rows.append(dict(i=i,a=a,b=b,d=d,S=S,intervals=out))
        (ROOT/'finite_intervals.json').write_text(json.dumps(dict(schema=1,upper=UPPER,rows=rows),separators=(',',':'))+'\n')
    small.INDICES=INDICES
    small.ROOT=ROOT
    small.main()

if __name__=='__main__': main()
