from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import MessageCreate, MessageRead, ConversationCreate, ConversationRead
from app.crud import send_message, create_conversation, get_user_conversations, get_conversation
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

# Créer une conversation
@router.post("/conversations", response_model=ConversationRead)
def create_new_conversation(data: ConversationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_conversation(db, data)

# Récupérer toutes les conversations de l'utilisateur
@router.get("/conversations", response_model=list[ConversationRead])
def list_conversations(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_user_conversations(db, current_user.id)

# Envoyer un message
@router.post("/messages", response_model=MessageRead)
def post_message(data: MessageCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return send_message(db, current_user.id, data)
    except Exception as e:
        raise HTTPException(400, str(e))

# Récupérer les messages d'une conversation
@router.get("/conversations/{conv_id}/messages", response_model=list[MessageRead])
def list_messages(conv_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    conv = get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(404, "Conversation non trouvée")
    if current_user.id not in [conv.client_id, conv.prestataire_id]:
        raise HTTPException(403, "Accès refusé")
    return conv.messages
