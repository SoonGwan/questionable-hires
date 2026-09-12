#!/usr/bin/env python3
"""Recompute the focused chart values from sanitized per-cell records."""
import argparse
import json
from pathlib import Path
import statistics


def summarize(rows):
    arms = {'baseline', 'skill'}
    indexed = {(row['case'], row['arm']): row for row in rows}
    cases = sorted({row['case'] for row in rows})
    if len(indexed) != len(rows) or set(row['arm'] for row in rows) != arms:
        raise ValueError('Expected unique baseline and skill records')
    if any((case, arm) not in indexed for case in cases for arm in arms):
        raise ValueError('Every case requires both arms')
    for row in rows:
        if row['cached_input_tokens'] > row['input_tokens']:
            raise ValueError('Cached input cannot exceed input')
        if any(row[field] < 0 for field in ('input_tokens', 'cached_input_tokens',
                                            'output_tokens', 'elapsed_seconds')):
            raise ValueError('Resource values must be nonnegative')

    def value(row, metric):
        return row['input_tokens'] + row['output_tokens'] if metric == 'total_tokens' else row[metric]

    ratios = {}
    for metric in ('total_tokens', 'elapsed_seconds'):
        ratios[metric] = {'baseline': 100.0, 'skill': round(statistics.mean(
            100 * value(indexed[(case, 'skill')], metric) /
            value(indexed[(case, 'baseline')], metric) for case in cases), 1)}
    return dict(cases=len(cases), resource_ratios=ratios,
                quality={arm: sum(bool(indexed[(case, arm)]['quality_target_met'])
                                  for case in cases) for arm in arms},
                clean_false_positives={arm: sum(bool(indexed[(case, arm)]['clean_false_positive'])
                                                for case in cases) for arm in arms},
                raw_sums={arm: {
                    'total_tokens': sum(value(indexed[(case, arm)], 'total_tokens') for case in cases),
                    'elapsed_seconds': round(sum(value(indexed[(case, arm)], 'elapsed_seconds')
                                                 for case in cases), 3)} for arm in arms})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    summary = summarize(json.loads((args.directory / 'cells.json').read_text()))
    published = json.loads((args.directory / 'data.json').read_text())
    for key in ('cases', 'resource_ratios', 'quality', 'clean_false_positives'):
        if published[key] != summary[key]:
            raise ValueError(f'Published {key} does not match cell evidence')
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
