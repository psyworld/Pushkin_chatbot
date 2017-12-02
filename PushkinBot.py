from Bot import telegram

class PushkinBot(telegram.Bot):
    def __init__(self, config, loop=None):
        super().__init__(config, loop=loop)

    async def handler(self, update):
        print(update)
