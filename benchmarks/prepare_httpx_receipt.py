#!/usr/bin/env python3
"""Prepare a disclosed seeded defect in an owned full HTTPX checkout copy."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from run import command, prepare_repository
from run_httpx import REVISION, interpreter_path

TARGET = 'httpx/_urls.py'
CHECKS = ['tests/models/test_url.py::test_url_set_param_manipulation',
          'tests/models/test_url.py::test_url_add_param_manipulation',
          'tests/models/test_url.py::test_url_remove_param_manipulation']


def seeded_source(text):
    original = 'return self.copy_with(params=self.params.set(key, value))'
    if text.count(original) != 1:
        raise ValueError('Expected exactly one frozen set-param implementation')
    return text.replace(original, 'return self.copy_with(params=self.params.add(key, value))')


def prepare(source, python, output):
    source, python, output = source.resolve(), interpreter_path(python), output.resolve()
    if output == source or source in output.parents:
        raise ValueError('Output must not be inside the original checkout')
    if command(['git', 'rev-parse', 'HEAD'], source) != REVISION:
        raise ValueError('Unexpected upstream revision')
    output.mkdir(parents=True, exist_ok=False)
    project = output / 'project'
    prepare_repository(source, project)
    names = command(['git', 'ls-files'], project).splitlines()
    initial = {name: hashlib.sha256((project / name).read_bytes()).hexdigest() for name in names}
    results = {}
    target = project / TARGET
    original = target.read_text()
    for variant in ('upstream', 'seeded'):
        if variant == 'seeded':
            target.write_text(seeded_source(original))
        process = subprocess.run([str(python), '-B', '-m', 'pytest', '-q',
                                  '-p', 'no:cacheprovider', *CHECKS], cwd=project,
                                 text=True, capture_output=True, timeout=60)
        results[variant] = dict(exit_code=process.returncode,
                                stdout=process.stdout, stderr=process.stderr)
        (output / 'preflight.json').write_text(json.dumps(results, indent=2) + '\n')
        expected = 0 if variant == 'upstream' else 1
        summary = '3 passed' if variant == 'upstream' else '1 failed, 2 passed'
        if process.returncode != expected or summary not in process.stdout:
            raise ValueError('Preflight outcome mismatch; retained artifacts are not ready')
        if variant == 'seeded' and not all(s in process.stdout for s in
                ('AssertionError', 'a=123&a=456', 'a=456')):
            raise ValueError('Missing actual/expected defect evidence')
    for name in names:
        if name != TARGET and hashlib.sha256((project / name).read_bytes()).hexdigest() != initial[name]:
            raise ValueError('Unexpected fixture file change: ' + name)
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != initial[name]:
            raise ValueError('Original upstream file changed: ' + name)
    command(['git', 'add', '--', TARGET], project)
    command(['git', '-c', 'user.name=Benchmark Fixture', '-c',
             'user.email=fixture@example.invalid', 'commit', '-qm',
             'Authored benchmark fault: append rather than replace query parameter'], project)
    if command(['git', 'status', '--porcelain'], project):
        raise ValueError('Prepared checkout is not clean')
    manifest = dict(upstream_revision=REVISION, seeded_revision=command(['git', 'rev-parse', 'HEAD'], project),
                    interpreter=str(python), checks=CHECKS, original_sha256=initial,
                    seeded_target_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                    limitation='Authored fault in actual upstream code, not a historical upstream bug. No model execution.')
    (output / 'fixture.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = prepare(args.source, args.python, args.output)
    print(json.dumps({key: result[key] for key in ('upstream_revision', 'seeded_revision', 'checks', 'limitation')}, indent=2))
