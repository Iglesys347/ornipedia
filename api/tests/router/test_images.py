import pytest

from tests.consts import TEST_BIRD_1


@pytest.mark.parametrize(
    "img_id, content_type",
    [
        (TEST_BIRD_1["images"][0]["id"], "image/png"),
        (TEST_BIRD_1["images"][1]["id"], "image/jpeg"),
    ],
)
def test_images(client, img_id, content_type):
    response = client.get(f"/images/{img_id}")
    assert response.status_code == 200
    assert "content-type" in response.headers
    assert response.headers.get("content-type") == content_type


def test_images_missing_id(client):
    response = client.get("/images/123456789")
    assert response.status_code == 404
    assert response.json() == {"detail": "Image not found"}


@pytest.mark.parametrize(
    "img_id",
    [
        "a",
        "123abc",
    ],
)
def test_images_invalid_param(client, img_id):
    response = client.get(f"/images/{img_id}")
    assert response.status_code == 422


@pytest.mark.parametrize("lang, translation", [("en", 0), ("fr", 1)])
def test_image_info(client, lang, translation):
    image = TEST_BIRD_1["images"][0]
    response = client.get(f"/images/{image['id']}/info", params={"language": lang})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == image["id"]
    assert data["original_url"] == image["original_url"]
    assert data["author"] == {"name": image["author"]["name"], "link": image["author"]["link"]}
    assert data["license"]["short_name"] == image["license"]["short_name"]
    assert data["bird"]["name"] == TEST_BIRD_1["translations"][translation]["name"]
    assert data["bird"]["language_code"] == lang


@pytest.mark.parametrize("img_id, lang", [(123456789, "fr"), (1, "de")])
def test_image_info_not_found(client, img_id, lang):
    response = client.get(f"/images/{img_id}/info", params={"language": lang})
    assert response.status_code == 404
    assert response.json() == {"detail": "Image not found"}


@pytest.mark.parametrize("url", ["/images/random", "/images/image/random"])
def test_random_image(client, url):
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["bird_id"] == TEST_BIRD_1["id"]
    assert response.json()["id"] in [img["id"] for img in TEST_BIRD_1["images"]]


def test_random_image_species_filter(client, bird_without_images):
    species = TEST_BIRD_1["translations"][0]["species"]
    response = client.get("/images/random", params={"species": species})
    assert response.status_code == 200
    assert response.json()["bird_id"] == TEST_BIRD_1["id"]

    # the bird of this species has no image
    species = bird_without_images["translations"][0]["species"]
    response = client.get("/images/random", params={"species": species})
    assert response.status_code == 404


def test_images_per_page_too_large(client):
    response = client.get("/images", params={"per_page": 1000})
    assert response.status_code == 422
