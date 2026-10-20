import io
import os

import pytest
from PIL import Image as PILImage

from tests.consts import TEST_BIRD_1

NEW_BIRD = {
    "latin_name": " Pica pica ",
    "translations": [
        {"language_code": "fr", "name": "pie bavarde", "species": "corvidés", "sub_species": " ", "details": None},
        {"language_code": "en", "name": "eurasian magpie", "species": "crows"},
    ],
}

PHOTO_FORM = {
    "author_name": "Jane Doe",
    "author_link": "https://example.org/jane",
    "license_short_name": "CC BY 4.0",
    "license_full_name": "Creative Commons Attribution 4.0",
    "license_link": "https://creativecommons.org/licenses/by/4.0/",
    "original_url": "https://example.org/photo",
}


def image_bytes(fmt="JPEG", size=(800, 600)):
    buffer = io.BytesIO()
    PILImage.new("RGB", size, (90, 140, 200)).save(buffer, fmt)
    return buffer.getvalue()


def test_admin_disabled_without_password(client):
    response = client.get("/admin/check", headers={"Authorization": "Bearer anything"})
    assert response.status_code == 503


@pytest.mark.parametrize("headers", [{}, {"Authorization": "Bearer wrong"}, {"Authorization": "Basic x"}])
def test_admin_invalid_password(client, admin, headers):
    assert client.get("/admin/check", headers=headers).status_code == 401
    assert client.post("/admin/birds", json=NEW_BIRD, headers=headers).status_code == 401
    assert client.delete("/admin/images/1", headers=headers).status_code == 401


def test_admin_check(client, admin):
    assert client.get("/admin/check", headers=admin["headers"]).json() == {"status": "ok"}


def test_create_bird(client, admin):
    response = client.post("/admin/birds", json=NEW_BIRD, headers=admin["headers"])
    assert response.status_code == 201
    bird_id = response.json()["id"]
    assert response.json()["latin_name"] == "Pica pica"

    bird = client.get(f"/birds/{bird_id}", params={"language": "fr"}).json()
    assert bird["name"] == "pie bavarde"
    assert bird["species"] == "corvidés"
    assert bird["sub_species"] == ""  # blank sub-species stored as null
    assert client.get(f"/birds/{bird_id}", params={"language": "en"}).json()["name"] == "eurasian magpie"


@pytest.mark.parametrize("payload", [
    {**NEW_BIRD, "translations": []},
    {**NEW_BIRD, "latin_name": ""},
    {**NEW_BIRD, "translations": [NEW_BIRD["translations"][0], NEW_BIRD["translations"][0]]},
    {**NEW_BIRD, "translations": [{**NEW_BIRD["translations"][0], "name": "  "}]},
])
def test_create_bird_invalid(client, admin, payload):
    assert client.post("/admin/birds", json=payload, headers=admin["headers"]).status_code == 422


@pytest.mark.parametrize("fmt, extension", [("JPEG", "jpg"), ("PNG", "png"), ("WEBP", "webp")])
def test_add_photo(client, admin, fmt, extension):
    bird_id = client.post("/admin/birds", json=NEW_BIRD, headers=admin["headers"]).json()["id"]
    response = client.post(
        f"/admin/birds/{bird_id}/images",
        data=PHOTO_FORM,
        files={"file": ("photo.whatever", image_bytes(fmt), "application/octet-stream")},
        headers=admin["headers"],
    )
    assert response.status_code == 201
    img_id = response.json()["id"]

    # saved under a random name with the extension of its real format
    saved = os.listdir(admin["images"])
    assert len(saved) == 1 and saved[0].endswith(f".{extension}")
    assert client.get(f"/images/{img_id}").status_code == 200
    info = client.get(f"/images/{img_id}/info", params={"language": "fr"}).json()
    assert info["bird"]["name"] == "pie bavarde"
    assert info["author"] == {"name": "Jane Doe", "link": "https://example.org/jane"}
    assert info["license"]["short_name"] == "CC BY 4.0"
    assert img_id in client.get(f"/birds/{bird_id}/images", params={"language": "fr"}).json()["image_ids"]


def test_add_photo_reuses_author_and_license(client, admin):
    bird_id = client.post("/admin/birds", json=NEW_BIRD, headers=admin["headers"]).json()["id"]
    for _ in range(2):
        client.post(f"/admin/birds/{bird_id}/images", data=PHOTO_FORM,
                    files={"file": ("p.jpg", image_bytes(), "image/jpeg")}, headers=admin["headers"])
    authors = client.get("/admin/authors", headers=admin["headers"]).json()
    licenses = client.get("/admin/licenses", headers=admin["headers"]).json()
    assert [a["name"] for a in authors].count("Jane Doe") == 1
    assert [lic["short_name"] for lic in licenses].count("CC BY 4.0") == 1


def test_add_photo_invalid_file(client, admin):
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/images", data=PHOTO_FORM,
                           files={"file": ("p.jpg", b"not an image", "image/jpeg")}, headers=admin["headers"])
    assert response.status_code == 422
    assert not admin["images"].exists() or os.listdir(admin["images"]) == []


def test_add_photo_unsupported_format(client, admin):
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/images", data=PHOTO_FORM,
                           files={"file": ("p.gif", image_bytes("GIF"), "image/gif")}, headers=admin["headers"])
    assert response.status_code == 422
    assert os.listdir(admin["images"]) == []


def test_add_photo_too_big(client, admin, monkeypatch):
    monkeypatch.setattr("src.settings.MAX_UPLOAD_SIZE", 1000)
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/images", data=PHOTO_FORM,
                           files={"file": ("p.jpg", image_bytes(), "image/jpeg")}, headers=admin["headers"])
    assert response.status_code == 413


def test_add_photo_unknown_bird(client, admin):
    response = client.post("/admin/birds/999999/images", data=PHOTO_FORM,
                           files={"file": ("p.jpg", image_bytes(), "image/jpeg")}, headers=admin["headers"])
    assert response.status_code == 404


def test_delete_photo(client, admin):
    bird_id = client.post("/admin/birds", json=NEW_BIRD, headers=admin["headers"]).json()["id"]
    img_id = client.post(f"/admin/birds/{bird_id}/images", data=PHOTO_FORM,
                         files={"file": ("p.jpg", image_bytes(), "image/jpeg")}, headers=admin["headers"]).json()["id"]
    assert client.get(f"/images/{img_id}", params={"width": 320}).status_code == 200

    assert client.delete(f"/admin/images/{img_id}", headers=admin["headers"]).status_code == 204
    assert client.get(f"/images/{img_id}").status_code == 404
    assert os.listdir(admin["images"]) == []  # the photo file is deleted
    assert client.delete(f"/admin/images/{img_id}", headers=admin["headers"]).status_code == 404


def test_delete_photo_keeps_files_outside_image_folder(client, admin, real_image):
    # photos added before the administration may be stored anywhere: their files are kept
    assert client.delete(f"/admin/images/{real_image['id']}", headers=admin["headers"]).status_code == 204
    assert real_image["path"].is_file()


def mpo_bytes():
    """Photo in the MPO format of some cameras: a JPEG followed by another picture"""
    buffer = io.BytesIO()
    first = PILImage.new("RGB", (800, 600), (90, 140, 200))
    first.save(buffer, "MPO", save_all=True, append_images=[PILImage.new("RGB", (800, 600))])
    return buffer.getvalue()


def test_add_photo_mpo(client, admin, real_image):
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/images", data=PHOTO_FORM,
                           files={"file": ("photo.jpg", mpo_bytes(), "image/jpeg")}, headers=admin["headers"])
    assert response.status_code == 201
    assert os.listdir(admin["images"])[0].endswith(".jpg")
    # its thumbnail is the first picture
    thumbnail = client.get(f"/images/{response.json()['id']}", params={"width": 320})
    assert thumbnail.headers["content-type"] == "image/jpeg"
    assert PILImage.open(io.BytesIO(thumbnail.content)).size == (320, 240)
