from os import path

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db

from src.models.responses import ErrorMessage

from src.database.crud import get_image


router = APIRouter(
    prefix="/species",
    tags=["species"],
)


# TODO: species spefic endpoints:
#           - get the list of species
#           - get the list of sub-species (for each species)
