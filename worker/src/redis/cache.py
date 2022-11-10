from email import message
from .config import Redis
from reJson import Path

class Cache:                                                    # initializing the cache with a rejson client
    def __init__(self, json_client):
        self.json_client = json_client

    async def get_chat_history(self, token: str):                       # takes in a token to get the chat history for that token, from Redis
        data = self.json_client.jsonget(
            str(token), Path.rootPATH())

        return data

async def add_message_to_cache(self, token: str, source: str, message_data: dict):       # the jsonarrapend method provided by rejson appends the new message to the message array
    if source == "human":
        message_data['msg'] = "Human: " + (message_data['msg'])
    elif source == "bot":
        message_data['msg'] = "Bot: " + (message_data['msg'])

    self.json_client.jsonapprappend(
        str(token), Path('.messages'), message_data)

