"""Species specific endpoints: list of species and of sub-species (for each species)"""

from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from src.dependencies import get_db

from src.models.responses import MAX_PER_PAGE, PaginatedResponse

from src.database.crud import get_species, get_sub_species


router = APIRouter(
    prefix="/species",
    tags=["species"],
)


@router.get("", response_model=PaginatedResponse[str])
def read_species(
    language: str = "fr",
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=25, ge=0, le=MAX_PER_PAGE),
    db: Session = Depends(get_db),
):
    return get_species(db, language=language, page=page, per_page=per_page)


@router.get("/{species}", response_model=PaginatedResponse[str])
def read_sub_species(
    species: str,
    language: str = "fr",
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=25, ge=0, le=MAX_PER_PAGE),
    db: Session = Depends(get_db),
):
    return get_sub_species(db, species, language=language, page=page, per_page=per_page)
