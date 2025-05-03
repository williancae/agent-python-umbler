from typing import Optional

import redis.asyncio as redis_async

from app.config.config import settings


class RedisRepository:
    def __init__(self):
        self.redis = redis_async.from_url(settings.REDIS_URL, decode_responses=True)

    # === IA: Pausa e retomada ===
    async def is_paused(self, canal_id: str) -> bool:
        return await self.redis.get(f"canal:{canal_id}:paused") == "1"

    async def pause_ia(self, canal_id: str):
        await self.redis.set(f"canal:{canal_id}:paused", "1")

    async def resume_ia(self, canal_id: str):
        await self.redis.delete(f"canal:{canal_id}:paused")

    # === Cache básico ===
    async def set_cache(self, key: str, value: str, ttl: int = 300):
        await self.redis.set(key, value, ex=ttl)

    async def get_cache(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def delete_cache(self, key: str):
        await self.redis.delete(key)

    # === Locks ===
    async def acquire_lock(self, key: str, ttl: int = 10) -> bool:
        # Retorna True se conseguiu adquirir o lock
        return await self.redis.set(name=key, value="1", ex=ttl, nx=True)

    async def release_lock(self, key: str):
        await self.redis.delete(key)

    # === Helpers por canal ===
    async def get_last_message_ts(self, canal_id: str) -> Optional[str]:
        return await self.redis.get(f"canal:{canal_id}:last_msg")

    async def set_last_message_ts(self, canal_id: str, timestamp: str):
        await self.redis.set(f"canal:{canal_id}:last_msg", timestamp)

    # ==== Langchain ====
    # app/services/redis.py (adicionar no RedisRepository)
    async def append_history(self, phone: str, role: str, content: str):
        key = f"history:{phone}"
        await self.redis.rpush(key, f"{role}:{content}")

    async def get_history(self, phone: str, limit: int = 10) -> list[dict]:
        key = f"history:{phone}"
        items = await self.redis.lrange(key, -limit, -1)
        return [
            {"role": role, "content": content}
            for item in items
            if ":" in item
            for role, content in [item.split(":", 1)]
        ]
