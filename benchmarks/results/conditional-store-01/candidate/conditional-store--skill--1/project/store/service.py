from .backend import FileStore


def submit(directory, key, value):
    return FileStore(directory).save(key, value)
