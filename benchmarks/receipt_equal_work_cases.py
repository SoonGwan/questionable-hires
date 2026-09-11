#!/usr/bin/env python3
"""Make historical verification explicit without prescribing a helper."""
import argparse
import json
from pathlib import Path


def cases():
    result = json.loads(Path(__file__).with_name('receipt-package-cases.json').read_text())
    case = result[0]
    case['id'] = 'receipt-explicit-history'
    case['task'] = (
        'Verify the committed record-decoding fix by executing the same current '
        'regression tests and sample data against the implementation before the '
        'fix and the implementation after it. Use the documented test runner '
        'and identify the actual implementation revisions exercised. Check that '
        'the original failure concerns separators inside values, and retain the '
        'simple and empty-value controls. Keep comparisons in disposable '
        'project-local copies; do not modify original files, install dependencies '
        'or use external services.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
