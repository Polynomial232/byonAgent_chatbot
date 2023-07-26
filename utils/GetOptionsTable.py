from decouple import config

from models.restaurant import Restaurant
from models.menu import Menu

IP = config("IP")


class GetOptionsTable:
    def __init__(self):
        self.restaurant = Restaurant(IP)
        self.menu = Menu(IP)

    def restaurants_options(self, options_template, _):
        options = []
        restaurants = self.restaurant.get_restaurants()

        for idx, response_restaurant in enumerate(restaurants):
            options.append(options_template[0].copy())
            options[idx]['id_restaurant'] = response_restaurant.get('id_restaurant')
            options[idx]['option_text'] = response_restaurant.get('name')
        
        return options

    def menus_options(self, options_template, custom_id):
        menus_by_category = self.menu.get_menus_by_category(custom_id)

        options = []
        for idx, category_menu in enumerate(menus_by_category):
            start_num = idx if idx == 0 else idx*len(category_menu.get("menus"))-1

            for menu_idx, menu in enumerate(category_menu.get("menus"), start=start_num):
                options.append(options_template[0].copy())
                options[menu_idx]['group'] = category_menu.get('name')
                harga = "{:,}".format(menu.get('price'))
                options[menu_idx]['option_text'] = f"{menu.get('name')} (Rp {harga})"
        
        return options