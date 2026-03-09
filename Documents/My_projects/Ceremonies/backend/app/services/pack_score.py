import math
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models

WEIGHTS = {
    "category": 0.35,
    "interaction": 0.15,
    "quality": 0.25,
    "budget": 0.25,
}

def calculate_pack_score(pack: models.Pack, db: Session) -> int:
    pack_offers = pack.offers  # liste de PackOffer
    if not pack_offers:
        return 0

    offers = [po.offer for po in pack_offers]  # liste des offres
    total_price = sum(o.base_price or 0 for o in offers)
    categories = db.query(models.ServiceCategory).all()
    important_categories = [cat.name for cat in categories]

    prestataires_map = {}
    category_name_map = {}
    for offer in offers:
        prestataire = offer.prestataire
        prestataires_map[prestataire.id] = prestataire
        if prestataire.category_id:
            cat = db.get(models.ServiceCategory, prestataire.category_id)
            if cat:
                category_name_map[prestataire.category_id] = cat.name

    category_coverage = _calculate_category_coverage(
        offers, important_categories, category_name_map, prestataires_map
    )
    user_interaction = _calculate_user_interaction(offers)
    quality = _calculate_quality_signal(offers, prestataires_map, db)

    if pack.user_budget is None:
        budget_fit = 100
    else:
        budget_fit = _calculate_budget_fit(total_price, pack.user_budget)

    total = (
        category_coverage * WEIGHTS["category"] +
        user_interaction * WEIGHTS["interaction"] +
        quality * WEIGHTS["quality"] +
        budget_fit * WEIGHTS["budget"]
    )
    return round(total)

def _calculate_category_coverage(offers, important_categories, category_name_map, prestataires_map):
    if not important_categories:
        return 0
    covered = set()
    for offer in offers:
        prestataire = prestataires_map.get(offer.prestataire_id)
        if prestataire and prestataire.category_id:
            cat_name = category_name_map.get(prestataire.category_id)
            if cat_name and cat_name in important_categories:
                covered.add(cat_name)
    return (len(covered) / len(important_categories)) * 100

def _calculate_user_interaction(offers):
    count = len(offers)
    if count == 0:
        return 0
    base = min(count / 10, 1) * 100
    unique_prestataires = len({o.prestataire_id for o in offers})
    diversity = min(unique_prestataires / 5, 1) * 20
    return min(base + diversity, 100)

def _calculate_quality_signal(offers, prestataires_map, db):
    if not offers:
        return 0
    total_rating = 0
    rating_count = 0
    verified_count = 0

    for offer in offers:
        prestataire = prestataires_map.get(offer.prestataire_id)
        if not prestataire:
            continue
        avg_rating = db.query(func.avg(models.Review.rating)).filter(
            models.Review.prestataire_id == prestataire.id
        ).scalar() or 0.0
        total_rating += avg_rating
        rating_count += 1
        if prestataire.verified:
            verified_count += 1

    avg_rating_score = (total_rating / rating_count / 5 * 100) if rating_count else 0
    verified_ratio = (verified_count / len(offers) * 100) if offers else 0
    return avg_rating_score * 0.5 + verified_ratio * 0.5

def _calculate_budget_fit(total_price, budget):
    if budget <= 0:
        return 0
    if total_price <= budget:
        return 100
    excess = total_price - budget
    return 100 * math.exp(-excess / budget)