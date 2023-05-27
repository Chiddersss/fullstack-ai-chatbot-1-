import os 
from dotenv import load_dotenv
import requests
import json

load_dotenv()

class GPT:                                                                                  # initializing the HUGGINFACE model url
    def __init__(self):
        self.url = os.environ.get('MODEL_URL')
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HUGGINFACE_INFERENCE_TOKEN')}"}      # authenctation header
        self.payload = {
            'inputs': "",                                                                   # predefined payload
            "parameters": {
                "return_full_text": False,                                                 # the payload is a dyamic field that is provided by the query method and updated before we send a request to the HUGGINFACE endpoint
                "use_cache": False,           # use_cache false so the model creates a new response when the input is the same
                "max_new_tokens": 25
            }
        
        }

def query(self, input: str) -> list:
    self.payload["inputs"] = f"Human: {input} Bot:"
    data = json.dumps(self.payload)
    response = requests.request(
        "POST", self.url, headers=self.headers, data=data)
    data = json.loads(response.content.decode("utf-8"))
    text = data[0]['generated_text']
    res = str(text.split("Human: ")[0]).strip("/n").strip()
    return res

if __name__ == "__main__":
    GPT().query("Will artifical intelligence help humanity conquer the universe?")         # testing using the query method

