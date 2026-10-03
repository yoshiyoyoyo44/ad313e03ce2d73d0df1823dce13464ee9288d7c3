"""Verify the received October 3 package, backups, and optional import snapshot."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / 'archive/attachments/all_progress_2026-10-03'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(relative):
    name = PurePosixPath(relative)
    assert not name.is_absolute() and '..' not in name.parts
    assert not any(':' in part or '\\' in part for part in name.parts)
    result = (ROOT / relative).resolve()
    assert result.is_relative_to(ROOT)
    return result


def check_hashes(verify_working_tree=True):
    if not __debug__:
        raise SystemExit('Assertions must be enabled: do not use python -O.')
    manifest = json.loads((ARCHIVE / 'import_manifest.json').read_text(encoding='utf-8'))
    package = ARCHIVE / manifest['source_zip']
    assert package.stat().st_size == manifest['source_zip_bytes']
    assert digest(package) == manifest['source_zip_sha256']
    expected = json.loads((ARCHIVE / 'SHA256.json').read_text(encoding='utf-8'))
    entries = manifest['entries']
    assert len(expected) == manifest['source_manifest_hash_count'] == 665
    assert len(entries) == manifest['source_entry_count'] == 666
    assert len({entry['source_path'] for entry in entries}) == len(entries)
    backups = working_files = 0
    with ZipFile(package) as received:
        assert len(received.namelist()) == len(set(received.namelist())) == 666
        assert set(received.namelist()) == {entry['source_path'] for entry in entries}
        for entry in entries:
            content = received.read(entry['source_path'])
            assert len(content) == entry['source_bytes']
            assert hashlib.sha256(content).hexdigest() == entry['source_sha256'], entry['source_path']
            if entry['source_path'] in expected:
                assert entry['source_sha256'] == expected[entry['source_path']]
            if entry['backup_path']:
                assert digest(safe_path(entry['backup_path'])) == entry['before_sha256']
                backups += 1
            target = safe_path(entry['target_path'])
            if verify_working_tree or target.is_relative_to(ARCHIVE):
                assert digest(target) == entry['integrated_sha256'], entry['target_path']
                working_files += 1
        assert received.read('SHA256.json') == (ARCHIVE / 'SHA256.json').read_bytes()
        assert received.read('BUILD_METADATA.json') == (ARCHIVE / 'BUILD_METADATA.json').read_bytes()
    assert backups == 13
    return {'zip_entries': len(entries), 'source_manifest_hashes': len(expected),
            'backups_verified': backups, 'integrated_files_verified': working_files,
            'working_tree_snapshot_checked': verify_working_tree}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-only', action='store_true',
                        help='Verify immutable received files and backups after further edits.')
    args = parser.parse_args()
    print(json.dumps({'status': 'passed', **check_hashes(not args.source_only)}, indent=2))


if __name__ == '__main__':
    main()
