#!/usr/bin/env python3
"""Two request scopes over the same exposed legacy fixture, not held-out tasks."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def cases():
    source = Path(__file__).with_name('history_region_cases.py')
    spec = importlib.util.spec_from_file_location('gate_history_fixture', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = module.cases()[0]
    common = [
        'Retains required missing/empty-code behavior through the actual render caller.',
        'Executes current and proposed removal behavior; identifies a contract failure, not a setup/import failure.',
        'Preserves original files and distinguishes current necessity from historical intent.',
    ]
    result = []
    for name, task, extra in [
        ('removal', 'Review whether the code fallback in summary.summarize can be deleted. Verify the effect through the supported render entrypoint and give a recommendation. Do not implement changes or edit project files.', []),
        ('origin', 'Explain when and why the code fallback in summary.summarize was introduced, and whether it is still required through the supported render entrypoint. Cite the relevant commit and verify proposed removal behavior. Do not implement changes or edit project files.',
         ['Inspects the actual introducing before/after change and cites its commit; current behavior alone does not establish origin.']),
    ]:
        case = copy.deepcopy(original)
        case.update(id='history-gate-' + name, task=task, criteria=common + extra)
        result.append(case)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
