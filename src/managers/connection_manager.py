from typing import Any

from fastapi import WebSocket
from fastapi.websockets import WebSocketState

from managers.exceptions import ConnIdAlreadyExists
from utils.generators import generate_random_digit_char_string


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    def generate_next_id(self):
        ids: list[str] = self.get_conn_ids()
        while True:
            new_id: str = generate_random_digit_char_string()
            if new_id not in ids:
                return new_id

    def get_conn_ids(self):
        return list(self.connections.keys())

    async def connect(self, conn_id: str, websocket: WebSocket):
        if conn_id in self.connections.keys():
            raise ConnIdAlreadyExists()
        self.connections.update({conn_id: websocket})
        await websocket.accept()

    def disconnect(self, conn_id: str):
        self.connections.pop(conn_id)

    async def send_personal_data(self, data: Any, conn_id: str):
        await self.connections.get(conn_id).send_json(data)

    async def broadcast_except_sender(self, data: Any, sender_conn_id: str):
        for [conn_id, conn] in self.connections.items():
            if conn_id == sender_conn_id:
                continue
            await conn.send_json(data)

    async def broadcast(self, data: Any):
        for conn in self.connections.values():
            await conn.send_json(data)
