import json
import asyncio
from pushkin_api import PushkinApi 
import pprint

base_url = 'https://all.culture.ru/api/2.2/'
organization_id = 607

loop = asyncio.get_event_loop()   
http = PushkinApi(loop)

async def events(start=0, end=0, offset=0,limit=10, sort='start'):
    params = {"start": start, "end": end, "offset": offset, "limit": limit, "sort": sort}
    r = await http.api_get("https://all.culture.ru/api/2.2/events", params=params)git status
    return r