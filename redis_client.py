import redis
import logging

logging.basicConfig(level=logging.INFO)

def get_redis_client(host: str = 'localhost', port: int = 6379, db: int = 0) -> redis.Redis:
    """
    Get a Redis client instance.

    Args:
        host (str): Redis server host.
        port (int): Redis server port.
        db (int): Redis database index.

    Returns:
        redis.Redis: Redis client connected to the specified database.
    """
    try:
        client = redis.Redis(host=host, port=port, db=db)
        logging.info("Redis client successfully connected")
        return client
    except redis.RedisError as e:
        logging.error(f"Redis connection error: {e}")
        raise e
