# pylint: disable=no-name-in-module, too-few-public-methods

""" docstring """

import os
import json
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from decouple import config

from classes.PredictResponse import PredictResponse
from classes.Train import Train
from functions import *

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IP = config("IP")
FILENAME = 'dataset.json'

@app.get('/')
async def index():
    """ docstring """

    return 0

@app.get('/{region}/bot-response')
async def bot_response(text, region, agent_number, customer_number, id_user, chat_uuid):
    """ docstring """

    predict_response = PredictResponse(region)
    predict = predict_response.predict(text)
    response_bot_detail = predict_response.get_response(predict)
    fuzzy_prob = await fuzzy_check(text, response_bot_detail.get('pattern'))

    if fuzzy_prob < 70 and predict[1] < 70:
        message = "restoran tersebut tidak tersedia"
    else:
        check_open = requests.get(f"http://{IP}:8000/dummy/restoran/{region}/{response_bot_detail.get('id')}")
        if not check_open.json().get("status_buka"):
            message = "restoran tersebut tidak tersedia"
        else:
            message = await get_message(id_user, chat_uuid, region, response_bot_detail.get('id'))

    return {
        "message": message,
        "bot_detail": response_bot_detail,
        "dl_probabilitas": predict[1].item(),
        "fuzzy_probabilitas": fuzzy_prob,
        "agent_number": agent_number,
        "customer_number": customer_number
    }

@app.get('/{region}/train-model')
async def train_model(region, epochs=400):
    """ docstring """

    os.makedirs(f"model/{region}", exist_ok=True)

    restoran_dataset = requests.get(f"http://{IP}:8000/dummy/restoran/{region}")
    flow_options_dataset = requests.get(f"http://{IP}:8000/dummy/flow-options/{region}")

    intents = list()
    temp_intents = restoran_dataset.json() + flow_options_dataset.json()

    for intent in temp_intents:
        if intent.get("nama") is not None:
            pattern = intent.get("nama")
        else:
            pattern = intent.get("option_text")

        intents.append({
            "id":  intent.get("uuid"),
            "pattern": pattern
        })

    with open(f"model/{region}/intents.json", "w", encoding='utf-8') as f:
        json.dump({"intents": intents}, f, indent=4)

    train = Train(region, int(epochs))
    _ = train.start()

    currect_train = train.currect_train()
    train.plot_history()

    return currect_train

@app.get('/{region}/current-accuracy')
async def current_accuracy(region):
    """ docstring """

    return json.loads(open(f'model/{region}/current.json', encoding='utf-8').read())

@app.get('/{region}/intents')
def get_intents(region):
    """ docstring """

    return json.loads(open(f'model/{region}/intents.json', encoding='utf-8').read())

@app.get('/{region}/intents/{intent_id}')
def get_intent_by_id(intent_id, region):
    """ docstring """

    intents = get_intents(region).get('intents')
    get_data = [item for item in intents if item.get('id')==intent_id]
    if get_data:
        return get_data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
