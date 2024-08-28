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
