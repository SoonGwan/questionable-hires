"""Run only inside newly owned, unmounted /testbed Docker containers."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

CONFIG = {
    'requests': ('091991be0da19de9108dbe5e3752917fea3d7fdc',
                 'ac2af6596a097252c97353aa2ec771591053b08b',
                 '980e006268fb816b7d2686baef7242418d895d9a', 'test_requests.py'),
    'pytest': ('e6e300e729dd33956e5448d8be9a0b1540b4e53a',
               'a0d8040ee4ee621e86a39ae62208596bc865c9c1',
               '877d433795f3d7288b9edd5696724bb2d8e47f88', 'testing/test_skipping.py'),
}
repo = sys.argv[1]
base, expected_head, expected_tree, tests = CONFIG[repo]
root = Path('/testbed')
assert Path.cwd() == root and Path('/.dockerenv').is_file()
assert os.environ.get('QH_DISPOSABLE_CONTAINER') == '1'
assert (root / '.git').is_dir() and not (root / '.git').is_symlink()
def git(*args, **kwargs):
    return subprocess.check_output(['git', *args], **kwargs)
assert git('rev-parse', 'HEAD').decode().strip() == expected_head
assert git('rev-parse', base + '^{tree}').decode().strip() == expected_tree
paths = git('ls-tree', '-rz', '--name-only', base)
archive = git('archive', base)
subprocess.run(['tar', '-xf', '-', '-C', str(root)], input=archive, check=True)
# Only this newly created container's exact Git database is removed. The original
# image and previous read-only containers retain it for recovery and provenance.
shutil.rmtree('/testbed/.git')
git('init', '-q')
git('add', '--pathspec-from-file=-', '--pathspec-file-nul', input=paths)
git('-c', 'user.name=Benchmark fixture', '-c', 'user.email=fixture@example.invalid',
    'commit', '-q', '-m', 'Frozen base source; upstream history omitted')
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == expected_tree
assert git('rev-list', '--all', '--count').strip() == b'1'
assert not git('remote').strip()
old_object = subprocess.run(['git', 'cat-file', '-e', base], capture_output=True)
assert old_object.returncode != 0
print(json.dumps(dict(repo=repo, tree=expected_tree, archive_sha256=hashlib.sha256(archive).hexdigest(),
                     commits=1, remotes=0, old_commit_available=False)), flush=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
for key in ('PYTEST_ADDOPTS', 'PYTEST_PLUGINS'):
    env.pop(key, None)
probe = 'import ' + repo + '; print(' + repo + '.__version__, ' + repo + '.__file__)'
subprocess.run([sys.executable, '-B', '-c', probe], env=env, check=True, timeout=30)
command = [sys.executable, '-B', '-m', 'pytest', '-p', 'no:cacheprovider',
           '--collect-only', '-q', tests]
result = subprocess.run(command, env=env, timeout=90)
print(json.dumps(dict(stage='native_collection', command=command, exit_code=result.returncode)), flush=True)
raise SystemExit(result.returncode)
