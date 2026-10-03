"""Audit the fetched GitHub baseline against its local Git object and tracked tree.

The snapshot was read with the GitHub plugin. This script does not access the
network. Run in a development checkout with Git objects; a distributable ZIP
instead has its complete SHA256 manifest and BUILD_METADATA.
"""

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT/'data/results/verification_github_baseline_2026-10-03.json'


def git(*arguments):
    return subprocess.check_output(['git', *arguments], cwd=ROOT)


def main():
    snapshot = json.loads((ROOT/'sources/github699_baseline_snapshot_2026-10-03.json').read_text())
    baseline = snapshot['commit']
    assert git('rev-parse', f'{baseline}^{{tree}}').decode().strip() == snapshot['tree']
    assert git('rev-parse', f'{baseline}:README.md').decode().strip() == snapshot['readme']['blob_sha']
    assert git('show', f'{baseline}:README.md') == snapshot['readme']['content'].encode('utf-8')
    subprocess.run(['git', 'merge-base', '--is-ancestor', baseline, 'HEAD'], cwd=ROOT, check=True)
    tracked = set(git('ls-files', '-z').decode().rstrip('\0').split('\0'))
    assert OUTPUT.relative_to(ROOT).as_posix() in tracked
    original, changed = [], []
    for entry in git('ls-tree', '-r', '-z', baseline).rstrip(b'\0').split(b'\0'):
        meta, path_bytes = entry.split(b'\t', 1)
        path = path_bytes.decode('utf-8')
        mode, kind, expected_blob = meta.decode().split()
        assert kind == 'blob' and path in tracked and (ROOT/path).is_file(), path
        content = (ROOT/path).read_bytes()
        actual_blob = hashlib.sha1(f'blob {len(content)}\0'.encode()+content).hexdigest()
        record = {'path': path, 'baseline_blob': expected_blob, 'current_blob': actual_blob}
        (original if actual_blob == expected_blob else changed).append(record)
    baseline_paths = {r['path'] for r in original+changed}
    assert len(baseline_paths) == 504
    added = sorted(tracked-baseline_paths)
    commits = git('log', '--reverse', '--format=%H%x09%s', f'{baseline}..HEAD').decode().splitlines()
    result = {
        'status': 'passed', 'repository': snapshot['repository'], 'checked_at': snapshot['checked_at_utc'],
        'baseline_commit': baseline, 'baseline_tree': snapshot['tree'], 'baseline_readme_bytes_match': True,
        'all_504_baseline_paths_present': True, 'baseline_file_count': len(baseline_paths),
        'tracked_working_file_count': len(tracked), 'byte_identical_baseline_files': len(original),
        'updated_baseline_files': changed, 'added_file_count': len(added), 'added_files': added,
        'additional_commits_before_this_package_update': commits,
        'scope': 'complete tracked working files, including staged package update; final package commit is in BUILD_METADATA.json',
        'external_writes': False,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'baseline_file_count', 'tracked_working_file_count',
                                           'byte_identical_baseline_files', 'added_file_count')}, indent=2))


if __name__ == '__main__':
    main()
