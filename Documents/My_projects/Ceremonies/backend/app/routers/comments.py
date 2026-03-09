from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.auth import get_current_user
from app import models, schemas
from app.crud import create_comment

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("/", response_model=List[schemas.CommentRead])
def get_comments_by_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    comments = db.query(models.Comment).filter(
        models.Comment.offer_id == offer_id,
        models.Comment.is_visible == True
    ).order_by(models.Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for c in comments:
        user = db.query(models.User).filter(models.User.id == c.user_id).first()
        result.append({
            "id": c.id,
            "content": c.content,
            "is_visible": c.is_visible,
            "created_at": c.created_at,
            "user_id": c.user_id,
            "offer_id": c.offer_id,
            "author_name": user.full_name if user else None,
            "author_avatar": user.avatar_url if user else None,
        })
    return result

@router.post("/", response_model=schemas.CommentRead)
def create_new_comment(
    data: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    offer = db.query(models.Offer).filter(models.Offer.id == data.offer_id).first()
    if not offer:
        raise HTTPException(404, "Offre non trouvée")
    
    comment = models.Comment(
        user_id=current_user.id,
        offer_id=data.offer_id,
        content=data.content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return {
        "id": comment.id,
        "content": comment.content,
        "is_visible": comment.is_visible,
        "created_at": comment.created_at,
        "user_id": comment.user_id,
        "offer_id": comment.offer_id,
        "author_name": current_user.full_name,
        "author_avatar": current_user.avatar_url,
    }

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Supprimer un commentaire (propriétaire ou admin)"""
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(404, "Commentaire non trouvé")
    
    if comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Vous n'êtes pas autorisé à supprimer ce commentaire")
    
    db.delete(comment)
    db.commit()
    return {"ok": True}