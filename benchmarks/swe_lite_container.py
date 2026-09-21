"""Container lifecycle adapter for run.run_cell; no model API of its own.

Keep credentials in tmpfs, persist only per-cell sessions, and remove the exact
owned container on ordinary exits and SIGTERM. External network use, if enabled,
is not an enforced solution-lookup barrier.
"""
import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import uuid


def inspected_container(result, name):
    """A Docker/daemon error is not proof that a container is absent."""
    if result.returncode == 0:
        return json.loads(result.stdout)[0]
    missing = {'Error: No such object: ' + name,
               'error: no such object: ' + name,
               'Error response from daemon: No such container: ' + name}
    if result.stderr.strip() in missing:
        return None
    raise RuntimeError('Unable to verify container presence; inspect Docker state')


def translated_args(workspace, args):
    if args[:2] != ['codex', 'exec'] or '--ephemeral' in args:
        raise ValueError('Requires persistent codex exec')
    if args.count('-C') != 1 or args[args.index('-C') + 1] != str(workspace):
        raise ValueError('Expected exact per-cell workspace')
    if args.count('--sandbox') != 1:
        raise ValueError('Expected explicit sandbox setting')
    index = args.index('--sandbox')
    if args[index + 1] != 'workspace-write':
        raise ValueError('Unexpected sandbox setting')
    result = list(args)
    result[index:index + 2] = ['--dangerously-bypass-approvals-and-sandbox']
    result[result.index('-C') + 1] = '/testbed'
    return result


def container_launcher(image, auth_file, state, project, network='none', timeout=360,
                       context='default', memory_gib=2):
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', image):
        raise ValueError('Use an immutable local image ID')
    if project not in ('requests', 'pytest') or network not in ('none', 'bridge'):
        raise ValueError('Unexpected project/network')
    if timeout < 1:
        raise ValueError('Positive command timeout required')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', context) or not 1 <= memory_gib <= 16:
        raise ValueError('Explicit Docker context and bounded memory required')
    auth_file = Path(auth_file)
    if auth_file.is_symlink() or not auth_file.is_file():
        raise ValueError('Regular auth file required')
    state = Path(state)
    state.mkdir(mode=0o700, parents=True, exist_ok=False)
    state = state.resolve()
    (state / 'sessions').mkdir(mode=0o700)
    auth_file = auth_file.resolve()

    def launch(workspace, args):
        workspace = Path(workspace).resolve()
        if workspace == state or workspace in state.parents or state in workspace.parents:
            raise ValueError('Session state must be separate from project')
        if workspace == auth_file or workspace in auth_file.parents:
            raise ValueError('Credentials must not be inside project')
        translated = translated_args(workspace, args)
        return [sys.executable, str(Path(__file__).resolve()), '--image', image,
            '--auth-file', str(auth_file), '--state', str(state),
            '--workspace', str(workspace), '--project', project, '--network', network,
            '--context', context, '--memory-gib', str(memory_gib),
            '--timeout', str(timeout), '--', *translated]
    return launch


def execute(args):
    name = 'qh-swe-solver-' + uuid.uuid4().hex
    owner = uuid.uuid4().hex
    state = args.state.resolve()
    lifecycle = dict(name=name, network=args.network, project=args.project,
                     context=args.context, memory_gib=args.memory_gib,
                     command_timeout=args.timeout, interrupted=False)
    prefix = ['docker', '--context', args.context]
    def docker(*argv, check=True):
        return subprocess.run([*prefix, *argv], text=True, capture_output=True,
                              timeout=30, check=check)
    def terminate(signum, frame):
        raise InterruptedError('Runner interrupted')
    # Refuse a repeated attempt before installing handlers or touching artifacts.
    with (state / 'started.json').open('x') as stream:
        json.dump(lifecycle, stream)
    previous = signal.signal(signal.SIGTERM, terminate)
    result = 1
    try:
        command = [
            'create', '--name', name, '--label', 'qh.solver.owner=' + owner,
            '--pull', 'never', '--platform', 'linux/amd64', '--network', args.network,
            '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--memory', str(args.memory_gib) + 'g', '--cpus', '2', '--pids-limit', '256',
            '--tmpfs', '/run/codex-home:rw,noexec,nosuid,nodev,mode=0700',
            '--mount', f'type=bind,src={args.auth_file},dst=/run/codex-auth.json,readonly',
            '--mount', f'type=bind,src={args.workspace},dst=/testbed',
            '--mount', f'type=bind,src={state / "sessions"},dst=/run/codex-home/sessions',
            '-e', 'CODEX_HOME=/run/codex-home',
            '-e', 'PYTEST_DISABLE_PLUGIN_AUTOLOAD=1',
            '-e', 'PYTHONPATH=' + ('/testbed' if args.project == 'requests' else '/testbed/src'),
            '-e', 'HTTPBIN_URL=http://httpbin/', '--workdir', '/testbed',
            '--entrypoint', '/bin/sh', args.image, '-c',
            'set -eu; install -m 600 /run/codex-auth.json /run/codex-home/auth.json; '
            'exec timeout --signal=TERM --kill-after=3 "$@"',
            'sh', str(args.timeout), *args.command,
        ]
        lifecycle['container_id'] = docker(*command).stdout.strip()
        # Connect only when needed. Explicit address never occupies timeout-test
        # tarpit10.255.255.1. Serial schedule must release this address each cell.
        if args.project == 'requests':
            docker('network', 'connect', '--ip', '10.255.255.5',
                   'qh-swelite-contract-01', name)
        result = subprocess.call([*prefix, 'start', '--attach', name])
        inspected = json.loads(docker('inspect', name).stdout)[0]
        lifecycle['container_exit_code'] = inspected['State']['ExitCode']
        lifecycle['mount_targets'] = [m['Destination'] for m in inspected['Mounts']]
        lifecycle['networks'] = sorted(inspected['NetworkSettings']['Networks'])
        lifecycle['oom_killed'] = inspected['State']['OOMKilled']
        lifecycle['timed_out'] = (True if lifecycle['container_exit_code'] == 124
                                  else None if lifecycle['container_exit_code'] == 137 else False)
        # Docker start's status alone is not the model's container exit status.
        result = lifecycle['container_exit_code'] if result == 0 else result
    except InterruptedError:
        lifecycle['interrupted'] = True
        result = 143
    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        try:
            record = inspected_container(docker('inspect', name, check=False), name)
            if record is not None:
                if record['Config']['Labels'].get('qh.solver.owner') != owner:
                    raise RuntimeError('Refusing cleanup of unowned container')
                docker('stop', '--time', '1', name)
                docker('rm', name)
            lifecycle['removed'] = inspected_container(docker('inspect', name, check=False), name) is None
        except Exception as error:
            lifecycle.update(removed=None, cleanup_error=type(error).__name__)
            raise
        finally:
            (state / 'lifecycle.json').write_text(json.dumps(lifecycle, indent=2) + '\n')
            signal.signal(signal.SIGTERM, previous)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    parser.add_argument('--auth-file', type=Path, required=True)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--project', choices=['requests', 'pytest'], required=True)
    parser.add_argument('--network', choices=['none', 'bridge'], required=True)
    parser.add_argument('--timeout', type=int, required=True)
    parser.add_argument('--context', required=True)
    parser.add_argument('--memory-gib', type=int, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    options = parser.parse_args()
    if options.command[:1] == ['--']:
        options.command.pop(0)
    raise SystemExit(execute(options))
