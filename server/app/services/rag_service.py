from typing import List, Optional

from app.db.repositories.user_repo import UserRepository
from app.db.mongodb import get_database
from app.utils.constants import RANK_DIFFICULTY_MAP


class RAGService:
    """RAG-based difficulty adjustment service"""

    def __init__(self):
        self.user_repo = UserRepository()

    async def get_recommended_difficulty(self, user_id: str, path: str) -> str:
        """Get recommended difficulty based on user performance"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return "easy"

        progress = (
            user.pirate_progress if path == "pirate" else user.marine_progress
        )
        rank_index = progress.rank

        difficulty_map = RANK_DIFFICULTY_MAP.get(path, {})
        difficulties = difficulty_map.get(rank_index, ["easy"])

        # TODO: Integrate with Pinecone/LangChain for smarter recommendations
        # For now, return the first difficulty in the mapped list
        return difficulties[0]

    async def get_weak_areas(self, user_id: str) -> List[str]:
        """Get user's weak areas from their progress data"""
        db = get_database()
        if not db:
            return []

        progress_doc = await db.user_progress.find_one({"user_id": user_id})
        if not progress_doc:
            return []

        return progress_doc.get("weak_areas", [])
