"""Exercise the frozen author's native tests and a payload-loss assertion."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from cases_conditional_store import FILES


def main():
    root = Path(__file__).resolve().parent
    output = root / 'conditional-store-01-preflight.json'
    if output.exists():
        raise ValueError('Preflight output already exists')
    records = []
    with tempfile.TemporaryDirectory(prefix='conditional-store-preflight-', dir=root / 'local-runs') as folder:
        for strengthened in (False, True):
            for faulty in (False, True):
                project = Path(folder) / ('improved' if strengthened else 'original') / ('faulty' if faulty else 'correct')
                for name, text in FILES.items():
                    if faulty and name == 'store/backend.py':
                        text = text.replace('destination.write_bytes(payload)', 'destination.write_bytes(b"null")')
                    if strengthened and name == 'tests/test_submit.py':
                        text = 'import json\n' + text
                        first = '            self.assertEqual(result, {"accepted": True, "key": "ticket"})'
                        assertions = [
                            '            self.assertEqual(json.loads((Path(folder) / "ticket.json").read_text()), {"title": "첫 요청", "count": 2})',
                            '            self.assertEqual(json.loads((Path(folder) / "ticket.json").read_text()), {"title": "수정 요청", "count": 3})',
                        ]
                        parts = text.split(first)
                        assert len(parts) == 3
                        text = parts[0] + first + '\n' + assertions[0] + parts[1] + first + '\n' + assertions[1] + parts[2]
                    path = project / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text)
                before = {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in project.rglob('*') if p.is_file()}
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'tests.test_submit'],
                                        cwd=project, capture_output=True, text=True, timeout=10)
                expected = 1 if strengthened and faulty else 0
                assert result.returncode == expected, result.stderr
                assert 'Ran 2 tests' in result.stderr
                if expected:
                    assert 'FAILED (failures=2)' in result.stderr and 'AssertionError: None !=' in result.stderr
                after = {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in project.rglob('*') if p.is_file()}
                assert before == after
                assert sorted(p.name for p in project.iterdir()) == ['README.md', 'store', 'tests']
                records.append(dict(tests='improved' if strengthened else 'original',
                                    implementation='faulty' if faulty else 'correct',
                                    exit_code=result.returncode, output=result.stderr.replace(str(project), '<PROJECT>'),
                                    original_files_unchanged=True, scratch_removed=True))
    with output.open('x') as stream:
        json.dump(dict(records=records, original_files_sha256={n:hashlib.sha256(t.encode()).hexdigest() for n,t in FILES.items()},
                       limitation='Authored native preflight only; not model evidence or a full mutation score.'), stream, indent=2)
        stream.write('\n')
    print('Four native checks verified: original pass/pass, improved pass/two assertion failures.')


if __name__ == '__main__':
    main()
