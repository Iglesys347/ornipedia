"""Search and download of photos on Wikimedia Commons (https://commons.wikimedia.org)."""

from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse

import httpx

from src import settings

API_URL = "https://commons.wikimedia.org/w/api.php"
# photos are only downloaded from the Wikimedia upload server
DOWNLOAD_HOST = "upload.wikimedia.org"
# width of the thumbnails shown in the search results
# Wikimedia only serves some thumbnail widths reliably (the "standard" widths: 500, 960,
# 1280, 1920...); other widths are generated on demand and may be refused or rate limited
THUMBNAIL_WIDTH = 500
# bigger photos are downloaded at this width (originals can be very large)
DOWNLOAD_WIDTH = 1920
MAX_REDIRECTS = 3
# the search ignores small images (icons, maps...)
MIN_WIDTH = 800
SUPPORTED_MIME_TYPES = ("image/jpeg", "image/png", "image/webp")
EXTMETADATA = "Artist|LicenseShortName|LicenseUrl|UsageTerms|ObjectName"

# replaced in the tests by a mock transport
transport: httpx.BaseTransport | None = None  # pylint: disable=invalid-name


class CommonsError(Exception):
    """Wikimedia Commons is unreachable or returned an unexpected answer."""


class CommonsPhotoTooBig(CommonsError):
    """The photo exceeds the maximum size."""


@dataclass
class CommonsPhoto:  # pylint: disable=too-many-instance-attributes
    title: str
    page_url: str
    thumbnail_url: str
    download_url: str
    # the original file and its size in bytes, used when the resized version cannot be downloaded
    original_url: str
    size: int
    width: int
    height: int
    description: str
    author_name: str
    author_link: str | None
    license_short_name: str
    license_full_name: str
    license_link: str


class _TextAndLink(HTMLParser):
    """Text and first link of a HTML snippet (the "Artist" field is HTML)."""

    def __init__(self):
        super().__init__()
        self.text: list[str] = []
        self.link: str | None = None

    def handle_starttag(self, tag, attrs):
        if tag == "a" and self.link is None:
            self.link = dict(attrs).get("href")

    def handle_data(self, data):
        self.text.append(data)


def _absolute(url: str | None) -> str | None:
    if not url:
        return None
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return "https://commons.wikimedia.org" + url
    return url


def _text_and_link(html: str) -> tuple[str, str | None]:
    parser = _TextAndLink()
    parser.feed(html or "")
    text = " ".join(unescape("".join(parser.text)).split())
    return text, _absolute(parser.link)


def _metadata(info: dict, name: str) -> str:
    value = info.get("extmetadata", {}).get(name, {}).get("value", "")
    return value if isinstance(value, str) else str(value)


def _parse_page(page: dict) -> CommonsPhoto | None:
    """Photo of a page of the API answer, None if it cannot be used."""
    infos = page.get("imageinfo") or []
    if not infos:
        return None
    info = infos[0]
    if info.get("mime") not in SUPPORTED_MIME_TYPES:
        return None
    license_short_name, _ = _text_and_link(_metadata(info, "LicenseShortName"))
    if not license_short_name:
        return None

    page_url = _absolute(info.get("descriptionurl")) or ""
    author_name, author_link = _text_and_link(_metadata(info, "Artist"))
    license_full_name, _ = _text_and_link(_metadata(info, "UsageTerms"))
    license_link = _absolute(_metadata(info, "LicenseUrl"))
    description, _ = _text_and_link(_metadata(info, "ObjectName"))
    width, height = info.get("width", 0), info.get("height", 0)
    # the thumbnail requested with iiurlwidth, or the original when it is smaller
    resized_url = _absolute(info.get("thumburl")) or _absolute(info.get("url")) or ""
    return CommonsPhoto(
        title=page.get("title", ""),
        page_url=page_url,
        thumbnail_url=resized_url,
        download_url=resized_url,
        original_url=_absolute(info.get("url")) or resized_url,
        size=info.get("size", 0),
        width=width,
        height=height,
        description=description or page.get("title", "").removeprefix("File:"),
        author_name=author_name or "Unknown",
        author_link=author_link,
        license_short_name=license_short_name,
        license_full_name=license_full_name or license_short_name,
        # public domain files have no license URL: their page describes their status
        license_link=license_link or page_url,
    )


def _client(follow_redirects: bool = True) -> httpx.Client:
    return httpx.Client(
        transport=transport,
        timeout=20,
        follow_redirects=follow_redirects,
        headers={"User-Agent": settings.COMMONS_USER_AGENT},
    )


def _query(params: dict) -> dict:
    try:
        with _client() as client:
            response = client.get(
                API_URL, params={"action": "query", "format": "json", "formatversion": 2, **params}
            )
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPError, ValueError) as err:
        # some errors have no message (e.g. timeouts): their type is always given
        raise CommonsError(f"{type(err).__name__} when querying the Commons API: {err}") from err
    if "error" in data:
        raise CommonsError(str(data["error"]))
    return data


def search(query: str, limit: int = 10, offset: int = 0) -> tuple[list[CommonsPhoto], int | None]:
    """Photos matching the query, in the order of relevance, and the offset of the next results."""
    data = _query(
        {
            "generator": "search",
            "gsrsearch": f"{query} filetype:bitmap filew:>{MIN_WIDTH}",
            "gsrnamespace": 6,
            "gsrlimit": limit,
            "gsroffset": offset,
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": THUMBNAIL_WIDTH,
            "iiextmetadatafilter": EXTMETADATA,
        }
    )
    pages = sorted(data.get("query", {}).get("pages", []), key=lambda p: p.get("index", 0))
    photos = [photo for photo in map(_parse_page, pages) if photo is not None]
    next_offset = data.get("continue", {}).get("gsroffset")
    return photos, next_offset


def get_photo(title: str) -> CommonsPhoto | None:
    """Photo of a file page ("File:..."), with the URL of its version to download."""
    data = _query(
        {
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": DOWNLOAD_WIDTH,
            "iiextmetadatafilter": EXTMETADATA,
        }
    )
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing"):
        return None
    photo = _parse_page(pages[0])
    if photo is not None and photo.width <= DOWNLOAD_WIDTH:
        # smaller than the download width: the original
        photo.download_url = photo.original_url
    return photo


def _check_download_url(url: str):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != DOWNLOAD_HOST:
        raise CommonsError(f"Unexpected download URL: {url}")


def _fetch(client: httpx.Client, url: str, max_size: int) -> bytes:
    """Content of the URL, following the redirections only on the upload server."""
    for _ in range(MAX_REDIRECTS + 1):
        _check_download_url(url)
        with client.stream("GET", url) as response:
            if response.is_redirect:
                # relative to the URL of the answer (not to Commons)
                url = str(response.url.join(response.headers.get("location", "")))
                continue
            if response.status_code != 200:
                raise CommonsError(f"HTTP {response.status_code} when downloading {url}")
            content = bytearray()
            for chunk in response.iter_bytes():
                content.extend(chunk)
                if len(content) > max_size:
                    raise CommonsPhotoTooBig("The photo is too big")
            return bytes(content)
    raise CommonsError(f"Too many redirections when downloading {url}")


def download(photo: CommonsPhoto, max_size: int) -> bytes:
    """Content of the photo, only from the Wikimedia upload server and up to `max_size` bytes.
    The original file is used when its resized version cannot be downloaded."""
    urls = [photo.download_url]
    if photo.original_url != photo.download_url and 0 < photo.size <= max_size:
        urls.append(photo.original_url)
    errors = []
    with _client(follow_redirects=False) as client:
        for url in urls:
            try:
                return _fetch(client, url, max_size)
            except CommonsPhotoTooBig:
                raise
            except CommonsError as err:
                errors.append(str(err))
            except httpx.HTTPError as err:
                errors.append(f"{type(err).__name__} when downloading {url}: {err}")
    raise CommonsError("; ".join(errors))
