from redis.asyncio import Redis
from config import config


redis = Redis.from_url(config.REDIS_DSN)
