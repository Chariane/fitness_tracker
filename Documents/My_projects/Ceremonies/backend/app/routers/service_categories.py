from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.auth import get_current_user
from app.schemas import ServiceCategoryCreate, ServiceCategoryRead
from app.crud import (
    get_service_categories,
    get_service_category,
    create_service_category as crud_create_service_category,
    update_service_category as crud_update_service_category,
    delete_service_category as crud_delete_service_category,
)
from app.models import User

router = APIRouter(prefix="/service-categories", tags=["Service Categories"])

# Dépendance pour vérifier que l'utilisateur est admin
def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(403, "Seuls les administrateurs peuvent effectuer cette action")
    return current_user

# Routes publiques (lecture)
@router.get("/", response_model=List[ServiceCategoryRead])
def read_service_categories(db: Session = Depends(get_db)):
    return get_service_categories(db)


@router.get("/{category_id}", response_model=ServiceCategoryRead)
def read_service_category(category_id: int, db: Session = Depends(get_db)):
    db_cat = get_service_category(db, category_id)
    if not db_cat:
        raise HTTPException(404, "Catégorie non trouvée")
    return db_cat


# Routes admin (écriture)
@router.post("/", response_model=ServiceCategoryRead)
def create_service_category(
    data: ServiceCategoryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required),
):
    return crud_create_service_category(db, data)


@router.put("/{category_id}", response_model=ServiceCategoryRead)
def update_service_category(
    category_id: int,
    data: ServiceCategoryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required),
):
    db_cat = crud_update_service_category(db, category_id, data)
    if not db_cat:
        raise HTTPException(404, "Catégorie non trouvée")
    return db_cat


@router.delete("/{category_id}")
def delete_service_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required),
):
    deleted = crud_delete_service_category(db, category_id)
    if not deleted:
        raise HTTPException(404, "Catégorie non trouvée")
    return {"ok": True}