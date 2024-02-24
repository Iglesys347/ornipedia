from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db

from models.schemas import Bird, BirdWithImages
from models.responses import PaginatedResponse, ErrorMessage

from database.crud import get_bird, get_birds, get_bird_with_images

router = APIRouter(
    prefix="/birds",
    tags=["birds"],
)


@router.get("/", response_model=PaginatedResponse[Bird])
def read_birds(
    language: str = "fr",
    species: str | None = None,
    sub_species: str | None = None,
    page: int = 1,
    per_page: int = 25,
    db: Session = Depends(get_db),
):
    return get_birds(
        db,
        language=language,
        species=species,
        sub_species=sub_species,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{bird_id}",
    response_model=Bird,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Bird not found",
        }
    },
)
def read_bird(
    bird_id: int,
    language: str = "fr",
    db: Session = Depends(get_db),
):
    bird = get_bird(db, bird_id=bird_id, language=language)
    if bird is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bird not found",
        )
    return bird


@router.get(
    "/{bird_id}/images",
    response_model=BirdWithImages,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Bird not found",
        }
    },
)
def read_bird_images(
    bird_id: int,
    language: str = "fr",
    db: Session = Depends(get_db),
):
    bird = get_bird_with_images(db, bird_id=bird_id, language=language)
    if bird is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bird not found",
        )
    return bird
