import aiohttp


def kawaii(token):
    async def get(main, endpoint, f=None):
        if f is None:
            f = []
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kawaii.red/api/{main}/{endpoint}/token={token}&filter={f}/") as url:
                image = await url.json()
                return image["response"]

    async def endpoints(main=None):
        if main is None:
            main = "gif"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://kawaii.red/api/{main}/endpoints/token={token}/") as url:
                points = await url.json()
                return points["response"]

    kawaii.get = get
    kawaii.endpoints = endpoints
    return kawaii
