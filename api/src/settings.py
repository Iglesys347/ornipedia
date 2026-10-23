"""Application settings.

Values can be overridden by a `src/settings_local.py` file (used by the Ansible
deployment) and then by environment variables prefixed with `ORNIPEDIA_`.
"""

import os
import tempfile
from urllib.parse import quote_plus

DEV = False

PSQL_USER = "postgres"
PSQL_PASSWORD = "mysecretpassword"
PSQL_HOST = "127.0.0.1"
PSQL_PORT = 5432
PSQL_DB = "ornipedia"

DB_URL = None
DB_DEBUG = False

ALLOWED_ORIGINS = []

IMAGE_FOLDER = "/path/to/the/image/folder"

# password of the administration (adding birds and photos), disabled when empty
ADMIN_PASSWORD = ""

# maximum size of an uploaded photo
MAX_UPLOAD_SIZE = 25 * 1024 * 1024

# identification of the requests to Wikimedia Commons (required by the Wikimedia policy)
COMMONS_USER_AGENT = "Ornipedia/1.0 (https://github.com/Iglesys347/ornipedia)"

# folder where the resized images are cached
THUMBNAIL_FOLDER = os.path.join(tempfile.gettempdir(), "ornipedia-thumbnails")

try:
    from src.settings_local import *  # noqa: F401,F403 pylint: disable=wildcard-import,unused-wildcard-import
except ImportError:
    pass

PSQL_USER = os.environ.get("ORNIPEDIA_PSQL_USER", PSQL_USER)
PSQL_PASSWORD = os.environ.get("ORNIPEDIA_PSQL_PASSWORD", PSQL_PASSWORD)
PSQL_HOST = os.environ.get("ORNIPEDIA_PSQL_HOST", PSQL_HOST)
PSQL_PORT = int(os.environ.get("ORNIPEDIA_PSQL_PORT", PSQL_PORT))
PSQL_DB = os.environ.get("ORNIPEDIA_PSQL_DB", PSQL_DB)

DB_URL = os.environ.get("ORNIPEDIA_DB_URL", DB_URL) or (
    "postgresql+psycopg2://"
    f"{quote_plus(PSQL_USER)}:{quote_plus(PSQL_PASSWORD)}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"
)
DB_DEBUG = os.environ.get("ORNIPEDIA_DB_DEBUG", str(DB_DEBUG)).lower() in ("1", "true", "yes")

if "ORNIPEDIA_ALLOWED_ORIGINS" in os.environ:
    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.environ["ORNIPEDIA_ALLOWED_ORIGINS"].split(",")
        if origin.strip()
    ]

IMAGE_FOLDER = os.environ.get("ORNIPEDIA_IMAGE_FOLDER", IMAGE_FOLDER)
THUMBNAIL_FOLDER = os.environ.get("ORNIPEDIA_THUMBNAIL_FOLDER", THUMBNAIL_FOLDER)
ADMIN_PASSWORD = os.environ.get("ORNIPEDIA_ADMIN_PASSWORD", ADMIN_PASSWORD)
