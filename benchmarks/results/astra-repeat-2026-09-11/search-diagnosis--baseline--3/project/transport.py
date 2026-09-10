async def fetch(query, request):
    return await request('/search', params={'q': query}, headers={'Cache-Control': 'no-cache'})
