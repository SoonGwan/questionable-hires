#!/usr/bin/env python3
"""Prospective display-contract clarification; frozen prior gates stay unchanged."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLARIFICATION = (
    'For normal overlapping completion, require the latest result after both requests '
    'finish. While the newer request is pending, no particular intermediate display '
    'is required: retaining the previously displayed result is allowed. Do not make '
    'an older response appearing during that interval a required behavior. The '
    'reversed-completion test must still detect an older response overwriting the '
    'completed latest result.')


def cases():
    result = json.loads((ROOT / 'bundle-contract-cases.json').read_text())
    for case in result:
        if case['id'] == 'search-order':
            case['task'] += '\n' + CLARIFICATION
            case['files']['requirements.md'] += CLARIFICATION + '\n'
            case['criteria'].append(CLARIFICATION)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    with args.output.open('x') as stream:
        json.dump(cases(), stream, indent=2)
        stream.write('\n')
