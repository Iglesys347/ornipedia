import random

from sqlalchemy.orm import Session, contains_eager, Query

from src.models.responses import PaginatedResponse

from src.database import db_models
from src.models.schemas import Bird


def paginate(query: Query, page=1, per_page=10, distinct=False, str_items=False):
    total = query.count()
    if distinct:
        query = query.distinct()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    if str_items:
        items = [item[0] for item in items]
    if items == [None]:
        items = []
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
    search: str | None = None,
    species: str | None = None,
    sub_species: str | None = None,
    page: int = 1,
    per_page: int = 25,
):
    query = (
        db.query(db_models.Image.id)
        .join(
            db_models.Translation,
            onclause=db_models.Translation.bird_id == db_models.Image.bird_id,
        )
        .filter(db_models.Translation.language_code == language)
    )
    if search:
        query = query.filter(db_models.Translation.name.ilike(f"%{search}%"))
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


def get_image_info(db: Session, img_id: int, language: str = "fr"):
    res = (
        db.query(db_models.Image)
        .filter(db_models.Image.id == img_id)
        .filter(db_models.Translation.language_code == language)
        .first()
        # db.query(db_models.Bird)
        # .join(db_models.Translation)
        # .options(contains_eager(db_models.Bird.translations))
        # .join(db_models.Image)
        # .filter(db_models.Translation.language_code == language)
        # .filter(db_models.Image.id == img_id)
        # .first()
    )
    print(res.__dict__)
    return res


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


def insert_bird(db: Session, latin_name: str) -> db_models.Bird:
    db_bird = db_models.Bird(latin_name=latin_name)
    db.add(db_bird)
    db.commit()
    db.refresh(db_bird)
    return db_bird


def insert_translation(
    db: Session,
    bird_id: int,
    language_code: str,
    name: str,
    species: str,
    sub_species: str | None = None,
    details: str | None = None,
) -> db_models.Translation:
    db_translation = db_models.Translation(
        bird_id=bird_id,
        language_code=language_code,
        name=name,
        species=species,
        sub_species=sub_species,
        details=details,
    )
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation


def insert_img_author(db: Session, name: str, link: str) -> db_models.ImageAuthor:
    db_img_author = db_models.ImageAuthor(name=name, link=link)
    db.add(db_img_author)
    db.commit()
    db.refresh(db_img_author)
    return db_img_author


def get_img_author(db: Session, name: str, link: str) -> db_models.ImageAuthor | None:
    res = (
        db.query(db_models.ImageAuthor)
        .filter(db_models.ImageAuthor.name == name)
        .filter(db_models.ImageAuthor.link == link)
        .first()
    )
    if res:
        return res
    return None


def insert_img_license(
    db: Session, short_name: str, full_name: str, link: str
) -> db_models.ImageLicense:
    db_img_license = db_models.ImageLicense(
        short_name=short_name, full_name=full_name, link=link
    )
    db.add(db_img_license)
    db.commit()
    db.refresh(db_img_license)
    return db_img_license


def get_img_license(
    db: Session, short_name: str, link: str
) -> db_models.ImageLicense | None:
    res = (
        db.query(db_models.ImageLicense)
        .filter(db_models.ImageLicense.short_name == short_name)
        .filter(db_models.ImageLicense.link == link)
        .first()
    )
    if res:
        return res
    return None


def insert_image(
    db: Session,
    bird_id: int,
    license_id: int,
    author_id: int,
    image_path: str,
    original_url: str,
) -> db_models.Image:
    db_image = db_models.Image(
        bird_id=bird_id,
        license_id=license_id,
        author_id=author_id,
        image_path=image_path,
        original_url=original_url,
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
