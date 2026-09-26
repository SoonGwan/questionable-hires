from backend import Duplicate

class Store:
    def __init__(self, backend):
        self.backend = backend
    def put(self, key, value):
        try:
            self.backend.put(key, value)
        except Duplicate:
            return False
        return True
