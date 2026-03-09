from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.db.session import get_db
from app.core.auth import get_current_user
from app import models, schemas

router = APIRouter(prefix="/prestataire-favorites", tags=["Prestataire Favorites"])

@router.get("/", response_model=List[schemas.PrestataireRead])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Récupérer les favoris avec chargement des prestataires et de leurs utilisateurs associés
    favorites = db.query(models.PrestataireFavorite).filter(
        models.PrestataireFavorite.user_id == current_user.id
    ).options(
        joinedload(models.PrestataireFavorite.prestataire).joinedload(models.Prestataire.user)
    ).all()
    
    # Construire manuellement les objets PrestataireRead
    result = []
    for fav in favorites:
        prestataire = fav.prestataire
        user = prestataire.user
        prestataire_read = schemas.PrestataireRead(
            id=prestataire.id,
            business_name=prestataire.business_name,
            description=prestataire.description,
            city=prestataire.city,
            verified=prestataire.verified,
            category_id=prestataire.category_id,
            proposed_category=prestataire.proposed_category,
            created_at=prestataire.created_at,
            whatsapp=prestataire.whatsapp,
            business_image_url=prestataire.business_image_url,
            map_url=prestataire.map_url,
            avatar_url=user.avatar_url if user else None,
        )
        result.append(prestataire_read)
    return result

@router.get("/count", response_model=dict)
def get_favorites_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    count = db.query(models.PrestataireFavorite).filter(
        models.PrestataireFavorite.user_id == current_user.id
    ).count()
    return {"count": count}

@router.get("/check/{prestataire_id}", response_model=dict)
def check_favorite(
    prestataire_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    favorite = db.query(models.PrestataireFavorite).filter(
        models.PrestataireFavorite.user_id == current_user.id,
        models.PrestataireFavorite.prestataire_id == prestataire_id
    ).first()
    return {"isFavorite": favorite is not None}

@router.post("/{prestataire_id}", status_code=201)
def add_favorite(
    prestataire_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    prestataire = db.query(models.Prestataire).filter(models.Prestataire.id == prestataire_id).first()
    if not prestataire:
        raise HTTPException(404, "Prestataire non trouvé")
    existing = db.query(models.PrestataireFavorite).filter(
        models.PrestataireFavorite.user_id == current_user.id,
        models.PrestataireFavorite.prestataire_id == prestataire_id
    ).first()
    if existing:
        raise HTTPException(400, "Déjà en favori")
    favorite = models.PrestataireFavorite(
        user_id=current_user.id,
        prestataire_id=prestataire_id
    )
    db.add(favorite)
    db.commit()
    return {"ok": True}

@router.delete("/{prestataire_id}")
def remove_favorite(
    prestataire_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    favorite = db.query(models.PrestataireFavorite).filter(
        models.PrestataireFavorite.user_id == current_user.id,
        models.PrestataireFavorite.prestataire_id == prestataire_id
    ).first()
    if not favorite:
        raise HTTPException(404, "Favori non trouvé")
    db.delete(favorite)
    db.commit()
    return {"ok": True}