from os import path

from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.dependencies import get_db

from src.models.responses import ErrorMessage, PaginatedResponse
from src.models.schemas import Bird, ImageWoPath, ImageInfo

from src.database.crud import (
    get_image,
    get_images_ids,
    get_image_bird,
    get_random_image,
    get_image_info,
)


router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.get("", response_model=PaginatedResponse[int])
def read_images(
    language: str = "fr",
    search: str | None = None,
    species: str | None = None,
    sub_species: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=25, ge=0),
    db: Session = Depends(get_db),
):
    images = get_images_ids(
        db,
        language=language,
        search=search,
        species=species,
        sub_species=sub_species,
        page=page,
        per_page=per_page,
    )
    images.items = [img_id[0] for img_id in images.items]
    return images


@router.get(
    "/{img_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Image not found",
        }
    },
)
def read_image(
    img_id: int,
    db: Session = Depends(get_db),
):
    image = get_image(db, img_id=img_id)
    if not image or not path.isfile(str(image.image_path)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return FileResponse(str(image.image_path))


@router.get(
    "/{img_id}/bird",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Image not found",
        }
    },
    response_model=Bird,
)
def read_image_bird(img_id: int, language: str = "fr", db: Session = Depends(get_db)):
    bird = get_image_bird(db, img_id=img_id, language=language)
    if not bird:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return bird


@router.get(
    "/{img_id}/info",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Image not found",
        }
    },
    response_model=ImageInfo,
)
def read_image_info(img_id: int, language: str = "fr", db: Session = Depends(get_db)):
    info = get_image_info(db, img_id=img_id, language=language)
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return info


@router.get(
    "/image/random",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Image not found",
        }
    },
    response_model=ImageWoPath,
)
def read_random_image(
    species: str | None = None,
    sub_species: str | None = None,
    db: Session = Depends(get_db),
):
    image = get_random_image(db, species=species, sub_species=sub_species)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return image
