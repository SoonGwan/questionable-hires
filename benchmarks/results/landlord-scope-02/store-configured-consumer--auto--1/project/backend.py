class Duplicate(Exception):
    pass

class Backend:
    def __init__(self):
        self.rows = {}
    def put(self, key, value):
        if key in self.rows:
            raise Duplicate(key)
        self.rows[key] = value
