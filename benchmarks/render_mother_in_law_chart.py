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
    cases = data['cases']
    if not 1 <= cases <= 10 or any(not 0 <= quality[arm] <= cases for arm in ('baseline', 'skill')):
        raise ValueError('Invalid case or quality counts')

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
    text(x0, 170, 'Quality target met', 20)
    text(x0, 194, 'Case-level reviewed outcomes', 13, opacity=.78)
    for index, arm in enumerate(('baseline', 'skill')):
        y = 260 + index * 120
        width = 280 * quality[arm] / cases
        parts.append(f'<rect x="{x0}" y="{y}" width="280" height="42" '
                     f'fill="{neutral}" fill-opacity=".16"/>')
        parts.append(f'<rect x="{x0}" y="{y}" width="{width}" height="42" '
                     f'fill="{blue if arm == "skill" else neutral}" '
                     f'fill-opacity="{1 if arm == "skill" else .48}"/>')
        text(x0, y-10, arm, 15)
        text(x0+290, y+28, f'{quality[arm]}/{cases}', 17)
    text(x0, 500, f'Clean-case false positives: {data["clean_false_positives"]["baseline"]} / '
                   f'{data["clean_false_positives"]["skill"]} (baseline / skill)', 14)
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
