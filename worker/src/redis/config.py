import os 
from dotenv import load_dotenv
import aioredis 
from rejson import Client

load_dotenv()

class Redis():                                                                                          # we create a Redis object and initialize the required parameters from the environment variables
    def __init__(self):
        """initialize connection """
        self.REDIS_URL = os.environ['REDIS_URL']
        self.REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
        self.REDIS_USER = os.environ['REDIS_USER']
        self.connection_url = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_URL}"

async def create_connection(self):                                                                      # creating a Redis connection and return the connection pool obtained by the aioredis method from_url
    self.connection = aioredis.from_url(
        self.connection_url, db=0)
    
    return self.connection

async def create_connection(self):
    self.connection = aioredis.from_url(
        self.connection_url, db=0)

    return self.connection

def create_rejson_connection(self):
    self.redisJson = Client(host=self.REDIS_HOST,
                            port=self.REDIS_PORT, decode_responses=True, username=self.REDIS_USER, password=self.REDIS_PASSWORD)