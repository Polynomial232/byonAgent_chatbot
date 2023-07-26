import requests

class Get_Options_Table:
    def __init__(self, ip, port="8000"):
        self.ip = ip
        self.port = port

    def restaurants_options(self, options_template, _):
        options = []
        response_restaurants = requests.get(f"http://{self.ip}:{self.port}/restaurants")

        for idx, response_restaurant in enumerate(response_restaurants.json()):
            options.append(options_template[0].copy())
            options[idx]['id_restaurant'] = response_restaurant.get('id_restaurant')
            options[idx]['option_text'] = response_restaurant.get('name')
            
        return options

    def menus_options(self, options_template, custom_id):
        options = []
        categories_menu = requests.get(f"http://{self.ip}:{self.port}/categories-menus/{custom_id}")

        for idx, category_menu in enumerate(categories_menu.json()):
            start_num = idx if idx == 0 else idx*len(category_menu.get("menus"))-1

            for menu_idx, menu in enumerate(category_menu.get("menus"), start=start_num):
                options.append(options_template[0].copy())
                options[menu_idx]['group'] = category_menu.get('name')
                harga = "{:,}".format(menu.get('price'))
                options[menu_idx]['option_text'] = f"{menu.get('name')} (Rp {harga})"

        return options