"""Summarize recorded cumulative usage without exporting private context.

This reports counter advances, not API requests, wall-time attribution or billing.
Missing or inconsistent counters are errors, not reconstructed token estimates.
"""
import argparse
import json
from pathlib import Path
from extract_rollout_tools import extract

FIELDS = ('input_tokens', 'cached_input_tokens', 'output_tokens')


def summarize(raw, expected):
    previous = dict.fromkeys(FIELDS, 0)
    advances = []
    responses = {}
    duplicates = 0
    for number, line in enumerate(raw.splitlines(), 1):
        record = json.loads(line)
        payload = record.get('payload', {})
        if record.get('type') == 'token_usage_record':
            identity = payload.get('response_id')
            usage = payload.get('usage', {})
            if not isinstance(identity, str) or not identity or any(type(usage.get(k)) is not int or usage[k] < 0 for k in FIELDS):
                raise ValueError('Invalid response usage record')
            selected = {k: usage[k] for k in FIELDS}
            if selected['cached_input_tokens'] > selected['input_tokens']:
                raise ValueError('Invalid response cached usage')
            if identity in responses and any(responses[identity][k] != selected[k] for k in FIELDS):
                raise ValueError('Conflicting duplicate response usage')
            responses.setdefault(identity, dict(line=number, **selected))
            continue
        if record.get('type') != 'event_msg' or payload.get('type') != 'token_count':
            continue
        info = payload.get('info')
        if not info:
            continue
        total = info.get('total_token_usage', {})
        if any(type(total.get(k)) is not int or total[k] < previous[k] for k in FIELDS):
            raise ValueError('Missing, invalid or decreasing cumulative usage')
        current = {k: total[k] for k in FIELDS}
        if current == previous:
            duplicates += 1
            continue
        delta = {k: current[k] - previous[k] for k in FIELDS}
        if delta['cached_input_tokens'] > delta['input_tokens']:
            raise ValueError('Cached input exceeds input advance')
        advances.append(dict(line=number, **delta))
        previous = current
    if not advances:
        raise ValueError('No cumulative usage advances recorded')
    if any(type(expected.get(k)) is not int or expected[k] != previous[k] for k in FIELDS):
        raise ValueError('Stored cumulative usage does not match CLI final usage')
    if responses and any(sum(r[k] for r in responses.values()) != previous[k] for k in FIELDS):
        raise ValueError('Response usage does not reconcile with final cumulative usage')
    return dict(totals=previous, uncached_input_tokens=previous['input_tokens']-previous['cached_input_tokens'],
        total_tokens=previous['input_tokens']+previous['output_tokens'],
        recorded_advances=advances, duplicate_counter_records=duplicates,
        recorded_responses=list(responses.values()) if responses else None,
        limitation='Recorded cumulative counter advances only. Cache is a subset of input; reasoning is not added again to output. Advances need not map one-to-one to model requests. No text-based token estimates, billing, latency attribution or causal savings.')


def inspect(rollout, events):
    raw, identity = extract(Path(rollout), Path(events))
    cli = [json.loads(line) for line in Path(events).read_text().splitlines()]
    completed = [event for event in cli if event.get('type') == 'turn.completed']
    if len(completed) != 1:
        raise ValueError('Expected one completed CLI turn')
    result = summarize(raw, completed[0]['usage'])
    result.update(session_id=identity['session_id'], source_sha256=identity['source_sha256'])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rollout', type=Path, required=True)
    parser.add_argument('--events', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(inspect(args.rollout, args.events), indent=2))
