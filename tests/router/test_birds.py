import pytest

from tests.client import client
from tests.db import TEST_BIRD_1

BIRD1_EN = {
    "id": TEST_BIRD_1["id"],
    "latin_name": TEST_BIRD_1["latin_name"],
    "name": TEST_BIRD_1["translations"][0]["name"],
    "species": TEST_BIRD_1["translations"][0]["species"],
    "sub_species": TEST_BIRD_1["translations"][0]["sub_species"],
    "details": TEST_BIRD_1["translations"][0]["details"],
    "language_code": "en",
}

BIRD1_FR = {
    "id": TEST_BIRD_1["id"],
    "latin_name": TEST_BIRD_1["latin_name"],
    "name": TEST_BIRD_1["translations"][1]["name"],
    "species": TEST_BIRD_1["translations"][1]["species"],
    "sub_species": TEST_BIRD_1["translations"][1]["sub_species"],
    "details": TEST_BIRD_1["translations"][1]["details"],
    "language_code": "fr",
}

BIRD1_EN_IMAGES = {
    "id": TEST_BIRD_1["id"],
    "latin_name": TEST_BIRD_1["latin_name"],
    "name": TEST_BIRD_1["translations"][0]["name"],
    "species": TEST_BIRD_1["translations"][0]["species"],
    "sub_species": TEST_BIRD_1["translations"][0]["sub_species"],
    "details": TEST_BIRD_1["translations"][0]["details"],
    "language_code": "en",
    "image_ids": [img["id"] for img in TEST_BIRD_1["images"]],
}

BIRD1_FR_IMAGES = {
    "id": TEST_BIRD_1["id"],
    "latin_name": TEST_BIRD_1["latin_name"],
    "name": TEST_BIRD_1["translations"][1]["name"],
    "species": TEST_BIRD_1["translations"][1]["species"],
    "sub_species": TEST_BIRD_1["translations"][1]["sub_species"],
    "details": TEST_BIRD_1["translations"][1]["details"],
    "language_code": "fr",
    "image_ids": [img["id"] for img in TEST_BIRD_1["images"]],
}


def test_birds():
    response = client.get("/birds")
    assert response.status_code == 200
    assert response.json() == {
        "items": [BIRD1_FR],
        "page": 1,
        "per_page": 25,
        "total": 1,
    }


def test_birds_en_language():
    response = client.get("/birds", params={"language": "en"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [BIRD1_EN],
        "total": 1,
        "page": 1,
        "per_page": 25,
    }


def test_birds_missing_language():
    response = client.get("/birds", params={"language": "de"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "total": 0,
        "page": 1,
        "per_page": 25,
    }


@pytest.mark.parametrize(
    "species,lang,expected",
    [
        (None, "fr", BIRD1_FR),
        (TEST_BIRD_1["translations"][0]["species"], "en", BIRD1_EN),
        (TEST_BIRD_1["translations"][1]["species"], "fr", BIRD1_FR),
    ],
)
def test_birds_species_filter(species, lang, expected):
    response = client.get("/birds", params={"language": lang, "species": species})
    assert response.status_code == 200
    assert response.json() == {
        "items": [expected],
        "total": 1,
        "page": 1,
        "per_page": 25,
    }


@pytest.mark.parametrize(
    "sub_species,lang,expected",
    [
        (None, "fr", BIRD1_FR),
        (TEST_BIRD_1["translations"][0]["sub_species"], "en", BIRD1_EN),
        (TEST_BIRD_1["translations"][1]["sub_species"], "fr", BIRD1_FR),
    ],
)
def test_birds_sub_species_filter(sub_species, lang, expected):
    response = client.get(
        "/birds", params={"language": lang, "sub_species": sub_species}
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [expected],
        "total": 1,
        "page": 1,
        "per_page": 25,
    }


@pytest.mark.parametrize(
    "page,per_page,expected_page,expected_per_page",
    [(1, 25, 1, 25), (2, 25, 2, 25), (1, 1, 1, 1), (1, 0, 1, 0)],
)
def test_birds_custom_pagination(page, per_page, expected_page, expected_per_page):
    response = client.get("/birds", params={"page": page, "per_page": per_page})
    assert response.status_code == 200
    assert response.json()["page"] == expected_page
    assert response.json()["per_page"] == expected_per_page
    if per_page == 0:
        assert response.json()["items"] == []


@pytest.mark.parametrize(
    "page,per_page",
    [(None, None), (0, 0), (-1, 0), (1, -1)],
)
def test_birds_wrong_pagination(page, per_page):
    response = client.get("/birds", params={"page": page, "per_page": per_page})
    assert response.status_code == 422


def test_bird():
    response = client.get(f"/birds/{BIRD1_FR['id']}")
    assert response.status_code == 200
    assert response.json() == BIRD1_FR


def test_bird_en_language():
    response = client.get(f"/birds/{BIRD1_FR['id']}", params={"language": "en"})
    assert response.status_code == 200
    assert response.json() == BIRD1_EN


def test_bird_missing_language():
    response = client.get(f"/birds/{BIRD1_FR['id']}", params={"language": "de"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Bird not found"}


def test_bird_missing_id():
    response = client.get("/birds/123456789")
    assert response.status_code == 404
    assert response.json() == {"detail": "Bird not found"}
