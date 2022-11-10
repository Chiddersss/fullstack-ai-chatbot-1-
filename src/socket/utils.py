from optparse import Option
from fastapi import WebSocket, status, Query
from typing import Optional
from ..redis.config import Redis

async def get_token(                                                        # receives a WebSocket and token, 
    websocket: Websocket,                                                   
    token: Optional[str] = Query(None),
):
    if token is None or token == "":                                        # checks if the token is None or null
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)         # if this is the case, the function reutnrs a policy violation status
    return token                                                            # and if available, the function returns the token

    redis_client = await redis.create_connection()
    isexists = await redis_client.exists(token)

    if isexists ==1:
        return token
    else:
        await websocket.close(code=status.WS-WS_1008_POLICY_VIOLATION, reason="Session not authenticated or expired token")