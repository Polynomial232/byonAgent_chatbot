""" docstring """

from decouple import config

from models.conversation import Conversation
from utils.get_response_bot import get_response_bot
from utils.get_message import get_message

IP = config("IP")
conversation = Conversation(IP)

def get_response_handler(message, sender, receiver):
    """ docstring """

    if not message:
        id_flow_page = 1
        id_restaurant = 1
    else:
        last_message = conversation.get_conversation(sender, receiver)
        id_flow_page = last_message.get("id_flow_page") if last_message.get("id_flow_page") else 1
        id_restaurant = last_message.get("id_restaurant") if last_message.get("id_restaurant") else 1

        if "resto" in message.lower():
            id_flow_page = 1
        else:
            id_flow_page, id_restaurant = get_response_bot(message, id_flow_page, id_restaurant)

    wa_messages = []
    if id_flow_page == conversation.get_conversation(sender, receiver).get("id_flow_page"):
        wa_messages.append("Silahkan kirim pesan kembali")

    conversation.add_conversation({
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "id_flow_page": id_flow_page,
        "id_restaurant": id_restaurant
    })

    if id_flow_page == "pesan":
        wa_message = "pesan ke agent"
    else:
        wa_message = get_message(id_flow_page, id_restaurant) if id_flow_page != -1 else "no more"

    wa_messages.append(wa_message)

    return {
        "message": "success",
        "wa_messages": wa_messages,
        "sender": sender,
        "receiver": receiver,
        "data": {
            "id_flow_page" : id_flow_page,
            "id_restaurant": id_restaurant
        }
    }
