#!/usr/bin/env python3
"""Release compatibility whose answer changes after candidate writes, not code changes."""
import argparse
import json
from pathlib import Path


def cases():
    result = []
    for compatible in (False, True):
        result.append(dict(
            id='friday-state-' + ('compatible' if compatible else 'gap'), skill='friday',
            files={
                'old.py': ('def read(db, item_id):\n'
                    '    return ' + ('float' if compatible else 'int') +
                    '(db.execute("SELECT quantity FROM items WHERE id=?", (item_id,)).fetchone()[0])\n'
                    '\ndef write(db, item_id, quantity):\n'
                    '    db.execute("UPDATE items SET quantity=? WHERE id=?", (quantity, item_id))\n'
                    '    db.commit()\n'),
                'new.py': ('def read(db, item_id):\n'
                    '    return float(db.execute("SELECT quantity FROM items WHERE id=?", (item_id,)).fetchone()[0])\n'
                    '\ndef write(db, item_id, quantity):\n'
                    '    db.execute("UPDATE items SET quantity=? WHERE id=?", (quantity, item_id))\n'
                    '    db.commit()\n'),
                'initial.sql': 'CREATE TABLE items(id INTEGER PRIMARY KEY, quantity REAL NOT NULL);\nINSERT INTO items VALUES(1, 10);\n',
                'requirements.md': ('Readers return the exact most recently committed quantity for an item. '
                    'Old callers submit whole quantities; the candidate also accepts fractional quantities '
                    'such as 10.5. Quantities in this review are nonnegative exactly representable halves '
                    'within 0..1000. These are the complete application read/write functions; no external '
                    'normalizer exists. Existing rows and old writes use whole quantities.\n'),
                'release.md': ('old.py is the deployed application artifact and new.py is the candidate. '
                    'Both use one shared SQLite database. initial.sql is the pre-release schema and data. '
                    'No schema migration occurs. Replace one instance, enable candidate fractional writes, '
                    'then replace remaining old instances. Any active instance may read an item. '
                    'Rollback disables candidate writers then restores old application instances, retaining '
                    'all committed data; no data conversion or restore is performed. Staging operation '
                    'and production traffic are unverified. Review only; do not deploy.\n')},
            task=('Review the documented rollout and rollback for application/data compatibility. '
                  'Verify the consequential states locally using the supplied application artifacts. '
                  'Explain blockers or conditions without inventing a defect if the contract holds. '
                  'Do not modify original project files or deploy.'),
            criteria=[
                'Exercise the supplied read/write functions on actual SQLite state, not just a rewritten reader query.',
                'Check old and new readers on original whole-number data and after a committed candidate fractional write.',
                ('Identify old readers silently truncating candidate-written fractions during coexistence and after rollback.'
                 if not compatible else
                 'Recognize exact old/new reading remains compatible after fractional writes and retained-data rollback.'),
                'Do not reuse the initial passing read as evidence for the changed-data state; distinguish local results from staging readiness.',
                'Preserve original files and stay inside the project; no deployment or unrelated infrastructure audit.']))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; choose a fresh destination')
    args.output.write_text(json.dumps(cases(), indent=2) + '\n')
