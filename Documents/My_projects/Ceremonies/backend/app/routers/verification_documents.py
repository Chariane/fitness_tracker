import os
import shutil
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.crud import create_verification_document
from app.db.session import get_db
from app.core.auth import get_current_user
from app.schemas import VerificationDocumentCreate, VerificationDocumentRead
from app import models

router = APIRouter(prefix="/verification_documents", tags=["VerificationDocuments"])

# Dossier où stocker les fichiers uploadés
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/{prestataire_id}", response_model=VerificationDocumentRead)
def upload_document(
    prestataire_id: int,
    file: UploadFile = File(...),
    doc_type: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Vérifier que le prestataire appartient bien à l'utilisateur
    prestataire = db.query(models.Prestataire).filter(
        models.Prestataire.id == prestataire_id,
        models.Prestataire.user_id == current_user.id
    ).first()
    if not prestataire:
        raise HTTPException(403, "Vous n'êtes pas autorisé à uploader pour ce prestataire")

    # Générer un nom de fichier unique
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{prestataire_id}_{int(datetime.utcnow().timestamp())}{file_extension}"
    file_path = UPLOAD_DIR / filename

    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # URL relative pour accéder au fichier
    document_url = f"/uploads/{filename}"

    doc_data = VerificationDocumentCreate(
        document_url=document_url,
        document_type=doc_type
    )
    verification_doc = create_verification_document(db, prestataire_id, doc_data)
    return verification_doc