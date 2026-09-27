"""Exercise the exact prospective inventory without selected issue inputs."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile


def load(path):
    spec = importlib.util.spec_from_file_location('inventory_control', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.inventory


def run(resource, status_control):
    inventory = load(resource / 'inventory.py')
    owned = Path(tempfile.mkdtemp(prefix='qh-native-cache-control-'))
    project = owned / 'mutations'
    project.mkdir()
    source = project / 'module.py'
    source.write_text('value = 1\n')
    baseline = inventory(project)
    cache = project / '.cache' / 'v' / 'cache' / 'lastfailed'
    cache.parent.mkdir(parents=True)
    cache.write_text('{"control": true}')
    changed = inventory(project)
    assert baseline['source'] == changed['source']
    assert baseline['runtime_cache'] != changed['runtime_cache']
    source.write_text('value = 2\n')
    assert baseline['source'] != inventory(project)['source']
    source.write_text('value = 1\n')
    source.chmod(0o700)
    assert baseline['source'] != inventory(project)['source']
    nested = project / 'package' / '.cache' / 'important.py'
    nested.parent.mkdir(parents=True)
    nested.write_text('contract = True\n')
    assert 'package/.cache/important.py' in inventory(project)['source']
    link = project / 'link.py'
    link.symlink_to('module.py')
    first = inventory(project)
    link.unlink()
    link.symlink_to('package/.cache/important.py')
    assert first['source'] != inventory(project)['source']
    source.unlink()
    assert 'module.py' not in inventory(project)['source']
    native = []
    for runtime in ['requests28', 'requests40']:
        working = owned / runtime
        working.mkdir()
        fixture = working / 'test_states.py'
        fixture.write_bytes((status_control / 'test_states.py').read_bytes())
        before = inventory(working)
        summary = owned / (runtime + '.json')
        result = subprocess.run(
            ['/tmp/qh-external-bundle-02-' + runtime + '/env/bin/python', '-B',
             str(status_control / 'control.py'), str(fixture),
             str(owned / (runtime + '-basetemp')), str(summary)],
            cwd=working, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
                                 PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),
            capture_output=True, timeout=30)
        assert result.returncode == 0, result.stderr.decode(errors='replace')
        after = inventory(working)
        assert before['source'] == after['source']
        assert before['runtime_cache'] != after['runtime_cache']
        native.append(dict(runtime=runtime, control_exit=result.returncode,
                           source_unchanged=True, cache_changed=True,
                           cache_paths=sorted(after['runtime_cache']),
                           status_control=json.loads(summary.read_text())))
    return dict(result='PASS', mutation_controls=['source bytes', 'source mode',
                'source deletion', 'symlink target', 'nested .cache source retained'],
                root_cache_change_visible=True, native=native, model_calls=0)


if __name__ == '__main__':
    import sys
    print(json.dumps(run(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()), indent=2))
