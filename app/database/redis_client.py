# app/database/redis_client.py
import os
from redis.asyncio import Redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


async def test_redis():
    try:
        await redis_client.set("health", "ok")
        result = await redis_client.get("health")
        print(f"✔ Redis connected: {result}")
    except Exception as e:
        print(f"✘ Redis Error: {e}")
