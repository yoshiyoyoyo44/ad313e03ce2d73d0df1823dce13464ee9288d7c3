"""Run every independent checker with assertions enabled."""
from pathlib import Path
import subprocess,sys,json,hashlib
ROOT=Path(__file__).resolve().parent
if not __debug__:raise RuntimeError('Do not use python -O.')
for name in ['verify_spacing.py','enumerate_pairs.py','verify_finite.py',
             'verify_product_bootstrap.py','verify_prefix.py']:
    subprocess.run([sys.executable,str(ROOT/name)],check=True,cwd=ROOT)
print('All five verification stages completed. See REPORT.md for scope and external inputs.')
