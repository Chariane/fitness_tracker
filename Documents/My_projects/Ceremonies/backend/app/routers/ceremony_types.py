from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.auth import get_current_user
from app.schemas import CeremonyTypeCreate, CeremonyTypeRead
from app.crud import (
    get_ceremony_types,
    get_ceremony_type,
    create_ceremony_type as crud_create_ceremony_type,
    update_ceremony_type as crud_update_ceremony_type,
    delete_ceremony_type as crud_delete_ceremony_type,
)

router = APIRouter(prefix="/ceremony-types", tags=["Ceremony Types"])

# Routes publiques
@router.get("/", response_model=List[CeremonyTypeRead])
def read_ceremony_types(db: Session = Depends(get_db)):
    return get_ceremony_types(db)

@router.get("/{type_id}", response_model=CeremonyTypeRead)
def read_ceremony_type(type_id: int, db: Session = Depends(get_db)):
    db_type = get_ceremony_type(db, type_id)
    if not db_type:
        raise HTTPException(404, "Type non trouvé")
    return db_type

# Routes protégées pour admin
@router.post("/", response_model=CeremonyTypeRead)
def create_ceremony_type(
    data: CeremonyTypeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(403, "Seuls les administrateurs peuvent créer des types")
    return crud_create_ceremony_type(db, data)

@router.put("/{type_id}", response_model=CeremonyTypeRead)
def update_ceremony_type(
    type_id: int,
    data: CeremonyTypeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(403, "Seuls les administrateurs peuvent modifier des types")
    db_type = crud_update_ceremony_type(db, type_id, data)
    if not db_type:
        raise HTTPException(404, "Type non trouvé")
    return db_type

@router.delete("/{type_id}")
def delete_ceremony_type(
    type_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(403, "Seuls les administrateurs peuvent supprimer des types")
    deleted = crud_delete_ceremony_type(db, type_id)
    if not deleted:
        raise HTTPException(404, "Type non trouvé")
    return {"ok": True}