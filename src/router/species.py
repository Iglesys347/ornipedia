"""
TODO: species spefic endpoints:
          - get the list of species
          - get the list of sub-species (for each species)
"""

from fastapi import APIRouter


router = APIRouter(
    prefix="/species",
    tags=["species"],
)
