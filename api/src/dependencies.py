from src.database.sql.database import SessionLocal
from src.database.redis.database import redis_client


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    try:
        yield redis_client
    finally:
        redis_client.close()
