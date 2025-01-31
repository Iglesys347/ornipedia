DEV = False

PSQL_USER = "postgres"
PSQL_PASSWORD = "mysecretpassword"
PSQL_HOST = "127.0.0.1"
PSQL_PORT = 5432
PSQL_DB = "ornipedia"

DB_URL = f"postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"
DB_DEBUG = False

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0

ALLOWED_ORIGINS = ["http://localhost:3000"]

IMAGE_FOLDER = "/path/to/the/image/folder"

try:
    from src.settings_local import *  # type: ignore
except ImportError:
    pass
