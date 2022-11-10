from http.client import HTTPException
import os
from urllib import response
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, Request, Depends
import uuid
from ..socket.connection import ConnectionManager
from ..socket.utils import get_token
import time
from ..redis.producer import Producer
from ..redis.config import Redis
from ..schema.chat import Chat
from rejson import Path
from redis.cache import Cache

chat = APIRouter()
manager = ConnectionManager()
redis = Redis()


# @route   POST /token
# @desc    Route to generate chat token
# @access  Public


@chat.post("/token")
async def token_generator(name: str, request: Request):             # client provides their name
    token = str(uuid.uuid4())                                       # generation of the token using UUID4

    if name == "":                                                  # we do a quick check to ensure the field is not empty
        raise HTTPException(status_code=400, detail={
            "loc": "name",  "msg": "Enter a valid name"})           # a simple dictionary for the name and token

    # Create nee chat session
    json_client = redis.create_rejson_connection()
    chat_session = Chat(
        token=token,
        messages=[],
        name=name
    )

    print(chat_session.dict())

    # Store chat session in redis JSON with the token as key
    json_client.jsonset(str(token), Path.rootPath(), chat_session.dict())

    # Set a timeout for redis data
    redis_client = await redis.create_connection()
    await redis_client.expire(str(token), 3600)

    return chat_session.dict()


# @route   POST /refresh_token
# @desc    Route to refresh token
# @access  Public


@chat.get("/refresh_token")
async def refresh_token(request: Request, token: str):
    json_client = redis.create_json_connection()
    cache = Cache(json_client)
    data = await cache.get_chat_history(token)

    if data == None:
        raise HTTPException(
            status_code=400, detail="Session expired or does not exist")
    else:
        return data


# @route   Websocket /chat
# @desc    Socket for chat bot
# @access  Public

@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):                                        # takes a WebSocket and adds the new websocket to the connection manager
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)
    json_client = redis.create_rejson_connection()
    consumer = StreamConsumer(redis_client)

    try:
        while True:                                                                                                        # running a while loop to ensure the socket stays open
            data = await websocket.receive_text()
            stream_data = {}
            stream_data[str(token)] = str(data)
            await producer.add_to_stream(stream_data, "message_channel", blovk=0)
            response = await consumer.consume_stream(stream_channel='response_channel', block=0)

            print(response)
            for stream, messages in response:
                for message in messages:
                 response_token = [k.decode('utf-8')
                                      for k, v in message[1].items()][0]

                if token == response_token:
                        response_message = [v.decode('utf-8')
                                            for k, v in message[1].items()][0]
                        
                        print(message[0].decode('utf-8'))
                        print(token)
                        print(response_token)

                        await manager.send_personal_message(response_message, websocket)

                await consumer.delete_message(stream_channel="response_channel", message_id=message[0].decode('utf-8'))
           
    except WebSocketDisconnect:                                                                                            # stops the while loop if there is a disconnect
        manager.disconnect(websocket)

# /token will issue the user a session token for access to the chat session, this wont authenticate but identifies the user

# /refresh_token will get the session history of the user if connection is lost 

# /chat will open a websocket to send messages to the client and the server