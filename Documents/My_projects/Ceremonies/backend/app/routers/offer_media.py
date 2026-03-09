import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import get_current_user
from app import models, schemas

router = APIRouter(prefix="/offer-media", tags=["Offer Media"])

UPLOAD_DIR = Path("uploads/offers")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/{offer_id}", response_model=schemas.OfferMediaRead)
def upload_offer_media(
    offer_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Vérifier que l'offre appartient au prestataire connecté
    offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(404, "Offre non trouvée")
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire or offer.prestataire_id != prestataire.id:
        raise HTTPException(403, "Vous n'êtes pas autorisé à modifier cette offre")

    # Générer un nom de fichier unique
    ext = os.path.splitext(file.filename)[1]
    filename = f"offer_{offer_id}_{int(datetime.utcnow().timestamp())}{ext}"
    file_path = UPLOAD_DIR / filename

    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    media_url = f"/uploads/offers/{filename}"

    media = models.OfferMedia(
        offer_id=offer_id,
        media_url=media_url,
        media_type=file.content_type
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media

@router.get("/{offer_id}", response_model=List[schemas.OfferMediaRead])
def get_offer_media(offer_id: int, db: Session = Depends(get_db)):
    media = db.query(models.OfferMedia).filter(models.OfferMedia.offer_id == offer_id).all()
    return media

@router.delete("/{media_id}")
def delete_offer_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    media = db.query(models.OfferMedia).filter(models.OfferMedia.id == media_id).first()
    if not media:
        raise HTTPException(404, "Média non trouvé")
    offer = db.query(models.Offer).filter(models.Offer.id == media.offer_id).first()
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire or offer.prestataire_id != prestataire.id:
        raise HTTPException(403, "Vous n'êtes pas autorisé à supprimer ce média")

    # Supprimer le fichier physique
    file_path = Path("." + media.media_url)  # media_url commence par /uploads/...
    if file_path.exists():
        file_path.unlink()

    db.delete(media)
    db.commit()
    return {"ok": True}