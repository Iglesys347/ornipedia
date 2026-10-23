"""Resized versions of the images, generated on demand and cached on disk."""

import logging
import os
import tempfile

from PIL import Image, ImageOps, UnidentifiedImageError

from src.settings import THUMBNAIL_FOLDER

logger = logging.getLogger(__name__)

# only a few widths are allowed, so that the cache size stays bounded
THUMBNAIL_WIDTHS = (320, 640, 1280)

JPEG_QUALITY = 82


def get_thumbnail(image_path: str, img_id: int, width: int) -> str | None:
    """Returns the path of the image resized to `width` pixels wide (at most),
    or None if the image cannot be read (the original should then be used)."""
    thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"{img_id}-{width}.jpg")
    try:
        # the thumbnail is regenerated when the original image is modified
        if os.path.getmtime(thumbnail_path) >= os.path.getmtime(image_path):
            return thumbnail_path
    except OSError:
        pass

    try:
        with Image.open(image_path) as img:
            img = ImageOps.exif_transpose(img)
            if img.mode != "RGB":
                img = img.convert("RGB")
            if img.width > width:
                height = round(img.height * width / img.width)
                img = img.resize((width, height), Image.Resampling.LANCZOS)

            os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)
            # written in a temporary file first, as several workers may generate it at the same time
            fd, tmp_path = tempfile.mkstemp(dir=THUMBNAIL_FOLDER, suffix=".jpg")
            with os.fdopen(fd, "wb") as tmp_file:
                img.save(tmp_file, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
            os.replace(tmp_path, thumbnail_path)
    except (OSError, UnidentifiedImageError, ValueError) as err:
        logger.warning("Unable to create the thumbnail of image %s: %s", img_id, err)
        return None
    return thumbnail_path
