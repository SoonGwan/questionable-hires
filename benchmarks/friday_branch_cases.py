#!/usr/bin/env python3
"""Interior conversion branch defeats endpoint-only compatibility sampling."""
import argparse
import importlib.util
import json
from pathlib import Path


def cases():
    spec = importlib.util.spec_from_file_location('state_cases', Path(__file__).with_name('friday_state_cases.py'))
    state = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(state)
    result = state.cases()
    for case in result:
        compatible = case['id'].endswith('compatible')
        case['id'] = 'friday-branch-' + ('compatible' if compatible else 'gap')
        writer = case['files']['old.py'].split('\ndef write', 1)[1]
        case['files']['old.py'] = (
            'def read(db, item_id):\n'
            '    quantity = db.execute("SELECT quantity FROM items WHERE id=?", (item_id,)).fetchone()[0]\n'
            '    if 400 <= quantity < 600:\n'
            '        return ' + ('float' if compatible else 'int') + '(quantity)\n'
            '    return float(quantity)\n'
            '\ndef write' + writer)
        case['criteria'][1] = ('Exercise the interior conversion branch as well as values outside it, '
                               'using actual committed candidate writes and old/new reads.')
        case['criteria'][2] = (
            'Identify truncation only for non-whole values in [400,600), including retained-data rollback; do not claim all fractions fail.'
            if not compatible else
            'Recognize both interior and exterior reader paths preserve candidate data; do not invent a branch defect.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; choose a fresh destination')
    args.output.write_text(json.dumps(cases(), indent=2) + '\n')
