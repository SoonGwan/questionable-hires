#!/usr/bin/env python3
"""Extract tool records from one explicitly selected, matching CLI session.

No model calls, session search, execution, or automatic publication. The full
rollout can contain private instructions; retain it only in local-run storage.
"""
import argparse
import hashlib
import json
from pathlib import Path

TOOL_TYPES = {'function_call', 'function_call_output',
              'custom_tool_call', 'custom_tool_call_output'}
LIMIT = 50_000_000


def command_output_candidates(selected, events):
    """Index possible stored stdout by text/exit; never infer command identity."""
    calls, outputs = {}, {}
    for record in selected:
        payload = record['record']['payload']
        call_id = payload.get('call_id')
        if isinstance(call_id, str) and call_id:
            group = outputs if payload['type'].endswith('_output') else calls
            group.setdefault(call_id, []).append(record)
    envelopes = []
    for call_id, records in outputs.items():
        parents = calls.get(call_id, [])
        if len(parents) != 1 or len(records) != 1 or parents[0]['line'] >= records[0]['line']:
            continue
        record, parent = records[0], parents[0]
        value = record['record']['payload'].get('output')
        blocks = [(None, value)] if isinstance(value, str) else [
            (index, block.get('text')) for index, block in enumerate(value if isinstance(value, list) else [])
            if isinstance(block, dict) and block.get('type') in ('input_text', 'text')]
        for index, text in blocks:
            try:
                envelope = json.loads(text) if isinstance(text, str) else None
            except ValueError:
                continue
            if (not isinstance(envelope, dict) or not isinstance(envelope.get('output'), str)
                    or type(envelope.get('exit_code')) is not int):
                continue
            output = envelope['output']
            identity = dict(call_id=call_id, call_line=parent['line'],
                            call_line_sha256=parent['line_sha256'],
                            output_line=record['line'], output_line_sha256=record['line_sha256'],
                            output_block_index=index, exit_code=envelope['exit_code'],
                            output_sha256=hashlib.sha256(output.encode()).hexdigest(),
                            output_chars=len(output))
            envelopes.append((output, identity))
    result = []
    for event_line, event in enumerate(events, 1):
        command = event.get('item', {})
        if event.get('type') != 'item.completed' or command.get('type') != 'command_execution':
            continue
        captured, exit_code = command.get('aggregated_output'), command.get('exit_code')
        matches = []
        if isinstance(captured, str) and captured and type(exit_code) is int:
            for output, identity in envelopes:
                if identity['exit_code'] == exit_code and output.endswith(captured):
                    matches.append(dict(identity, relation='equal' if output == captured else 'longer_suffix_match'))
        status = ('empty_cli_output' if captured == '' else
                  'single_candidate' if len(matches) == 1 else
                  'ambiguous' if len(matches) > 1 else 'unmatched')
        result.append(dict(command_id=command.get('id'), cli_event_line=event_line,
                           status=status, candidates=matches))
    return result


def extract(source, cli_events):
    if source.is_symlink() or not source.is_file() or source.stat().st_size > LIMIT:
        raise ValueError('Expected a regular rollout of at most 50 MB')
    raw = source.read_bytes()
    if len(raw) > LIMIT:
        raise ValueError('Rollout exceeded size limit while reading')
    event_raw = cli_events.read_bytes()
    events = [json.loads(line) for line in event_raw.splitlines()]
    ids = {event['thread_id'] for event in events if event.get('type') == 'thread.started'}
    if len(ids) != 1:
        raise ValueError('CLI events must identify exactly one thread')
    records = [json.loads(line) for line in raw.splitlines()]
    identities = [r['payload']['id'] for r in records if r.get('type') == 'session_meta']
    if identities != list(ids):
        raise ValueError('Rollout does not identify the requested CLI session')
    selected = []
    for index, (line, record) in enumerate(zip(raw.splitlines(), records), 1):
        if record.get('type') == 'response_item' and record.get('payload', {}).get('type') in TOOL_TYPES:
            selected.append(dict(line=index, line_sha256=hashlib.sha256(line).hexdigest(), record=record))
    calls = [r['record']['payload']['call_id'] for r in selected
             if not r['record']['payload']['type'].endswith('_output')]
    outputs = [r['record']['payload']['call_id'] for r in selected
               if r['record']['payload']['type'].endswith('_output')]
    summary = dict(session_id=identities[0], source_bytes=len(raw),
                   source_sha256=hashlib.sha256(raw).hexdigest(),
                   cli_events_sha256=hashlib.sha256(event_raw).hexdigest(),
                   source_lines=len(records), records=selected,
                   command_output_candidates=command_output_candidates(selected, events),
                   command_output_candidate_limitation='Candidates match unredacted output suffix and exit only, not command identity or complete stdout. Review the paired call input, order and any earlier chunks. Empty CLI output is never matched; ambiguous matches are never selected automatically.',
                   missing_output_call_ids=sorted(set(calls)-set(outputs)),
                   unmatched_output_call_ids=sorted(set(outputs)-set(calls)),
                   duplicate_call_ids=len(calls) != len(set(calls)),
                   duplicate_output_call_ids=len(outputs) != len(set(outputs)),
                   limitation='Selected stored response_item tool records only, not the full rollout or proof of complete model context. Review private content before export. Line hashes identify unredacted source lines without line terminators.')
    return raw, summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rollout', type=Path, required=True)
    parser.add_argument('--events', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='New local-only directory')
    args = parser.parse_args()
    raw, summary = extract(args.rollout, args.events)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'rollout.original.jsonl').write_bytes(raw)
    (args.output / 'tool-records.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'records'}, indent=2))
