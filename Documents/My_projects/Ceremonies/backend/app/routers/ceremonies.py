from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas import CeremonyCreate, CeremonyRead
from app.crud import create_ceremony, get_intelligent_suggestions, get_user_ceremonies
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/ceremonies", tags=["Ceremonies"])

@router.get("/", response_model=List[CeremonyRead])
def read_user_ceremonies(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupère toutes les cérémonies de l'utilisateur connecté"""
    ceremonies = get_user_ceremonies(db, current_user.id)
    return ceremonies

@router.post("/", response_model=CeremonyRead)
def create_new_ceremony(data: CeremonyCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_ceremony(db, current_user.id, data)

@router.get("/{ceremony_id}/suggestions")
def get_suggestions(ceremony_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        suggestions = get_intelligent_suggestions(db, ceremony_id)
    except Exception as e:
        raise HTTPException(404, str(e))
    return suggestions