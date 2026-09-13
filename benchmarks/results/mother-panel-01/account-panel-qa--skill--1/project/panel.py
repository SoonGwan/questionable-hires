class AccountPanel:
    def __init__(self, fetch):
        self.fetch = fetch
        self.view = None
        self.error = None
        self.loading = False
        self._request = 0

    async def refresh(self, account):
        self._request += 1
        request = self._request
        self.loading = True
        self.error = None
        try:
            payload = await self.fetch(account)
            if request == self._request:
                self.view = payload
        except Exception as error:
            if request == self._request:
                self.error = str(error)
        finally:
            if request == self._request:
                self.loading = False
