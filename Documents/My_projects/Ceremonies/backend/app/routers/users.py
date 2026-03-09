import os
import shutil
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import get_current_user
from app import models, schemas
from app.crud import get_user_by_id
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])

UPLOAD_DIR = Path("uploads/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/me", response_model=schemas.UserRead)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user

class UserUpdate(BaseModel):
    full_name: Optional[str] = None

@router.put("/me", response_model=schemas.UserRead)
def update_current_user(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = get_user_by_id(db, current_user.id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    if data.full_name is not None:
        user.full_name = data.full_name
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, "Accès interdit")
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Utilisateur non trouvé")
    return user

@router.post("/avatar", response_model=schemas.UserRead)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.avatar_url:
        old_path = Path("." + current_user.avatar_url)
        if old_path.exists():
            old_path.unlink()
    ext = os.path.splitext(file.filename)[1]
    filename = f"avatar_{current_user.id}_{int(datetime.utcnow().timestamp())}{ext}"
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    avatar_url = f"/uploads/avatars/{filename}"
    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user