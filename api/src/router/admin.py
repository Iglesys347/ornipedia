"""Administration: adding birds and photos, deleting photos (password protected)."""

import os
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image as PILImage, UnidentifiedImageError
from sqlalchemy.orm import Session

from src import settings
from src.auth import require_admin
from src.dependencies import get_db
from src.database import db_models
from src.models.admin import AuthorOut, BirdCreated, BirdIn, LicenseOut
from src.models.responses import ErrorMessage
from src.models.schemas import ImageWoPath
from src import thumbnails

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
IMAGE_FORMATS = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}


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
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
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


@router.post(
    "/birds/{bird_id}/images",
    response_model=ImageWoPath,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessage, "description": "Bird not found"},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "model": ErrorMessage,
            "description": "Photo too big",
        },
    },
)
# the form fields are separate arguments (FastAPI form parameters)
def create_image(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
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
    os.makedirs(settings.IMAGE_FOLDER, exist_ok=True)
    tmp_path = os.path.join(settings.IMAGE_FOLDER, f".upload-{uuid.uuid4().hex}")
    with open(tmp_path, "wb") as tmp_file:
        tmp_file.write(content)
    image_path = None
    try:
        extension = _image_extension(tmp_path)
        image_path = os.path.join(settings.IMAGE_FOLDER, f"{uuid.uuid4().hex}.{extension}")
        os.replace(tmp_path, image_path)

        author = _get_or_create_author(db, author_name.strip(), (author_link or "").strip() or None)
        img_license = _get_or_create_license(
            db, license_short_name.strip(), license_full_name.strip(), license_link.strip()
        )
        image = db_models.Image(
            bird_id=bird_id,
            author_id=author.id,
            license_id=img_license.id,
            image_path=image_path,
            original_url=original_url.strip(),
        )
        db.add(image)
        db.commit()
    except BaseException:
        db.rollback()
        for path in (tmp_path, image_path):
            if path and os.path.exists(path):
                os.remove(path)
        raise
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
