import aiofiles

from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session

from src.dependencies import get_db

from src.models.schemas import Bird, BirdWithImages
from src.models.responses import PaginatedResponse, ErrorMessage

from src.database.crud import (
    insert_bird,
    insert_translation,
    insert_image,
    insert_img_author,
    insert_img_license,
    get_img_license,
    get_img_author,
)

from src.settings import IMAGE_FOLDER

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.post("/bird")
async def create_bird(
    image: Annotated[UploadFile, File()],
    image_license_short_name: str,
    image_license_full_name: str,
    image_license_link: str,
    image_author_name: str,
    image_author_link: str,
    image_original_url: str,
    language_code: str,
    latin_name: str,
    name: str,
    species: str,
    sub_species: str | None = None,
    details: str | None = None,
    db: Session = Depends(get_db),
):
    # save the image on disk
    img_path = f"{IMAGE_FOLDER}/{image.filename}"
    async with aiofiles.open(img_path, "wb") as out_file:
        content = await image.read()  # async read
        await out_file.write(content)  # async write

    bird = insert_bird(db, latin_name=latin_name)
    translation = insert_translation(
        db,
        bird_id=bird.id,  # type: ignore
        language_code=language_code,
        name=name,
        species=species,
        sub_species=sub_species,
        details=details,
    )
    img_license = get_img_license(
        db, short_name=image_license_short_name, link=image_license_link
    )
    if img_license is None:
        img_license = insert_img_license(
            db,
            short_name=image_license_short_name,
            full_name=image_license_full_name,
            link=image_license_link,
        )
    img_author = get_img_author(db, name=image_author_name, link=image_author_link)
    if img_author is None:
        img_author = insert_img_author(
            db,
            name=image_author_name,
            link=image_author_link,
        )
    img = insert_image(
        db,
        bird_id=bird.id,  # type: ignore
        license_id=img_license.id,  # type: ignore
        author_id=img_author.id,  # type: ignore
        image_path=img_path,
        original_url=image_original_url,
    )

    return {"Result": "OK"}
