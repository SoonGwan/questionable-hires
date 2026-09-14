"""Author-only four-phase native check; never copied into model workspaces."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from cases_sqlite_debit import FILES, PYTHON


def main():
    root = Path(__file__).resolve().parent
    output = root / 'sqlite-debit-01-preflight.json'
    if output.exists():
        raise ValueError('Refusing to overwrite preflight evidence')
    records = []
    with tempfile.TemporaryDirectory(prefix='sqlite-debit-preflight-', dir=root) as folder:
        for improved in (False, True):
            for faulty in (False, True):
                project = Path(folder) / f'{improved}-{faulty}'
                for name, contents in FILES.items():
                    if faulty and name == 'ledger.py':
                        assert contents.count('connection.commit()') == 1
                        contents = contents.replace('connection.commit()', 'connection.rollback()')
                    if improved and name == 'tests/test_debit.py':
                        contents = 'import sqlite3\n' + contents
                        contents += '''    with sqlite3.connect(database) as reader:
        balances = dict(reader.execute("SELECT name, balance FROM accounts"))
    assert balances == {"alice": 100 - amount, "bob": 250}
'''
                    path = project / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(contents)
                def snapshot():
                    return {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in project.rglob('*') if p.is_file()}
                before = snapshot()
                result = subprocess.run([PYTHON, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                                         'tests/test_debit.py'], cwd=project, capture_output=True,
                                        text=True, timeout=15)
                failure = improved and faulty
                assert result.returncode == (1 if failure else 0), result.stdout + result.stderr
                assert ('2 failed' if failure else '2 passed') in result.stdout, result.stdout
                if failure:
                    assert "{'alice': 100} != {'alice': 93}" in result.stdout, result.stdout
                    assert "{'alice': 100} != {'alice': 87}" in result.stdout, result.stdout
                    assert 'AssertionError' in result.stdout and 'ERROR at' not in result.stdout
                assert before == snapshot()
                assert sorted(p.name for p in project.iterdir()) == ['README.md', 'ledger.py', 'tests']
                records.append(dict(improved=improved, faulty=faulty, exit_code=result.returncode,
                                    output=(result.stdout + result.stderr).replace(str(project), '<PROJECT>'),
                                    source_unchanged=True, project_local_scratch_removed=True))
    with output.open('x') as stream:
        json.dump(dict(records=records, fixture_sha256={n: hashlib.sha256(t.encode()).hexdigest()
                                                       for n, t in FILES.items()},
                       limitation='Author native preflight, not model performance evidence.'), stream, indent=2)
        stream.write('\n')
    print('Original 2 pass/pass; improved 2 pass/2 actual balance assertion failures; files/scratch verified.')


if __name__ == '__main__':
    main()
