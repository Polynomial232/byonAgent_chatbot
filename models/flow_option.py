import requests
from utils.GetOptionsTable import GetOptionsTable

class FlowOption:
    def __init__(self, ip, port=8000):
        self.ip = ip
        self.port = port

    def get_page_options(self, option_group, id_restaurant):
        response_options = requests.get(f"http://{self.ip}:{self.port}/flow-options/{option_group}")
        options = response_options.json()

        if options[0].get("table_name") is None:
            return options

        table_name = options[0].get("table_name")

        return getattr(globals()['GetOptionsTable'](), f"{table_name}_options")(options, id_restaurant)