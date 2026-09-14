#!/usr/bin/env python3
"""Reconcile four frozen capture diagnostics; never run the model or emitter."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNS = ('cli-output-probe-01', 'cli-output-probe-02',
        'cli-yield-probe-01', 'cli-yield-control-02')


def verify(name):
    case = json.loads((ROOT / (name + '-cases.json')).read_text())[0]
    cell = ROOT / 'results' / name / (case['id'] + '--baseline--1')
    project = cell / 'project'
    for path, contents in case['files'].items():
        assert (project / path).read_bytes() == contents.encode(), path
    events = [json.loads(line) for line in (cell / 'events.jsonl').read_text().splitlines()]
    commands = [e['item'] for e in events if e['type'] == 'item.completed'
                and e.get('item', {}).get('type') == 'command_execution']
    assert commands == json.loads((cell / 'commands.json').read_text())
    final = json.loads([e['item']['text'] for e in events if e['type'] == 'item.completed'
                       and e.get('item', {}).get('type') == 'agent_message'][-1])
    meta = json.loads((cell / 'metadata.json').read_text())
    assert meta['usage'] == next(e['usage'] for e in events if e['type'] == 'turn.completed')
    assert meta['completed'] and not meta['timed_out'] and meta['exit_code'] == 0
    assert meta['arm'] == 'baseline' and meta['skill_sha256'] is None
    modes = ('tiny', 'bulk', 'chunked') if name.startswith('cli-output') else ('delayed',)
    assert len(commands) == len(modes)
    assert set(p.name for p in project.iterdir()) == set(case['files']) | {
        'witness-' + mode + '.json' for mode in modes}
    rows = []
    for mode, command in zip(modes, commands):
        suffix = '' if mode == 'delayed' else ' ' + mode
        assert command['command'] == "/bin/zsh -lc 'python3 -B emit.py" + suffix + "'"
        assert command['exit_code'] == 0
        witness = json.loads((project / ('witness-' + mode + '.json')).read_text())
        start = 'BEGIN ' + mode + ' ' + witness['first'] + '\n'
        end = 'END ' + mode + ' ' + witness['last'] + '\n'
        middle = '' if mode == 'delayed' else ''.join(
            'ROW %04d ' % n + 'x' * 120 + '\n' for n in range(witness['rows']))
        expected = (start + middle + end).encode()
        assert len(expected) == witness['bytes']
        assert hashlib.sha256(expected).hexdigest() == witness['sha256']
        answer = final if mode == 'delayed' else final[mode]
        assert all(answer[key] == witness[key] for key in ('first', 'last'))
        assert answer['exit_code'] == 0
        captured = command['aggregated_output'].encode()
        assert captured == (end.encode() if mode == 'delayed' else expected)
        if mode == 'delayed':
            for event in events:
                item = event.get('item', {})
                if item.get('type') == 'command_execution':
                    assert witness['first'] not in json.dumps(item)
            assert final['live_session_poll_needed'] == (name == 'cli-yield-probe-01')
        rows.append({'mode': mode, 'expected_bytes': len(expected),
                     'captured_bytes': len(captured), 'both_nonces_in_final': True})
    return {'run': name, 'outputs': rows}


if __name__ == '__main__':
    print(json.dumps([verify(name) for name in RUNS], indent=2))
