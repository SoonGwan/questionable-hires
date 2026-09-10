#!/usr/bin/env python3
"""Rebuild descriptive metrics and Montage SVGs from exported cell evidence."""
import argparse
from collections import defaultdict
import html
import json
import math
from pathlib import Path
import statistics

ARMS = ('baseline', 'control', 'skill')
IMPLEMENTATION = {'boundary-fix', 'label-change'}
METRICS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'total_tokens', 'elapsed_seconds', 'changed_loc')


def stats(values):
    values = list(values)
    return {'n': len(values), 'mean': statistics.mean(values) if values else None,
            'sd': statistics.stdev(values) if len(values) > 1 else None,
            'min': min(values) if values else None, 'max': max(values) if values else None}


def ratio(value, baseline):
    return None if baseline == 0 else 100 * value / baseline


def diff_loc(diff):
    """Count physical text lines in final diff; exclude skill/cache files."""
    result = {'production': 0, 'tests': 0}
    path = ''
    for line in diff.splitlines():
        if line.startswith('diff --git '):
            path = line.split(' b/', 1)[-1]
        elif line.startswith(('+++', '---')):
            continue
        elif line.startswith(('+', '-')) and path:
            if any(part in {'.agents', '__pycache__'} for part in Path(path).parts):
                continue
            bucket = 'tests' if Path(path).name.startswith('test_') or 'tests' in Path(path).parts else 'production'
            result[bucket] += 1
    return result


def read_cells(directory):
    rows = []
    for cell in sorted(directory.glob('*--*')):
        row = json.loads((cell / 'metadata.json').read_text())
        row['cell'] = cell.name
        usage = row.get('usage') or {}
        for name in METRICS[:3]:
            row[name] = usage.get(name)
        input_, cached, output = (row[name] for name in METRICS[:3])
        if any(v is not None and (not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0)
               for v in (input_, cached, output)):
            raise ValueError(f'Invalid token usage: {cell.name}')
        if input_ is not None and cached is not None and cached > input_:
            raise ValueError(f'Cached input exceeds input: {cell.name}')
        row['total_tokens'] = input_ + output if input_ is not None and output is not None else None
        row['uncached_input_tokens'] = input_ - cached if input_ is not None and cached is not None else None
        diff = cell / 'changes.diff'
        loc = diff_loc(diff.read_text()) if diff.exists() else None
        row['loc_by_type'] = loc
        row['changed_loc'] = sum(loc.values()) if loc is not None and row['case'] in IMPLEMENTATION else None
        rows.append(row)
    return rows


def summarize(rows):
    keys = [(r['case'], r['arm'], r['repeat']) for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError('Duplicate cell')
    if any(r['arm'] not in ARMS for r in rows):
        raise ValueError('Only the preregistered three arms are supported')
    normalized = {}
    for metric in METRICS:
        blocks = defaultdict(dict)
        for row in rows:
            if metric == 'changed_loc' and row['case'] not in IMPLEMENTATION:
                continue
            blocks[(row['case'], row['repeat'])][row['arm']] = row
        means = defaultdict(lambda: defaultdict(list))
        eligible = 0
        for (case, repeat), arms in blocks.items():
            if all(a in arms and arms[a].get('completed') and not arms[a].get('timed_out')
                   and arms[a].get(metric) is not None for a in ARMS):
                eligible += 1
                for arm in ARMS:
                    means[case][arm].append(arms[arm][metric])
        case_ratios, zero = {}, []
        for case, arms in sorted(means.items()):
            base = statistics.mean(arms['baseline'])
            if base == 0:
                zero.append(case)
                continue
            case_ratios[case] = {arm: ratio(statistics.mean(arms[arm]), base) for arm in ARMS}
        normalized[metric] = {'eligible_blocks': eligible, 'excluded_blocks': len(blocks) - eligible,
                              'zero_baseline_cases': zero, 'included_cases': len(case_ratios),
                              'case_ratios': case_ratios,
                              'arms': {a: stats(v[a] for v in case_ratios.values()) for a in ARMS}}
    per_case = {}
    for case in sorted({r['case'] for r in rows}):
        per_case[case] = {a: {m: stats(r[m] for r in rows if r['case'] == case and r['arm'] == a and r.get(m) is not None)
                              for m in METRICS} for a in ARMS}
    execution = {}
    for a in ARMS:
        cells = [r for r in rows if r['arm'] == a]
        execution[a] = {'scheduled': len(cells), 'attempted': sum(r.get('attempted', True) for r in cells),
                        'completed': sum(bool(r.get('completed')) for r in cells),
                        'timeouts': sum(bool(r.get('timed_out')) for r in cells),
                        'missing_usage': sum(r.get('usage') is None for r in cells),
                        'all_attempt_wall_seconds': stats(r['elapsed_seconds'] for r in cells if r.get('elapsed_seconds') is not None)}
    return {'method': 'Equal-weight arithmetic mean of case arithmetic-mean ratios; paired-complete blocks; range is across task ratios, not CI.',
            'normalized': normalized, 'per_case_raw': per_case, 'execution': execution, 'cells': rows}


def svg_chart(summary, theme):
    dark = theme == 'dark'
    bg, fg, neutral, blue = ('#0F0F10', '#F7F7F8', '#C2C4C8', '#3385FF') if dark else ('#F7F7F8', '#171719', '#2E2F33', '#0066FF')
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-labelledby="title desc">',
             '<title id="title">Repeated synthetic comparison: baseline = 100%</title>',
             '<desc id="desc">Grouped bars for total tokens, elapsed time, and implementation-only changed lines. Labeled baseline, control, skill. Whiskers show range across task ratios, not confidence intervals. Quality is separate.</desc>',
             f'<rect width="1200" height="760" fill="{bg}"/>',
             f'<g font-family="Arial, sans-serif" fill="{fg}">']
    def text(x, y, value, size=18, anchor='start'):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{html.escape(str(value))}</text>')
    text(44, 48, 'Same ticket. Three coworkers.', 30)
    text(44, 80, 'GPT-6 Astra · medium · 8 synthetic tasks × 3 arms × 3 repeats', 18)
    text(44, 110, 'No-skill baseline = 100% · descriptive results, no superiority claim', 17)
    metrics = [('total_tokens', 'Total tokens', 'Input (cache included) + output'),
               ('elapsed_seconds', 'Elapsed time', 'Process wall time'),
               ('changed_loc', 'Changed lines · implementation only', 'Added + deleted; lower is not inherently better')]
    for panel, (metric, label, sub) in enumerate(metrics):
        x0 = 44 + panel * 390
        data = summary['normalized'][metric]
        values = data['arms']
        ceiling = max(150, max((v['max'] or 0) for v in values.values()) * 1.2)
        ceiling = math.ceil(ceiling / 50) * 50
        ybottom, height = 448, 235
        text(x0, 155, label, 19)
        text(x0, 180, sub, 12)
        for tick in range(0, int(ceiling) + 1, max(50, int(math.ceil(ceiling / 5 / 50) * 50))):
            y = ybottom - tick / ceiling * height
            parts.append(f'<path d="M{x0+35} {y}h300" stroke="{neutral}" stroke-opacity="0.18"/>')
            text(x0+30, y+4, f'{tick}%', 11, 'end')
        ybase = ybottom - 100 / ceiling * height
        parts.append(f'<path d="M{x0+35} {ybase}h300" stroke="{neutral}" stroke-dasharray="4 4" stroke-opacity="0.88"/>')
        for j, arm in enumerate(ARMS):
            x = x0 + 58 + 94 * j
            value = values[arm]
            mean = value['mean']
            if mean is None:
                text(x+27, ybottom-12, 'N/A', 16, 'middle')
            else:
                h = mean / ceiling * height
                color = blue if arm == 'skill' else neutral
                opacity = '0.42' if arm == 'baseline' else '0.88' if arm == 'control' else '1'
                parts.append(f'<rect x="{x}" y="{ybottom-h}" width="54" height="{h}" fill="{color}" fill-opacity="{opacity}"/>')
                lo, hi = (ybottom - value[k] / ceiling * height for k in ('min', 'max'))
                parts.append(f'<path d="M{x+27} {lo}V{hi} M{x+19} {lo}h16 M{x+19} {hi}h16" stroke="{fg}" fill="none"/>')
                text(x+27, hi-10, f'{mean:.1f}%', 15, 'middle')
            text(x+27, 474, arm, 15, 'middle')
        text(x0, 503, f"{data['included_cases']} tasks · {data['eligible_blocks']} complete blocks · {data['excluded_blocks']} excluded", 13)
        text(x0, 525, f"Zero-baseline exclusions: {len(data['zero_baseline_cases'])}", 12)
    text(44, 572, 'Quality and execution · absolute counts out of 24 scheduled per arm', 20)
    quality = summary.get('quality', {})
    for j, arm in enumerate(ARMS):
        x = 44 + j*390
        e = summary['execution'][arm]
        q = quality.get(arm, {})
        text(x, 605, f"{arm}: completed {e['completed']}/{e['scheduled']} · timeout {e['timeouts']}", 16)
        text(x, 631, f"Task success {q.get('success', 'pending')}/{e['scheduled']} · scope {q.get('scope_pass', 'pending')}/{e['scheduled']}", 15)
        text(x, 655, f"Regressions: {q.get('regressions', 'pending')} · scope unknown: {q.get('scope_unknown', 'pending')}", 14)
    text(44, 701, 'Bars: mean of task mean ratios. Whiskers: task-ratio min–max, not confidence intervals.', 15)
    text(44, 727, 'n=3 per task/arm. Shared host/cache. No dollar estimate. See report for raw values and criterion evidence.', 15)
    parts.append('</g></svg>')
    return '\n'.join(parts) + '\n'


def markdown_tables(summary):
    lines = ['# Generated descriptive tables', '', 'Rebuilt by `benchmarks/aggregate.py`. All raw values are in `aggregate.json`. No confidence intervals or dollar billing estimates.', '',
             '## Normalized resource metrics', '', 'Equal-weight mean of task mean ratios. Brackets show task-ratio min–max, not confidence intervals.', '',
             '| Metric | Baseline | Control | Skill | Tasks / complete blocks |', '| --- | ---: | ---: | ---: | ---: |']
    for metric, data in summary['normalized'].items():
        values = []
        for arm in ARMS:
            v = data['arms'][arm]
            values.append('N/A' if v['mean'] is None else f"{v['mean']:.1f}% [{v['min']:.1f}, {v['max']:.1f}]")
        lines.append('| ' + ' | '.join([metric] + values + [f"{data['included_cases']} / {data['eligible_blocks']}"]) + ' |')
    lines += ['', '## Raw values by task and arm', '', 'Arithmetic mean ± sample SD over n=3; all observed values, including any censored termination times. LOC is implementation-only churn.', '',
              '| Task | Arm | Total tokens | Wall seconds | Production / test changed LOC (mean) |', '| --- | --- | ---: | ---: | ---: |']
    for case, arms in summary['per_case_raw'].items():
        for arm, data in arms.items():
            def value(metric):
                v = data[metric]
                if v['mean'] is None:
                    return 'N/A'
                sd = f"{v['sd']:.2f}" if v['sd'] is not None else 'N/A'
                return f"{v['mean']:.2f} ± {sd} (n={v['n']})"
            loc = 'N/A'
            if case in IMPLEMENTATION:
                rows = [r for r in summary['cells'] if r['case'] == case and r['arm'] == arm and r['loc_by_type'] is not None]
                if rows:
                    loc = ' / '.join(f"{statistics.mean(r['loc_by_type'][k] for r in rows):.2f}" for k in ('production', 'tests'))
            lines.append(f"| {case} | {arm} | {value('total_tokens')} | {value('elapsed_seconds')} | {loc} |")
    if 'quality' in summary:
        lines += ['', '## Absolute quality and execution', '', 'Strict success requires completed execution, all three case criteria, and scope pass. Unknown is not success.', '',
                  '| Arm | Strict success | Scope pass | Scope fail / unknown | Observed regressions | Completed / timeout |', '| --- | ---: | ---: | ---: | ---: | ---: |']
        for arm in ARMS:
            q, e = summary['quality'][arm], summary['execution'][arm]
            n = e['scheduled']
            lines.append(f"| {arm} | {q['success']}/{n} ({100*q['success']/n:.1f}%) | {q['scope_pass']}/{n} | {q['scope_fail']} / {q['scope_unknown']} | {q['regressions']} | {e['completed']} / {e['timeouts']} |")
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--reviews', type=Path)
    args = parser.parse_args()
    summary = summarize(read_cells(args.directory))
    manifest = json.loads((args.directory / 'run.json').read_text())
    if 'schedule' in manifest and set(manifest['schedule']) != {r['cell'] for r in summary['cells']}:
        raise ValueError('Evidence does not match scheduled cells')
    if args.reviews:
        reviews = json.loads(args.reviews.read_text())
        indexed = {r['cell']: r for r in reviews}
        if len(indexed) != len(reviews) or set(indexed) != {r['cell'] for r in summary['cells']}:
            raise ValueError('Review coverage mismatch')
        for review in reviews:
            if len(review.get('criteria', [])) != 3 or any(v not in {'pass', 'fail', 'unknown'} for v in review['criteria']):
                raise ValueError('Each review needs three explicit criterion verdicts')
            if review.get('scope') not in {'pass', 'fail', 'unknown'} or review.get('regression') not in {'observed', 'none_observed', 'unknown'}:
                raise ValueError('Invalid scope or regression verdict')
            if not review.get('evidence'):
                raise ValueError('Review must cite evidence')
        quality = {}
        for arm in ARMS:
            cells = [r for r in summary['cells'] if r['arm'] == arm]
            rr = [indexed[r['cell']] for r in cells]
            quality[arm] = {'success': sum(bool(r.get('completed')) and all(v == 'pass' for v in q['criteria']) and q['scope'] == 'pass' for r, q in zip(cells, rr)),
                            'scope_pass': sum(q['scope'] == 'pass' for q in rr),
                            'scope_fail': sum(q['scope'] == 'fail' for q in rr),
                            'scope_unknown': sum(q['scope'] == 'unknown' for q in rr),
                            'regressions': sum(q['regression'] == 'observed' for q in rr),
                            'regression_unknown': sum(q['regression'] == 'unknown' for q in rr),
                            'criteria_pass': [sum(q['criteria'][i] == 'pass' for q in rr) for i in range(3)]}
        summary['quality'] = quality
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'aggregate.json').write_text(json.dumps(summary, indent=2) + '\n')
    (args.output / 'tables.md').write_text(markdown_tables(summary))
    for theme in ('light', 'dark'):
        (args.output / f'comparison-{theme}.svg').write_text(svg_chart(summary, theme))


if __name__ == '__main__':
    main()
