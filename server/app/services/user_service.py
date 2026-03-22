from datetime import datetime
from typing import Optional, List

from app.db.repositories.user_repo import UserRepository
from app.db.repositories.submission_repo import SubmissionRepository
from app.models.user import User
from app.schemas.user import UserUpdate, UserPreferencesUpdate, UserStatsResponse


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.submission_repo = SubmissionRepository()

    async def update_user(self, user_id: str, update: UserUpdate) -> Optional[User]:
        """Update user profile"""
        update_data = update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        return await self.user_repo.update(user_id, update_data)

    async def get_user_stats(self, user_id: str) -> UserStatsResponse:
        """Get user statistics"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None

        total_solved = (
            user.pirate_progress.problems_solved + user.marine_progress.problems_solved
        )

        return UserStatsResponse(
            total_problems_solved=total_solved,
            pirate_progress=user.pirate_progress,
            marine_progress=user.marine_progress,
            current_streak=max(
                user.pirate_progress.current_streak,
                user.marine_progress.current_streak,
            ),
            best_streak=max(
                user.pirate_progress.best_streak, user.marine_progress.best_streak
            ),
            achievements_count=len(user.achievements),
        )

    async def get_submission_history(
        self, user_id: str, skip: int = 0, limit: int = 20
    ) -> List:
        """Get user's submission history"""
        return await self.submission_repo.get_by_user(user_id, skip, limit)

    async def get_achievements(self, user_id: str) -> List[str]:
        """Get user achievements"""
        user = await self.user_repo.get_by_id(user_id)
        return user.achievements if user else []

    async def update_preferences(
        self, user_id: str, preferences: UserPreferencesUpdate
    ) -> dict:
        """Update user preferences"""
        update_data = preferences.model_dump(exclude_unset=True)
        prefixed = {f"preferences.{k}": v for k, v in update_data.items()}
        prefixed["updated_at"] = datetime.utcnow()
        await self.user_repo.update(user_id, prefixed)
        return {"message": "Preferences updated"}
