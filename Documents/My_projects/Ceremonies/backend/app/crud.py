from sqlalchemy.orm import Session
from app import models
from app.core.security import hash_password
from app.schemas import MessageCreate, ConversationCreate, PrestataireRequest

# =================================================
# USER
# =================================================
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, email: str, password: str, full_name=None):
    user = models.User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# =================================================
# TYPE CEREMONY
# =================================================
def get_ceremony_types(db: Session):
    return db.query(models.CeremonyType).all()

def get_ceremony_type(db: Session, type_id: int):
    return db.query(models.CeremonyType).filter(models.CeremonyType.id == type_id).first()

def create_ceremony_type(db: Session, data):
    db_type = models.CeremonyType(**data.dict())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

def update_ceremony_type(db: Session, type_id: int, data):
    db_type = get_ceremony_type(db, type_id)
    if not db_type:
        return None
    for key, value in data.dict().items():
        setattr(db_type, key, value)
    db.commit()
    db.refresh(db_type)
    return db_type

def delete_ceremony_type(db: Session, type_id: int):
    db_type = get_ceremony_type(db, type_id)
    if not db_type:
        return False
    db.delete(db_type)
    db.commit()
    return True

# =================================================
# CEREMONY
# =================================================
def create_ceremony(db: Session, user_id: int, ceremony_data):
    ceremony = models.Ceremony(
        user_id=user_id,
        **ceremony_data.dict()
    )
    db.add(ceremony)
    db.commit()
    db.refresh(ceremony)
    return ceremony

def get_user_ceremonies(db: Session, user_id: int):
    return db.query(models.Ceremony).filter(models.Ceremony.user_id == user_id).all()

# =================================================
# PRESTATAIRE
# =================================================
def create_prestataire(db: Session, user_id: int, data: PrestataireRequest):
    business_name = data.business_name
    category_id = None
    proposed_category = None

    if data.category_id:
        category = db.query(models.ServiceCategory).filter(models.ServiceCategory.id == data.category_id).first()
        if not category:
            raise Exception("Catégorie invalide")
        category_id = category.id
    elif data.new_category_name:
        proposed_category = data.new_category_name

    prestataire = models.Prestataire(
        user_id=user_id,
        business_name=business_name,
        category_id=category_id,
        description=data.description,
        city=data.city,
        whatsapp=data.whatsapp,
        map_url=data.map_url,
        proposed_category=proposed_category,
    )
    db.add(prestataire)
    db.commit()
    db.refresh(prestataire)
    return prestataire

# =================================================
# OFFER
# =================================================
def create_offer(db: Session, prestataire_id: int, data):
    offer = models.Offer(
        prestataire_id=prestataire_id,
        **data.model_dump()
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer

def get_active_offers(db: Session):
    return db.query(models.Offer).filter(models.Offer.is_active == True).all()

# =================================================
# RESERVATION
# =================================================
def create_reservation(db: Session, client_id: int, prestataire_id: int, data):
    offer = db.query(models.Offer).filter(models.Offer.id == data.offer_id).first()
    reservation = models.Reservation(
        client_id=client_id,
        prestataire_id=offer.prestataire_id,
        **data.model_dump()
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def update_reservation_status(db: Session, reservation_id: int, status: str):
    reservation = db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id
    ).first()
    if reservation:
        reservation.status = status
        db.commit()
        db.refresh(reservation)
    return reservation

# =================================================
# COMMENT
# =================================================
def create_comment(db: Session, user_id: int, data):
    comment = models.Comment(
        user_id=user_id,
        **data.model_dump()
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

# =================================================
# REVIEW
# =================================================
def create_review(db: Session, client_id: int, prestataire_id: int, data):
    review = models.Review(
        client_id=client_id,
        prestataire_id=prestataire_id,
        **data.model_dump()
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

# =================================================
# PAYMENT
# =================================================
def create_payment(db: Session, data):
    payment = models.Payment(**data.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

# =================================================
# CONVERSATIONS
# =================================================
def create_conversation(db: Session, data: ConversationCreate):
    from app import models
    conv = models.Conversation(
        client_id=data.client_id,
        prestataire_id=data.prestataire_id,
        ceremony_id=data.ceremony_id
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_conversation(db: Session, conv_id: int):
    from app import models
    return db.query(models.Conversation).filter(models.Conversation.id == conv_id).first()

def get_user_conversations(db: Session, user_id: int):
    from app import models
    return db.query(models.Conversation).filter(
        (models.Conversation.client_id == user_id) |
        (models.Conversation.prestataire_id == user_id)
    ).all()

# =================================================
# MESSAGES
# =================================================
def send_message(db: Session, sender_id: int, data: MessageCreate):
    from app import models
    if data.conversation_id:
        conversation = db.query(models.Conversation).filter(models.Conversation.id == data.conversation_id).first()
        if not conversation:
            raise Exception("Conversation non trouvée")
    else:
        conversation = models.Conversation(
            client_id=sender_id,
            prestataire_id=data.receiver_id
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    message = models.Message(
        sender_id=sender_id,
        receiver_id=data.receiver_id,
        content=data.content,
        conversation_id=conversation.id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

# =================================================
# VERIFICATION DOCUMENT
# =================================================
def create_verification_document(db: Session, prestataire_id: int, data):
    from app import models
    doc = models.VerificationDocument(
        prestataire_id=prestataire_id,
        **data.model_dump()
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

# =================================================
# SERVICE CATEGORIES
# =================================================
def get_service_categories(db: Session):
    return db.query(models.ServiceCategory).all()

def get_service_category(db: Session, category_id: int):
    return db.query(models.ServiceCategory).filter(models.ServiceCategory.id == category_id).first()

def create_service_category(db: Session, data):
    db_cat = models.ServiceCategory(**data.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_service_category(db: Session, category_id: int, data):
    db_cat = get_service_category(db, category_id)
    if not db_cat:
        return None
    for key, value in data.model_dump().items():
        setattr(db_cat, key, value)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def delete_service_category(db: Session, category_id: int):
    db_cat = get_service_category(db, category_id)
    if not db_cat:
        return False
    db.delete(db_cat)
    db.commit()
    return True

# =================================================
# SUGGESTION (à adapter plus tard)
# =================================================
def get_intelligent_suggestions(db: Session, ceremony_id: int):
    return []

def save_message(db: Session, sender_id: int, receiver_id: int, content: str, conversation_id: int):
    message = models.Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        conversation_id=conversation_id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message