from copy import deepcopy


class Editor:
    def __init__(self, settings, persist):
        self.settings = deepcopy(settings)
        self.persist = persist
        self.revision = 0
        self.saved_revision = 0

    @property
    def dirty(self):
        return self.revision != self.saved_revision

    def set_theme(self, theme):
        self.settings['display']['theme'] = theme
        self.revision += 1

    async def save(self):
        revision = self.revision
        payload = dict(self.settings)
        await self.persist(payload)
        self.saved_revision = revision
