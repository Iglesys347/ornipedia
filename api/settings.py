DEV = False

PSQL_USER = "postgres"
PSQL_PASSWORD = "mysecretpassword"
PSQL_HOST = "127.0.0.1"
PSQL_PORT = 5432
PSQL_DB = "ornipedia"

DB_URL = f"postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"

try:
    from settings_local import *
except ImportError:
    pass
