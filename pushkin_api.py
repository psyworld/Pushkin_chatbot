import signal
import aiohttp
import sys


class PushkinApi:
    def __init__(self, loop):
        self.session = aiohttp.ClientSession(loop=loop)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        self.session.close()
        sys.exit(0)

    async def api_get(self, url, params={}):
        r = await self.session.get(url, params=params)
        r = await r.json()
        return r

    async def api_post(self, url, method: str, params: dict, data: dict=None):
        r = await self.session.post(url, params=params, data=data)
        r = await r.json()
        return r
