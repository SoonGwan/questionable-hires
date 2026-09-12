class FormatterRegistry:
    def __init__(self):
        self.providers = {}
    def register(self, name, provider):
        self.providers[name] = provider
    def format(self, name, value):
        return self.providers[name](value)

registry = FormatterRegistry()
registry.register('usd', lambda cents: f'${cents / 100:.2f}')
