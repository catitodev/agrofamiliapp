from typing import Dict, Optional
import os
import httpx
from datetime import datetime


class FeedbackCollector:
    def __init__(self):
        self.feedback_data: list = []

    async def log_interaction(
        self,
        user_id: str,
        message: str,
        agent: str,
        response: str,
        rating: Optional[int] = None,
        metadata: Optional[Dict] = None
    ) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id_hash": self._hash_user(user_id),
            "message_preview": message[:100],
            "agent": agent,
            "response_length": len(response),
            "rating": rating,
            "metadata": metadata or {}
        }
        self.feedback_data.append(entry)

    async def log_feedback(self, user_id: str, agent: str, rating: int, comment: Optional[str] = None) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id_hash": self._hash_user(user_id),
            "agent": agent,
            "rating": rating,
            "comment": comment,
        }
        self.feedback_data.append(entry)

    async def get_aggregate_stats(self) -> Dict:
        if not self.feedback_data:
            return {"total_interactions": 0, "avg_rating": 0, "agents": {}}

        ratings = [e.get("rating") for e in self.feedback_data if e.get("rating")]
        agent_counts: Dict[str, int] = {}
        for e in self.feedback_data:
            agent = e.get("agent", "unknown")
            agent_counts[agent] = agent_counts.get(agent, 0) + 1

        return {
            "total_interactions": len(self.feedback_data),
            "avg_rating": sum(ratings) / len(ratings) if ratings else 0,
            "agents": agent_counts,
            "rated_count": len(ratings)
        }

    @staticmethod
    def _hash_user(user_id: str) -> str:
        import hashlib
        return hashlib.sha256(user_id.encode()).hexdigest()[:16]


feedback_collector = FeedbackCollector()