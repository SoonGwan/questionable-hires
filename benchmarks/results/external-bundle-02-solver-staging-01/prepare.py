"""Stage all selected pristine sources; this does not create OS isolation."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess


def inventory(root):
    return {p.relative_to(root).as_posix(): [hashlib.sha256(p.read_bytes()).hexdigest(),
            p.stat().st_mode & 0o777] for p in root.rglob('*')
            if p.is_file() and '.git' not in p.relative_to(root).parts}


def run(manifest_path, destination):
    manifest = json.loads(manifest_path.read_text())
    destination.mkdir(mode=0o700)
    destination = destination.resolve()
    env = {'PATH': '/usr/bin:/bin', 'GIT_CONFIG_NOSYSTEM': '1',
           'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_TERMINAL_PROMPT': '0',
           'PYTHONDONTWRITEBYTECODE': '1', 'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1'}
    records = []
    for row in manifest['selected']:
        ident = row['instance_id']
        requests = row['repo'] == 'psf/requests'
        modern = ident.endswith('11143')
        candidates = list((Path('/tmp/qh-external-bundle-02-native-imports') / ident).glob(
            ('requests-' if requests else 'pytest-') + '*'))
        assert len(candidates) == 1
        original = candidates[0]
        assert original.is_dir() and not (original / '.git').exists()
        before = inventory(original)
        project = destination / ident
        shutil.copytree(original, project)
        assert inventory(project) == before
        metadata_record = None
        if not requests:
            metadata = (Path('/tmp/qh-external-bundle-02-pytest11143-build/project/src/_pytest/_version.py')
                        if modern else Path('/tmp/qh-external-bundle-02-legacy-build') / ident / 'project/src/_pytest/_version.py')
            target = project / 'src/_pytest/_version.py'
            assert not target.exists()
            shutil.copy2(metadata, target)
            metadata_record = {'path': 'src/_pytest/_version.py',
                               'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
        for args in [['git', 'init', '-q'], ['git', 'add', '-A'],
                     ['git', '-c', 'user.name=Benchmark fixture', '-c',
                      'user.email=fixture@example.invalid', 'commit', '-q', '-m', 'Frozen upstream base']]:
            subprocess.run(args, cwd=project, env=env, capture_output=True, check=True, timeout=30)
        count = subprocess.check_output(['git', 'rev-list', '--all', '--count'], cwd=project, env=env, timeout=10)
        assert count.strip() == b'1'
        assert not subprocess.check_output(['git', 'remote'], cwd=project, env=env, timeout=10).strip()
        old = subprocess.run(['git', 'cat-file', '-e', row['base_commit']], cwd=project,
                             env=env, capture_output=True, timeout=10)
        assert old.returncode != 0
        interpreter = ('/tmp/qh-external-bundle-02-owned-envs/modern/bin/python' if modern
                       else '/tmp/qh-external-bundle-02-requests28/env/bin/python' if ident.endswith('3362')
                       else '/tmp/qh-external-bundle-02-legacy-env/env/bin/python')
        source = project / 'src' if (project / 'src').is_dir() else project
        code = ('import pathlib,sys,importlib; sys.path.insert(0,sys.argv[1]); '
                'm=importlib.import_module(sys.argv[3]); '
                'assert pathlib.Path(m.__file__).resolve().is_relative_to(pathlib.Path(sys.argv[2]).resolve()); '
                'print(m.__version__)')
        result = subprocess.run([interpreter, '-I', '-B', '-c', code, str(source), str(project),
                                 'requests' if requests else 'pytest'], cwd=project,
                                env=env, capture_output=True, timeout=30)
        assert result.returncode == 0, (ident, result.stderr.decode(errors='replace'))
        assert inventory(original) == before
        expected = dict(before)
        if metadata_record:
            path = metadata_record['path']
            expected[path] = [metadata_record['sha256'], (project / path).stat().st_mode & 0o777]
        assert inventory(project) == expected
        records.append(dict(instance_id=ident, base_commit=row['base_commit'],
                            source_files=len(before), source_map_sha256=hashlib.sha256(
                                json.dumps(before, sort_keys=True).encode()).hexdigest(),
                            source_bytes_modes_match_original=True, original_preserved=True,
                            generated_metadata=metadata_record, git_commits=1, git_remotes=0,
                            upstream_commit_available=False, fresh_public_import_exit=result.returncode,
                            native_version=result.stdout.decode().strip()))
    return dict(result='PASS', cells=records, staged_projects=len(records),
                dataset_revision=manifest['revision'], grading_inputs_used=False,
                model_calls=0, os_isolation_established=False)


if __name__ == '__main__':
    import sys
    print(json.dumps(run(Path(sys.argv[1]), Path(sys.argv[2])), indent=2))
