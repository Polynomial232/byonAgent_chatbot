import requests

class Restaurant:
    def __init__(self, ip, port="8000"):
        self.ip = ip
        self.port = port

    def restaurants_options(self, options_template):
        options = []
        response_restaurants = requests.get(f"http://{self.ip}:{self.port}/restaurants")

        for idx, response_restaurant in enumerate(response_restaurants.json()):
            options.append(options_template[0].copy())
            options[idx]['id_restaurant'] = response_restaurant.get('id_restaurant')
            options[idx]['option_text'] = response_restaurant.get('name')
            
        return options
    
    def get_restaurants(self):
        response_restaurants = requests.get(f"http://{self.ip}:{self.port}/restaurants")
            
        return response_restaurants.json()

