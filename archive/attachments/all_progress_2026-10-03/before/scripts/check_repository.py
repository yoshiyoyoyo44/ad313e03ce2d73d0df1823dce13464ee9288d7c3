"""Check navigation, artifact preservation, and optional isolated smoke runs."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

from repo_paths import ROOT, artifact_path


def check_layout():
    manifest = json.loads((ROOT/'archive/reorganization_2026-09-21.json').read_text(encoding='utf-8'))
    preserved = 0
    for entry in manifest['files']:
        path = ROOT/entry['new']
        assert path.is_file(), entry['new']
        assert artifact_path(entry['old']).resolve() == path.resolve(), entry['old']
        if entry['preserve_bytes']:
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256_before'], entry['new']
            preserved += 1
    python_files = list((ROOT/'scripts').glob('*.py'))
    for path in python_files:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    for path in (ROOT/'data').rglob('*.json'):
        json.loads(path.read_text(encoding='utf-8'))

    # Raw sources/snapshots intentionally preserve historical links. Their
    # index pages and the complete old-to-new lookup are checked separately.
    documents = [ROOT/'README.md']
    documents += list((ROOT/'docs').glob('*.md'))
    documents += list((ROOT/'research').rglob('*.md'))
    documents += [ROOT/name/'README.md' for name in ('scripts','data','magma','formal','sources','archive')]
    documents += [ROOT/'archive/FILE_MAP.md']
    documents += [ROOT/'archive/attachments/incoming_2026-09-26/README.md']
    documents += [ROOT/'archive/attachments/incoming_2026-09-27/README.md']
    broken, links, commands = [], 0, 0
    for path in documents:
        text = path.read_text(encoding='utf-8')
        without_code = re.sub(r'```.*?```', '', text, flags=re.S)
        for match in re.finditer(r'\]\(([^\s)]+)\)', without_code):
            target = match[1]
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith('#'):
                continue
            resolved = (path.parent/unquote(parsed.path)).resolve()
            if not resolved.exists():
                broken.append(f'{path.relative_to(ROOT)} -> {target}')
            links += 1
        for match in re.finditer(r'\bpython(?:3)?(?: -X utf8)? ([\w/]+\.py)\b', text):
            if not (ROOT/match[1]).is_file():
                broken.append(f'{path.relative_to(ROOT)} command -> {match[1]}')
            commands += 1
        assert r'\[' not in without_code and r'\(' not in without_code, f'Old math delimiter: {path}'
    assert not broken, '\n'.join(broken)
    from replay_september26_attachments import check_hashes
    new_originals, package_hash_entries = check_hashes()
    from audit_handoff_integration_2026_09_26 import check_source_hashes
    handoff_originals = check_source_hashes()
    from replay_september27_attachments import check_hashes as check_september27_hashes
    september27_preserved = check_september27_hashes()
    extension = ROOT/'data/certificates/weighted_cover_2026-09-26'
    extension_manifest = json.loads((extension/'manifest.json').read_text())
    for name, digest in extension_manifest['files'].items():
        assert hashlib.sha256((extension/name).read_bytes()).hexdigest() == digest, name
    return {'legacy_paths': len(manifest['files']), 'byte_preserved_files': preserved,
            'new_original_attachments': new_originals,
            'additional_handoff_originals': handoff_originals,
            'september27_preserved': september27_preserved,
            'new_package_hash_entries': package_hash_entries,
            'extension_certificate_hashes': len(extension_manifest['files']),
            'python_files_parsed': len(python_files), 'documents_checked': len(documents),
            'local_links_checked': links, 'script_commands_checked': commands}


def smoke():
    # A disposable copy keeps historical outputs and hashes unchanged.
    temp_parent = Path(tempfile.gettempdir()).resolve()
    temp = Path(tempfile.mkdtemp(prefix='erdos699-layout-', dir=temp_parent)).resolve()
    assert temp.parent == temp_parent and temp.name.startswith('erdos699-layout-')
    runs = []
    try:
        for name in ('scripts', 'data', 'magma'):
            shutil.copytree(ROOT/name, temp/name, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        (temp/'archive').mkdir()
        shutil.copy2(ROOT/'archive/reorganization_2026-09-21.json', temp/'archive')
        # Mix cwd values to exercise resolution independent of the shell's cwd.
        cases = [
            ('audit_i3_irreducible_cubic_and_rational_gaps.py', [], temp),
            ('audit_i3_dyadic_denominators_and_continued_fractions.py', [], temp/'scripts'),
            ('audit_i3_2adic_square.py', [], temp),
            ('replay_critical_indices.py', [], temp/'scripts'),
            ('audit_i3_center_curve.py', [], temp),
            ('audit_i3_fixed_blocks.py', [], temp/'scripts'),
            ('replay_i3_gap13.py', [], temp),
            ('replay_certificate.py', ['i3_original_replay.json','--output','verification_layout_smoke.json'], temp),
        ]
        for script, args, cwd in cases:
            result = subprocess.run([sys.executable, '-X', 'utf8', str(temp/'scripts'/script), *args],
                                    cwd=cwd, capture_output=True, text=True, encoding='utf-8', timeout=90)
            assert result.returncode == 0, f'{script}\n{result.stdout[-2500:]}\n{result.stderr}'
            print(f'PASS {script}', flush=True)
            runs.append(script)
        assert not list(temp.glob('verification_*.json')), 'Output leaked to root'
        assert not list((temp/'scripts').glob('verification_*.json')), 'Output leaked to scripts'
    finally:
        # Verify the absolute target before recursive cleanup on Windows.
        assert temp.resolve().parent == temp_parent and temp.name.startswith('erdos699-layout-')
        shutil.rmtree(temp)
    return runs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    result = check_layout()
    if args.smoke:
        result['isolated_smoke_runs'] = smoke()
        check_layout()
    print(json.dumps({'status':'passed', **result}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
