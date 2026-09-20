"""Author-only replay of generated suites under the preregistered argument controls."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = '''import copy, sys, unittest
import sender
mode = sys.argv[1]
original = sender.Sender.send
if mode != 'healthy':
    async def changed(self, payload, deliver):
        def adjusted(value):
            if mode == 'argument_copy':
                value = copy.copy(value)
            elif mode == 'missing_normalization':
                value = payload
            elif mode == 'fresh_normalized_string':
                value = ''.join(list(value))
            else:
                raise ValueError(mode)
            return deliver(value)
        return await original(self, payload, adjusted)
    sender.Sender.send = changed
suite = unittest.defaultTestLoader.discover('.')
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
'''


def inventory(project):
    files = {}
    for path in project.rglob('*'):
        if path.is_symlink():
            raise ValueError('Replay input may not contain symlinks')
        if path.is_file():
            files[str(path.relative_to(project))] = dict(
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(), mode=path.stat().st_mode & 0o777)
    return files


def inspect(project, mode):
    project = Path(project).resolve(strict=True)
    if mode not in ('opaque', 'normalized'):
        raise ValueError('Unknown argument contract')
    before = inventory(project)
    variants = (['healthy', 'argument_copy'] if mode == 'opaque' else
                ['healthy', 'missing_normalization', 'fresh_normalized_string'])
    rows = []
    for variant in variants:
        with tempfile.TemporaryDirectory(prefix='sender-replay-', dir=ROOT / 'benchmarks') as temp:
            copied = Path(temp) / 'project'
            shutil.copytree(project, copied)
            try:
                result = subprocess.run([sys.executable, '-B', '-c', BOOTSTRAP, variant], cwd=copied,
                    capture_output=True, text=True, timeout=20)
                row = dict(variant=variant, exit_code=result.returncode, timed_out=False,
                           output=(result.stdout + result.stderr).replace(str(copied), '<COPY>'))
            except subprocess.TimeoutExpired as error:
                def decode(value): return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                row = dict(variant=variant, exit_code=None, timed_out=True,
                           output=(decode(error.stdout) + decode(error.stderr)).replace(str(copied), '<COPY>'))
            rows.append(row)
    assert before == inventory(project)
    return dict(kind='Post-run author replay, not original model execution or model cost',
                mode=mode, python=sys.version, source_files=before, rows=rows,
                limitation='Callback-boundary mutations; inspect assertion failures versus support errors. Not exhaustive coverage or automatic task scoring.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('mode', choices=['opaque', 'normalized'])
    args = parser.parse_args()
    print(json.dumps(inspect(args.project, args.mode), indent=2))
