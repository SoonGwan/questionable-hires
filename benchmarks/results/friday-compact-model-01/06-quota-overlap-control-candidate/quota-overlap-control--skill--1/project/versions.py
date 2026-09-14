def old_read(db, key):
    return db.execute('SELECT quota FROM accounts WHERE id=?', (key,)).fetchone()[0]

def new_read(db, key):
    return db.execute('SELECT quota_limit FROM accounts WHERE id=?', (key,)).fetchone()[0]

def old_write(db, key, value):
    db.execute('UPDATE accounts SET quota=? WHERE id=?', (value, key))

def new_write(db, key, value):
    db.execute('UPDATE accounts SET quota_limit=? WHERE id=?', (value, key))

def old_insert(db, key, value):
    db.execute('INSERT INTO accounts (id,quota) VALUES (?,?)', (key,value))

def new_insert(db, key, value):
    db.execute('INSERT INTO accounts (id,quota,quota_limit) VALUES (?,?,?)', (key,value,value))
