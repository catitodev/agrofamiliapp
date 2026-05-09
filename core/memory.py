import redis.asyncio as redis
from typing import Optional, List, Dict
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
MAX_HISTORY = 20


class ConversationMemory:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None

    async def connect(self):
        self.redis_client = await redis.from_url(REDIS_URL, decode_responses=True)

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()

    def _key(self, user_id: str) -> str:
        return f"agrofam:conv:{user_id}"

    async def add_message(self, user_id: str, role: str, content: str, agent: str = "general") -> None:
        if not self.redis_client:
            return

        message = json.dumps({"role": role, "content": content, "agent": agent})
        key = self._key(user_id)
        await self.redis_client.rpush(key, message)
        await self.redis_client.ltrim(key, -MAX_HISTORY, -1)
        await self.redis_client.expire(key, 86400 * 30)

    async def get_history(self, user_id: str) -> List[Dict]:
        if not self.redis_client:
            return []

        key = self._key(user_id)
        raw = await self.redis_client.lrange(key, 0, -1)
        return [json.loads(m) for m in raw]

    async def clear_history(self, user_id: str) -> None:
        if self.redis_client:
            await self.redis_client.delete(self._key(user_id))

    async def get_user_context(self, user_id: str) -> Dict:
        history = await self.get_history(user_id)
        if not history:
            return {}
        last = history[-1]
        return {
            "last_agent": last.get("agent", "general"),
            "message_count": len(history),
            "recent_topics": list(set(m.get("agent", "general") for m in history[-5:]))
        }


memory = ConversationMemory()