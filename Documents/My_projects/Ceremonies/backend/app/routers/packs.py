from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.auth import get_current_user
from app import models, schemas
from app.services.pack_score import calculate_pack_score

router = APIRouter(prefix="/packs", tags=["Packs"])

@router.post("/", response_model=schemas.PackRead)
def create_pack(
    data: schemas.PackCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    pack = models.Pack(
        user_id=current_user.id,
        event_id=data.event_id,
        name=data.name,
        user_budget=data.user_budget,
        total_price=0.0,
        completion_score=0,
    )
    db.add(pack)
    db.commit()
    db.refresh(pack)

    if data.offer_ids:
        for offer_id in data.offer_ids:
            pack_offer = models.PackOffer(pack_id=pack.id, offer_id=offer_id)
            db.add(pack_offer)
        db.commit()

    # Recharger le pack avec les relations
    db.refresh(pack)
    pack.total_price = sum(po.offer.base_price or 0 for po in pack.offers)
    pack.completion_score = calculate_pack_score(pack, db)
    db.commit()
    db.refresh(pack)
    return pack


@router.get("/", response_model=List[schemas.PackRead])
def get_my_packs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    packs = db.query(models.Pack).filter(models.Pack.user_id == current_user.id).all()
    return packs

@router.get("/{pack_id}", response_model=schemas.PackRead)
def get_pack(
    pack_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    pack = db.query(models.Pack).filter(models.Pack.id == pack_id).first()
    if not pack:
        raise HTTPException(404, "Pack non trouvé")
    if pack.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Accès interdit")
    return pack

@router.put("/{pack_id}", response_model=schemas.PackRead)
def update_pack(
    pack_id: int,
    data: schemas.PackUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    pack = db.query(models.Pack).filter(
        models.Pack.id == pack_id,
        models.Pack.user_id == current_user.id
    ).first()
    if not pack:
        raise HTTPException(404, "Pack non trouvé")

    if data.offer_ids is not None:
        # Supprimer les anciens liens
        db.query(models.PackOffer).filter(models.PackOffer.pack_id == pack.id).delete()
        # Ajouter les nouveaux
        for offer_id in data.offer_ids:
            pack_offer = models.PackOffer(pack_id=pack.id, offer_id=offer_id)
            db.add(pack_offer)
        db.commit()

    if data.name is not None:
        pack.name = data.name

    if data.user_budget is not None:
        pack.user_budget = data.user_budget

    # Recalcul
    db.refresh(pack)  # Pour recharger les relations
    pack.total_price = sum(po.offer.base_price or 0 for po in pack.offers)
    pack.completion_score = calculate_pack_score(pack, db)
    db.commit()
    db.refresh(pack)
    return pack


@router.delete("/{pack_id}")
def delete_pack(
    pack_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    pack = db.query(models.Pack).filter(models.Pack.id == pack_id).first()
    if not pack:
        raise HTTPException(404, "Pack non trouvé")
    if pack.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Accès interdit")
    db.delete(pack)
    db.commit()
    return {"ok": True}