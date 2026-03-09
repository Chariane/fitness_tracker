from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.core.auth import get_current_user
from app import models, schemas

router = APIRouter(prefix="/admin", tags=["Admin"])

def admin_required(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(403, "Admin privileges required")
    return current_user

@router.get("/prestataires/pending")
def get_pending_prestataires(
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    prestataires = db.query(models.Prestataire).filter(models.Prestataire.verified == False).all()
    return prestataires

@router.get("/prestataires/{prestataire_id}/documents")
def get_prestataire_documents(
    prestataire_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    docs = db.query(models.VerificationDocument).filter(
        models.VerificationDocument.prestataire_id == prestataire_id
    ).all()
    return docs

@router.post("/prestataires/{prestataire_id}/verify")
def verify_prestataire(
    prestataire_id: int,
    data: dict,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    prestataire = db.query(models.Prestataire).filter(models.Prestataire.id == prestataire_id).first()
    if not prestataire:
        raise HTTPException(404, "Prestataire not found")

    if data['approved']:
        # Si une nouvelle catégorie a été proposée, la créer
        if prestataire.proposed_category:
            existing_cat = db.query(models.ServiceCategory).filter(
                models.ServiceCategory.name == prestataire.proposed_category
            ).first()
            if existing_cat:
                prestataire.category_id = existing_cat.id
            else:
                new_cat = models.ServiceCategory(name=prestataire.proposed_category)
                db.add(new_cat)
                db.flush()
                prestataire.category_id = new_cat.id
                # Note : on ne crée plus de service par défaut, car la table Service a été supprimée.
            prestataire.proposed_category = None

        prestataire.verified = True
        prestataire.verified_at = datetime.utcnow()
        user = db.query(models.User).filter(models.User.id == prestataire.user_id).first()
        if user:
            user.is_prestataire = True
    else:
        db.delete(prestataire)

    db.commit()
    return {"ok": True}

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    total_users = db.query(models.User).count()
    total_prestataires = db.query(models.Prestataire).count()
    total_ceremonies = db.query(models.Ceremony).count()
    pending_verifications = db.query(models.Prestataire).filter(models.Prestataire.verified == False).count()
    return {
        "totalUsers": total_users,
        "totalPrestataires": total_prestataires,
        "totalCeremonies": total_ceremonies,
        "pendingVerifications": pending_verifications
    }

# Gestion des catégories de services
from app import crud
@router.get("/service-categories", response_model=List[schemas.ServiceCategoryRead])
def get_service_categories(db: Session = Depends(get_db)):
    return crud.get_service_categories(db)

@router.post("/service-categories", response_model=schemas.ServiceCategoryRead)
def create_service_category(
    data: schemas.ServiceCategoryCreate,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    return crud.create_service_category(db, data)

@router.put("/service-categories/{category_id}", response_model=schemas.ServiceCategoryRead)
def update_service_category(
    category_id: int,
    data: schemas.ServiceCategoryCreate,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    return crud.update_service_category(db, category_id, data)

@router.delete("/service-categories/{category_id}")
def delete_service_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    crud.delete_service_category(db, category_id)
    return {"ok": True}

@router.get("/users", response_model=List[schemas.UserRead])
def get_all_users(
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    users = db.query(models.User).all()
    return users

@router.patch("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    user.is_active = not user.is_active
    db.commit()
    return {"ok": True, "is_active": user.is_active}