import requests
import json

from utils.replace import replace_link, replace_restaurant_name
from .Get_Options_Table import Get_Options_Table

class Chatbot_Agent:
    def __init__(self, ip):
        self.ip = ip

    def get_page(self, id_flow_pages):
        flow = requests.get(f"http://{self.ip}:8000/flow-pages/{id_flow_pages}")
        return flow.json()

    def get_page_options(self, option_group, id_restaurant):
        response_options = requests.get(f"http://{self.ip}:8000/flow-options/{option_group}")
        options = response_options.json()

        if options[0].get("table_name") is None:
            return options

        table_name = options[0].get("table_name")

        return getattr(globals()['Get_Options_Table'](self.ip), f"{table_name}_options")(options, id_restaurant)
    
    def get_last_message(self, sender, receiver):
        response_last_message = requests.get(f"http://{self.ip}:8000/last-message?sender={sender}&receiver={receiver}")

        return response_last_message.json()

    def post_last_message(self, data):
        post_last_message = requests.post(f"http://{self.ip}:8000/last-message", data=json.dumps(data))

        return post_last_message.status_code

    def get_message(self, id_flow_pages, id_restaurant):
        page = self.get_page(id_flow_pages)
        page_text = page.get("page_text")

        if "{restaurant_name}" in page_text:
            page_text = replace_restaurant_name(page_text, id_restaurant) + "\n\n"
        elif "{link}" in page_text:
            page_text = replace_link(page_text, id_restaurant) + "\n\n"
        else:
            page_text = page_text + "\n\n"

        option_group = page.get("option_group")

        if option_group is None:
            return page_text
        
        page_options = self.get_page_options(option_group, id_restaurant)

        group = ''
        for idx, options in enumerate(page_options, start=1):
            if group != options.get('group') and page_options[0].get('group') is not None:
                group = options.get('group')
                page_text = page_text + f"{group}\n"
            page_text = page_text + f"{idx}. {options.get('option_text')}\n"

        return page_text