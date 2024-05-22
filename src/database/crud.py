import random

from sqlalchemy.orm import Session, contains_eager, Query

from src.models.responses import PaginatedResponse

from src.database import db_models
from src.models.schemas import Bird


def paginate(query: Query, page=1, per_page=10, distinct=False, str_items=False):
    total = query.count()
    if distinct:
        items = query.offset((page - 1) * per_page).limit(per_page).distinct()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    if str_items:
        items = [item[0] for item in items]
    return PaginatedResponse(page=page, per_page=per_page, total=total, items=items)


def get_bird(db: Session, bird_id: int, language: str = "fr") -> Bird | None:
    bird = (
        db.query(db_models.Bird)
        .join(db_models.Translation)
        .options(contains_eager(db_models.Bird.translations))
        .filter(db_models.Bird.id == bird_id)
        .filter(db_models.Translation.language_code == language)
        .first()
    )
    return bird


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
        .options(contains_eager(db_models.Bird.translations))
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
        .options(contains_eager(db_models.Bird.translations))
        .join(db_models.Image)
        .filter(db_models.Bird.id == bird_id)
        .filter(db_models.Translation.language_code == language)
        .first()
    )


def get_image(db: Session, img_id: int):
    return db.query(db_models.Image).filter(db_models.Image.id == img_id).first()


def get_images_ids(
    db: Session,
    language: str = "fr",
    species: str | None = None,
    sub_species: str | None = None,
    page: int = 1,
    per_page: int = 25,
):
    query = db.query(db_models.Image.id).filter(
        db_models.Translation.language_code == language
    )
    if species:
        query = query.filter(db_models.Translation.species == species)
    if sub_species:
        query = query.filter(db_models.Translation.sub_species == sub_species)
    return paginate(query, page, per_page)


def get_image_bird(db: Session, img_id: int, language: str = "fr"):
    return (
        db.query(db_models.Bird)
        .join(db_models.Translation)
        .options(contains_eager(db_models.Bird.translations))
        .join(db_models.Image)
        .filter(db_models.Translation.language_code == language)
        .filter(db_models.Image.id == img_id)
        .first()
    )


def get_random_image(
    db: Session, species: str | None = None, sub_species: str | None = None
):
    query = db.query(db_models.Image)
    if species:
        query = query.filter(db_models.Translation.species == species)
    if sub_species:
        query = query.filter(db_models.Translation.sub_species == sub_species)
    row_count = query.count()
    if row_count:
        random_offset = random.randint(0, row_count - 1)
        return query.offset(random_offset).first()
    return None


def get_species(
    db: Session,
    language: str = "fr",
    page: int = 1,
    per_page: int = 25,
) -> PaginatedResponse[str]:
    query = db.query(db_models.Translation.species).filter(
        db_models.Translation.language_code == language
    )
    return paginate(query, page, per_page, distinct=True, str_items=True)


def get_sub_species(
    db: Session, species: str, language: str = "fr", page: int = 1, per_page: int = 25
) -> PaginatedResponse[str]:
    query = db.query(db_models.Translation.sub_species).filter(
        db_models.Translation.language_code == language,
        db_models.Translation.species == species,
    )
    return paginate(query, page, per_page, distinct=True, str_items=True)
