"""Author-only actual SQLite checks, including the active column mismatch."""
import ast
import json
from pathlib import Path
import sqlite3

from cases_view_contract import FILES


def main():
    output = Path(__file__).with_name('view-contract-01-preflight.json')
    if output.exists():
        raise ValueError('Refusing to replace preflight evidence')
    readers = {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(FILES['readers.py']).body}
    records = []
    db = sqlite3.connect(':memory:')
    try:
        for index, filename in enumerate(['001_schema.sql', '002_up.sql', '003_new_writes.sql', None, '002_down.sql']):
            if filename:
                db.executescript(FILES[filename])
            checks = {}
            expected = [(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')] if index < 2 else [
                (1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
            for reader, query in readers.items():
                try:
                    cursor = db.execute(query)
                    columns = [c[0] for c in cursor.description]
                    rows = cursor.fetchall()
                    cursor.close()
                    assert rows == expected, (rows, expected)
                    expected_columns = ['id', 'label' if reader == 'OLD' else 'title', 'payload']
                    try:
                        assert columns == expected_columns, (columns, expected_columns)
                    except AssertionError as error:
                        assert reader == 'OLD' and index in (1, 2, 3)
                        checks[reader] = dict(query_ok=True, contract_ok=False, assertion=str(error))
                    else:
                        checks[reader] = dict(query_ok=True, contract_ok=True)
                    checks[reader].update(columns=columns, rows=rows)
                except sqlite3.OperationalError as error:
                    assert reader == 'NEW' and index in (0, 4)
                    assert 'no such column: title' in str(error)
                    checks[reader] = dict(query_ok=False, error=str(error), inactive=True)
            records.append(dict(checkpoint=index + 1, checks=checks))
    finally:
        db.close()
    with output.open('x') as stream:
        json.dump(dict(records=records, limitation='Author preflight only, not model performance.'), stream,
                  indent=2, default=lambda value: {'blob_hex': value.hex()})
        stream.write('\n')
    print('Five checkpoints / ten reader observations; expected native values and active column assertion failures verified.')


if __name__ == '__main__':
    main()
