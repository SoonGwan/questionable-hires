"""Non-model, public-source runtime probe. Run inside the prepared image only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

project = sys.argv[1]
assert project in ('requests', 'pytest')
assert Path('/.dockerenv').is_file() and Path.cwd() == Path('/testbed')
assert not Path('/var/run/docker.sock').exists()
assert not Path('/run/codex-auth.json').exists()
assert not Path('/root/.codex/auth.json').exists()
def command(*args):
    return subprocess.check_output(args, text=True).strip()
assert command('git', 'rev-list', '--all', '--count') == '1'
assert not command('git', 'remote')
assert not command('git', 'diff', 'HEAD', '--')
assert command('codex', '--version') == 'codex-cli 0.153.4'
subprocess.run([sys.executable, '-B', '-c',
    'import ' + project + '; assert ' + project + '.__file__.startswith("/testbed/"); '
    'print("FRESH_IMPORT", ' + project + '.__file__)'], check=True)
package = __import__(project)
assert package.__file__.startswith('/testbed/')
import pytest
expected = 142 if project == 'requests' else 77
test_file = 'test_requests.py' if project == 'requests' else 'testing/test_skipping.py'
class Bindings:
    def pytest_collection_modifyitems(self, items):
        assert len(items) == expected, (len(items), expected)
        for item in items:
            assert Path(item.module.__file__).resolve() == Path('/testbed') / test_file
            assert getattr(item.module, project) is package
        print('QH_PUBLIC_SOURCE_BINDINGS=' + str(len(items)), flush=True)

print(json.dumps(dict(project=project, python=sys.version, source=package.__file__,
    tree=command('git', 'rev-parse', 'HEAD^{tree}'), commits=1,
    cli=command('codex', '--version'),
    installer_sha256=hashlib.sha256(Path('/tmp/qh-codex-install.sh').read_bytes()).hexdigest())), flush=True)
code = pytest.main(['-p', 'no:cacheprovider', '-q', test_file], plugins=[Bindings()])
assert not command('git', 'diff', 'HEAD', '--')
print('QH_PUBLIC_NATIVE_EXIT=' + str(code), flush=True)
raise SystemExit(code)
