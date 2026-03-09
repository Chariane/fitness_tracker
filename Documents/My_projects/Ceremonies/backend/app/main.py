from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    auth,
    users,
    ceremonies,
    prestataires,
    offers,
    messages,
    verification_documents,
    reservations,
    ceremony_types,
    admin,
    service_categories,
    reviews,
    offer_media, 
    comments,
    favorites,
    recommendations,
    packs,
    prestataire_favorites,
)

app = FastAPI()

# Monter le répertoire des uploads pour servir les fichiers
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs
app.include_router(auth.router)
app.include_router(ceremonies.router)
app.include_router(prestataires.router)
app.include_router(reservations.router)
app.include_router(users.router)
app.include_router(verification_documents.router)
app.include_router(ceremony_types.router)
app.include_router(admin.router)
app.include_router(service_categories.router)
app.include_router(offers.router)
app.include_router(messages.router)
app.include_router(reviews.router)
app.include_router(offer_media.router)
app.include_router(comments.router)      
app.include_router(favorites.router)     
app.include_router(recommendations.router)
app.include_router(packs.router)
app.include_router(prestataire_favorites.router)