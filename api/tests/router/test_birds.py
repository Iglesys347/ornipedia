import pytest

from tests.consts import (
    TEST_BIRD_1,
    BIRD1_EN,
    BIRD1_FR,
    BIRD1_EN_IMAGES,
    BIRD1_FR_IMAGES,
)


def test_birds(client):
    response = client.get("/birds")
    assert response.status_code == 200
    assert response.json() == {
        "items": [BIRD1_FR],
        "page": 1,
        "per_page": 25,
        "total": 1,
    }


def test_birds_en_language(client):
    response = client.get("/birds", params={"language": "en"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [BIRD1_EN],
        "total": 1,
        "page": 1,
        "per_page": 25,
    }


def test_birds_missing_language(client):
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
def test_birds_species_filter(client, species, lang, expected):
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
def test_birds_sub_species_filter(client, sub_species, lang, expected):
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
def test_birds_custom_pagination(
    client, page, per_page, expected_page, expected_per_page
):
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
def test_birds_wrong_pagination(client, page, per_page):
    response = client.get("/birds", params={"page": page, "per_page": per_page})
    assert response.status_code == 422


@pytest.mark.parametrize(
    "img_id",
    [
        "a",
        "123abc",
    ],
)
def test_birds_invalid_param(client, img_id):
    response = client.get(f"/images/{img_id}")
    assert response.status_code == 422


def test_bird(client):
    response = client.get(f"/birds/{BIRD1_FR['id']}")
    assert response.status_code == 200
    assert response.json() == BIRD1_FR


def test_bird_en_language(client):
    response = client.get(f"/birds/{BIRD1_FR['id']}", params={"language": "en"})
    assert response.status_code == 200
    assert response.json() == BIRD1_EN


def test_bird_missing_language(client):
    response = client.get(f"/birds/{BIRD1_FR['id']}", params={"language": "de"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Bird not found"}


def test_bird_missing_id(client):
    response = client.get("/birds/123456789")
    assert response.status_code == 404
    assert response.json() == {"detail": "Bird not found"}


def test_bird_images(client):
    response = client.get(f"/birds/{BIRD1_FR['id']}/images")
    assert response.status_code == 200
    assert response.json() == BIRD1_FR_IMAGES


def test_bird_images_en_language(client):
    response = client.get(f"/birds/{BIRD1_FR['id']}/images", params={"language": "en"})
    assert response.status_code == 200
    assert response.json() == BIRD1_EN_IMAGES


def test_bird_images_missing_language(client):
    response = client.get(f"/birds/{BIRD1_FR['id']}/images", params={"language": "de"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Bird not found"}


def test_bird_images_missing_id(client):
    response = client.get("/birds/123456789/images")
    assert response.status_code == 404
    assert response.json() == {"detail": "Bird not found"}
