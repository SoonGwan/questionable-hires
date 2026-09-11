#!/usr/bin/env python3
"""Run the frozen browser screen with local dependency copies; never resume."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import shutil

from run import ROOT, command, disabled_skills, prepare, resource_manifest, run_cell

TASK = ('QA the catalog interaction against its README using actual browser input '
        'and rendered observations. Demonstrate any reproducible failure and nearby '
        'normal behavior, report commands and limits, and retain focused checks '
        'under qa/. Preserve original files; do not install dependencies or use '
        'external sites or personal browser profiles.')


def stage(destination):
    source = ROOT / 'benchmarks/browser/model-project'
    dependency = ROOT / 'benchmarks/browser/node_modules/playwright-core'
    inventory = resource_manifest(dependency)
    if not inventory or any(r['kind'] != 'file' for r in inventory.values()):
        raise ValueError('Requires an existing regular-file Playwright tree')
    package = json.loads((dependency / 'package.json').read_text())
    if package['version'] != '1.63.0' or not (dependency / 'LICENSE').is_file():
        raise ValueError('Expected pinned Playwright 1.63.0 with license')
    fixture_inventory = resource_manifest(source)
    if not fixture_inventory or any(r['kind'] != 'file' for r in fixture_inventory.values()):
        raise ValueError('Requires a regular-file browser fixture tree')
    files = {name: (source / name).read_text() for name in fixture_inventory}
    files['.gitignore'] = 'node_modules/\n'
    prepare(dict(files=files), destination)
    shutil.copytree(dependency, destination / 'node_modules/playwright-core')
    if resource_manifest(destination / 'node_modules/playwright-core') != inventory:
        raise ValueError('Dependency copy changed')
    return inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--stage-only', action='store_true', help='Prepare and verify without model usage')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = output / 'source'
    inventory = stage(source)
    manifest = dict(revision=command(['git', 'rev-parse', 'HEAD'], ROOT),
                    task=TASK, model='gpt-6-astra', effort='medium',
                    order=['baseline', 'skill'], timeout=240,
                    started_at=datetime.now(timezone.utc).isoformat(),
                    runtime=dict(codex=command(['codex', '--version'], ROOT, timeout=10),
                                 node=command(['node', '--version'], ROOT, timeout=10),
                                 python=platform.python_version(),
                                 os=platform.system(), release=platform.release(),
                                 machine=platform.machine()),
                    dependency=inventory,
                    fixture=resource_manifest(ROOT / 'benchmarks/browser/model-project'),
                    staged_only=args.stage_only, cells=[])
    path = output / 'run.json'
    def save():
        path.write_text(json.dumps(manifest, indent=2) + '\n')
    save()
    if args.stage_only:
        print('Prepared verified local dependency copy; no model session')
        return 0
    disabled = disabled_skills()
    for arm in manifest['order']:
        result = run_cell(dict(id='browser-catalog', skill='mother-in-law', task=TASK),
                          arm, 1, output, 'gpt-6-astra', 'medium', 240, disabled,
                          project_source=source)
        manifest['cells'].append(result)
        result['dependency_unchanged'] = resource_manifest(
            output / ('browser-catalog--' + arm + '--1') /
            'project/node_modules/playwright-core') == inventory
        save()
        print(arm, result['completed'], result['elapsed_seconds'], flush=True)
        if result['limit_detected']:
            manifest['stopped_after_limit'] = True
            save()
            return 1
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    save()
    return 0 if all(cell['completed'] and cell['dependency_unchanged']
                    for cell in manifest['cells']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
