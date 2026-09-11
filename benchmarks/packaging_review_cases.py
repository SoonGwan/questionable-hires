#!/usr/bin/env python3
"""Review an actual committed packaging cleanup, not a synthetic replacement."""
import argparse
import importlib.util
import json
from pathlib import Path

SNAPSHOT = '436e409'


def cases():
    spec = importlib.util.spec_from_file_location(
        'packaging_export', Path(__file__).with_name('packaging_cases.py'))
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    exporter.SNAPSHOT = SNAPSHOT
    case = exporter.cases()[0]
    case.update(
        id='packaging-cleanup-review', skill='necromancer',
        task=('Review whether the exception handler around copying in '
              'scripts/build.py can be removed while keeping the current build '
              'behavior. Verify your recommendation using the project tests and '
              'a local reproduction if needed. Do not edit project files, install '
              'skills or publish anything.'),
        criteria=[
            'Retains cleanup needed after a failed build; demonstrates the effect of removal on owned partial output or retry.',
            'Distinguishes exclusive destination creation from copying cleanup; existing destinations remain untouched.',
            'Uses actual build code and relevant tests, including successful bundle behavior; setup failure is not a counterexample.',
            'Preserves original error semantics and project files; no install or publication.',
        ])
    case['files']['README.md'] += (
        '\nThe export preserves source bytes but not upstream Git history. '
        'The evaluation repository has a snapshot commit, not the original '
        'change ancestry. Do not infer historical intent from that commit.\n')
    return [case]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
