"""Isolated Receipt prototype: bounded-memory exact final byte comparison."""


def transform(source):
    old = '''def read_limited(path, limit):
    info = path.lstat()'''
    new = '''@contextmanager
def selected_reader(path):
    info = path.lstat()'''
    if source.count(old) != 1:
        raise ValueError('Expected original selected reader')
    source = source.replace('import argparse\n', 'import argparse\nfrom contextlib import contextmanager\n', 1)
    source = source.replace(old, new, 1)
    end = '        return stream.read(limit + 1)\n'
    if source.count(end) != 1:
        raise ValueError('Expected original bounded read')
    source = source.replace(end, '''        yield stream


def read_limited(path, limit):
    with selected_reader(path) as stream:
        return stream.read(limit + 1)


def content_matches(path, expected):
    """Exact comparison in bounded chunks; never replace the later tree scan."""
    with selected_reader(path) as stream:
        for start in range(0, len(expected), 65536):
            wanted = expected[start:start + 65536]
            if stream.read(len(wanted)) != wanted:
                return False
        return stream.read(1) == b''
''', 1)
    check = 'read_limited(root/name, len(content)) != content'
    if source.count(check) != 1:
        raise ValueError('Expected original final byte comparison')
    return source.replace(check, 'not content_matches(root/name, content)', 1)
