#!/usr/bin/env python3
"""Writer transfer fixtures with an explicit actual commit-before-ack caller."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = '''import sqlite3
import versions


def write(path, version, operation, key, value):
    handler = {('old', 'update'): versions.old_write,
               ('new', 'update'): versions.new_write,
               ('old', 'insert'): versions.old_insert,
               ('new', 'insert'): versions.new_insert}[(version, operation)]
    db = sqlite3.connect(path, timeout=1)
    try:
        with db:
            handler(db, key, value)
    finally:
        db.close()
    return {'acknowledged': True, 'id': key, 'value': value}


def read(path, version, key):
    db = sqlite3.connect(path, timeout=1)
    try:
        return {'old': versions.old_read, 'new': versions.new_read}[version](db, key)
    finally:
        db.close()
'''


def cases():
    source = json.loads((ROOT / 'benchmarks/friday-writer-cases.json').read_text())
    result = []
    for original in source:
        files = dict(original['files'])
        files['application.py'] = APP
        files['release.md'] += (
            'The actual application entrypoints are application.write and application.read. '
            'A write is acknowledged only when application.write returns its success dictionary, '
            'after transaction commit and connection close; exceptions are not acknowledgments. '
            'Use existing keys for updates and fresh keys for inserts. Calls are sequential; '
            'each completed acknowledged write must be visible through both versions on fresh '
            'connections before the next call. No concurrent request ordering or crash-durability '
            'claim is requested. All acknowledged values must survive the documented rollback.\n')
        result.append(dict(id=original['id'].replace('quota-overlap', 'quota-ack'), skill='friday',
            files=files,
            task=('Review release.md for local mixed-version compatibility and rollback. '
                  'Exercise the supplied application.write/read entrypoints with actual migration '
                  'files on a disposable project-local SQLite database. Check old/new updates '
                  'and inserts, cross-version visibility after acknowledged writes, and values '
                  'after the documented rollback. Distinguish observed defects from missing '
                  'production evidence; do not invent defects in compatible behavior. Preserve '
                  'original files. No deployment, installation or external services.'),
            criteria=[
                'Exercise actual application entrypoints, not replacement SQL writers, for old/new updates and inserts.',
                'Check acknowledged values through independent application.read connections and after documented rollback.',
                ('Identify stale cross-version values, null after old insert and lost acknowledged new update after down.'
                 if original['id'].endswith('gap') else
                 'Recognize supplied local data contract is preserved without manufacturing a compatibility defect.'),
                'Preserve original files, use project-local disposable database, and leave production evidence unverified.']))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as stream:
        stream.write(json.dumps(cases(), indent=2) + '\n')
