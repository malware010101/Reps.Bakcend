from fastapi import WebSocket
from typing import Dict, List
from app.models import Mensaje, Chat


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.admin_connections: List[WebSocket] = []

    async def connect(self, chat_id: int, websocket: WebSocket, user_id: int, is_admin=False):
        await websocket.accept()
        websocket.user_id = user_id
        if is_admin:
            self.admin_connections.append(websocket)
        else:
            if chat_id not in self.active_connections:
                self.active_connections[chat_id] = []
            self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: int, websocket: WebSocket, is_admin=False):
        if is_admin and websocket in self.admin_connections:
            self.admin_connections.remove(websocket)
        elif chat_id in self.active_connections and websocket in self.active_connections[chat_id]:
            self.active_connections[chat_id].remove(websocket)
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast_chat(self, chat_id: int, message: dict):
        """Enviar a todos los usuarios de este chat y a todos los admins"""
        if chat_id in self.active_connections:
            for ws in self.active_connections[chat_id]:
                await ws.send_json(message)
        for ws in self.admin_connections:
            await ws.send_json(message)

    async def broadcast_total_no_leidos(self):
        """Actualizar badge global y por chat en todos los WS conectados"""
        from app.models import Mensaje

        # Admins
        for ws in self.admin_connections:
            total = await Mensaje.filter(leido=False).exclude(remitente_id=ws.user_id).count()
            await ws.send_json({"type": "total_no_leidos_por_chat", "totales": {0: total}})

        # Usuarios: cada usuario recibe su chat
        for chat_id, conns in self.active_connections.items():
            for ws in conns:
                total = await Mensaje.filter(chat_id=chat_id, leido=False).exclude(remitente_id=ws.user_id).count()
                await ws.send_json({"type": "total_no_leidos_por_chat", "totales": {chat_id: total}})


manager = ConnectionManager()
