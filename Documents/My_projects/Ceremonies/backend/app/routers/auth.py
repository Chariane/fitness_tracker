from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import UserCreate, UserRead
from app.schemas import LoginInput, TokenOutput
from app.crud import get_user_by_email, create_user
from app.core.security import verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(400, "Email déjà utilisé")

    user = create_user(
        db,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
    )
    return user

@router.post("/login", response_model=TokenOutput)
def login(data: LoginInput, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Identifiants invalides")
    token = create_token({"sub": str(user.id)})
    return {"access_token": token}