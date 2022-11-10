from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []       #initialized with an active_connections attribute that is a list of active connections

    async def connect(self, websocket: WebSocket):          # accept a Websocket and add it to the list of active connections
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):             # this will remove the Websocket from the list of active connections
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):      # this will take in a message and the Websocket we want to send the messgae to and asynchronously send the message
        await websocket.send_text(message) 