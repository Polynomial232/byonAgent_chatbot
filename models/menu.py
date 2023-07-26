import requests

class Menu:
    def __init__(self, ip, port="8000"):
        self.ip = ip
        self.port = port

    def get_menus_by_category(self, custom_id):
        categories_menu = requests.get(f"http://{self.ip}:{self.port}/categories-menus/{custom_id}")

        return categories_menu.json()

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