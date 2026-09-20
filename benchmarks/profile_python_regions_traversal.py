"""End-to-end region-selection profile, including parsing, not model performance."""
import argparse
import json
from pathlib import Path
from profile_python_regions_budget import measure, workloads


def cases():
    yield from workloads()
    # Expression-heavy generated configuration; neither arm executes the input.
    source = 'settings = [\n' + ''.join(
        f'    dict(name="item{i}", values=[1, 2, 3], enabled=True),\n' for i in range(5000))
    source += ']\ndef target():\n    return settings\n'
    yield 'generated-config', source.encode(), ['target']
    source = ''.join(f'def function{i}(value):\n    return transform(value, offset={i})\n' for i in range(1000))
    yield 'many-functions', source.encode(), ['function0', 'function999']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = measure(before='b8b2f3f', cases=cases())
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for row in result['rows']:
        print(json.dumps({key: row[key] for key in ('case', 'median_seconds', 'median_peak_traced_bytes')}))
