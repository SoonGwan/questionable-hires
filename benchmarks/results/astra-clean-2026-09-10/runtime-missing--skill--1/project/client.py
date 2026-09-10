async def lookup(request, key):
    return await request('/lookup', params={'key': key})
