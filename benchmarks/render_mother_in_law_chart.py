#!/usr/bin/env python3
"""Render the focused interaction-skill checkpoint with Montage semantic colors."""
import argparse
import html
import json
from pathlib import Path


def render(data, dark=False):
    bg, fg, neutral, blue = (
        ('#0F0F10', '#F7F7F8', '#C2C4C8', '#3385FF') if dark else
        ('#F7F7F8', '#171719', '#2E2F33', '#0066FF'))
    metrics = data['resource_ratios']
    if set(metrics) != {'total_tokens', 'elapsed_seconds'}:
        raise ValueError('Expected token and elapsed ratios')
    if any(set(metrics[name]) != {'baseline', 'skill'} for name in metrics):
        raise ValueError('Every resource metric requires baseline and skill')
    quality = data['quality']
    quality_rows = data['quality_rows']
    cases = data['cases']
    if not 1 <= cases <= 10 or any(not 0 <= quality[arm] <= cases for arm in ('baseline', 'skill')):
        raise ValueError('Invalid case or quality counts')
    if not quality_rows or any(set(row) != {'label', 'baseline', 'skill'}
                               for row in quality_rows):
        raise ValueError('Quality rows require label, baseline and skill')

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" '
        'viewBox="0 0 1200 700" role="img" aria-labelledby="title desc">',
        f'<title id="title">{html.escape(data["title"])}</title>',
        f'<desc id="desc">{html.escape(data["description"])}</desc>',
        f'<rect width="1200" height="700" fill="{bg}"/>',
        f'<g font-family="Arial, sans-serif" fill="{fg}">',
    ]

    def text(x, y, value, size=16, anchor='start', opacity=1):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" '
                     f'text-anchor="{anchor}" opacity="{opacity}">{html.escape(str(value))}</text>')

    text(48, 55, data['title'], 30)
    text(48, 88, data['subtitle'], 17)
    text(48, 116, data['note'], 15, opacity=.78)
    panels = [
        ('total_tokens', 'Total tokens', 'Input (cache included) + output'),
        ('elapsed_seconds', 'Elapsed time', 'Process wall time'),
    ]
    for panel, (key, label, sublabel) in enumerate(panels):
        x0 = 48 + panel * 390
        text(x0, 170, label, 20)
        text(x0, 194, sublabel, 13, opacity=.78)
        top, bottom, height = 235, 490, 255
        ceiling = max(150, int(max(metrics[key].values()) / 50 + 1) * 50)
        for tick in range(0, ceiling + 1, 50):
            y = bottom - tick / ceiling * height
            parts.append(f'<path d="M{x0+42} {y}h285" stroke="{neutral}" stroke-opacity=".18"/>')
            text(x0+34, y+4, f'{tick}%', 12, 'end', .78)
        for index, arm in enumerate(('baseline', 'skill')):
            value = metrics[key][arm]
            x = x0 + 82 + index * 130
            bar_height = value / ceiling * height
            color = blue if arm == 'skill' else neutral
            opacity = 1 if arm == 'skill' else .48
            parts.append(f'<rect x="{x}" y="{bottom-bar_height}" width="72" '
                         f'height="{bar_height}" fill="{color}" fill-opacity="{opacity}"/>')
            text(x+36, bottom-bar_height-12, f'{value:.1f}%', 16, 'middle')
            text(x+36, 520, arm, 15, 'middle')

    x0 = 828
    text(x0, 170, 'One extra bug.', 20)
    text(x0, 194, 'No extra false alarms.', 20)
    text(x0, 225, f'Reviewed targets: {quality["baseline"]}/{cases} → {quality["skill"]}/{cases}', 14, opacity=.78)
    text(x0+205, 260, 'baseline', 12, 'middle', .78)
    text(x0+295, 260, 'skill', 12, 'middle', .78)
    for index, row in enumerate(quality_rows):
        y = 300 + index * 50
        parts.append(f'<path d="M{x0} {y+15}h330" stroke="{neutral}" stroke-opacity=".13"/>')
        text(x0, y, row['label'], 14)
        for arm, x in (('baseline', x0+205), ('skill', x0+295)):
            status = row[arm]
            color = blue if arm == 'skill' and status != 'MISSED' else neutral
            opacity = .42 if status == 'MISSED' else 1
            text(x, y, status, 11, 'middle', opacity)
            if arm == 'skill' and status != 'MISSED':
                parts.append(f'<path d="M{x-27} {y+7}h54" stroke="{color}" stroke-width="3"/>')
    text(x0, 520, f'False positives  {data["clean_false_positives"]["baseline"]} → '
                   f'{data["clean_false_positives"]["skill"]}', 15)
    text(48, 585, data['footer'], 15)
    text(48, 615, 'Baseline = 100% per task; bars are equal-weight means of task ratios.', 14, opacity=.78)
    text(48, 643, 'Descriptive checkpoint, not a confidence interval or universal superiority claim.', 14, opacity=.78)
    parts.append('</g></svg>')
    return '\n'.join(parts) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('data', type=Path)
    parser.add_argument('--light', type=Path, required=True)
    parser.add_argument('--dark', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.data.read_text())
    args.light.write_text(render(data, dark=False))
    args.dark.write_text(render(data, dark=True))


if __name__ == '__main__':
    main()
