from .replace import *
from decouple import config

from models.flow_page import FlowPage
from models.flow_option import FlowOption

IP = config("IP")

flow_page = FlowPage(IP)
flow_option = FlowOption(IP)

def get_message(id_flow_pages, id_restaurant):
    page = flow_page.get_page(id_flow_pages)
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
    
    page_options = flow_option.get_page_options(option_group, id_restaurant)
    group = ''
    for idx, options in enumerate(page_options, start=1):
        if group != options.get('group') and page_options[0].get('group') is not None:
            group = options.get('group')
            page_text = page_text + f"{group}\n"
        page_text = page_text + f"{idx}. {options.get('option_text')}\n"
    return page_text