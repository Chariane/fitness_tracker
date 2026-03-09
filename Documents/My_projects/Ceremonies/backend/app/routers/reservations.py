from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ReservationCreate, ReservationRead
from app.crud import create_reservation
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationRead)
def reserve_offer(data: ReservationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    reservation = create_reservation(db, client_id=current_user.id, prestataire_id=None, data=data)
    return reservation