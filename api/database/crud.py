from sqlalchemy.orm import Session

from models.responses import PaginatedResponse

from database import db_models
from models.schemas import Bird


def paginate(query, page: int = 1, per_page: int = 10):
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(page=page, per_page=per_page, total=total, items=items)


def get_bird(db: Session, bird_id: int, language: str = "fr") -> Bird | None:
    bird = (
        db.query(db_models.Bird)
        .join(db_models.Translation)
        .filter(db_models.Bird.id == bird_id)
        .filter(db_models.Translation.language_code == language)
        .first()
    )
    return bird


def get_image_path(db: Session, image_id: int):
    return (
        db.query(db_models.Image.image_path)
        .filter(db_models.Image.id == image_id)
        .first()
    )


def get_birds(
    db: Session,
    language: str = "fr",
    species: str | None = None,
    sub_species: str | None = None,
    page: int = 1,
    per_page: int = 25,
) -> PaginatedResponse[Bird]:
    query = (
        db.query(db_models.Bird)
        .join(db_models.Translation)
        .filter(db_models.Translation.language_code == language)
    )
    if species:
        query = query.filter(db_models.Translation.species == species)
    if sub_species:
        query = query.filter(db_models.Translation.sub_species == sub_species)
    return paginate(query, page, per_page)


def get_bird_with_images(db: Session, bird_id: int, language: str = "fr"):
    return (
        db.query(db_models.Bird)
        .join(db_models.Translation)
        .join(db_models.Image)
        .filter(db_models.Bird.id == bird_id)
        .filter(db_models.Translation.language_code == language)
        .first()
    )


def get_image(db: Session, img_id: int):
    return db.query(db_models.Image).filter(db_models.Image.id == img_id).first()
