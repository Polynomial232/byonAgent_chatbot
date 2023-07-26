"""
    kumpulan beberapa fungsi
"""

import requests
from decouple import config

LINK = config("MICROSITE_URL")
IP = config("IP")

def replace_restaurant_name(page_text, custom_id):
    restaurant = requests.get(f"http://{IP}:8000/restaurants/{custom_id}")
    return page_text.format(restaurant_name=restaurant.json().get("name"))

def replace_link(page_text, custom_id):
    return page_text.format(link=LINK) + "/" + str(custom_id)
