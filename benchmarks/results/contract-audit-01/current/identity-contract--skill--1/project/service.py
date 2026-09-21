class Registry:
    def __init__(self, records):
        self.records = records
    def get(self, key):
        return self.records[key]
