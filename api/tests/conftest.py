import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine, func
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
            group_name=translation["group"],
            subgroup_name=translation["subgroup"],
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
    """Temporarily adds a bird without images nor sub-group to the database"""
    session = TestingSessionLocal()
    session.add(Bird(id=TEST_BIRD_2["id"], latin_name=TEST_BIRD_2["latin_name"]))
    for translation in TEST_BIRD_2["translations"]:
        session.add(Translation(
            bird_id=TEST_BIRD_2["id"],
            id=translation["id"],
            name=translation["name"],
            group_name=translation["group"],
            subgroup_name=translation["subgroup"],
            details=translation["details"],
            language_code=translation["language_code"],
        ))
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


ADMIN_PASSWORD = "test-admin-password"


@pytest.fixture
def admin(tmp_path, monkeypatch):
    """Enables the administration and removes everything created by the test"""
    monkeypatch.setattr("src.settings.ADMIN_PASSWORD", ADMIN_PASSWORD)
    monkeypatch.setattr("src.settings.IMAGE_FOLDER", str(tmp_path / "images"))
    monkeypatch.setattr("src.thumbnails.THUMBNAIL_FOLDER", str(tmp_path / "thumbnails"))
    monkeypatch.setattr("src.auth.FAILED_LOGIN_DELAY", 0)

    models = [Image, Translation, Bird, ImageAuthor, ImageLicense]
    session = TestingSessionLocal()
    last_ids = {model: session.query(func.max(model.id)).scalar() or 0 for model in models}
    yield {"headers": {"Authorization": f"Bearer {ADMIN_PASSWORD}"}, "images": tmp_path / "images"}
    for model in models:
        session.query(model).filter(model.id > last_ids[model]).delete()
    session.commit()
    session.close()


# id, name, group, subgroup (in english); the test bird 1 has photos too
QUIZ_BIRDS = [
    (101, "golden eagle", "raptors", "eagles"),
    (102, "bonelli's eagle", "raptors", "eagles"),
    (103, "booted eagle", "raptors", "eagles"),
    (104, "common buzzard", "raptors", "buzzards"),
    (105, "mallard", "ducks", None),
    (106, "robin", "passerines", None),
]
# a bird without photos is never part of the quiz
NO_PHOTO_BIRD = (107, "no photo", "raptors", "eagles")


@pytest.fixture
def quiz_birds():
    """Temporarily adds birds with photos to the database, for the quiz"""
    session = TestingSessionLocal()
    for bird_id, name, group, subgroup in QUIZ_BIRDS + [NO_PHOTO_BIRD]:
        session.add(Bird(id=bird_id, latin_name=f"latin {name}"))
        session.add(Translation(bird_id=bird_id, language_code="en", name=name,
                                group_name=group, subgroup_name=subgroup))
    for bird_id, *_ in QUIZ_BIRDS:
        for index in range(2):
            session.add(Image(id=bird_id * 10 + index, bird_id=bird_id, author_id=1, license_id=1,
                              image_path="unused", original_url="url"))
    session.commit()
    yield
    ids = [bird[0] for bird in QUIZ_BIRDS + [NO_PHOTO_BIRD]]
    session.query(Image).filter(Image.bird_id.in_(ids)).delete()
    session.query(Translation).filter(Translation.bird_id.in_(ids)).delete()
    session.query(Bird).filter(Bird.id.in_(ids)).delete()
    session.commit()
    session.close()
