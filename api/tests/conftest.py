import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.dependencies import get_db
from src.database.database import Base
from src.database.db_models import Bird, Translation, Image, ImageAuthor, ImageLicense

from tests.consts import SQLALCHEMY_DATABASE_URL, TEST_BIRD_1, TEST_BIRD_2


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_testing_db(tmp_path_factory):
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
        fp = tmp_path_factory.mktemp("images") / image["image_name"]
        fp.touch()
        db_img = Image(
            id=image["id"],
            bird_id=TEST_BIRD_1["id"],
            image_path=str(fp),
            original_url=image["original_url"],
            author_id=image["author"]["id"],
            license_id=image["license"]["id"],
        )
        session.add(db_img)

        db_img_author = ImageAuthor(
            id=image["author"]["id"],
            name=image["author"]["name"],
            link=image["author"]["link"],
        )
        session.add(db_img_author)
        db_img_license = ImageLicense(
            id=image["license"]["id"],
            short_name=image["license"]["short_name"],
            full_name=image["license"]["full_name"],
            link=image["license"]["link"],
        )
        session.add(db_img_license)

    session.commit()


@pytest.fixture
def bird_without_images():
    """Temporarily adds a bird without images nor sub-species to the database"""
    session = TestingSessionLocal()
    session.add(Bird(id=TEST_BIRD_2["id"], latin_name=TEST_BIRD_2["latin_name"]))
    for translation in TEST_BIRD_2["translations"]:
        session.add(Translation(bird_id=TEST_BIRD_2["id"], **translation))
    session.commit()
    yield TEST_BIRD_2
    session.query(Translation).filter(Translation.bird_id == TEST_BIRD_2["id"]).delete()
    session.query(Bird).filter(Bird.id == TEST_BIRD_2["id"]).delete()
    session.commit()
    session.close()


@pytest.fixture
def real_image(tmp_path, monkeypatch):
    """Temporarily adds a real 1000x750 image to the database, with an empty thumbnail cache"""
    from PIL import Image as PILImage  # pylint: disable=import-outside-toplevel

    monkeypatch.setattr("src.thumbnails.THUMBNAIL_FOLDER", str(tmp_path / "thumbnails"))
    image_path = tmp_path / "real.png"
    PILImage.new("RGB", (1000, 750), (120, 160, 90)).save(image_path)

    image = TEST_BIRD_1["images"][0]
    session = TestingSessionLocal()
    session.add(Image(
        id=100,
        bird_id=TEST_BIRD_1["id"],
        image_path=str(image_path),
        original_url="url",
        author_id=image["author"]["id"],
        license_id=image["license"]["id"],
    ))
    session.commit()
    yield {"id": 100, "path": image_path, "thumbnails": tmp_path / "thumbnails"}
    session.query(Image).filter(Image.id == 100).delete()
    session.commit()
    session.close()
