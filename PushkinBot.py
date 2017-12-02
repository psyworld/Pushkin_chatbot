from Bot import telegram
from pushkin_api import PushkinApi

class PushkinBot(telegram.Bot):
    def __init__(self, config, loop=None):
        super().__init__(config, loop=loop)
        self.loop.create_task(self.send_res())

    async def handler(self, update):
        user_id = update.message.user.id
        await self.api.send_message(user_id, "AAAAAAAAA")
        await self.api.send_sticker(user_id, "CAADAgADOAEAAkJPOQABXRK1Mn5TOgsC")
        

    async def send_res(self):
        p_api = PushkinApi(self.loop)
        r = await p_api.api_get("https://all.culture.ru/api/2.2/events?organizations=607&start=1512204775432&sort=start")
        print(r)
