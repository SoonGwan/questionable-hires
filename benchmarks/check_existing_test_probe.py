"""Author replay of retained model-written tests using native replacements."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

from cases_conditional_store import FILES

ROOT = Path(__file__).resolve().parents[1]


def check():
    spec = importlib.util.spec_from_file_location('existing_test_audit', ROOT / 'skills/con-artist/scripts/audit.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    improved = (ROOT / 'benchmarks/results/conditional-store-01/candidate/conditional-store--skill--1/project/tests/test_submit.py').read_text()
    with tempfile.TemporaryDirectory(prefix='existing-test-probe-', dir=ROOT / 'benchmarks') as folder:
        project = Path(folder)
        for name, content in FILES.items():
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        recipe = dict(files=['store','tests','README.md'], imports=['store.service','store.backend','store.codec','tests.test_submit'],
                      tests=['-v','tests.test_submit'], target='store/backend.py',
                      old='destination.write_bytes(payload)', new='destination.write_bytes(b"{}")',
                      probe_replacements={'tests/test_submit.py':improved},
                      probe_tests=['-v','tests.test_submit'], probe_when='survives')
        result = helper.audit(project, recipe)
        assert result['status'] == 'observed'
        assert {k:v['exit_code'] for k,v in result['checks'].items()} == dict(correct_tests=0,mutant_tests=0,correct_probe=0,mutant_probe=1)
        for phase in result['checks'].values():
            assert not phase['timed_out'] and not phase['output_truncated']
            assert 'Ran 2 tests' in phase['output']
        failure = result['checks']['mutant_probe']['output']
        assert 'FAILED (failures=2)' in failure and 'AssertionError: {} !=' in failure
        assert all((project / n).read_bytes() == t.encode() for n,t in FILES.items())
        actual = {p.relative_to(project).as_posix() for p in project.rglob('*') if p.is_file()}
        assert actual == set(FILES)
        result['proposed_test_sha256'] = hashlib.sha256(improved.encode()).hexdigest()
        result['limitation'] = 'Author replay of retained candidate tests, not a new model run or performance measurement; original tests unchanged.'
        return json.loads(json.dumps(result).replace(str(project), '<AUTHOR_PROJECT>'))


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
