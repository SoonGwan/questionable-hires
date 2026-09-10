#!/usr/bin/env python3
"""Export the reviewed transfer experiment and compute raw condition summaries."""
import argparse
import json
from pathlib import Path
import shutil
import statistics

from export import export
from scan_evidence import scan


def summarize(rows):
    result = {}
    for condition in ('baseline', 'original', 'candidate'):
        subset = [r for r in rows if r['condition'] == condition]
        metrics = {}
        for metric in ('total_tokens', 'elapsed_seconds'):
            values = [r[metric] for r in subset if r.get('completed') and r.get(metric) is not None]
            metrics[metric] = dict(n=len(values), mean=statistics.mean(values) if values else None,
                                   sd=statistics.stdev(values) if len(values) > 1 else None,
                                   min=min(values) if values else None, max=max(values) if values else None)
        result[condition] = dict(scheduled=len(subset), completed=sum(r['completed'] for r in subset),
                                 strict_success=sum(r['completed'] and r['scope'] == 'pass' and all(c == 'pass' for c in r['criteria']) for r in subset),
                                 metrics=metrics)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    reviews = json.loads((args.run / 'reviews.json').read_text())
    index = {(r['block'], r['condition'], r['case']): r for r in reviews}
    if len(index) != len(reviews) or len(index) != 27:
        raise ValueError('Expected 27 distinct reviewed cells')
    blocks = json.loads((args.run / 'blocks.json').read_text())
    if len(blocks) != 9 or any(r['exit_code'] or r['stopped_after_limit'] for r in blocks):
        raise ValueError('This export requires all nine blocks completed; preserve partial experiments separately')
    args.output.mkdir(parents=True, exist_ok=False)
    rows = []
    for record in blocks:
        block, condition = record['block'], record['condition']
        name = f'block-{block}-{condition}'
        export(args.run / name, args.output / name)
        for cell in sorted((args.output / name).glob('*--*')):
            meta = json.loads((cell / 'metadata.json').read_text())
            review = index[(block, condition, meta['case'])]
            usage = meta.get('usage') or {}
            total = usage['input_tokens'] + usage['output_tokens'] if 'input_tokens' in usage and 'output_tokens' in usage else None
            rows.append(dict(review, cell=f'{name}/{cell.name}', completed=meta['completed'],
                             total_tokens=total, elapsed_seconds=meta.get('elapsed_seconds'), usage=usage))
    for name in ('reviews.json', 'blocks.json', 'snapshots.json'):
        shutil.copyfile(args.run / name, args.output / name)
    report = dict(method='Raw arithmetic mean over nine cells per condition; input includes cached tokens, total=input+output; sample SD across heterogeneous tasks, not a confidence interval.',
                  reviewer='Author review, unblinded, against preregistered criteria; all original production files compared to fixture contents.',
                  conditions=summarize(rows), cells=rows)
    (args.output / 'metrics.json').write_text(json.dumps(report, indent=2) + '\n')
    findings = scan(args.output)
    if findings:
        print(json.dumps(findings, indent=2))
        raise SystemExit('Export retained but requires privacy review; do not publish yet')
    print(f'Exported {len(rows)} reviewed cells. Pattern scan clear; manual privacy review still required.')


if __name__ == '__main__':
    main()
