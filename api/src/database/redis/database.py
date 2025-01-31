from redis import Redis

from src.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
