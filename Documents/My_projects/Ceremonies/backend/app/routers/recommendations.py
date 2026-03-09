import math
from typing import List, Dict
from itertools import product
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app import models, schemas

router = APIRouter(prefix="/pack-recommendations", tags=["Pack Recommendations"])

# Poids par défaut (α, β, γ, δ, ε)
BASE_WEIGHTS = {
    "diversity": 0.25,
    "quality": 0.25,
    "budget": 0.25,
    "temporal": 0.15,
    "popularity": 0.10,
}

def adjust_weights(priority: schemas.Priority) -> dict:
    """Ajuste les poids en fonction de la priorité choisie."""
    weights = BASE_WEIGHTS.copy()
    if priority == "quality":
        weights["quality"] *= 2
    elif priority == "price":
        weights["budget"] *= 2
    elif priority == "verified":
        weights["quality"] *= 1.5  # bonus vérifié déjà dans quality
    elif priority == "availability":
        weights["temporal"] *= 2
    # Renormalisation
    total = sum(weights.values())
    return {k: v / total for k, v in weights.items()}

def calculate_individual_score(prestataire, avg_rating):
    """Score individuel d'une offre (rating + vérifié) normalisé entre 0 et 1."""
    rating_score = (avg_rating / 5.0) if avg_rating else 0.0
    verified_score = 1.0 if prestataire.verified else 0.0
    # Pondération rating 70%, vérifié 30%
    return 0.7 * rating_score + 0.3 * verified_score

def calculate_diversity_score(offers_in_pack: List[dict]) -> float:
    """Score de diversité basé sur le nombre de prestataires distincts."""
    prestataire_ids = {item["prestataire"].id for item in offers_in_pack}
    unique_ratio = len(prestataire_ids) / len(offers_in_pack)
    return unique_ratio

def calculate_budget_score(total_price: float, budget: float) -> float:
    """Score budgétaire avec pénalité exponentielle."""
    if total_price <= budget:
        return 1.0
    excess = total_price - budget
    return math.exp(-excess / budget)

def calculate_popularity_score(offers_in_pack: List[dict], max_reservations: int) -> float:
    """Score de popularité basé sur le nombre de réservations (normalisé)."""
    if max_reservations == 0:
        return 0.0
    total_reservations = sum(item.get("reservation_count", 0) for item in offers_in_pack)
    max_possible = len(offers_in_pack) * max_reservations
    return total_reservations / max_possible if max_possible > 0 else 0.0

@router.post("/", response_model=List[schemas.PackRecommendation])
def get_pack_recommendations(
    request: schemas.RecommendationRequest,
    db: Session = Depends(get_db)
):
    # 1. Sous-requêtes pour les agrégats
    avg_rating_subq = db.query(
        models.Review.prestataire_id,
        func.avg(models.Review.rating).label('avg_rating')
    ).group_by(models.Review.prestataire_id).subquery()

    reservation_count_subq = db.query(
        models.Reservation.offer_id,
        func.count(models.Reservation.id).label('reservation_count')
    ).group_by(models.Reservation.offer_id).subquery()

    # 2. Requête principale
    offers_query = db.query(
        models.Offer,
        models.Prestataire,
        models.ServiceCategory.name.label('category_name'),
        models.User.avatar_url,
        avg_rating_subq.c.avg_rating,
        reservation_count_subq.c.reservation_count
    ).join(
        models.Prestataire,
        models.Offer.prestataire_id == models.Prestataire.id
    ).join(
        models.ServiceCategory,
        models.Prestataire.category_id == models.ServiceCategory.id
    ).join(
        models.User,
        models.User.id == models.Prestataire.user_id
    ).outerjoin(
        avg_rating_subq,
        avg_rating_subq.c.prestataire_id == models.Prestataire.id
    ).outerjoin(
        reservation_count_subq,
        reservation_count_subq.c.offer_id == models.Offer.id
    ).filter(
        models.Offer.ceremony_type_id == request.ceremony_type_id,
        models.Offer.is_active == True,
        func.lower(models.Prestataire.city) == func.lower(request.city)
    )

    # 3. Organiser les offres par catégorie
    offers_by_category: Dict[int, List[dict]] = {}
    max_reservations = 0
    for offer, prestataire, cat_name, avatar, avg_rating, res_count in offers_query:
        cat_id = prestataire.category_id
        if cat_id is None:
            continue
        if cat_id not in offers_by_category:
            offers_by_category[cat_id] = []
        indiv_score = calculate_individual_score(prestataire, avg_rating)
        res_count = res_count or 0
        if res_count > max_reservations:
            max_reservations = res_count
        offers_by_category[cat_id].append({
            "offer": offer,
            "prestataire": prestataire,
            "category_name": cat_name,
            "avatar_url": avatar,
            "avg_rating": avg_rating,
            "reservation_count": res_count,
            "score": indiv_score
        })

    if not offers_by_category:
        return []

    # 4. Garder les meilleures offres par catégorie (max 5)
    for cat_id in offers_by_category:
        offers_by_category[cat_id].sort(key=lambda x: x["score"], reverse=True)
        offers_by_category[cat_id] = offers_by_category[cat_id][:5]

    # 5. Générer toutes les combinaisons
    category_offer_lists = list(offers_by_category.values())
    all_combinations = list(product(*category_offer_lists))

    # 6. Ajuster les poids
    weights = adjust_weights(request.priority)

    # 7. Calculer les scores et construire les packs
    packs = []
    for comb in all_combinations:
        total_price = sum(float(item["offer"].base_price or 0) for item in comb)
        diversity_score = calculate_diversity_score(comb)
        quality_score = sum(item["score"] for item in comb) / len(comb)
        budget_score = calculate_budget_score(total_price, request.total_budget)
        temporal_score = 1.0  # par défaut (à enrichir)
        popularity_score = calculate_popularity_score(comb, max_reservations)

        final_score = (weights["diversity"] * diversity_score +
                       weights["quality"] * quality_score +
                       weights["budget"] * budget_score +
                       weights["temporal"] * temporal_score +
                       weights["popularity"] * popularity_score)

        offers_detail = []
        for item in comb:
            prestataire = item["prestataire"]
            offer = item["offer"]
            prestataire_read = schemas.PrestataireRead(
                id=prestataire.id,
                business_name=prestataire.business_name,
                description=prestataire.description,
                city=prestataire.city,
                verified=prestataire.verified,
                category_id=prestataire.category_id,
                proposed_category=prestataire.proposed_category,
                created_at=prestataire.created_at,
                whatsapp=prestataire.whatsapp,
                business_image_url=prestataire.business_image_url,
                map_url=prestataire.map_url,
                avatar_url=item["avatar_url"]
            )
            offer_read = schemas.OfferRead(
                id=offer.id,
                ceremony_type_id=offer.ceremony_type_id,
                title=offer.title,
                description=offer.description,
                prestataire_id=offer.prestataire_id,
                base_price=float(offer.base_price) if offer.base_price else None,
                is_active=offer.is_active,
                created_at=offer.created_at,
                likes_count=0
            )
            offers_detail.append(schemas.PackOfferDetail(
                offer=offer_read,
                prestataire=prestataire_read,
                category_name=item["category_name"],
                individual_score=item["score"]
            ))

        packs.append({
            "offers": offers_detail,
            "total_price": total_price,
            "average_score": quality_score,
            "budget_score": budget_score,
            "final_score": final_score
        })

    # 8. Trier et limiter
    packs.sort(key=lambda x: x["final_score"], reverse=True)
    return packs[:20]