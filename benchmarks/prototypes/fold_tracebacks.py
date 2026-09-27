#!/usr/bin/env python3
"""Unadopted display-only prototype: reference identical traceback prefixes.

Read an already captured native output file; never execute or score tests. Keep
that complete file and its native exit separately. Unknown formats pass through.
Only use the rendered view if it is strictly smaller, including its raw-file
reference/hash. Records retain literal text or backward original-line references;
expand() reconstructs the exact UTF-8 text. No claims about model token savings.
"""
import argparse
import hashlib
from pathlib import Path
import sys

LIMIT = 1_048_576


def frames(lines, start):
    """Recognize ordinary Python frames, keeping source/caret lines verbatim."""
    result = []
    while start < len(lines) and lines[start].startswith('  File "'):
        end = start + 1
        while end < len(lines) and lines[end].startswith('    '):
            end += 1
        result.append((start, end))
        start = end
    return result


def fold(text):
    if len(text.encode('utf-8')) > LIMIT:
        raise ValueError('Display input exceeds 1 MiB; inspect the retained raw file')
    lines = text.splitlines(keepends=True)
    records, first, cursor = [], {}, 0
    for i, line in enumerate(lines):
        if line.rstrip('\r\n') != 'Traceback (most recent call last):':
            continue
        group = frames(lines, i + 1)
        if not group:
            continue
        # One remembered prefix per first frame bounds lookup; exact equality is
        # mandatory. Other matching opportunities are deliberately left alone.
        key = ''.join(lines[slice(*group[0])])
        prior = first.get(key)
        if prior is None:
            first[key] = group
            continue
        count = 0
        for old, new in zip(prior, group):
            if lines[slice(*old)] != lines[slice(*new)]:
                break
            count += 1
        if not count:
            continue
        start, end = group[0][0], group[count - 1][1]
        old_start, old_end = prior[0][0], prior[count - 1][1]
        if len(''.join(lines[start:end]).encode('utf-8')) < 160:
            continue
        records.append({'text': ''.join(lines[cursor:start])})
        records.append({'repeat': [old_start, old_end]})
        cursor = end
    records.append({'text': ''.join(lines[cursor:])})
    return records


def expand(records):
    lines = []
    for record in records:
        if set(record) == {'text'} and isinstance(record['text'], str):
            lines.extend(record['text'].splitlines(keepends=True))
        elif set(record) == {'repeat'}:
            start, end = record['repeat']
            if (type(start) is not int or type(end) is not int or
                    not 0 <= start < end <= len(lines)):
                raise ValueError('Expected a backward original-line reference')
            lines.extend(lines[start:end])
        else:
            raise ValueError('Unknown display record')
    return ''.join(lines)


def display(raw, source):
    if len(raw) > LIMIT:
        raise ValueError('Display input exceeds 1 MiB; inspect the retained raw file')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw
    records = fold(text)
    if not any('repeat' in r for r in records):
        return raw
    assert expand(records) == text
    header = ('[Folded display only; complete native output: ' + repr(str(source)) +
              '; SHA-256 ' + hashlib.sha256(raw).hexdigest() + ']\n')
    parts = [header]
    for record in records:
        if 'text' in record:
            parts.append(record['text'])
        else:
            start, end = record['repeat']
            parts.append(f'  [Repeated traceback frames: original lines {start + 1}-{end}]\n')
    rendered = ''.join(parts).encode('utf-8')
    return rendered if len(rendered) < len(raw) else raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='Already retained complete native output')
    args = parser.parse_args()
    try:
        with args.output.open('rb') as stream:
            raw = stream.read(LIMIT + 1)
        sys.stdout.buffer.write(display(raw, args.output))
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
