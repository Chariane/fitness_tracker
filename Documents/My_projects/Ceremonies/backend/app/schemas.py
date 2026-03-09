from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

# =========================
# AUTH
# =========================
class LoginInput(BaseModel):
    email: EmailStr
    password: str

class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"

# =========================
# USER
# =========================
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    is_client: bool
    is_prestataire: bool
    is_admin: bool
    created_at: datetime
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

# =========================
# CEREMONY TYPE
# =========================
class CeremonyTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CeremonyTypeRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True

# =========================
# CEREMONY
# =========================
class CeremonyCreate(BaseModel):
    ceremony_type_id: int
    title: str
    event_date: date
    location: Optional[str] = None
    budget: Optional[float] = None
    guest_count: Optional[int] = None

class CeremonyRead(BaseModel):
    id: int
    title: str
    event_date: date
    location: Optional[str]
    budget: Optional[float]
    guest_count: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# =========================
# SERVICE CATEGORY
# =========================
class ServiceCategoryCreate(BaseModel):
    name: str

class ServiceCategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# =========================
# PRESTATAIRE
# =========================
class PrestataireRequest(BaseModel):
    business_name: str
    category_id: Optional[int] = None
    new_category_name: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    whatsapp: Optional[str] = None
    map_url: Optional[str] = None

class PrestataireRead(BaseModel):
    id: int
    business_name: str
    description: Optional[str]
    city: Optional[str]
    verified: bool
    category_id: Optional[int]
    proposed_category: Optional[str]
    created_at: datetime
    whatsapp: Optional[str]
    business_image_url: Optional[str]
    map_url: Optional[str]
    avatar_url: Optional[str]  # ← ajouté

    class Config:
        from_attributes = True

class PrestataireSearchRead(BaseModel):
    id: int
    business_name: str
    description: Optional[str]
    city: Optional[str]
    verified: bool
    whatsapp: Optional[str]
    business_image_url: Optional[str]
    map_url: Optional[str]
    avatar_url: Optional[str]
    category_id: Optional[int]
    # Statistiques
    total_offers: int
    min_price: Optional[float]
    max_price: Optional[float]
    avg_rating: Optional[float]
    total_reviews: int

    class Config:
        from_attributes = True

class PrestataireUpdate(BaseModel):
    business_name: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    whatsapp: Optional[str] = None
    map_url: Optional[str] = None

# =========================
# OFFER
# =========================
class OfferCreate(BaseModel):
    ceremony_type_id: int
    title: str
    description: Optional[str] = None
    base_price: Optional[float] = None

class OfferRead(BaseModel):
    id: int
    ceremony_type_id: int
    title: str
    description: Optional[str]
    prestataire_id: int
    base_price: Optional[float]
    is_active: bool
    likes_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

# =========================
# OFFER MEDIA
# =========================
class OfferMediaRead(BaseModel):
    id: int
    media_url: str
    media_type: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# =========================
# RESERVATION
# =========================
class ReservationCreate(BaseModel):
    ceremony_id: int
    offer_id: int
    proposed_price: Optional[float] = None
    message: Optional[str] = None

class ReservationRead(BaseModel):
    id: int
    proposed_price: Optional[float]
    status: str
    message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# =========================
# PAYMENT
# =========================
class PaymentCreate(BaseModel):
    reservation_id: int
    amount: float
    provider: str

class PaymentRead(BaseModel):
    id: int
    amount: float
    status: Optional[str]
    provider: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# =========================
# COMMENT
# =========================
class CommentCreate(BaseModel):
    offer_id: int
    content: str

class CommentRead(BaseModel):
    id: int
    content: str
    is_visible: bool
    created_at: datetime
    author_name: Optional[str] = None
    author_avatar: Optional[str] = None

    class Config:
        from_attributes = True

# =========================
# REVIEW
# =========================
class ReviewCreate(BaseModel):
    reservation_id: int
    rating: int
    comment: Optional[str] = None

class ReviewRead(BaseModel):
    id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# =========================
# MESSAGE / CONVERSATION
# =========================
class MessageCreate(BaseModel):
    receiver_id: int
    content: str
    conversation_id: Optional[int] = None

class MessageRead(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    conversation_id: Optional[int]
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    client_id: int
    prestataire_id: int
    ceremony_id: Optional[int] = None

class ConversationRead(BaseModel):
    id: int
    client_id: int
    prestataire_id: int
    ceremony_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageRead] = []

    class Config:
        from_attributes = True

# =========================
# VERIFICATION DOCUMENT
# =========================
class VerificationDocumentCreate(BaseModel):
    document_url: str
    document_type: Optional[str] = None

class VerificationDocumentRead(BaseModel):
    id: int
    document_url: str
    document_type: Optional[str]
    status: str
    reviewed_at: Optional[datetime]

    class Config:
        from_attributes = True

class Priority(str, Enum):
    quality = "quality"
    price = "price"
    verified = "verified"
    availability = "availability"

class RecommendationRequest(BaseModel):
    ceremony_type_id: int
    total_budget: float
    city: str
    event_date: date
    guest_count: Optional[int] = None
    priority: Priority = Priority.quality  # valeur par défaut

class RecommendedPrestataire(BaseModel):
    prestataire: PrestataireRead
    score: float
    avg_price: Optional[float]
    avg_rating: Optional[float]

class PackOfferDetail(BaseModel):
    offer: OfferRead
    prestataire: PrestataireRead
    category_name: Optional[str]
    individual_score: float

class PackRecommendation(BaseModel):
    offers: List[PackOfferDetail]
    total_price: float
    average_score: float
    budget_score: float
    final_score: float

class PackBase(BaseModel):
    name: str
    event_id: Optional[int] = None
    user_budget: Optional[float] = None

class PackCreate(PackBase):
    offer_ids: List[int] = []  # pour créer le pack avec des offres initiales

class PackUpdate(BaseModel):
    name: Optional[str] = None
    offer_ids: Optional[List[int]] = None  # remplacement total des offres
    completion_score: Optional[int] = None
    total_price: Optional[float] = None

class PackRead(BaseModel):
    id: int
    user_id: int
    event_id: Optional[int]
    name: str
    total_price: float
    user_budget: Optional[float]
    completion_score: int
    created_at: datetime
    offers: List["PackOfferRead"] = []

    class Config:
        from_attributes = True

class PackOfferBase(BaseModel):
    pack_id: int
    offer_id: int

class PackOfferCreate(PackOfferBase):
    pass

class PackOfferRead(PackOfferBase):
    id: int
    added_at: datetime
    offer: "OfferRead"  # pour inclure les détails de l'offre

    class Config:
        from_attributes = True

# Pour éviter les imports circulaires
PackRead.model_rebuild()
PackOfferRead.model_rebuild()

class PrestataireFavoriteBase(BaseModel):
    prestataire_id: int

class PrestataireFavoriteCreate(PrestataireFavoriteBase):
    pass

class PrestataireFavoriteRead(PrestataireFavoriteBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True