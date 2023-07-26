import requests
import json

class Conversation:
    def __init__(self, ip, port=8000):
        self.ip = ip
        self.port = port

    def get_conversation(self, sender, receiver):
        response_last_message = requests.get(f"http://{self.ip}:{self.port}/last-message?sender={sender}&receiver={receiver}")

        return response_last_message.json()

    def add_conversation(self, data):
        post_last_message = requests.post(f"http://{self.ip}:{self.port}/last-message", data=json.dumps(data))

        return post_last_message.status_code
