from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base
from app.database.db_models import Bird, Translation, Image

SQLALCHEMY_DATABASE_URL = "sqlite://"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.sqlite"

TEST_BIRD_1 = {
    "id": 1,
    "latin_name": "test_latin_name1",
    "translations": [
        {
            "id": 1,
            "name": "test_name1",
            "species": "test_species1",
            "sub_species": "test_sub_species1",
            "details": "test_details1",
            "language_code": "en",
        },
        {
            "id": 2,
            "name": "test_name2",
            "species": "test_species2",
            "sub_species": "test_sub_species2",
            "details": "test_details2",
            "language_code": "fr",
        },
    ],
    "images": [
        {"id": 1, "image_path": "test_image_path1"},
        {"id": 2, "image_path": "test_image_path2"},
    ],
}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def init_db():
    session = TestingSessionLocal()

    bird = Bird(id=TEST_BIRD_1["id"], latin_name=TEST_BIRD_1["latin_name"])
    session.add(bird)

    for translation in TEST_BIRD_1["translations"]:
        db_translation = Translation(
            id=translation["id"],
            bird_id=TEST_BIRD_1["id"],
            name=translation["name"],
            species=translation["species"],
            sub_species=translation["sub_species"],
            details=translation["details"],
            language_code=translation["language_code"],
        )
        session.add(db_translation)

    for image in TEST_BIRD_1["images"]:
        db_img = Image(
            id=image["id"],
            bird_id=TEST_BIRD_1["id"],
            image_path=image["image_path"],
        )
        session.add(db_img)

    session.commit()


Base.metadata.create_all(bind=engine)
init_db()
