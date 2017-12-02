import asyncio
from config import config
import logging
from PushkinBot import PushkinBot



async def main(loop):
    bot = PushkinBot(config, loop=loop)

    await bot.run()
    await bot.api.delete_webhook()
    await bot.api.set_webhook(config['web_hook'])


if __name__ == "__main__":
    new_loop = asyncio.get_event_loop()
    new_loop.create_task(main(new_loop))
    try:
        new_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        new_loop.close()
