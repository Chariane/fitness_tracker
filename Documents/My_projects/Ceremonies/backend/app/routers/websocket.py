from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter, Query
from typing import Dict
import json
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import get_current_user_ws
from app.crud import save_message, get_conversation
from app import schemas

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}  # user_id -> websocket

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    # Authentification
    try:
        authenticated_user_id = await get_current_user_ws(websocket, token)
        if authenticated_user_id != user_id:
            await websocket.close(code=1008, reason="User ID mismatch")
            return
    except Exception:
        await websocket.close(code=1008, reason="Invalid token")
        return

    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            # data doit contenir: receiver_id, content, conversation_id (optionnel)
            receiver_id = data.get("receiver_id")
            content = data.get("content")
            conversation_id = data.get("conversation_id")

            if not receiver_id or not content:
                continue  # ignorer message invalide

            # Sauvegarder en base
            message = save_message(db, sender_id=user_id, receiver_id=receiver_id,
                                    content=content, conversation_id=conversation_id)
            # Convertir en dict pour l'envoi
            message_dict = {
                "id": message.id,
                "sender_id": message.sender_id,
                "receiver_id": message.receiver_id,
                "conversation_id": message.conversation_id,
                "content": message.content,
                "created_at": message.created_at.isoformat() if message.created_at else None,
            }
            # Envoyer au destinataire
            await manager.send_personal_message(message_dict, receiver_id)
            # Envoyer une confirmation à l'expéditeur (optionnel)
            await manager.send_personal_message({"status": "sent", "message": message_dict}, user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)