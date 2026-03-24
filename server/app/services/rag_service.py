from typing import List, Optional
from collections import defaultdict

from app.db.repositories.user_repo import UserRepository
from app.db.mongodb import get_database
from app.utils.constants import RANK_DIFFICULTY_MAP


# How many recent submissions to analyse for weak area detection
RECENT_SUBMISSIONS_WINDOW = 20


class RAGService:
    """
    Difficulty adjustment and weak area detection.

    Currently DB-based: analyses submission history to recommend the right
    difficulty and surface categories where the user is struggling.

    Structured for Pinecone/LangChain drop-in when API keys are available.
    """

    def __init__(self):
        self.user_repo = UserRepository()

    async def get_recommended_difficulty(self, user_id: str, path: str) -> str:
        """
        Return a difficulty string for the next problem.

        Logic:
        1. Start from rank-mapped baseline difficulty.
        2. If recent win-rate on that difficulty is high (≥70%), nudge up.
        3. If recent win-rate is low (<40%), nudge down.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return "easy"

        progress = user.fighter_progress if path == "fighter" else user.sentinel_progress
        rank_index = progress.rank if progress else 0

        difficulty_map = RANK_DIFFICULTY_MAP.get(path, {})
        baseline_difficulties: list = difficulty_map.get(rank_index, ["easy"])
        baseline = baseline_difficulties[0]

        # Adjust based on recent performance
        win_rate = await self._recent_win_rate(user_id, path, baseline)
        return self._adjust_difficulty(baseline, win_rate)

    async def get_weak_areas(self, user_id: str, path: str = "fighter") -> List[str]:
        """
        Return a list of DSA/design categories where the user has the highest
        failure rate, derived from their submission history.
        """
        db = get_database()
        if not db:
            return []

        cursor = (
            db.submissions
            .find({"user_id": user_id, "path": path})
            .sort("created_at", -1)
            .limit(RECENT_SUBMISSIONS_WINDOW)
        )
        submissions = await cursor.to_list(length=RECENT_SUBMISSIONS_WINDOW)

        if not submissions:
            return []

        # Tally attempts and failures per category
        attempts: dict = defaultdict(int)
        failures: dict = defaultdict(int)

        for sub in submissions:
            category = sub.get("category") or sub.get("problem_category")
            if not category:
                continue
            attempts[category] += 1
            if sub.get("status") not in ("accepted",):
                failures[category] += 1

        if not attempts:
            return []

        # Failure rate per category — only include categories with ≥2 attempts
        failure_rates = {
            cat: failures[cat] / attempts[cat]
            for cat in attempts
            if attempts[cat] >= 2
        }

        # Return categories sorted by highest failure rate (top 3)
        weak = sorted(failure_rates, key=lambda c: failure_rates[c], reverse=True)
        return weak[:3]

    async def get_next_problem_params(self, user_id: str, path: str) -> dict:
        """
        Convenience method: returns a dict with `difficulty` and `weak_areas`
        to pass directly into ProblemService or QuestionGenerator.
        """
        difficulty = await self.get_recommended_difficulty(user_id, path)
        weak_areas = await self.get_weak_areas(user_id, path)
        return {"difficulty": difficulty, "weak_areas": weak_areas}

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _recent_win_rate(self, user_id: str, path: str, difficulty: str) -> float:
        """Win rate of the last 10 submissions at a given difficulty."""
        db = get_database()
        if not db:
            return 0.5  # neutral — no data

        cursor = (
            db.submissions
            .find({"user_id": user_id, "path": path, "difficulty": difficulty})
            .sort("created_at", -1)
            .limit(10)
        )
        recent = await cursor.to_list(length=10)
        if not recent:
            return 0.5

        wins = sum(1 for s in recent if s.get("status") == "accepted")
        return wins / len(recent)

    @staticmethod
    def _adjust_difficulty(baseline: str, win_rate: float) -> str:
        """Nudge difficulty up or down based on win rate."""
        order = ["easy", "medium", "hard", "expert"]
        idx = order.index(baseline) if baseline in order else 0

        if win_rate >= 0.70 and idx < len(order) - 1:
            return order[idx + 1]
        if win_rate < 0.40 and idx > 0:
            return order[idx - 1]
        return baseline
