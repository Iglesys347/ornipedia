"""Entry point of the application, run with `uvicorn src.main:app [--reload]`"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.router import birds, images, species

# from src.router import admin

from src.settings import ALLOWED_ORIGINS

# the database schema is managed with Alembic (see README.md)

app = FastAPI(
    title="Ornipedia API",
    summary="Endpoints for Ornipedia",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(birds.router)
app.include_router(images.router)
app.include_router(species.router)
# app.include_router(admin.router)
