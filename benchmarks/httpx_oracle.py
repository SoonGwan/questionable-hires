#!/usr/bin/env python3
"""Independent mutation oracle; never give its expected results to evaluated agents."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

REVISION = '26d48e0634e6ee9cdc0533996db289ce4b430177'
FAULTS = {
    'wsgi-cleanup': ('httpx/_transports/wsgi.py', '            self._close()', '            pass', 'tests/test_wsgi.py'),
    'asgi-head': ('httpx/_transports/asgi.py', 'if body and request.method != "HEAD":', 'if body:', 'tests/test_asgi.py'),
    'asgi-exceptions': ('httpx/_transports/asgi.py', 'if self.raise_app_exceptions:', 'if False:', 'tests/test_asgi.py'),
}


def run(python, project, test):
    result = subprocess.run([str(python), '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', test], cwd=project,
                            text=True, capture_output=True, timeout=60)
    return dict(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--python', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    if revision != REVISION or subprocess.check_output(['git', 'status', '--porcelain'], cwd=source, text=True).strip():
        raise ValueError('Expected clean pinned upstream checkout')
    if args.output.exists():
        raise FileExistsError(args.output)
    records = {}
    with tempfile.TemporaryDirectory(prefix='qh-httpx-oracle-') as directory:
        for name, (filename, before, after, test) in FAULTS.items():
            project = Path(directory) / name
            shutil.copytree(source, project, ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache'))
            baseline = run(args.python, project, test)
            if baseline['exit_code'] != 0:
                raise RuntimeError(f'{name}: baseline is not green: {baseline}')
            target = project / filename
            original = target.read_text()
            if original.count(before) != 1:
                raise ValueError(f'{name}: mutation must match exactly once')
            target.write_text(original.replace(before, after))
            mutant = run(args.python, project, test)
            records[name] = dict(baseline=baseline, mutant=mutant, file=filename, before=before, after=after)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as handle:
        json.dump(dict(revision=revision, records=records, limitation='Suite sensitivity only; surviving faults require independent reachable-behavior witnesses before a coverage claim.'), handle, indent=2)
    for name, record in records.items():
        print(name, 'baseline', record['baseline']['exit_code'], 'mutant', record['mutant']['exit_code'])


if __name__ == '__main__':
    main()
