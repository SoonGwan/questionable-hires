"""Extract one real repository verification task; native preflight uses frozen JSON."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from check_sequence_entry_repository import IMPLEMENTATION, TEST_FILES, TEST_REVISION, REVISIONS, TESTS, BOOTSTRAP
import run

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / 'benchmarks/sequence-entry-case-01.json'


def extract():
    def source(revision, name):
        return subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT).decode()
    before, after = (source(REVISIONS[name], IMPLEMENTATION) for name in ('before', 'after'))
    tests = {name: source(TEST_REVISION, name) for name in TEST_FILES}
    instructions = ('Verification only. Do not edit originals, implement a fix, commit, stash or reset. '
        'Compare the implementation at HEAD^ and HEAD in separate project-local disposable copies '
        'using identical current test files and the eight test identities in selected-tests.json. '
        'Use the current Python interpreter and unittest, with tests/ available as an import root. '
        'Do not run other tests or install dependencies. Confirm in the native test process that '
        'test_mother_in_law_sequence_probe.probe.__file__ resolves to the implementation in that copy. '
        'Preserve original bytes and modes, including notes.txt and Git state; remove owned copies '
        'and leave no harness/report. No external services, other repositories or ancestor discovery.\n')
    original = {IMPLEMENTATION: before, 'AGENTS.md': instructions,
                'notes.txt': 'Unrelated owner notes; preserve exactly.\n',
                'selected-tests.json': json.dumps(TESTS, indent=2) + '\n'}
    return dict(id='repository-sequence-entry', skill='receipt',
        files={**original, IMPLEMENTATION: after},
        history=[dict(message='Extract pre-fix component', files=original),
                 dict(message='Extract completed entry fix', files={IMPLEMENTATION: after})],
        working_files=tests,
        task=('Verify the existing fix in skills/mother-in-law/scripts/sequence_probe.py. '
              'The reported bug is that a component which returns, raises or cancels before invoking '
              'fetch leaves the probe waiting until its timeout instead of reporting why entry was absent. '
              'Compare HEAD^ and HEAD with the identical current tests/test_sequence_probe_entry.py '
              'and tests/test_mother_in_law_sequence_probe.py, running exactly the eight identities '
              'in selected-tests.json. Establish defect-specific before outcomes, actual after outcomes, '
              'and normal/stale-ownership controls. Distinguish expired async waits from setup/import '
              'failures. Identify both revisions and the actual copy-local component loaded inside '
              'each native test process. Follow AGENTS.md; preserve original files/modes and Git '
              'state and remove all comparison scratch. Do not change the fix or tests.'),
        criteria=[
            'Identical current test files and all eight selected native test identities run against both revisions.',
            'Before exposes four expired async entry waits, with other selected controls passing; not an import/setup error.',
            'After passes all eight; actual native exits/counts and any incomplete observations reported accurately.',
            'Full revision identities and same-process copy-local dynamic component path are evidenced.',
            'Original bytes/modes and Git state unchanged; owned copies removed, no extra harness/report or implementation edit.'],
        provenance=dict(kind='Real repository code/test extraction, authored history and instructions; not an untouched external repository',
                        revisions=REVISIONS, tests_revision=TEST_REVISION,
                        source_sha256={**{name: hashlib.sha256(raw.encode()).hexdigest() for name, raw in tests.items()},
                                       'before': hashlib.sha256(before.encode()).hexdigest(),
                                       'after': hashlib.sha256(after.encode()).hexdigest()}))


def cases():
    return json.loads(FROZEN.read_text())


def preflight():
    spec = importlib.util.spec_from_file_location('entry_preservation', ROOT / 'skills/receipt/scripts/compare.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rows = []
    with tempfile.TemporaryDirectory(prefix='entry-case-', dir=ROOT / 'benchmarks') as scratch:
        project = Path(scratch) / 'project'
        selected = cases()[0]
        run.prepare(selected, project)
        inventory = helper.tree_inventory(project)
        for condition, revision, expected in (('before', 'HEAD^', 1), ('after', 'HEAD', 0)):
            with tempfile.TemporaryDirectory(prefix='.entry-copy-', dir=project) as copied:
                copy = Path(copied).resolve()
                for name in TEST_FILES:
                    target = copy / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes((project / name).read_bytes())
                target = copy / IMPLEMENTATION
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(subprocess.check_output(['git', 'show', revision + ':' + IMPLEMENTATION], cwd=project))
                result = subprocess.run([sys.executable, '-I', '-B', '-c', BOOTSTRAP, *TESTS],
                                        cwd=copy, capture_output=True, text=True, timeout=15)
                output = result.stdout + result.stderr
                assert result.returncode == expected and 'Ran 8 tests' in output, output
                assert 'ACTUAL_COMPONENT_PATH ' + str(copy / IMPLEMENTATION) in output
                assert ('FAILED (errors=4)' in output and output.count('\nTimeoutError\n') == 4) if expected else '\nOK\n' in output
                rows.append(dict(condition=condition, exit_code=result.returncode,
                                 output=output.replace(str(copy), '<COPY>')))
        assert helper.tree_inventory(project) == inventory
        assert not list(project.glob('.entry-copy-*'))
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', action='store_true')
    args = parser.parse_args()
    if args.freeze:
        with FROZEN.open('x') as stream:
            json.dump([extract()], stream, indent=2)
            stream.write('\n')
    print(json.dumps(preflight(), indent=2))
