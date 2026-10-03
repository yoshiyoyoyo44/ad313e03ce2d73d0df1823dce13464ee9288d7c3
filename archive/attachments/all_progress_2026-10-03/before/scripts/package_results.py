"""Package the current tracked tree, preserving its directory structure."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from zipfile import ZIP_DEFLATED, ZipFile

from repo_paths import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='dist/erdos699-current.zip')
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').rstrip('\0').split('\0')
    assert all((ROOT/name).is_file() for name in names)
    assert output.resolve() not in {(ROOT/name).resolve() for name in names}, 'Output would overwrite a tracked artifact'
    hashes = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for name in names:
            archive.write(ROOT/name, arcname=name)
        archive.writestr('SHA256.json', json.dumps(hashes, indent=2)+'\n')
    with ZipFile(output) as archive:
        assert archive.testzip() is None
        for name, expected in hashes.items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected
    print(f'{output}: {len(names)} files, SHA256 checked')


if __name__ == '__main__':
    main()
