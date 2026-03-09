import os
import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Request
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas import PrestataireRead, PrestataireRequest, PrestataireUpdate
from app.db.session import get_db
from app.core.auth import get_current_user
from typing import Optional, List
from app import models, schemas
from sqlalchemy import func, or_

router = APIRouter(prefix="/prestataires", tags=["Prestataires"])

# ==================== ROUTES SPÉCIFIQUES (avant la route paramétrée) ====================

@router.post("/request", response_model=PrestataireRead)
def request_prestataire(
    data: PrestataireRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.is_prestataire:
        raise HTTPException(400, "Vous êtes déjà prestataire")

    existing = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(400, "Vous avez déjà une demande en cours")

    business_name = data.business_name
    category_id = None
    proposed_category = None

    if data.category_id:
        category = db.query(models.ServiceCategory).filter(
            models.ServiceCategory.id == data.category_id
        ).first()
        if not category:
            raise HTTPException(400, "Catégorie invalide")
        category_id = category.id
    elif data.new_category_name:
        proposed_category = data.new_category_name

    prestataire = models.Prestataire(
        user_id=current_user.id,
        business_name=business_name,
        category_id=category_id,
        description=data.description,
        city=data.city,
        whatsapp=data.whatsapp,
        map_url=data.map_url,
        verified=False,
        proposed_category=proposed_category,
    )
    db.add(prestataire)
    db.commit()
    db.refresh(prestataire)
    return prestataire

@router.get("/me", response_model=schemas.PrestataireRead)
def get_my_prestataire_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire:
        raise HTTPException(404, "Profil prestataire introuvable")
    # current_user contient déjà l'avatar
    return {
        "id": prestataire.id,
        "business_name": prestataire.business_name,
        "description": prestataire.description,
        "city": prestataire.city,
        "verified": prestataire.verified,
        "category_id": prestataire.category_id,
        "proposed_category": prestataire.proposed_category,
        "created_at": prestataire.created_at,
        "whatsapp": prestataire.whatsapp,
        "business_image_url": prestataire.business_image_url,
        "map_url": prestataire.map_url,
        "avatar_url": current_user.avatar_url,
    }


@router.put("/me", response_model=PrestataireRead)
def update_my_prestataire_profile(
    data: PrestataireUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire:
        raise HTTPException(404, "Profil prestataire introuvable")

    if data.business_name is not None:
        prestataire.business_name = data.business_name
    if data.description is not None:
        prestataire.description = data.description
    if data.city is not None:
        prestataire.city = data.city
    if data.whatsapp is not None:
        prestataire.whatsapp = data.whatsapp
    if data.map_url is not None:
        prestataire.map_url = data.map_url

    db.commit()
    db.refresh(prestataire)
    return prestataire

@router.get("/me/dashboard")
def get_prestataire_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user.is_prestataire:
        raise HTTPException(403, "Accès réservé aux prestataires")

    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire:
        raise HTTPException(404, "Profil prestataire introuvable")

    total_views = 0
    total_contacts = db.query(models.Message).join(
        models.Conversation,
        models.Message.conversation_id == models.Conversation.id
    ).filter(
        models.Conversation.prestataire_id == current_user.id
    ).count()
    total_reservations = db.query(models.Reservation).filter(
        models.Reservation.prestataire_id == prestataire.id,
        models.Reservation.status == "confirmed"
    ).count()
    avg_rating = db.query(func.avg(models.Review.rating)).filter(
        models.Review.prestataire_id == prestataire.id
    ).scalar() or 0.0

    return {
        "totalViews": total_views,
        "totalContacts": total_contacts,
        "totalReservations": total_reservations,
        "averageRating": round(avg_rating, 1)
    }

UPLOAD_DIR = Path("uploads/business")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/me/business-image", response_model=schemas.PrestataireRead)
async def upload_business_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user.is_prestataire:
        raise HTTPException(403, "Accès réservé aux prestataires")
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire:
        raise HTTPException(404, "Profil prestataire introuvable")

    # Supprimer l'ancienne image si elle existe
    if prestataire.business_image_url:
        old_path = Path("." + prestataire.business_image_url)
        if old_path.exists():
            old_path.unlink()

    # Générer un nom de fichier unique
    ext = os.path.splitext(file.filename)[1]
    filename = f"business_{prestataire.id}_{int(datetime.utcnow().timestamp())}{ext}"
    file_path = UPLOAD_DIR / filename

    # Sauvegarder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    business_image_url = f"/uploads/business/{filename}"
    prestataire.business_image_url = business_image_url
    db.commit()
    db.refresh(prestataire)
    return prestataire


@router.get("/search", response_model=List[schemas.PrestataireSearchRead])
def search_prestataires(
    request: Request,
    q: Optional[str] = None,
    category_ids: Optional[List[int]] = Query(None),
    city: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    verified_only: bool = False,
    sort_by: str = "relevance",
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    print("Paramètres reçus :", dict(request.query_params))
    
    # Sous-requêtes pour les offres (prix min/max) et avis
    offers_subq = db.query(
        models.Offer.prestataire_id,
        func.min(models.Offer.base_price).label('min_price'),
        func.max(models.Offer.base_price).label('max_price'),
        func.count(models.Offer.id).label('total_offers')
    ).group_by(models.Offer.prestataire_id).subquery()

    reviews_subq = db.query(
        models.Review.prestataire_id,
        func.avg(models.Review.rating).label('avg_rating'),
        func.count(models.Review.id).label('total_reviews')
    ).group_by(models.Review.prestataire_id).subquery()

    # Requête principale (on pourrait joindre User pour récupérer avatar_url, mais on mettra None pour l'instant)
    query = db.query(
        models.Prestataire,
        offers_subq.c.min_price,
        offers_subq.c.max_price,
        offers_subq.c.total_offers,
        reviews_subq.c.avg_rating,
        reviews_subq.c.total_reviews
    ).outerjoin(offers_subq, offers_subq.c.prestataire_id == models.Prestataire.id) \
     .outerjoin(reviews_subq, reviews_subq.c.prestataire_id == models.Prestataire.id)

    # Filtres
    if verified_only:
        query = query.filter(models.Prestataire.verified == True)

    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                models.Prestataire.business_name.ilike(search),
                models.Prestataire.description.ilike(search),
                models.Prestataire.city.ilike(search)
            )
        )

    if category_ids:
        query = query.filter(models.Prestataire.category_id.in_(category_ids))

    if city:
        query = query.filter(models.Prestataire.city.ilike(f"%{city}%"))

    if min_price is not None:
        query = query.filter(offers_subq.c.min_price >= min_price)
    if max_price is not None:
        query = query.filter(offers_subq.c.max_price <= max_price)

    # Tri
    if sort_by == "rating":
        query = query.order_by(reviews_subq.c.avg_rating.desc().nullslast())
    elif sort_by == "price_asc":
        query = query.order_by(offers_subq.c.min_price.asc().nullslast())
    elif sort_by == "price_desc":
        query = query.order_by(offers_subq.c.min_price.desc().nullslast())
    else:
        query = query.order_by(models.Prestataire.created_at.desc())

    # Pagination
    if limit:
        query = query.limit(limit)
    if page and limit:
        query = query.offset((page - 1) * limit)

    results = query.all()

    output = []
    for prestataire, min_price_val, max_price_val, total_offers, avg_rating, total_reviews in results:
        output.append({
            "id": prestataire.id,
            "business_name": prestataire.business_name,
            "description": prestataire.description,
            "city": prestataire.city,
            "verified": prestataire.verified,
            "whatsapp": prestataire.whatsapp,
            "business_image_url": prestataire.business_image_url,
            "map_url": prestataire.map_url,
            "category_id": prestataire.category_id,
            "avatar_url": None,  # ← ajouté pour satisfaire le schéma (optionnel)
            "total_offers": total_offers or 0,
            "min_price": float(min_price_val) if min_price_val else None,
            "max_price": float(max_price_val) if max_price_val else None,
            "avg_rating": float(avg_rating) if avg_rating else None,
            "total_reviews": total_reviews or 0,
        })

    return output


@router.get("/ping")
def ping():
    return {"ping": "pong"}

# ==================== ROUTE GÉNÉRIQUE (DOIT ÊTRE EN DERNIER) ====================

@router.get("/{prestataire_id}", response_model=schemas.PrestataireRead)
def get_prestataire(
    prestataire_id: int,
    db: Session = Depends(get_db),
):
    prestataire = db.query(models.Prestataire).filter(models.Prestataire.id == prestataire_id).first()
    if not prestataire:
        raise HTTPException(404, "Prestataire non trouvé")
    user = db.query(models.User).filter(models.User.id == prestataire.user_id).first()
    # Construction manuelle pour inclure l'avatar
    return {
        "id": prestataire.id,
        "business_name": prestataire.business_name,
        "description": prestataire.description,
        "city": prestataire.city,
        "verified": prestataire.verified,
        "category_id": prestataire.category_id,
        "proposed_category": prestataire.proposed_category,
        "created_at": prestataire.created_at,
        "whatsapp": prestataire.whatsapp,
        "business_image_url": prestataire.business_image_url,
        "map_url": prestataire.map_url,
        "avatar_url": user.avatar_url if user else None,
    }

