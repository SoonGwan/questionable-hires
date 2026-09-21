"""Summarize recorded skill re-exposure, without inferring avoidable token cost."""
import argparse
import hashlib
import json
from pathlib import Path


def summarize(metadata, exposure):
    name = metadata['skill']
    entry = exposure['skills'].get(name)
    if entry is None:
        raise ValueError('Target skill has no exposure audit')
    if metadata['arm'] == 'skill' and entry['entry_sha256'] != metadata['skill_sha256']:
        raise ValueError('Exposure entry does not match measured skill')
    first_tool = exposure['first_tool_line']
    if first_tool is not None and (type(first_tool) is not int or first_tool < 1):
        raise ValueError('Invalid first tool line')
    observations = entry['observations']
    previous = 0
    for observation in observations:
        line, phase = observation['line'], observation['phase']
        if type(line) is not int or line <= previous:
            raise ValueError('Exposure lines must be strictly increasing')
        if phase not in ('initial_message', 'later_message', 'tool_output'):
            raise ValueError('Unknown exposure phase')
        if phase == 'initial_message':
            if first_tool is not None and line >= first_tool:
                raise ValueError('Initial exposure after first tool')
        elif first_tool is None or line <= first_tool:
            raise ValueError('Later exposure before first tool')
        previous = line
    initial = any(o['phase'] == 'initial_message' for o in observations)
    tool_lines = [o['line'] for o in observations if o['phase'] == 'tool_output']
    return dict(skill=name, arm=metadata['arm'], case=metadata['case'],
                initially_exposed=initial, tool_body_output_lines=tool_lines,
                tool_reexposure_after_initial=initial and bool(tool_lines))


def analyze(directory):
    directory = Path(directory)
    rows = []
    for path in sorted(directory.glob('*/*/metadata.json')):
        audit = path.with_name('skill-exposure.json')
        metadata_bytes, exposure_bytes = path.read_bytes(), audit.read_bytes()
        row = summarize(json.loads(metadata_bytes), json.loads(exposure_bytes))
        row.update(cell=str(path.parent.relative_to(directory)),
            metadata_sha256=hashlib.sha256(metadata_bytes).hexdigest(),
            exposure_sha256=hashlib.sha256(exposure_bytes).hexdigest())
        rows.append(row)
    if not rows:
        raise ValueError('No measured cells found')
    return dict(rows=rows, limitation='Exact body exposure only, not attention, unnecessary rereading, '
        'avoidable calls or recoverable tokens. Tool outputs can combine essential other work. '
        'No historical token subtraction or outcome adjustment. Missing exact matches do not prove absence.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    print(json.dumps(analyze(parser.parse_args().directory), indent=2))
