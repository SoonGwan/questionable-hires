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


def guide(source):
    return replace_once(source,
        'Format `v:2`: primitive builtins only; lists are JSON arrays, tuples use',
        'Format `v:3`: primitive builtins and exact standard pathlib types. Paths use\n'
        '  `{"PosixPath":"..."}` (or `WindowsPath`, `PurePosixPath`, `PureWindowsPath`);\n'
        '  lexical text is limited to 256 characters, with no resolving or subclass\n'
        '  conversion. Lists are JSON arrays, tuples use')


def write(source_directory, destination):
    """Create a candidate from explicit source files; no Git or model dependency."""
    source_directory, destination = Path(source_directory), Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    for name, transform in (('assertions.py', assertions), ('compare.py', comparison)):
        (destination / name).write_text(transform((source_directory / name).read_text()))
