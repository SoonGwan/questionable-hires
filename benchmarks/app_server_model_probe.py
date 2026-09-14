#!/usr/bin/env python3
"""One diagnostic model turn; not an equal-condition performance benchmark.

Python 3.11+ for reading configuration names without copying credential material.
Personal rules/hooks remain in force. Never silently retry a model turn.
"""
import argparse
import json
import os
from pathlib import Path
import time
import tomllib

from app_server_capture_probe import Connection
from run import prepare


def launch_args():
    codex_root = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    config_path = codex_root / 'config.toml'
    config = tomllib.loads(config_path.read_text()) if config_path.exists() else {}
    overrides = ['notify=[]', 'features.plugins=false', 'features.multi_agent=false']
    for name in config.get('mcp_servers', {}):
        overrides.append('mcp_servers.' + json.dumps(name) + '.enabled=false')
    roots = [Path.home() / '.agents/skills', Path.home() / '.codex/skills', codex_root / 'skills']
    paths = sorted({str(p.resolve()) for root in roots if root.is_dir()
                    for p in root.rglob('SKILL.md')})
    overrides.append('skills.config=[' + ','.join(
        '{path=' + json.dumps(p) + ',enabled=false}' for p in paths) + ']')
    args = ['codex', 'app-server', '--stdio']
    for value in overrides:
        args.extend(['-c', value])
    return args


def run(output):
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    case = json.loads(Path(__file__).with_name('cli-yield-probe-01-cases.json').read_text())[0]
    project = output / 'project'
    revision = prepare(case, project)
    args = launch_args()
    (output / 'launch.json').write_text(json.dumps(dict(args=args, fixture_revision=revision,
        model='gpt-6-astra', effort='medium', limitation='Personal config/rules/hooks are not globally ignored; not comparable performance costs.'), indent=2) + '\n')
    connection = Connection(output, args=args, cwd=project)
    started = time.monotonic()
    try:
        response, _ = connection.request('initialize', dict(clientInfo=dict(
            name='questionable_hires_model_capture', version='0.1.0')), 0)
        if 'error' in response:
            raise RuntimeError(response['error'])
        connection.send(dict(method='initialized', params={}))
        response, _ = connection.request('thread/start', dict(
            model='gpt-6-astra', cwd=str(project), sandbox='workspace-write',
            approvalPolicy='never', ephemeral=True,
            config={'model_reasoning_effort': 'medium'}), 1)
        if 'error' in response:
            raise RuntimeError(response['error'])
        result = response['result']
        if result['model'] != 'gpt-6-astra':
            raise RuntimeError('Unexpected model; no turn started')
        thread = result['thread']['id']
        response, notifications = connection.request('turn/start', dict(
            threadId=thread, model='gpt-6-astra', effort='medium',
            input=[dict(type='text', text=case['task'])]), 2)
        if 'error' in response:
            raise RuntimeError(response['error'])
        turn = response['result']['turn']['id']
        deadline = time.monotonic() + 240
        while True:
            for event in notifications:
                if ('method' in event and 'id' in event):
                    raise RuntimeError('Unexpected server request; no action authorized')
                if event.get('method') == 'turn/completed':
                    params = event['params']
                    if params['threadId'] == thread and params['turn']['id'] == turn:
                        outcome = dict(turn=params['turn'], elapsed_seconds=time.monotonic()-started)
                        (output / 'outcome.json').write_text(json.dumps(outcome, indent=2) + '\n')
                        return outcome
            remaining = deadline-time.monotonic()
            if remaining <= 0:
                connection.send(dict(id=3, method='turn/interrupt', params=dict(threadId=thread)))
                raise TimeoutError('Diagnostic turn exceeded 240 seconds; raw stream retained')
            message = connection.messages.get(timeout=remaining)
            if isinstance(message, Exception):
                raise message
            notifications = [message]
    finally:
        connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))
