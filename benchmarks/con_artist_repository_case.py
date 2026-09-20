"""An authored audit task over unchanged files from this actual repository."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = '716493b'
IMPLEMENTATION = 'skills/con-artist/scripts/context.py'
TEST = 'tests/test_context_line_index.py'


def source_files():
    return {name: subprocess.check_output(['git', 'show', REVISION + ':' + name], cwd=ROOT).decode()
            for name in (IMPLEMENTATION, TEST)}


def cases():
    files = source_files()
    files['SOURCE.md'] = (
        'The collector and test file are unchanged snapshots from questionable-hires '
        'commit 716493b. This audit request is authored for evaluation; it is not an '
        'external issue or held-out project. The four existing tests use unittest.\n')
    files['AGENTS.md'] = (
        'Audit only. Do not edit original production/tests, install dependencies, '
        'access outside this project, publish, or add a permanent harness/report. '
        'Use disposable project-local copies preserving the existing relative layout. '
        'The native command from each copy root is python3 -B -m unittest discover '
        '-s tests -p test_context_line_index.py -v. Create .test-tmp inside that copy '
        'and set TMPDIR to its absolute path only for the native test child, so the '
        'unchanged tests use project-local temporary directories. Do not change '
        'global launcher settings. Keep all four tests unchanged. Establish copied '
        'implementation identity and actual assertion outcomes, not just exit codes. '
        'Preserve all original contents/modes and owner notes/cache; remove owned '
        'copies after execution, including on failure.\n')
    files['requirements.md'] = (
        'Collector context is reusable only within a single collect invocation. '
        'A later call must observe edits to the same selected relative path, even '
        'when another project has the same relative filename. Definition excerpts, '
        'requested lines and hashes must describe the current source. Named and '
        'line selection must retain existing ambiguity behavior. This audit concerns '
        'cross-invocation cache reuse only, not concurrent filesystem mutation.\n')
    files.update({'.gitignore': '.cache/\n', 'notes.txt': 'Owner draft: preserve exactly.\n',
                  '.cache/owner.txt': 'Owner cache: preserve exactly.\n'})
    return [dict(id='repository-collector-cache', skill='con-artist', files=files,
        task=('Audit whether the existing tests detect erroneous reuse of collector '
              'context across separate collect calls. Trace the real collector/test '
              'binding, establish a correct-code baseline, then introduce one meaningful '
              'cross-invocation cache-reuse fault in an isolated copy and run the same '
              'four tests. Report which assertions detect it or what remains unprotected. '
              'Do not implement a production fix or change the tests. Follow AGENTS.md '
              'and preserve all original files; retain no harness or report.'),
        criteria=['All four unchanged native tests execute against correct and valid faulty copied implementations.',
                  'The fault actually reuses context across collect invocations, rather than a syntax/import error or unrelated behavior.',
                  'Explain actual correct/faulty assertion outcomes and detecting check or surviving coverage gap.',
                  'Evidence links the real test binding to the copied collector, with original/source identities and native exits.',
                  'Original files and owner changes preserved; test scratch/copies stay project-local and are removed.'])]


def preflight():
    files = source_files()
    anchor = '    budget = [0]\n    cache = {}\n'
    assert files[IMPLEMENTATION].count(anchor) == 1
    faulty = files[IMPLEMENTATION].replace(anchor,
        "    budget = [0]\n    cache = globals().setdefault('_process_cache', {})\n")
    rows = []
    with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks/local-runs') as scratch:
        for variant, source, expected in [('correct', files[IMPLEMENTATION], 0), ('faulty', faulty, 1)]:
            copy = Path(scratch) / variant
            for name, content in files.items():
                target = copy / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source if name == IMPLEMENTATION else content)
            temp = copy / '.test-tmp'
            temp.mkdir()
            probe = copy / '.author-probe'
            probe.mkdir()
            (probe / 'sitecustomize.py').write_text(
                'import json, sys\n'
                'def observe(event, args):\n'
                '    if event == "tempfile.mkdtemp":\n'
                '        print("AUTHOR_TEMP " + json.dumps(args[0]), flush=True)\n'
                'sys.addaudithook(observe)\n')
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                '-s', 'tests', '-p', 'test_context_line_index.py', '-v'], cwd=copy,
                env=dict(os.environ, TMPDIR=str(temp), PYTHONPATH=str(probe)), capture_output=True, text=True, timeout=10)
            output = result.stdout + result.stderr
            assert result.returncode == expected, output
            assert 'Ran 4 tests' in output and 'ERROR:' not in output, output
            assert not list(temp.iterdir())
            created = [json.loads(line.removeprefix('AUTHOR_TEMP ')) for line in output.splitlines()
                       if line.startswith('AUTHOR_TEMP ')]
            assert created and all(Path(path).parent == temp for path in created)
            assert (copy / TEST).read_text() == files[TEST]
            if expected:
                assert 'test_no_stale_spans_after_new_invocation' in output
                assert 'AssertionError:' in output and "'changed'" in output
            rows.append(dict(variant=variant, exit_code=result.returncode,
                implementation_sha256=hashlib.sha256(source.encode()).hexdigest(),
                test_sha256=hashlib.sha256(files[TEST].encode()).hexdigest(),
                output=output.replace(str(copy), '<COPY>'), test_scratch_removed=True,
                scratch_paths=[str(Path(path).relative_to(copy)) for path in created],
                instrumentation='Author-only audit hook observes actual tempfile paths; not supplied to model.'))
    return rows
