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


def extract(source, cli_events):
    if source.is_symlink() or not source.is_file() or source.stat().st_size > LIMIT:
        raise ValueError('Expected a regular rollout of at most 50 MB')
    raw = source.read_bytes()
    if len(raw) > LIMIT:
        raise ValueError('Rollout exceeded size limit while reading')
    events = [json.loads(line) for line in cli_events.read_text().splitlines()]
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
                   source_lines=len(records), records=selected,
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
