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

IMAGE = 'questionable-hires/browser-codex:0.153.4-pw1.63.0'
CHROMIUM = '/ms-playwright/chromium-1243/chrome-linux-arm64/chrome'


def container_launcher(context, image, auth_file):
    """Return a run_cell launcher with credentials confined to container tmpfs."""
    if not auth_file.is_file() or auth_file.is_symlink():
        raise ValueError('Auth file must be an existing regular file')
    auth_file = auth_file.resolve()

    def launch(workspace, codex_args):
        translated = []
        index = 0
        while index < len(codex_args):
            if codex_args[index:index + 2] == ['--sandbox', 'workspace-write']:
                translated.append('--dangerously-bypass-approvals-and-sandbox')
                index += 2
                continue
            value = codex_args[index]
            translated.append('/work' if value == str(workspace) else value)
            index += 1
        return [
            'docker', '--context', context, 'run', '--rm', '--ipc=host',
            '--tmpfs', '/run/codex-home:rw,noexec,nosuid,nodev,mode=0700',
            '-v', f'{auth_file}:/run/codex-auth.json:ro',
            '-v', f'{workspace}:/work:rw',
            '-e', 'CODEX_HOME=/run/codex-home',
            '-e', f'PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH={CHROMIUM}', image,
            'sh', '-c', 'install -m 600 /run/codex-auth.json '
            '/run/codex-home/auth.json && exec "$@"', 'sh', *translated,
        ]
    return launch


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
    parser.add_argument('--container', action='store_true', help='Run model cells in the pinned Linux image')
    parser.add_argument('--container-image', default=IMAGE)
    parser.add_argument('--docker-context', default='colima')
    parser.add_argument('--auth-file', type=Path,
                        help='Codex auth.json mounted read-only and copied only to container tmpfs')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = output / 'source'
    inventory = stage(source)
    if args.container and not args.auth_file:
        parser.error('--container requires --auth-file')
    launcher = (container_launcher(args.docker_context, args.container_image,
                                   args.auth_file) if args.container else None)
    if args.container:
        codex_runtime = command(['docker', '--context', args.docker_context, 'run', '--rm',
                                 args.container_image, 'codex', '--version'], ROOT, timeout=30)
        node_runtime = command(['docker', '--context', args.docker_context, 'run', '--rm',
                                args.container_image, 'node', '--version'], ROOT, timeout=30)
    else:
        codex_runtime = command(['codex', '--version'], ROOT, timeout=10)
        node_runtime = command(['node', '--version'], ROOT, timeout=10)
    manifest = dict(revision=command(['git', 'rev-parse', 'HEAD'], ROOT),
                    task=TASK, model='gpt-6-astra', effort='medium',
                    order=['baseline', 'skill'], timeout=240,
                    started_at=datetime.now(timezone.utc).isoformat(),
                    runtime=dict(codex=codex_runtime, node=node_runtime,
                                 python=platform.python_version(),
                                 os=platform.system(), release=platform.release(),
                                 machine=platform.machine(), container=args.container,
                                 image=args.container_image if args.container else None,
                                 docker_context=args.docker_context if args.container else None),
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
                          project_source=source, launcher=launcher)
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
