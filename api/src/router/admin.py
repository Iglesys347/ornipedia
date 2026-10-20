"""Administration: adding birds and photos, deleting photos (password protected)."""

import logging
import os
import uuid
from dataclasses import asdict, dataclass

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from PIL import Image as PILImage, UnidentifiedImageError
from sqlalchemy.orm import Session

from src import commons, settings
from src.auth import require_admin
from src.dependencies import get_db
from src.database import db_models
from src.models.admin import (
    AuthorOut,
    BirdCreated,
    BirdIn,
    CommonsImport,
    CommonsSearchOut,
    LicenseOut,
)
from src.models.responses import ErrorMessage
from src.models.schemas import ImageWoPath
from src import thumbnails

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorMessage, "description": "Invalid password"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorMessage,
            "description": "Administration disabled",
        },
    },
)

# accepted image formats (Pillow name -> file extension)
# MPO ("multi picture" JPEG, made by some cameras) is a JPEG followed by other pictures:
# browsers show it as a JPEG (its first picture)
IMAGE_FORMATS = {"JPEG": "jpg", "MPO": "jpg", "PNG": "png", "WEBP": "webp"}


@router.get("/check")
def check_password():
    """Checks the password (used by the login form)."""
    return {"status": "ok"}


@router.get("/authors", response_model=list[AuthorOut])
def read_authors(db: Session = Depends(get_db)):
    return db.query(db_models.ImageAuthor).order_by(db_models.ImageAuthor.name).all()


@router.get("/licenses", response_model=list[LicenseOut])
def read_licenses(db: Session = Depends(get_db)):
    return db.query(db_models.ImageLicense).order_by(db_models.ImageLicense.short_name).all()


@router.post("/birds", response_model=BirdCreated, status_code=status.HTTP_201_CREATED)
def create_bird(bird: BirdIn, db: Session = Depends(get_db)):
    """Creates a bird with its translations (in a single transaction)."""
    db_bird = db_models.Bird(latin_name=bird.latin_name)
    db.add(db_bird)
    db.flush()
    for translation in bird.translations:
        db.add(db_models.Translation(bird_id=db_bird.id, **translation.model_dump()))
    db.commit()
    return db_bird


def _read_upload(file: UploadFile) -> bytes:
    """Reads the uploaded file, refusing files bigger than MAX_UPLOAD_SIZE."""
    content = file.file.read(settings.MAX_UPLOAD_SIZE + 1)
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"The photo must not exceed {settings.MAX_UPLOAD_SIZE // (1024 * 1024)} MB",
        )
    return content


def _image_extension(path: str) -> str:
    """Returns the extension of a valid image, raises a 422 error otherwise."""
    try:
        with PILImage.open(path) as img:
            img_format = img.format
            img.verify()
    except (OSError, UnidentifiedImageError, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The file is not a valid image",
        ) from err
    if img_format not in IMAGE_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The photo must be a JPEG, PNG or WebP image",
        )
    return IMAGE_FORMATS[img_format]


def _get_or_create_author(db: Session, name: str, link: str | None) -> db_models.ImageAuthor:
    author = (
        db.query(db_models.ImageAuthor)
        .filter(db_models.ImageAuthor.name == name, db_models.ImageAuthor.link == link)
        .first()
    )
    if author is None:
        author = db_models.ImageAuthor(name=name, link=link)
        db.add(author)
        db.flush()
    return author


def _get_or_create_license(
    db: Session, short_name: str, full_name: str, link: str
) -> db_models.ImageLicense:
    img_license = (
        db.query(db_models.ImageLicense)
        .filter(
            db_models.ImageLicense.short_name == short_name,
            db_models.ImageLicense.link == link,
        )
        .first()
    )
    if img_license is None:
        img_license = db_models.ImageLicense(short_name=short_name, full_name=full_name, link=link)
        db.add(img_license)
        db.flush()
    return img_license


@dataclass
class PhotoCredits:
    author_name: str
    author_link: str | None
    license_short_name: str
    license_full_name: str
    license_link: str
    original_url: str


def _save_photo(
    db: Session, bird_id: int, content: bytes, photo_credits: PhotoCredits
) -> db_models.Image:
    """Saves a photo in IMAGE_FOLDER under a random name and adds it to the bird.
    Nothing is kept if the photo is invalid or the database update fails."""
    os.makedirs(settings.IMAGE_FOLDER, exist_ok=True)
    tmp_path = os.path.join(settings.IMAGE_FOLDER, f".upload-{uuid.uuid4().hex}")
    with open(tmp_path, "wb") as tmp_file:
        tmp_file.write(content)
    image_path = None
    try:
        extension = _image_extension(tmp_path)
        image_path = os.path.join(settings.IMAGE_FOLDER, f"{uuid.uuid4().hex}.{extension}")
        os.replace(tmp_path, image_path)

        author = _get_or_create_author(
            db, photo_credits.author_name.strip(), (photo_credits.author_link or "").strip() or None
        )
        img_license = _get_or_create_license(
            db,
            photo_credits.license_short_name.strip(),
            photo_credits.license_full_name.strip(),
            photo_credits.license_link.strip(),
        )
        image = db_models.Image(
            bird_id=bird_id,
            author_id=author.id,
            license_id=img_license.id,
            image_path=image_path,
            original_url=photo_credits.original_url.strip(),
        )
        db.add(image)
        db.commit()
    except BaseException:
        db.rollback()
        for path in (tmp_path, image_path):
            if path and os.path.exists(path):
                os.remove(path)
        raise
    return image


@router.post(
    "/birds/{bird_id}/images",
    response_model=ImageWoPath,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessage, "description": "Bird not found"},
        status.HTTP_413_CONTENT_TOO_LARGE: {
            "model": ErrorMessage,
            "description": "Photo too big",
        },
    },
)
# the form fields are separate arguments (FastAPI form parameters)
def create_image(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    bird_id: int,
    file: UploadFile = File(description="JPEG, PNG or WebP photo"),
    author_name: str = Form(min_length=1, max_length=200),
    author_link: str | None = Form(default=None, max_length=500),
    license_short_name: str = Form(min_length=1, max_length=100),
    license_full_name: str = Form(min_length=1, max_length=200),
    license_link: str = Form(min_length=1, max_length=500),
    original_url: str = Form(default="", max_length=500),
    db: Session = Depends(get_db),
):
    """Adds a photo to a bird. The photo is saved in IMAGE_FOLDER under a random name."""
    if db.get(db_models.Bird, bird_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bird not found")

    content = _read_upload(file)
    image = _save_photo(
        db,
        bird_id,
        content,
        PhotoCredits(
            author_name=author_name,
            author_link=author_link,
            license_short_name=license_short_name,
            license_full_name=license_full_name,
            license_link=license_link,
            original_url=original_url,
        ),
    )
    return {"id": image.id, "bird_id": image.bird_id}


COMMONS_UNREACHABLE = "Wikimedia Commons cannot be reached, try again later"


def _commons_error(err: Exception) -> HTTPException:
    """502 error giving the cause (logged, and shown to the administrator)."""
    logger.warning("Wikimedia Commons error: %s", err)
    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY, detail=f"{COMMONS_UNREACHABLE} ({err})"
    )


@router.get(
    "/commons/search",
    response_model=CommonsSearchOut,
    responses={
        status.HTTP_502_BAD_GATEWAY: {"model": ErrorMessage, "description": "Commons unreachable"}
    },
)
def search_commons(
    q: str = Query(
        min_length=1, max_length=200, description="Name of the bird (the latin name works best)"
    ),
    limit: int = Query(default=10, ge=1, le=20),
    offset: int = Query(default=0, ge=0, le=1000),
    db: Session = Depends(get_db),
):
    """Photos of Wikimedia Commons matching the query, with their author and license."""
    try:
        photos, next_offset = commons.search(q.strip(), limit, offset)
    except commons.CommonsError as err:
        raise _commons_error(err) from err
    page_urls = [photo.page_url for photo in photos]
    added = (
        {
            url
            for (url,) in db.query(db_models.Image.original_url)
            .filter(db_models.Image.original_url.in_(page_urls))
            .all()
        }
        if page_urls
        else set()
    )
    return {
        "items": [{**asdict(photo), "already_added": photo.page_url in added} for photo in photos],
        "next_offset": next_offset,
    }


@router.post(
    "/birds/{bird_id}/commons",
    response_model=ImageWoPath,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessage,
            "description": "Bird or photo not found",
        },
        status.HTTP_409_CONFLICT: {"model": ErrorMessage, "description": "Photo already added"},
        status.HTTP_413_CONTENT_TOO_LARGE: {"model": ErrorMessage, "description": "Photo too big"},
        status.HTTP_502_BAD_GATEWAY: {"model": ErrorMessage, "description": "Commons unreachable"},
    },
)
def import_from_commons(bird_id: int, body: CommonsImport, db: Session = Depends(get_db)):
    """Adds a photo of Wikimedia Commons to a bird. The photo and its author and license
    are fetched from Commons by the API (only the title of the file is sent)."""
    if db.get(db_models.Bird, bird_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bird not found")
    try:
        photo = commons.get_photo(body.title)
    except commons.CommonsError as err:
        raise _commons_error(err) from err
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This file is not a usable photo on Wikimedia Commons",
        )
    if db.query(db_models.Image).filter(db_models.Image.original_url == photo.page_url).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This photo is already in Ornipedia"
        )
    try:
        content = commons.download(photo, settings.MAX_UPLOAD_SIZE)
    except commons.CommonsPhotoTooBig as err:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail="The photo is too big"
        ) from err
    except commons.CommonsError as err:
        raise _commons_error(err) from err

    image = _save_photo(
        db,
        bird_id,
        content,
        PhotoCredits(
            author_name=photo.author_name[:200],
            author_link=photo.author_link,
            license_short_name=photo.license_short_name[:100],
            license_full_name=photo.license_full_name[:200],
            license_link=photo.license_link,
            original_url=photo.page_url,
        ),
    )
    return {"id": image.id, "bird_id": image.bird_id}


def _is_managed_file(path: str) -> bool:
    """Only the files in IMAGE_FOLDER are deleted with their image."""
    folder = os.path.realpath(settings.IMAGE_FOLDER)
    return os.path.commonpath([folder, os.path.realpath(path)]) == folder


@router.delete(
    "/images/{img_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessage, "description": "Image not found"}
    },
)
def delete_image(img_id: int, db: Session = Depends(get_db)):
    image = db.get(db_models.Image, img_id)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    image_path = str(image.image_path)
    db.delete(image)
    db.commit()

    paths = [
        os.path.join(thumbnails.THUMBNAIL_FOLDER, f"{img_id}-{width}.jpg")
        for width in thumbnails.THUMBNAIL_WIDTHS
    ]
    if _is_managed_file(image_path):
        paths.append(image_path)
    for path in paths:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
