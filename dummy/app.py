# pylint: disable=no-name-in-module, too-few-public-methods

""" docstring """

import json
from fastapi import FastAPI, Request
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

@app.get('/flow-pages')
def get_flow_pages():
    return json.loads(open('tb_flow_pages.json', 'r', encoding='utf-8').read())

@app.get('/flow-pages/{id_flow_page}')
def get_flow_pages_id(id_flow_page):
    flow_pages = get_flow_pages()
    for flow_page in flow_pages:
        if str(flow_page.get("id_flow_page")) == id_flow_page:
            return flow_page

@app.get('/flow-options')
def get_flow_options():
    return json.loads(open('tb_flow_options.json', 'r', encoding='utf-8').read())

@app.get('/flow-options/{group_id}')
def get_flow_options_group_id(group_id):
    flow_options = get_flow_options()

    return [option for option in flow_options if option.get("group_id") == group_id]

@app.get('/restaurants')
def get_restaurants():
    return json.loads(open('tb_restaurants.json', 'r', encoding='utf-8').read())

@app.get('/restaurants/{id_restaurant}')
def get_restaurants_id(id_restaurant):
    restaurants = get_restaurants()
    for restaurant in restaurants:
        if str(restaurant.get("id_restaurant")) == id_restaurant:
            return restaurant

@app.get('/categories-menus')
def get_categories():
    categories = json.loads(open('tb_categories_menu.json', 'r', encoding='utf-8').read())
    for idx, category in enumerate(categories):
        categories[idx]['menus'] = []
        for menu in get_menus_id_category(category.get("id_category_menu")):
            categories[idx]['menus'].append(menu)
    
    return categories

@app.get('/categories-menus/{id_restaurant}')
def get_categories_id_restaurant(id_restaurant):
    return [categories for categories in get_categories() if str(categories.get("id_restaurant")) == id_restaurant]

@app.get('/last-message')
def get_last_message(sender, receiver):
    conversations = json.loads(open('tb_conversations.json', 'r', encoding='utf-8').read())
    for conversation in conversations:
        if conversation.get("sender") == sender and conversation.get("receiver") == receiver:
            return conversation
    return 0

@app.post('/last-message')
async def post_last_message(request: Request):
    request = await request.json()

    conversations = json.loads(open('tb_conversations.json', 'r', encoding='utf-8').read())
    for idx, conversation in enumerate(conversations):
        if conversation.get("sender") == request.get("sender") and conversation.get("receiver") == request.get("receiver"):
            conversations[idx] = request
            break
    else:
        conversations.append(request)
    
    with open('tb_conversations.json', 'w', encoding='utf-8') as f:
        json.dump(conversations, f, indent=4)
    
    return request

def get_menus():
    return json.loads(open('tb_menus.json', 'r', encoding='utf-8').read())

def get_menus_id_category(id_category):
    menus = get_menus()
    return [menu for menu in menus if menu.get("id_category_menu") == id_category]

""" DUMMY DATA API CLOSE """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
