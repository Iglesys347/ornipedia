"""Import of photos from Wikimedia Commons, with a fake Commons (answers in the format of the
MediaWiki API, formatversion=2)."""

import io
import os
from urllib.parse import parse_qs

import httpx
import pytest
from PIL import Image as PILImage

from src import commons
from tests.consts import TEST_BIRD_1

UPLOAD = "https://upload.wikimedia.org/wikipedia/commons"


def image_info(name, width, height, mime="image/jpeg", artist=None, license_url=True):
    metadata = {
        "Artist": {"value": artist if artist is not None else
                   '<a href="//commons.wikimedia.org/wiki/User:Jane" title="User:Jane">Jane &amp; Co</a>'},
        "LicenseShortName": {"value": "CC BY-SA 4.0"},
        "UsageTerms": {"value": "Creative Commons Attribution-Share Alike 4.0"},
        "ObjectName": {"value": name.replace("_", " ")},
    }
    if license_url:
        metadata["LicenseUrl"] = {"value": "https://creativecommons.org/licenses/by-sa/4.0"}
    else:
        metadata["LicenseShortName"] = {"value": "Public domain"}
        metadata["UsageTerms"] = {"value": "Public domain"}
    return {
        "width": width,
        "height": height,
        "size": 5_000_000,
        "mime": mime,
        "url": f"{UPLOAD}/a/ab/{name}.jpg",
        "thumburl": f"{UPLOAD}/thumb/a/ab/{name}.jpg/640px-{name}.jpg",
        "descriptionurl": f"https://commons.wikimedia.org/wiki/File:{name}.jpg",
        "extmetadata": metadata,
    }


SEARCH_ANSWER = {
    "batchcomplete": True,
    "continue": {"gsroffset": 10, "continue": "gsroffset||"},
    "query": {"pages": [
        {"pageid": 3, "ns": 6, "title": "File:Pica_pica_2.jpg", "index": 2,
         "imageinfo": [image_info("Pica_pica_2", 1200, 900, artist="John Smith", license_url=False)]},
        {"pageid": 1, "ns": 6, "title": "File:Pica_pica_1.jpg", "index": 1,
         "imageinfo": [image_info("Pica_pica_1", 4000, 3000)]},
        {"pageid": 2, "ns": 6, "title": "File:Pica_pica_map.svg", "index": 3,
         "imageinfo": [image_info("Pica_pica_map", 1000, 1000, mime="image/svg+xml")]},
    ]},
}


def jpeg(size=(800, 600)):
    buffer = io.BytesIO()
    PILImage.new("RGB", size, (60, 90, 40)).save(buffer, "JPEG")
    return buffer.getvalue()


class FakeCommons:
    """Fake Commons API and upload server, recording the requests."""

    def __init__(self):
        self.requests = []
        self.files = {}  # title -> imageinfo
        self.download_content = jpeg()
        # answers of the upload server by URL (default: the photo)
        self.upload_answers = {}

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if request.url.host != "commons.wikimedia.org":
            answer = self.upload_answers.get(str(request.url))
            return answer(request) if answer else httpx.Response(200, content=self.download_content)
        params = parse_qs(request.url.query.decode())
        if "generator" in params:
            return httpx.Response(200, json=SEARCH_ANSWER)
        title = params["titles"][0]
        if title not in self.files:
            return httpx.Response(200, json={"query": {"pages": [{"title": title, "missing": True}]}})
        info = dict(self.files[title])
        if info["width"] > int(params["iiurlwidth"][0]):
            name = title.removeprefix("File:")
            info["thumburl"] = f"{UPLOAD}/thumb/a/ab/{name}/{params['iiurlwidth'][0]}px-{name}"
        return httpx.Response(200, json={"query": {"pages": [{"title": title, "imageinfo": [info]}]}})


@pytest.fixture
def fake_commons(monkeypatch):
    fake = FakeCommons()
    monkeypatch.setattr(commons, "transport", httpx.MockTransport(fake.handler))
    return fake


def test_search(client, admin, fake_commons):
    response = client.get("/admin/commons/search", params={"q": " Pica pica "}, headers=admin["headers"])
    assert response.status_code == 200
    data = response.json()
    assert data["next_offset"] == 10
    # in the order of relevance, the SVG map is ignored
    assert [p["title"] for p in data["items"]] == ["File:Pica_pica_1.jpg", "File:Pica_pica_2.jpg"]

    first, second = data["items"]
    assert first["author_name"] == "Jane & Co"
    assert first["author_link"] == "https://commons.wikimedia.org/wiki/User:Jane"
    assert first["license_short_name"] == "CC BY-SA 4.0"
    assert first["license_link"] == "https://creativecommons.org/licenses/by-sa/4.0"
    assert first["page_url"] == "https://commons.wikimedia.org/wiki/File:Pica_pica_1.jpg"
    assert first["thumbnail_url"].startswith(f"{UPLOAD}/thumb/")
    assert first["already_added"] is False
    # plain text author, public domain: the license link is the page of the file
    assert second["author_name"] == "John Smith" and second["author_link"] is None
    assert second["license_link"] == second["page_url"]

    request = fake_commons.requests[0]
    params = parse_qs(request.url.query.decode())
    assert params["gsrsearch"][0].startswith("Pica pica filetype:bitmap")
    assert request.headers["user-agent"].startswith("Ornipedia/")


def test_search_requires_password(client, admin, fake_commons):
    assert client.get("/admin/commons/search", params={"q": "x"}).status_code == 401
    assert fake_commons.requests == []


@pytest.mark.parametrize("failure", [
    lambda request: httpx.Response(503),
    lambda request: httpx.Response(200, json={"error": {"code": "internal"}}),
    lambda request: (_ for _ in ()).throw(httpx.ConnectError("down")),
])
def test_search_commons_unreachable(client, admin, monkeypatch, failure):
    monkeypatch.setattr(commons, "transport", httpx.MockTransport(failure))
    response = client.get("/admin/commons/search", params={"q": "x"}, headers=admin["headers"])
    assert response.status_code == 502


def test_import(client, admin, fake_commons):
    fake_commons.files["File:Pica_pica_1.jpg"] = image_info("Pica_pica_1", 4000, 3000)
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/commons", json={"title": "File:Pica_pica_1.jpg"},
                           headers=admin["headers"])
    assert response.status_code == 201
    img_id = response.json()["id"]

    # bigger than 1920px (a standard thumbnail width): the 1920px version is downloaded
    download = fake_commons.requests[-1]
    assert download.url.host == "upload.wikimedia.org" and "1920px-" in str(download.url)
    info = client.get(f"/images/{img_id}/info", params={"language": "en"}).json()
    assert info["author"] == {"name": "Jane & Co", "link": "https://commons.wikimedia.org/wiki/User:Jane"}
    assert info["license"]["short_name"] == "CC BY-SA 4.0"
    assert info["original_url"] == "https://commons.wikimedia.org/wiki/File:Pica_pica_1.jpg"
    assert len(os.listdir(admin["images"])) == 1

    # marked in the search results, refused a second time
    search = client.get("/admin/commons/search", params={"q": "Pica"}, headers=admin["headers"]).json()
    assert search["items"][0]["already_added"] is True
    again = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/commons", json={"title": "File:Pica_pica_1.jpg"},
                        headers=admin["headers"])
    assert again.status_code == 409


def test_import_small_photo_downloads_the_original(client, admin, fake_commons):
    fake_commons.files["File:Pica_pica_2.jpg"] = image_info("Pica_pica_2", 1200, 900)
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/commons", json={"title": "File:Pica_pica_2.jpg"},
                           headers=admin["headers"])
    assert response.status_code == 201
    assert str(fake_commons.requests[-1].url) == f"{UPLOAD}/a/ab/Pica_pica_2.jpg"


def test_import_only_from_the_upload_server(client, admin, fake_commons):
    info = image_info("Evil", 1200, 900)
    info["url"] = "https://example.org/evil.jpg"
    fake_commons.files["File:Evil.jpg"] = info
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/commons", json={"title": "File:Evil.jpg"},
                           headers=admin["headers"])
    assert response.status_code == 502
    assert all(r.url.host != "example.org" for r in fake_commons.requests)
    assert not admin["images"].exists() or os.listdir(admin["images"]) == []


def test_import_too_big(client, admin, fake_commons, monkeypatch):
    monkeypatch.setattr("src.settings.MAX_UPLOAD_SIZE", 1000)
    fake_commons.files["File:Pica_pica_2.jpg"] = image_info("Pica_pica_2", 1200, 900)
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/commons", json={"title": "File:Pica_pica_2.jpg"},
                           headers=admin["headers"])
    assert response.status_code == 413


def test_import_not_an_image(client, admin, fake_commons):
    fake_commons.files["File:Pica_pica_2.jpg"] = image_info("Pica_pica_2", 1200, 900)
    fake_commons.download_content = b"<html>not an image</html>"
    response = client.post(f"/admin/birds/{TEST_BIRD_1['id']}/commons", json={"title": "File:Pica_pica_2.jpg"},
                           headers=admin["headers"])
    assert response.status_code == 422
    assert os.listdir(admin["images"]) == []


@pytest.mark.parametrize("bird_id, title, expected", [
    (TEST_BIRD_1["id"], "File:Missing.jpg", 404),
    (999999, "File:Pica_pica_1.jpg", 404),
    (TEST_BIRD_1["id"], "Pica_pica_1.jpg", 422),
])
def test_import_invalid(client, admin, fake_commons, bird_id, title, expected):
    response = client.post(f"/admin/birds/{bird_id}/commons", json={"title": title}, headers=admin["headers"])
    assert response.status_code == expected


def thumbnail_url(name, width=1920):
    return f"{UPLOAD}/thumb/a/ab/{name}.jpg/{width}px-{name}.jpg"


def import_photo(client, admin, title):
    return client.post(f"/admin/birds/{TEST_BIRD_1['id']}/commons", json={"title": title},
                       headers=admin["headers"])


def test_search_uses_standard_thumbnail_width(client, admin, fake_commons):
    client.get("/admin/commons/search", params={"q": "Pica"}, headers=admin["headers"])
    assert parse_qs(fake_commons.requests[0].url.query.decode())["iiurlwidth"] == ["500"]


def test_import_falls_back_to_the_original(client, admin, fake_commons):
    # the resized version is refused (e.g. rate limited): the original is downloaded
    fake_commons.files["File:Pica_pica_1.jpg"] = image_info("Pica_pica_1", 4000, 3000)
    fake_commons.upload_answers[thumbnail_url("Pica_pica_1")] = lambda r: httpx.Response(429)
    response = import_photo(client, admin, "File:Pica_pica_1.jpg")
    assert response.status_code == 201
    assert [str(r.url) for r in fake_commons.requests[-2:]] == [
        thumbnail_url("Pica_pica_1"), f"{UPLOAD}/a/ab/Pica_pica_1.jpg"]


def test_import_original_too_big_for_the_fallback(client, admin, fake_commons):
    info = image_info("Pica_pica_1", 4000, 3000)
    info["size"] = 100_000_000
    fake_commons.files["File:Pica_pica_1.jpg"] = info
    fake_commons.upload_answers[thumbnail_url("Pica_pica_1")] = lambda r: httpx.Response(429)
    response = import_photo(client, admin, "File:Pica_pica_1.jpg")
    assert response.status_code == 502
    # the cause is given to the administrator
    assert "HTTP 429" in response.json()["detail"]
    assert all(str(r.url) != f"{UPLOAD}/a/ab/Pica_pica_1.jpg" for r in fake_commons.requests)


def test_import_follows_redirections_on_the_upload_server(client, admin, fake_commons):
    fake_commons.files["File:Pica_pica_2.jpg"] = image_info("Pica_pica_2", 1200, 900)
    original = f"{UPLOAD}/a/ab/Pica_pica_2.jpg"
    fake_commons.upload_answers[original] = lambda r: httpx.Response(
        302, headers={"location": "/wikipedia/commons/a/ab/Pica_pica_2_moved.jpg"})
    response = import_photo(client, admin, "File:Pica_pica_2.jpg")
    assert response.status_code == 201
    assert str(fake_commons.requests[-1].url) == f"{UPLOAD}/a/ab/Pica_pica_2_moved.jpg"


def test_import_refuses_redirections_elsewhere(client, admin, fake_commons):
    fake_commons.files["File:Pica_pica_2.jpg"] = image_info("Pica_pica_2", 1200, 900)
    fake_commons.upload_answers[f"{UPLOAD}/a/ab/Pica_pica_2.jpg"] = lambda r: httpx.Response(
        302, headers={"location": "https://example.org/evil.jpg"})
    response = import_photo(client, admin, "File:Pica_pica_2.jpg")
    assert response.status_code == 502
    assert all(r.url.host != "example.org" for r in fake_commons.requests)
    assert "Unexpected download URL" in response.json()["detail"]
