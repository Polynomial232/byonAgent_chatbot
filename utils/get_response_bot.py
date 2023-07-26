import numpy as np
from thefuzz import process
from thefuzz import fuzz
from decouple import config

from classes.Chatbot_Agent import Chatbot_Agent
from .utils import get_bag_of_word, compare_bag_of_word

LINK = config("MICROSITE_URL")
IP = config("IP")

def fuzzy_check(text, id_flow_pages, id_restaurants=None):
    chatbot_agent = Chatbot_Agent(IP)

    try:
        page = chatbot_agent.get_page(id_flow_pages)
        page_options = chatbot_agent.get_page_options(page.get("option_group"), id_restaurants)

        if page_options[0].get("option_goto") == "pesan":
            return "pesan", id_restaurants

        options = [f"{idx} {page_option.get('option_text')}" for idx, page_option in enumerate(page_options, start=1)]

        list_ratio = process.extract(text, options, scorer=fuzz.token_set_ratio)
        check_ration = [ratio for ratio in list_ratio if ratio[1] >= 80]
        
        if len(check_ration) == 0:
            all_bag_of_words = []
            for option in options:
                all_bag_of_words.append(get_bag_of_word(option, options))
            all_bag_of_words = np.array(all_bag_of_words)
            sentence_bag_of_word = get_bag_of_word(text, options)
            get_index = compare_bag_of_word(sentence_bag_of_word, all_bag_of_words)

            if get_index < 0:
                return id_flow_pages, id_restaurants

            list_ratio = options[get_index]
        elif len(check_ration) == 1:
            list_ratio = list_ratio[0][0]
        else:
            return id_flow_pages, id_restaurants
        
        max_prob = list_ratio[2:]
        for page_option in page_options:
            if page_option.get('option_text') == max_prob:
                if id_flow_pages == 1:
                    return page_option.get("option_goto"), page_option.get("id_restaurant")
                return page_option.get("option_goto"), id_restaurants
        return id_flow_pages, id_restaurants
    except:
        return -1, -1