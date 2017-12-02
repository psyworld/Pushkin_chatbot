from Bot import telegram
import datetime
from pushkin_api import PushkinApi
import json
from helpers import get_range
import random

hello_phrase = '''
Добрый день! Вас приветствует официальный телеграм-бот Государственного музея изобразительных искусств имени А.С. Пушкина. Это музейный комплекс, обладающий одним из крупнейших в России художественных собраний зарубежного искусства. Сегодня в его коллекции находится около 700 тысяч произведений разных эпох, начиная с Древнего Египта и античной Греции и заканчивая началом XXI века. \n
Бот поможет вам узнать, какие события проводятся в музее в интересующую вас дату. Для этого введите дату в формате «дд.мм.гггг» (например, 02.12.2017). \n
Если вы хотите узнать режим работы музея, перейти в раздел покупки билета и узнать новости, воспользуйтесь командой /links \n
У нас также есть свой стикерпак – он доступен для установки. \n
Хорошего дня, ждем вас в музее! \n
'''

cool_links = """
*Перейти к покупке билетов онлайн:* \n https://tickets.arts-museum.ru/ru/ \n
*Узнать режим работы музея:* \n http://www.arts-museum.ru/visitors/contact/index.php \n
*Новости:* \n http://www.arts-museum.ru/museum/news/index.php
"""

stickers = [
    'CAADAgADMAEAAkJPOQABhh2uh-uMEhYC',
    'CAADAgADOAEAAkJPOQABXRK1Mn5TOgsC',
    'CAADAgADJgEAAkJPOQAB6lqgusQR1YUC',
    'CAADAgADHAEAAkJPOQABSSG0t8PoTVsC',
    'CAADAgADLgEAAkJPOQABajImSfltvzcC',
    'CAADAgADEgEAAkJPOQAB-Mo9Ns1FuFEC'
]

class PushkinBot(telegram.Bot):
    def __init__(self, config, loop=None):
        super().__init__(config, loop=loop)
        self.p_api = PushkinApi(loop)

    async def handler(self, update):
        if update.message is not None:
            if update.message.text == "/start":
                await self.hello(update)
            if update.message.text == "/links":
                await self.links(update)
            await self.start(update)
        if update.callback_query is not None:
            user_id = update.callback_query.user.id
            if update.callback_query.data[0] == '{':
                print(update.callback_query.data)
                type = json.loads(update.callback_query.data).get("type", "")
                if type == "notification":
                    await self.notification(update)
                else:
                    await self.send_next(update)

    async def links(self, update):
        user_id = update.message.user.id
        await self.api.send_message(user_id, cool_links, parse_mode='Markdown')

    async def notification(self, update):
        user_id = update.callback_query.user.id
        await self.api.send_message(user_id, "Мы напомним вам о предстоящем мероприятии.")

    async def send_next(self, update):
        user_id = update.callback_query.user.id
        data = json.loads(update.callback_query.data)
        print("AAAAAAA", data)
        start_ts, end_ts = get_range(data, data['D'])
        params = {
            "start": start_ts * 1000,
            'sort': 'start'
        }
        print("start_ts", start_ts * 1000)
        res = await self.p_api.api_get("https://all.culture.ru/api/2.2/events?organizations=607", params=params)

        if res["total"] == 0:
            await self.api.send_message(user_id, "В этот день ещё нет мероприятий.")
            return

        found = False
        offset_counter = 0
        for event in res['events']:
            if event["category"]["sysName"] == data["sysName"]:
                if offset_counter == data["o"]:
                    kb_inline = telegram.InlineKeyboardMarkup()
                    data['o'] += 1
                    cb_data = json.dumps(data)
                    cbn_data = json.dumps({"type": "notification", "id": event["_id"]})
                    print(cbn_data)
                    # todo handler cbn
                    print(cb_data)
                    kb_inline.add_button("Далее >>", callback_data=cb_data)
                    kb_inline.add_button("Напомнить", callback_data=cbn_data)
                    start_date = (datetime.datetime.fromtimestamp(event["start"]/1000).strftime("%d.%m.%Y %I:%M %p"))
                    end_date = (datetime.datetime.fromtimestamp(event["end"]/1000).strftime("%d.%m.%Y %I:%M %p"))
                    r = await self.api.send_message(user_id, "*{}*. {}\n{} -- {}".format(event["category"]["name"], event["name"], start_date, end_date), reply_markup=kb_inline.json, parse_mode='Markdown')
                    found = True
                    break;
                offset_counter += 1

        if not found:
            await self.api.send_message(user_id, "В этот день больше нет мероприятий.")



    async def hello(self, update):
        user_id = update.message.user.id
        kb = telegram.ReplyKeyboardMarkup()
        kb.add_button("сегодня")
        kb.add_button("завтра")
        kb.add_button("выходные")
        await self.api.send_message(user_id, hello_phrase, reply_markup=kb.json)
        await self.api.send_sticker(user_id, random.choice(stickers))

    async def start(self, update):
        user_id = update.message.user.id
        date_ts = None
        cur_ts = int(datetime.datetime.now().strftime("%s"))
        cur_ts = (cur_ts - cur_ts % (24*60*60))
        D = 1

        if update.message.text == "сегодня":
            date_ts = cur_ts
            start_ts = date_ts
            end_ts = int(date_ts) + (24*60*60)
        elif update.message.text == "завтра":
            date_ts = cur_ts + (24*60*60)
            start_ts = date_ts
            end_ts = int(date_ts) + (24*60*60)
        elif update.message.text == "выходные":
            date_ts = int((datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().isoweekday() % 7 - 1)).strftime('%s'))+ (24 * 60 * 60) * 5
            start_ts = date_ts
            end_ts = int(date_ts) + (24*60*60)*2
            D = 2
        else:
            try:
                des_ts = int(datetime.datetime.strptime(update.message.text, "%d.%m.%Y").strftime("%s"))
                des_ts = (des_ts - des_ts % 24*60*60)
                date_ts = des_ts
            except:
              pass
              # do fucking nothing

        if date_ts is not None:

            params = {
                'start': start_ts * 1000,
                'limit': 100,
                'sort': 'start'
            }
            response = await self.p_api.api_get("https://all.culture.ru/api/2.2/events?organizations=607", params=params)

            if response["total"] == 0:
                await self.api.send_message(user_id, "В этот день ещё нет мероприятий.")
                return

            event = response["events"][0]
            callback_data_vys = json.dumps({"date_ts": date_ts, "o": 0, 'sysName': "vystavki", 'D': D})
            callback_data_kons = json.dumps({"date_ts": date_ts, "o": 0, 'sysName': "koncerty", 'D': D})
            callback_data_vst = json.dumps({"date_ts": date_ts, "o": 0, 'sysName': "vstrechi", 'D': D})
            kb_inline = telegram.InlineKeyboardMarkup()

            kb_inline.add_button("Выставки >>", callback_data=callback_data_vys)
            kb_inline.add_button("Встречи >>", callback_data=callback_data_vst)
            kb_inline.add_button("Концерты >>", callback_data=callback_data_kons)

            start_date = (datetime.datetime.fromtimestamp(event["start"]/1000).strftime("%d.%m.%Y %I:%M %p"))
            end_date = (datetime.datetime.fromtimestamp(event["end"]/1000).strftime("%d.%m.%Y %I:%M %p"))
            r = await self.api.send_message(user_id, "Выберите категорию:", reply_markup=kb_inline.json, parse_mode='Markdown')
