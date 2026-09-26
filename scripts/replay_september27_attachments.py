"""Replay the September 27 package in an isolated copy, preserving originals."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'archive/attachments/incoming_2026-09-27'
PACKAGE = ARCHIVE / 'erdos699_continuation'
STAGES = [
    ('verify_spacing.py', 'spacing_verification.json'),
    ('enumerate_pairs.py', 'pairs_verification.json'),
    ('verify_finite.py', 'finite_verification.json'),
    ('verify_product_bootstrap.py', 'product_bootstrap_verification.json'),
    ('verify_prefix.py', 'prefix_verification.json'),
]


def check_hashes():
    originals = json.loads((ARCHIVE / 'import_manifest.json').read_text(encoding='utf-8'))
    for entry in originals:
        raw = (ARCHIVE / entry['saved_name']).read_bytes()
        assert len(raw) == entry['bytes']
        assert hashlib.sha256(raw).hexdigest() == entry['sha256']
    entries = json.loads((PACKAGE / 'SHA256.json').read_text(encoding='utf-8'))
    for name, digest in entries.items():
        assert hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest() == digest, name
    with zipfile.ZipFile(ARCHIVE / originals[1]['saved_name']) as archive:
        for entry in archive.infolist():
            assert archive.read(entry) == (ARCHIVE / entry.filename).read_bytes()
        zip_entries = len(archive.infolist())
    provenance = json.loads((PACKAGE / 'provenance.json').read_text(encoding='utf-8'))
    for entry in provenance['git_blob_map']:
        raw = (PACKAGE / entry['local']).read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert digest == entry['git_blob_sha'], entry['local']
    return dict(originals=len(originals), package_hashes=len(entries),
                zip_entries=zip_entries, baseline_git_blobs=len(provenance['git_blob_map']))


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: assertions are part of the verification.')
    preserved = check_hashes()
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='september27-', dir=dist)).resolve()
    stages = []
    outputs = {}
    try:
        shutil.copytree(PACKAGE, work, dirs_exist_ok=True)
        with (dist / 'september27-last-replay.log').open('w', encoding='utf-8') as log:
            for script, output_name in STAGES:
                completed = subprocess.run(
                    [sys.executable, '-X', 'utf8', '-u', str(work / script)],
                    cwd=work, capture_output=True, text=True, encoding='utf-8',
                )
                log.write(f'\n{script}\n{completed.stdout}\n{completed.stderr}')
                log.flush()
                if completed.returncode:
                    raise RuntimeError(f'{script} failed; see dist/september27-last-replay.log')
                result = json.loads((work / output_name).read_text(encoding='utf-8'))
                saved = json.loads((PACKAGE / output_name).read_text(encoding='utf-8'))
                assert result == saved, output_name
                outputs[script] = result
                stages.append(dict(script=script, output=output_name,
                                   matches_archived_result=True))
                print(f'PASS {script}: full replay matches archived result', flush=True)
    finally:
        # Check the absolute target before recursive cleanup on Windows.
        assert work.parent == dist.resolve() and work.name.startswith('september27-')
        shutil.rmtree(work)
    assert check_hashes() == preserved
    finite = outputs['verify_finite.py']
    product = outputs['verify_product_bootstrap.py']
    prefix = outputs['verify_prefix.py']
    result = dict(
        status='PASS', preserved=preserved, stages=stages,
        all_n_indices=[28, 31, 34], finite_bound=10**87,
        finite_indices=[row['i'] for row in product['rows']],
        spacing_prime_pairs=outputs['verify_spacing.py']['prime_pairs'],
        close_pair_maximum=outputs['enumerate_pairs.py']['merge']['maximum'],
        middle_intervals=sum(row['intervals'] for row in finite['middle']),
        small_exceptions=finite['small']['exception_count'],
        bootstrap_steps=sum(row['steps'] for row in product['rows']),
        exact_binomial_checks=sum(row['exact_binomial_checks'] for row in product['rows']),
        prefix_intervals=prefix['interval_count'], prefix_singletons=prefix['singleton_count'],
        external_theorem='Matveev (2000), Corollary 2.3; paper proof remains an input',
        independent_peer_review=False, formal_lean_verification=False,
    )
    target = ROOT / 'data/results/verification_september27_attachments.json'
    target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
