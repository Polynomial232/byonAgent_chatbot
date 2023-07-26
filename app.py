""" docstring """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from decouple import config

from utils.get_response_bot import fuzzy_check
from classes.Chatbot_Agent import Chatbot_Agent

LINK = config("MICROSITE_URL")
IP = config("IP")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index():
    """ docstring """

    return 0

@app.get('/response')
async def get_response(message, sender, receiver):
    """ docstring """
    
    chatbot_agent = Chatbot_Agent(IP)

    if not message:
        id_flow_page = 1
        id_restaurant = 1
    else:
        last_message = chatbot_agent.get_last_message(sender, receiver)
        id_flow_page = last_message.get("id_flow_page") if last_message.get("id_flow_page") else 1
        id_restaurant = last_message.get("id_restaurant") if last_message.get("id_restaurant") else 1

        if "resto" in message.lower():
            id_flow_page = 1
        else:
            id_flow_page, id_restaurant = fuzzy_check(message, id_flow_page, id_restaurant)

    wa_messages = []
    if id_flow_page == chatbot_agent.get_last_message(sender, receiver).get("id_flow_page"):
        wa_messages.append("Silahkan kirim pesan kembali")
    
    chatbot_agent.post_last_message({
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "id_flow_page": id_flow_page,
        "id_restaurant": id_restaurant
    })

    if id_flow_page == "pesan":
        wa_message = "pesan ke agent"
    else:
        wa_message = chatbot_agent.get_message(id_flow_page, id_restaurant) if id_flow_page != -1 else "no more"
    
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
