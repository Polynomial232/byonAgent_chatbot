import requests

class FlowPage:
    def __init__(self, ip, port=8000):
        self.ip = ip
        self.port = port

    def get_page(self, id_flow_pages):
        flow = requests.get(f"http://{self.ip}:{self.port}/flow-pages/{id_flow_pages}")
        return flow.json()