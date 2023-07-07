# pylint: disable=no-name-in-module, too-few-public-methods

""" docstring """

import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FILENAME = 'dataset.json'

@app.get('/')
async def index():
    """ docstring """

    return 0

""" DUMMY DATA API OPEN """

@app.get('/dummy/restoran/{region}')
def get_dummy_restoran(region):
    with open(f"{region}/restoran.json", encoding='utf-8') as f:
        return json.loads(f.read())

@app.get('/dummy/restoran/{region}/{id_resto}')
def get_dummy_restoran_id(region, id_resto):
    restoran = get_dummy_restoran(region)
    for i in restoran:
        if i.get("uuid") == id_resto:
            return i

@app.get('/dummy/menu/{region}/{restoran}')
def get_dummy_restoran_menu(region, restoran):
    with open(f"{region}/menu_{restoran}.json", encoding='utf-8') as f:
        return json.loads(f.read())

@app.get('/dummy/flow-chat/{region}')
def get_dummy_flow_chat(region):
    try:
        with open(f"{region}/flow_chat.json", encoding='utf-8') as f:
            return json.loads(f.read())
    except:
        return False

@app.get('/dummy/flow-chat/{region}/{id}')
def get_dummy_flow_chat_id(region, id):
    flow = get_dummy_flow_chat(region)

    if not flow:
        return False

    for i in flow:
        if i.get("uuid") == id:
            return i

@app.get('/dummy/flow-options/{region}')
def get_dummy_flow_options(region, group=None):
    try:
        with open(f"{region}/flow_options.json", encoding='utf-8') as f:
            flow_options = json.loads(f.read())

        if group is None:
            return flow_options
        
        for option in flow_options:
            if option.get("options_group") == group:
                return option
    except:
        return False


""" DUMMY DATA API CLOSE """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
