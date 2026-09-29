def save(store, key, value):
    return {'created': store.put(key, value)}
