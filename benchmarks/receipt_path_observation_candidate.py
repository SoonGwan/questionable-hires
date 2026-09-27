"""Unpromoted bounded pathlib observation, based on the integration06 resource."""
from pathlib import Path


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected source for path-observation candidate')
    return source.replace(old, new)


def assertions(source):
    source = replace_once(source, 'import json\n',
                          'import json\nfrom pathlib import PosixPath, WindowsPath, PurePosixPath, PureWindowsPath\n')
    source = replace_once(source, '    if depth < 3 and (kind is list or kind is tuple)',
        '    if kind in (PosixPath, WindowsPath, PurePosixPath, PureWindowsPath):\n'
        '        text = str(value)\n'
        '        if len(text) <= 256:\n'
        '            return {kind.__name__: text}\n'
        '        raise UnavailableValue("path length limit")\n'
        '    if depth < 3 and (kind is list or kind is tuple)')
    if source.count("'v': 2") != 2:
        raise ValueError('Unexpected assertion format version')
    return source.replace("'v': 2", "'v': 3")


def comparison(source):
    source = replace_once(source, "'v': 2", "'v': 3")
    return replace_once(source, "value['v'] == 2", "value['v'] == 3")


def write(source_directory, destination):
    """Create a candidate from explicit source files; no Git or model dependency."""
    source_directory, destination = Path(source_directory), Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    for name, transform in (('assertions.py', assertions), ('compare.py', comparison)):
        (destination / name).write_text(transform((source_directory / name).read_text()))
