#!/usr/bin/env python3
"""Preflight only the existing HTTPX exception audit, outside model inputs."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from httpx_oracle import FAULTS, REVISION, run, witness


def preflight(source, python):
    source = source.resolve(strict=True)
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip() != REVISION:
        raise ValueError('Expected pinned HTTPX revision')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=source):
        raise ValueError('Expected clean HTTPX checkout')
    name = 'asgi-exceptions'
    filename, old, new, test = FAULTS[name]
    with tempfile.TemporaryDirectory(prefix='httpx-exception-preflight-', dir=Path(__file__).resolve().parent) as temporary:
        project = Path(temporary) / 'project'
        shutil.copytree(source, project, ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache'))
        correct = run(python, project, test)
        correct_witness = witness(python, project, name)
        target = project / filename
        content = target.read_text()
        if content.count(old) != 1:
            raise ValueError('Fault must match once')
        target.write_text(content.replace(old, new))
        mutant = run(python, project, test)
        faulty_witness = witness(python, project, name)
    result = dict(revision=REVISION, case=name, correct=correct, mutant=mutant,
                  correct_witness=correct_witness, faulty_witness=faulty_witness)
    if [correct['exit_code'], mutant['exit_code'], correct_witness['exit_code'], faulty_witness['exit_code']] != [0, 1, 0, 1]:
        raise RuntimeError(json.dumps(result))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = preflight(args.source, args.python)
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    for key in ('correct', 'mutant', 'correct_witness', 'faulty_witness'):
        print(key, result[key]['exit_code'], result[key]['stdout'], result[key]['stderr'])
