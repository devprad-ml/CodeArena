from typing import Tuple, Dict, List

from app.db.repositories.user_repo import UserRepository
from app.utils.constants import (
    PIRATE_RANKS,
    MARINE_RANKS,
    SUPREME_RANK_REQUIREMENTS,
    DSA_CATEGORIES,
    SCORING,
)


class RankService:
    POINTS_PER_RANK = SCORING["points_per_rank"]
    FIRST_CORRECT_POINTS = SCORING["first_correct"]
    WRONG_SUBMISSION_PENALTY = SCORING["wrong_submission"]
    SKIP_PENALTY = SCORING["skip_penalty"]
    HINT_PENALTY = SCORING["hint_penalty"]

    def __init__(self):
        self.user_repo = UserRepository()

    def calculate_submission_points(
        self,
        is_correct: bool,
        attempt_number: int,
    ) -> int:
        """Calculate points for a submission"""
        if is_correct:
            wrong_attempts = attempt_number - 1
            points = self.FIRST_CORRECT_POINTS + (
                wrong_attempts * self.WRONG_SUBMISSION_PENALTY
            )
            return max(points, 5)  # Minimum 5 points for correct
        else:
            return self.WRONG_SUBMISSION_PENALTY

    async def update_user_progress(
        self,
        user_id: str,
        path: str,
        points: int,
        attempt_number: int,
    ):
        """Update user progress after a successful submission"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return

        progress_field = f"{path}_progress"
        progress = getattr(user, progress_field)

        new_points = progress.points + points
        new_total = progress.total_points + points
        new_solved = progress.problems_solved + 1

        update_data = {
            f"{progress_field}.points": new_points,
            f"{progress_field}.total_points": new_total,
            f"{progress_field}.problems_solved": new_solved,
        }

        if attempt_number == 1:
            update_data[f"{progress_field}.first_try_successes"] = (
                progress.first_try_successes + 1
            )

        # Update rank
        rank_info = self.get_rank_info(path, new_total)
        update_data[f"{progress_field}.rank"] = rank_info["rank_index"]

        await self.user_repo.update(user_id, update_data)

    async def apply_hint_penalty(self, user_id: str, path: str):
        """Apply hint penalty to user"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return

        progress_field = f"{path}_progress"
        progress = getattr(user, progress_field)
        new_points = max(0, progress.points + self.HINT_PENALTY)

        await self.user_repo.update(
            user_id,
            {f"{progress_field}.points": new_points},
        )

    def check_supreme_rank_qualification(
        self,
        path: str,
        user_stats: Dict,
    ) -> Tuple[bool, Dict]:
        """
        Check if user qualifies for supreme rank (GOL D. ROGER or MONKEY D. GARP).
        Supreme ranks cannot be achieved by grinding alone.
        """
        requirements = SUPREME_RANK_REQUIREMENTS[path]
        qualification_status = {}

        if path == "pirate":
            checks = {
                "points": user_stats.get("total_points", 0) >= requirements["min_points"],
                "first_try_rate": user_stats.get("first_try_rate", 0)
                >= requirements["min_first_try_rate"],
                "expert_solved": user_stats.get("expert_problems_solved", 0)
                >= requirements["min_expert_solved"],
                "all_categories": self._check_all_categories_completed(
                    user_stats.get("categories_completed", []),
                    requirements["categories"],
                ),
                "streak": user_stats.get("current_streak", 0)
                >= requirements["min_streak"],
            }

            qualification_status = {
                "points": {
                    "current": user_stats.get("total_points", 0),
                    "required": requirements["min_points"],
                    "met": checks["points"],
                },
                "first_try_rate": {
                    "current": f"{user_stats.get('first_try_rate', 0) * 100:.1f}%",
                    "required": f"{requirements['min_first_try_rate'] * 100:.0f}%",
                    "met": checks["first_try_rate"],
                },
                "expert_solved": {
                    "current": user_stats.get("expert_problems_solved", 0),
                    "required": requirements["min_expert_solved"],
                    "met": checks["expert_solved"],
                },
                "all_categories": {
                    "current": len(user_stats.get("categories_completed", [])),
                    "required": len(requirements["categories"]),
                    "met": checks["all_categories"],
                },
                "streak": {
                    "current": user_stats.get("current_streak", 0),
                    "required": requirements["min_streak"],
                    "met": checks["streak"],
                },
            }

        else:  # marine
            checks = {
                "points": user_stats.get("total_points", 0) >= requirements["min_points"],
                "first_try_rate": user_stats.get("first_try_rate", 0)
                >= requirements["min_first_try_rate"],
                "avg_ai_score": user_stats.get("avg_ai_score", 0)
                >= requirements["min_avg_ai_score"],
                "lld_solved": user_stats.get("lld_problems_solved", 0)
                >= requirements["min_lld_solved"],
                "hld_solved": user_stats.get("hld_problems_solved", 0)
                >= requirements["min_hld_solved"],
                "perfect_scores": user_stats.get("perfect_scores", 0)
                >= requirements["min_perfect_scores"],
            }

            qualification_status = {
                "points": {
                    "current": user_stats.get("total_points", 0),
                    "required": requirements["min_points"],
                    "met": checks["points"],
                },
                "first_try_rate": {
                    "current": f"{user_stats.get('first_try_rate', 0) * 100:.1f}%",
                    "required": f"{requirements['min_first_try_rate'] * 100:.0f}%",
                    "met": checks["first_try_rate"],
                },
                "avg_ai_score": {
                    "current": f"{user_stats.get('avg_ai_score', 0) * 100:.1f}%",
                    "required": f"{requirements['min_avg_ai_score'] * 100:.0f}%",
                    "met": checks["avg_ai_score"],
                },
                "lld_solved": {
                    "current": user_stats.get("lld_problems_solved", 0),
                    "required": requirements["min_lld_solved"],
                    "met": checks["lld_solved"],
                },
                "hld_solved": {
                    "current": user_stats.get("hld_problems_solved", 0),
                    "required": requirements["min_hld_solved"],
                    "met": checks["hld_solved"],
                },
                "perfect_scores": {
                    "current": user_stats.get("perfect_scores", 0),
                    "required": requirements["min_perfect_scores"],
                    "met": checks["perfect_scores"],
                },
            }

        all_requirements_met = all(checks.values())

        return all_requirements_met, {
            "qualified": all_requirements_met,
            "requirements": qualification_status,
            "requirements_met": sum(1 for c in checks.values() if c),
            "total_requirements": len(checks),
        }

    def _check_all_categories_completed(
        self,
        completed: List[str],
        required: List[str],
    ) -> bool:
        """Check if all required categories have been completed"""
        return all(cat in completed for cat in required)

    def get_rank_info(
        self, path: str, total_points: int, user_stats: Dict = None
    ) -> dict:
        """Get current rank info based on total points."""
        ranks = PIRATE_RANKS if path == "pirate" else MARINE_RANKS

        base_rank_index = min(total_points // self.POINTS_PER_RANK, len(ranks) - 1)

        supreme_requirements = SUPREME_RANK_REQUIREMENTS[path]
        supreme_rank_index = len(ranks) - 1

        if total_points >= supreme_requirements["min_points"] and user_stats:
            qualified, qualification_details = self.check_supreme_rank_qualification(
                path, user_stats
            )

            if qualified:
                rank_index = supreme_rank_index
            else:
                rank_index = supreme_rank_index - 1
        else:
            rank_index = min(base_rank_index, supreme_rank_index - 1)
            qualified = False
            qualification_details = None

        current_rank = ranks[rank_index]

        points_in_rank = total_points % self.POINTS_PER_RANK
        points_to_next = self.POINTS_PER_RANK - points_in_rank

        next_rank = ranks[rank_index + 1] if rank_index < len(ranks) - 1 else None

        result = {
            "rank_index": rank_index,
            "rank_name": current_rank["name"],
            "rank_title": current_rank.get("bounty") or current_rank.get("title"),
            "points_in_rank": points_in_rank,
            "points_to_next": points_to_next,
            "next_rank": next_rank["name"] if next_rank else None,
            "is_max_rank": next_rank is None,
            "is_supreme_rank": current_rank.get("is_supreme", False),
        }

        if total_points >= supreme_requirements["min_points"] - 100:
            result["supreme_rank_progress"] = qualification_details

        return result

    def check_rank_up(
        self,
        path: str,
        old_points: int,
        new_points: int,
        user_stats: Dict = None,
    ) -> Tuple[bool, dict]:
        """Check if user ranked up"""
        old_rank_info = self.get_rank_info(path, old_points, user_stats)
        new_rank_info = self.get_rank_info(path, new_points, user_stats)

        if new_rank_info["rank_index"] > old_rank_info["rank_index"]:
            ranks = PIRATE_RANKS if path == "pirate" else MARINE_RANKS
            new_rank_data = ranks[new_rank_info["rank_index"]]

            return True, {
                "old_rank": old_rank_info["rank_name"],
                "new_rank": new_rank_data["name"],
                "is_supreme": new_rank_data.get("is_supreme", False),
                "celebration_quote": new_rank_data.get("quote", ""),
            }

        return False, {}
