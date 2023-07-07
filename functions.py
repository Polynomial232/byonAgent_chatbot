"""
    kumpulan beberapa fungsi
"""

import json
import requests
from decouple import config
from thefuzz import fuzz

IP = config("IP")

async def fuzzy_check(text1, text2):
    return fuzz.token_set_ratio(text1, text2)

async def get_message(id_user, chat_uuid, region, id_bot_message):

    return await get_list_restoran(region)

    flow = requests.get(f"http://{IP}:8000/dummy/flow-chat/{region}/{chat_uuid}")

    if not flow.json():
        return "Message tidak tersedia"

    return flow.json().get("page_text")

async def get_list_restoran(region):
    message = ""
    list_restoran = requests.get(f"http://{IP}:8000/dummy/restoran/{region}")

    for idx, restoran in enumerate(list_restoran.json()):
        if not restoran.get('status_buka'):
            continue
        message += f"{chr(65+idx)}. {restoran.get('nama')}\n"

    return message