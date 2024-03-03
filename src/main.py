"""Entry point of the application, run with `uvircorn service:app [--reload]`"""

from fastapi import FastAPI

from app.database import db_models
from app.database.database import engine

from app.router import birds, images

# db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ornipedia API",
    summary="Endpoints for Ornipedia",
)

app.include_router(birds.router)
app.include_router(images.router)
