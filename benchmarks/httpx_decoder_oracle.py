#!/usr/bin/env python3
"""Author-only decoder witnesses; never copy this into model-evaluated projects."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

FAULTS = {
    'text-finalization': ('return self.decoder.decode(b"", True)', 'return ""'),
    'line-crlf-split': ('text = "\\r" + text', 'text = "\\n" + text'),
}
IMPORT = '''import httpx, json
from pathlib import Path
assert Path(httpx.__file__).resolve().parent == Path.cwd() / 'httpx'
'''
SUITE = IMPORT + '''import pytest
raise SystemExit(pytest.main(['-q', '-p', 'no:cacheprovider', 'tests/test_decoders.py']))
'''
WITNESSES = {
    'text-finalization': IMPORT + '''
normal = ''.join(httpx.Response(200, content=iter([b'\\xe2', b'\\x82\\xac'])).iter_text())
observed = ''.join(httpx.Response(200, content=iter([b'\\xe2\\x82'])).iter_text())
print(json.dumps({'normal': normal, 'expected_normal': '€',
                  'observed': observed, 'expected': '\\ufffd'}), flush=True)
assert normal == '€', (normal, '€')
assert observed == '\\ufffd', (observed, '\\ufffd')
''',
    'line-crlf-split': IMPORT + '''
normal = list(httpx.Response(200, content=iter([b'a\\r\\nb\\r\\n'])).iter_lines())
observed = list(httpx.Response(200, content=iter([b'a\\r', b'\\nb\\r\\n'])).iter_lines())
print(json.dumps({'normal': normal, 'expected_normal': ['a', 'b'],
                  'observed': observed, 'expected': ['a', 'b']}), flush=True)
assert normal == ['a', 'b'], normal
assert observed == ['a', 'b'], observed
''',
}


def run(source, python):
    records = []
    for name, (before, after) in FAULTS.items():
        for mutant in (False, True):
            with tempfile.TemporaryDirectory(prefix='qh-decoder-oracle-') as tmp:
                project = Path(tmp) / 'httpx'
                shutil.copytree(source, project, ignore=shutil.ignore_patterns(
                    '.git', '__pycache__', '.pytest_cache', '*.pyc'))
                target = project / 'httpx/_decoders.py'
                contents = target.read_text()
                if contents.count(before) != 1:
                    raise ValueError('Expected exactly one selected mutation site')
                if mutant:
                    target.write_text(contents.replace(before, after))
                row = {'case': name, 'mutant': mutant}
                for phase, code in [('suite', SUITE), ('witness', WITNESSES[name])]:
                    result = subprocess.run([str(python), '-B', '-c', code], cwd=project,
                                            capture_output=True, text=True, timeout=30)
                    row[phase] = {'exit_code': result.returncode,
                                  'stdout': result.stdout.replace(str(project), '<COPY>'),
                                  'stderr': result.stderr.replace(str(project), '<COPY>')}
                records.append(row)
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x', encoding='utf-8') as stream:
        records = run(args.source.resolve(), args.python.absolute())
        json.dump(records, stream, indent=2)
        stream.write('\n')
    for row in records:
        print(row['case'], 'mutant' if row['mutant'] else 'correct',
              'suite', row['suite']['exit_code'], 'witness', row['witness']['exit_code'])
