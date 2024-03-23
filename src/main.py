"""Entry point of the application, run with `uvircorn service:app [--reload]`"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import db_models
from src.database.database import engine

from src.router import birds, images

from src.settings import ALLOWED_ORIGINS

# TODO: move this line somewhere else so it is not executed each time
# db_models.Base.metadata.create_all(bind=engine)


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
