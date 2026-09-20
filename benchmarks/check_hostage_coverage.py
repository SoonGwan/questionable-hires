"""Author replay of retained suites against explicit mutations, not model scoring."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'benchmarks/results/all-eight-current-03'


def variants(source):
    publish = '            if generation == self.generation:\n                self.value = value'
    clear = '            if generation == self.generation:\n                self.pending = False'
    assert source.count(publish) == source.count(clear) == 1
    assert source.count('await fetch(key)') == 1
    return {
        'healthy': source,
        'stale_publish': source.replace(publish, '            self.value = value'),
        'stale_clear': source.replace(clear, '            self.pending = False'),
        'discard_prior_on_entry': source.replace('        self.pending = True',
                                               '        self.value = None\n        self.pending = True'),
        'stringify_callback_key': source.replace('await fetch(key)', 'await fetch(str(key))'),
    }


def inspect():
    rows = []
    source_hashes = {}
    implementations = []
    for condition, arm in [('baseline', 'baseline'), ('current', 'skill')]:
        project = EVIDENCE / condition / ('refresh-owner-a--' + arm + '--1') / 'project'
        implementation = (project / 'preview.py').read_text()
        implementations.append(implementation)
        names = ['preview.py', 'test_preview.py'] + (['test_support.py'] if condition == 'current' else [])
        source_hashes[condition] = {name: hashlib.sha256((project / name).read_bytes()).hexdigest()
                                    for name in names}
        for mutation, code in variants(implementation).items():
            with tempfile.TemporaryDirectory(prefix='hostage-coverage-', dir=ROOT / 'benchmarks') as folder:
                copy = Path(folder)
                for name in names:
                    (copy / name).write_bytes((project / name).read_bytes())
                (copy / 'preview.py').write_text(code)
                try:
                    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_preview'],
                        cwd=copy, text=True, capture_output=True, timeout=15)
                    row = dict(condition=condition, mutation=mutation, exit_code=result.returncode,
                               timed_out=False, output=(result.stdout + result.stderr).replace(str(copy), '<COPY>'))
                except subprocess.TimeoutExpired as error:
                    row = dict(condition=condition, mutation=mutation, exit_code=None, timed_out=True,
                               output=str(error))
                rows.append(row)
        assert source_hashes[condition] == {name: hashlib.sha256((project / name).read_bytes()).hexdigest()
                                            for name in names}
    assert implementations[0] == implementations[1]
    return dict(kind='Post-run author mutation replay of retained test artifacts, not fresh model evidence',
                python=sys.version, source_hashes=source_hashes, rows=rows,
                limitation='Authored mutations are not exhaustive correctness, task rescoring, causal token attribution or a skill improvement result.')


if __name__ == '__main__':
    print(json.dumps(inspect(), indent=2))
