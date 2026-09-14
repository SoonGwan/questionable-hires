import sqlite3
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
