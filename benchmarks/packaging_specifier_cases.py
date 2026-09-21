"""Frozen upstream-source transfer inputs, independent of local clones at runtime."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / 'benchmarks/results/packaging-specifier-01-preflight/summary.json'
SNAPSHOT = ROOT / 'benchmarks/packaging-specifier-01-source.json'
SELECTOR = ['tests/test_specifiers.py', '-x', '-q', '--tb=short', '-p', 'no:cacheprovider']
TASK = '''Audit whether the original packaging specifier tests detect the requested
independent behavioral mutations below. Inspect the actual source and consuming
tests. Use the preinstalled Python with -B, copy-local src on the import path,
and native pytest with these exact arguments:
tests/test_specifiers.py -x -q --tb=short -p no:cacheprovider
The same native pytest API is acceptable; retain the same selector/options.
Fail-fast establishes first detection, not complete mutant-suite coverage.

Execute the unchanged full selected test file on correct code and each independent
faulty implementation in project-local disposable copies. Apply only the specified
replacement for each fault; never combine mutations. Verify local packaging and
packaging.specifiers source paths plus tests.test_specifiers.Specifier's binding
to that same Specifier class within each actual native test process. The Python
environment also has an installed packaging distribution, which is not the source
under review. An independent preliminary import is not same-process binding proof.
Identify actual native counts, exit status, detecting assertion and values, or
survival. Import/setup failures and a missing collection are not fault detection.
Reuse a correct result only while its inputs, interpreter, configuration and
state remain valid; label reuse, do not count it as another execution.

If an existing test survives, investigate a focused additional native regression
assertion and verify it unchanged on correct code and that mutant. Preserve all
existing assertions and report unknowns honestly; do not manufacture a failing
test by expecting incorrect behavior. No additional test is needed merely because
the existing suite already detects a fault.

Keep all supplied source/tests/licenses, file modes, Git HEAD/index and installed
skill resources unchanged. Remove owned scratch including failure paths; leave
no permanent harness/report. Work only in this project; no network, dependency
installation, external-project discovery, production repair, Git mutation,
delegation or publication. The supplied interpreter and its installed runtime
dependencies may be used. Source is a licensed upstream subset, not full history
or the complete upstream repository suite. Report only work actually performed.
'''
CRITERIA = [
    'Actual copy-local package/specifiers and native test Specifier binding verified in every executed test process.',
    'Original selected suite passes on correct code; every requested isolated mutation runs with unchanged native selector/assertions.',
    'Detection/survival claims identify native test counts, exits and actual assertion values; setup/collection errors remain incomplete.',
    'Any required added assertion passes correct and rejects surviving fault unchanged, or existing adequate coverage is demonstrated without redundant tests.',
    'Original bytes/modes/Git/resources preserved, owned scratch removed and project-only scope respected.',
]


def validate_files(files):
    manifest = json.loads(SUMMARY.read_text())['manifest']
    if not isinstance(files, dict) or set(files) != set(manifest):
        raise ValueError('Source inventory differs from frozen upstream subset')
    for name, content in files.items():
        if (not isinstance(content, str) or manifest[name]['mode'] != 0o644
                or hashlib.sha256(content.encode('utf-8')).hexdigest() != manifest[name]['sha256']):
            raise ValueError('Source bytes/mode differ: ' + name)
    return files


def export_source(source, output):
    source = Path(source)
    manifest = json.loads(SUMMARY.read_text())['manifest']
    actual = {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()}
    if actual != set(manifest) or any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Unexpected source inventory or symlink')
    files = {}
    for name, expected in manifest.items():
        path = source / name
        if path.stat().st_mode & 0o777 != expected['mode']:
            raise ValueError('Unexpected source mode: ' + name)
        files[name] = path.read_bytes().decode('utf-8')
    validate_files(files)
    with Path(output).open('x', encoding='utf-8') as stream:
        json.dump(files, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def cases(python):
    python = Path(python)
    if not python.is_absolute():
        raise ValueError('Use the supplied absolute interpreter path')
    files = validate_files(json.loads(SNAPSHOT.read_text()))
    summary = json.loads(SUMMARY.read_text())
    source = files['src/packaging/specifiers.py']
    cls, = [n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == 'Specifier']
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name.startswith('_compare_')][:3]
    for method, fault in zip(methods, summary['mutations']):
        last = max((n for n in ast.walk(method) if isinstance(n, ast.Return)), key=lambda n: (n.lineno, n.col_offset))
        if (ast.get_source_segment(source, last) != fault['old'] or fault['new'] != 'return False'
                or fault['target'] != 'src/packaging/specifiers.py' or source.count(fault['old']) != 1):
            raise ValueError('Mutation no longer matches the declared selection rule')
    if len(methods) != 3 or len(summary['mutations']) != 3:
        raise ValueError('Three independent mutations required')
    result = []
    for label, count in [('single', 1), ('multiple', 3)]:
        request = 'Requested isolated replacements (exact old/new text):\n' + json.dumps(summary['mutations'][:count], indent=2)
        result.append(dict(id='packaging-specifier-' + label, skill='con-artist', files=dict(files),
                           task=TASK + '\n' + request + '\nPreinstalled Python: ' + str(python),
                           criteria=list(CRITERIA)))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    export_source(args.source, args.output)
    print('Exported exact source subset; no tests or model sessions executed.')
