#!/usr/bin/env python3
"""Render the frozen bundle-02 cost comparison, without scoring outcomes."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def render(data, dark=False):
    background, label, neutral, blue = ('#0F0F10', '#F7F7F8', '#C2C4C8', '#3385FF') if dark else (
        '#F7F7F8', '#171719', '#2E2F33', '#0066FF')
    cases = list(dict.fromkeys(row['case'] for row in data['rows']))
    rows = {(r['case'], r['arm']): r for r in data['rows']}
    assert len(cases) == 9 and len(rows) == len(data['rows']) == 18
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="750" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">',
           '<title id="title">Current bundle: resource use mostly increased</title>',
           '<desc id="desc">Nine exposed tasks, one fresh baseline and skill session per task. Points show percentage changes in tokens and process time. Eight tasks increase in each metric. Outcomes and verification differ; missing evidence is retained.</desc>',
           f'<rect width="1200" height="750" fill="{background}"/>',
           f'<g font-family="Arial, Helvetica, sans-serif" fill="{label}">']

    def text(x, y, value, size=18, anchor='start'):
        svg.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{html.escape(value)}</text>')

    text(36, 44, 'Current bundle. Higher costs in most tasks.', 30)
    text(36, 78, 'GPT-6 Astra · medium · 9 tasks × 2 arms × 1 repeat · resources e02c9bb')
    text(36, 105, 'Change from no-skill baseline · lower resource use is better · task outcomes differ', 17)
    metrics = [('Total tokens', lambda r: r['usage']['input_tokens'] + r['usage']['output_tokens'], 310),
               ('Process time', lambda r: r['elapsed_seconds'], 790)]
    for heading, metric, start in metrics:
        text(start, 143, heading, 21)
        for tick in (-20, 0, 20, 40, 60):
            x = start + (tick + 25) * 3.2
            svg.append(f'<line x1="{x}" x2="{x}" y1="185" y2="605" stroke="{neutral}" opacity="{0.65 if tick == 0 else 0.15}" stroke-dasharray="{4 if tick == 0 else 0}"/>')
            text(x, 174, f'{tick:+d}%' if tick else '0%', 14, 'middle')
        for index, case in enumerate(cases):
            y = 213 + index * 46
            base, candidate = metric(rows[(case, 'baseline')]), metric(rows[(case, 'skill')])
            assert base > 0
            change = 100 * (candidate / base - 1)
            assert -25 <= change <= 75, 'Update axis bounds explicitly for new data'
            x, zero = start + (change + 25) * 3.2, start + 80
            svg.append(f'<line x1="{zero}" x2="{x}" y1="{y}" y2="{y}" stroke="{blue}" stroke-width="3"/>')
            svg.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{blue}"/>')
            text(start + 375, y + 6, f'{change:+.1f}%', 17, 'end')
        total_base = sum(metric(rows[(case, 'baseline')]) for case in cases)
        total_skill = sum(metric(rows[(case, 'skill')]) for case in cases)
        text(start, 637, f'Sum change: {100 * (total_skill / total_base - 1):+.2f}%', 21)
    for index, case in enumerate(cases):
        text(36, 219 + index * 46, case)
    text(36, 677, '18/18 sessions completed; not 18/18 verified successes. No retries or exclusions.', 17)
    text(36, 704, 'Cached input included once. Shared host/cache; unequal checks and missing QA output. No superiority claim.', 16)
    text(36, 730, 'Sum ratios differ from the original chart’s equal-task mean ratios. See BUNDLE-CURRENT-02-REVIEW.md.', 16)
    return '\n'.join(svg + ['</g></svg>']) + '\n'


if __name__ == '__main__':
    data = json.loads((ROOT / 'results/bundle-current-02-costs.json').read_text())
    for dark in (False, True):
        name = 'bundle-current-02-' + ('dark' if dark else 'light') + '.svg'
        (ROOT / 'results' / name).write_text(render(data, dark))
        print(name)
