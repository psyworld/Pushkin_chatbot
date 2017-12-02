from Bot import telegram
import button_functions.py
import datetime 

class PushkinBot(telegram.Bot):
    def __init__(self, config, loop=None):
        super().__init__(config, loop=loop)

    async def handler(self, update):
        user_id = update.message.user.id
        await self.api.send_message(user_id, "AAAAAAAAA")
        kb = telegram.ResponseKeyboardMarkup()
        kb.add_button("Чо сегодня")
       	kb.add_button("Чо завтра")
       	kb.add_button("Чо на след неделе")
       	await self.api.send_message(user_id, "AAAAAAAAA", reply_markup=kb.json)
       	if (update.message.text == "Чо сегодня"):
       		def print_events(datetime.datetime)
       	if (update.message.text == "Чо завтра"):
       		def print_next_day(datetime.datetime)
       	if (update.message.text == "Чо на след неделе"):
       		def print_next_week(datetime.datetime)

