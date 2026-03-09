from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import get_current_user
from app import models

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{offer_id}")
def add_favorite(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Ajouter une offre aux favoris de l'utilisateur connecté"""
    # Vérifier que l'offre existe
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(404, "Offre non trouvée")
    
    # Vérifier si déjà en favori
    existing = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.offer_id == offer_id
    ).first()
    if existing:
        raise HTTPException(400, "Offre déjà dans les favoris")
    
    fav = models.Favorite(user_id=current_user.id, offer_id=offer_id)
    db.add(fav)
    db.commit()
    return {"ok": True}

@router.delete("/{offer_id}")
def remove_favorite(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Retirer une offre des favoris"""
    fav = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.offer_id == offer_id
    ).first()
    if not fav:
        raise HTTPException(404, "Offre non trouvée dans les favoris")
    
    db.delete(fav)
    db.commit()
    return {"ok": True}

@router.get("/check/{offer_id}")
def check_favorite(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Vérifier si l'offre est dans les favoris de l'utilisateur"""
    fav = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.offer_id == offer_id
    ).first()
    return {"liked": fav is not None}