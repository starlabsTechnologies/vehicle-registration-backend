from typing import List
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_ip: str):
        await websocket.accept()
        self.active_connections[client_ip] = websocket

    async def disconnect(self, client_ip: str):
        if client_ip in self.active_connections:
            del self.active_connections[client_ip]

    async def send_message(self, message: str, client_ip: str):
        websocket = self.active_connections.get(client_ip)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def get_websocket(self, client_ip: str):
        return self.active_connections.get(client_ip)
    
    # def __init__(self):
    #     self.active_connections: List[WebSocket] = []

    # async def connect(self, websocket: WebSocket):
    #     await websocket.accept()
    #     self.active_connections.append(websocket)

    # def disconnect(self, websocket: WebSocket):
    #     self.active_connections.remove(websocket)

    # async def send_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

