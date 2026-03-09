from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app import models, schemas

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/prestataire/{prestataire_id}")
def get_prestataire_reviews(prestataire_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(
        models.Review.prestataire_id == prestataire_id
    ).all()
    # Enrichir avec les données utilisateur
    result = []
    for r in reviews:
        user = db.query(models.User).filter(models.User.id == r.client_id).first()
        result.append({
            "id": r.id,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at,
            "author": user.full_name if user else "Anonyme",
            "eventType": "Événement",  # à remplacer si disponible
        })
    return result