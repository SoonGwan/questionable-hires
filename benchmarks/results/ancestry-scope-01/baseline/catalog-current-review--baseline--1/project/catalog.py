def cache_key(tenant, item):
    return (tenant, item)


class Catalog:
    def __init__(self, fetch):
        self.fetch = fetch
        self.cache = {}

    def lookup(self, tenant, item):
        key = cache_key(tenant, item)
        if key not in self.cache:
            self.cache[key] = self.fetch(tenant, item)
        return self.cache[key]
