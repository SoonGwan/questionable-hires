#!/usr/bin/env python3
"""Decompose recorded usage without inventing per-command token attribution."""
import argparse
import json
from pathlib import Path


def inspect(events):
    records = []
    for event in events:
        if not isinstance(event, dict):
            raise ValueError('Expected event objects')
        if 'usage' not in event:
            continue
        if event.get('type') != 'turn.completed':
            raise ValueError('Unsupported usage event; inspect its accounting semantics')
        usage = event['usage']
        if not isinstance(usage, dict):
            raise ValueError('Expected usage object')
        values = {}
        for key in ('input_tokens', 'cached_input_tokens', 'output_tokens'):
            value = usage.get(key)
            if type(value) is not int or value < 0:
                raise ValueError('Missing or invalid token count: ' + key)
            values[key] = value
        if values['cached_input_tokens'] > values['input_tokens']:
            raise ValueError('Cached input exceeds total input')
        records.append(values)
    # Current ephemeral benchmark cells contain one turn. Multiple records may
    # be cumulative or incremental; do not silently sum ambiguous counters.
    if len(records) != 1:
        raise ValueError('Expected exactly one completed-turn usage record')
    usage = records[0]
    return dict(cached_input_tokens=usage['cached_input_tokens'],
                uncached_input_tokens=usage['input_tokens'] - usage['cached_input_tokens'],
                output_tokens=usage['output_tokens'],
                total_tokens=usage['input_tokens'] + usage['output_tokens'],
                limitation='Cached input remains part of total tokens. This log does not '
                           'attribute tokens or latency to commands, skill text or model decisions. '
                           'No cost estimate or causal explanation follows from this decomposition.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('logs', type=Path, nargs='+')
    args = parser.parse_args()
    for path in args.logs:
        events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        print(json.dumps(dict(log=str(path), **inspect(events))))
