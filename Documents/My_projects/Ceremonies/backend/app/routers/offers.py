from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.core.auth import get_current_user
from app.schemas import OfferCreate, OfferRead
from app.crud import create_offer, get_active_offers
from app import models
from app import schemas

router = APIRouter(prefix="/offers", tags=["Offers"])

@router.get("/me", response_model=List[OfferRead])
def get_my_offers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user.is_prestataire:
        raise HTTPException(403, "Accès réservé aux prestataires")
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire:
        return []
    offers = db.query(models.Offer).filter(
        models.Offer.prestataire_id == prestataire.id
    ).all()
    return offers

@router.post("/", response_model=OfferRead)
def add_offer(
    data: OfferCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user.is_prestataire:
        raise HTTPException(403, "Seuls les prestataires peuvent créer des offres")
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire:
        raise HTTPException(400, "Profil prestataire incomplet")
    return create_offer(db, prestataire.id, data)

@router.get("/", response_model=List[OfferRead])
def list_offers(db: Session = Depends(get_db)):
    return get_active_offers(db)

@router.get("/{offer_id}", response_model=schemas.OfferRead)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(404, "Offre non trouvée")
    likes_count = db.query(models.Favorite).filter(models.Favorite.offer_id == offer_id).count()
    # On peut renvoyer un dictionnaire ou utiliser un modèle avec from_attributes
    # Pour simplifier, on convertit en dict et on ajoute likes_count
    offer_dict = {
        "id": offer.id,
        "ceremony_type_id": offer.ceremony_type_id,
        "title": offer.title,
        "description": offer.description,
        "prestataire_id": offer.prestataire_id,
        "base_price": float(offer.base_price) if offer.base_price else None,
        "is_active": offer.is_active,
        "created_at": offer.created_at,
        "likes_count": likes_count,
    }
    return offer_dict

@router.put("/{offer_id}", response_model=OfferRead)
def update_offer(
    offer_id: int,
    data: OfferCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(404, "Offre non trouvée")
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire or offer.prestataire_id != prestataire.id:
        raise HTTPException(403, "Vous n'êtes pas autorisé à modifier cette offre")

    offer.ceremony_type_id = data.ceremony_type_id
    offer.title = data.title
    offer.description = data.description
    offer.base_price = data.base_price
    db.commit()
    db.refresh(offer)
    return offer

@router.delete("/{offer_id}")
def delete_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(404, "Offre non trouvée")
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire or offer.prestataire_id != prestataire.id:
        raise HTTPException(403, "Vous n'êtes pas autorisé à supprimer cette offre")
    db.delete(offer)
    db.commit()
    return {"ok": True}

@router.get("/filter", response_model=List[OfferRead])
def filter_offers(
    ceremony_type_id: Optional[int] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    offers = get_active_offers(db)
    if ceremony_type_id:
        offers = [o for o in offers if o.ceremony_type_id == ceremony_type_id]
    if max_price:
        offers = [o for o in offers if o.base_price is not None and o.base_price <= max_price]
    return offers