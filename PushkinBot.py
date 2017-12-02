from Bot import telegram

class PushkinBot(telegram.Bot):
    def __init__(self, config, loop=None):
        super().__init__(config, loop=loop)

    async def handler(self, update):
        user_id = update.message.user.id
        await self.api.send_message(user_id, "AAAAAAAAA")
