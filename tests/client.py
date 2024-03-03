from fastapi.testclient import TestClient

from app.main import app

from app.dependencies import get_db
from tests.db import override_get_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
