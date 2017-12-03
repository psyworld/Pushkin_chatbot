import asyncio
from config import config
from PushkinBot import PushkinBot



async def main(bot, loop):
    await bot.run()
    await bot.api.delete_webhook()
    await bot.api.set_webhook(config['web_hook'])


if __name__ == "__main__":
    new_loop = asyncio.get_event_loop()
    bot = PushkinBot(config, loop=new_loop)
    new_loop.create_task(main(bot, new_loop))
    try:
        new_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        bot.stop_running()
        new_loop.close()
