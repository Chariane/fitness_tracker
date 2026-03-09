from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Date,
    DateTime,
    Boolean,
    Numeric,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base

# =========================
# USERS
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String(150))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_client = Column(Boolean, default=True)
    is_prestataire = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    avatar_url = Column(String(255), nullable=True)

    ceremonies = relationship("Ceremony", back_populates="user")
    prestataire_profile = relationship("Prestataire", back_populates="user", uselist=False)
    sent_messages = relationship("Message", back_populates="sender", foreign_keys='Message.sender_id')
    received_messages = relationship("Message", back_populates="receiver", foreign_keys='Message.receiver_id')
    packs = relationship("Pack", back_populates="user")


# =========================
# CEREMONY TYPES
# =========================
class CeremonyType(Base):
    __tablename__ = "ceremony_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    ceremonies = relationship("Ceremony", back_populates="ceremony_type")
    offers = relationship("Offer", back_populates="ceremony_type")


# =========================
# CEREMONIES
# =========================
class Ceremony(Base):
    __tablename__ = "ceremonies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ceremony_type_id = Column(Integer, ForeignKey("ceremony_types.id"))
    title = Column(String(200))
    event_date = Column(Date)
    location = Column(Text)
    budget = Column(Numeric(12, 2))
    guest_count = Column(Integer)
    status = Column(String(30), default="planning")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ceremonies")
    ceremony_type = relationship("CeremonyType", back_populates="ceremonies")
    reservations = relationship("Reservation", back_populates="ceremony")
    packs = relationship("Pack", back_populates="event")

# =========================
# SERVICE CATEGORIES
# =========================
class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

# =========================
# PRESTATAIRES
# =========================
class Prestataire(Base):
    __tablename__ = "prestataires"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    business_name = Column(String(150))
    category_id = Column(Integer, ForeignKey("service_categories.id"), nullable=True)
    description = Column(Text)
    city = Column(String(100))
    whatsapp = Column(String(20), nullable=True)                     # ← ajouté
    business_image_url = Column(String(255), nullable=True)         # ← ajouté
    map_url = Column(Text, nullable=True)                            # ← ajouté
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime)
    available_dates = Column(Text)
    proposed_category = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="prestataire_profile")
    category = relationship("ServiceCategory", foreign_keys=[category_id])
    offers = relationship("Offer", back_populates="prestataire")
    verification_documents = relationship("VerificationDocument", back_populates="prestataire")
    reservations = relationship("Reservation", back_populates="prestataire")

# =========================
# OFFERS
# =========================
class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    prestataire_id = Column(Integer, ForeignKey("prestataires.id"))
    ceremony_type_id = Column(Integer, ForeignKey("ceremony_types.id"), nullable=False)
    title = Column(String(200))
    description = Column(Text)
    base_price = Column(Numeric(12, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    prestataire = relationship("Prestataire", back_populates="offers")
    ceremony_type = relationship("CeremonyType", back_populates="offers")
    media = relationship("OfferMedia", back_populates="offer")
    reservations = relationship("Reservation", back_populates="offer")
    comments = relationship("Comment", back_populates="offer")
    packs = relationship("PackOffer", back_populates="offer")

# =========================
# OFFER MEDIA
# =========================
class OfferMedia(Base):
    __tablename__ = "offer_media"

    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    media_url = Column(Text, nullable=False)
    media_type = Column(String(30))
    created_at = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="media")

# =========================
# RESERVATIONS
# =========================
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    ceremony_id = Column(Integer, ForeignKey("ceremonies.id"))
    offer_id = Column(Integer, ForeignKey("offers.id"))
    client_id = Column(Integer, ForeignKey("users.id"))
    prestataire_id = Column(Integer, ForeignKey("prestataires.id"))
    proposed_price = Column(Numeric(12, 2))
    status = Column(String(30), default="pending")
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("User")
    prestataire = relationship("Prestataire", back_populates="reservations")
    ceremony = relationship("Ceremony", back_populates="reservations")
    offer = relationship("Offer", back_populates="reservations")
    payment = relationship("Payment", back_populates="reservation", uselist=False)

# =========================
# PAYMENTS
# =========================
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    amount = Column(Numeric(12, 2))
    status = Column(String(30))
    provider = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    reservation = relationship("Reservation", back_populates="payment")

# =========================
# COMMENTS
# =========================
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    offer = relationship("Offer", back_populates="comments")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    offer = relationship("Offer")

# =========================
# REVIEWS
# =========================
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    client_id = Column(Integer, ForeignKey("users.id"))
    prestataire_id = Column(Integer, ForeignKey("prestataires.id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_check"),
    )

# =========================
# MESSAGES / CHAT
# =========================
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_messages", foreign_keys=[receiver_id])
    conversation = relationship("Conversation", back_populates="messages")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    prestataire_id = Column(Integer, ForeignKey("users.id"))
    ceremony_id = Column(Integer, ForeignKey("ceremonies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

# =========================
# VERIFICATION DOCUMENTS
# =========================
class VerificationDocument(Base):
    __tablename__ = "verification_documents"

    id = Column(Integer, primary_key=True)
    prestataire_id = Column(Integer, ForeignKey("prestataires.id"))
    document_url = Column(Text, nullable=False)
    document_type = Column(String(50))
    status = Column(String(30), default="pending")
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    reviewed_at = Column(DateTime)

    prestataire = relationship("Prestataire", back_populates="verification_documents")


class Pack(Base):
    __tablename__ = "packs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("ceremonies.id"), nullable=True)
    name = Column(String(200), nullable=False)
    total_price = Column(Numeric(12, 2), default=0)
    completion_score = Column(Integer, default=0)  # sur 100
    created_at = Column(DateTime, default=datetime.utcnow)
    user_budget = Column(Numeric(12,2), nullable=True)

    # Relations
    user = relationship("User", back_populates="packs")
    event = relationship("Ceremony", back_populates="packs")
    offers = relationship("PackOffer", back_populates="pack", cascade="all, delete-orphan")


class PackOffer(Base):
    __tablename__ = "pack_offers"

    id = Column(Integer, primary_key=True)
    pack_id = Column(Integer, ForeignKey("packs.id"), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    pack = relationship("Pack", back_populates="offers")
    offer = relationship("Offer", back_populates="packs")

class PrestataireFavorite(Base):
    __tablename__ = "prestataire_favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prestataire_id = Column(Integer, ForeignKey("prestataires.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    prestataire = relationship("Prestataire")