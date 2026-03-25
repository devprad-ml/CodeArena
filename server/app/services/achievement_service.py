from typing import List

from app.models.user import User
from app.db.repositories.user_repo import UserRepository


class AchievementService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def check_and_award(
        self,
        user: User,
        path: str,
        submission_context: dict,
    ) -> List[str]:
        """
        Check which achievements the user just unlocked and award them.
        Returns list of newly awarded achievement IDs.
        """
        already_earned = set(user.achievements)
        newly_earned = []

        checks = self._get_checks(user, path, submission_context)
        for achievement_id, earned in checks.items():
            if earned and achievement_id not in already_earned:
                newly_earned.append(achievement_id)

        if newly_earned:
            await self.user_repo.add_achievements(user.id, newly_earned)

        return newly_earned

    def _get_checks(
        self, user: User, path: str, ctx: dict
    ) -> dict:
        fp = user.fighter_progress
        sp = user.sentinel_progress

        # ── Fighter achievements ──────────────────────────────────────────
        fighter_checks = {
            "first_blood": fp.problems_solved >= 1,
            "hat_trick": ctx.get("consecutive_correct", 0) >= 3,
            "speed_demon": (
                path == "fighter"
                and ctx.get("difficulty") == "hard"
                and ctx.get("solve_time_seconds", 9999) < 600
            ),
            "perfectionist": fp.first_try_successes >= 10,
            "grinder": fp.problems_solved >= 50,
            "graph_master": self._all_category_done(
                ctx.get("categories_solved", {}), "graphs"
            ),
            "dp_wizard": self._category_count(
                ctx.get("categories_solved", {}), "dynamic_programming"
            ) >= 10,
            "legend_born": fp.rank >= 6,  # index 6 = LEGEND
        }

        # ── Sentinel achievements ─────────────────────────────────────────
        sentinel_checks = {
            "architect": sp.problems_solved >= 1,
            "load_balancer": ctx.get("high_score_designs", 0) >= 5,
            "fault_tolerant": ctx.get("no_hint_sentinel_streak", 0) >= 5,
            "scalable": ctx.get("hld_solved", 0) >= 10,
            "oracle_born": sp.rank >= 5,  # index 5 = ORACLE
        }

        # ── General achievements ──────────────────────────────────────────
        best_streak = max(fp.best_streak, sp.best_streak)
        general_checks = {
            "streak_7": best_streak >= 7,
            "streak_30": best_streak >= 30,
            "dual_path": fp.points >= 100 and sp.points >= 100,
        }

        return {**fighter_checks, **sentinel_checks, **general_checks}

    @staticmethod
    def _all_category_done(categories_solved: dict, category: str) -> bool:
        """True if the user has solved at least one problem in the given category."""
        return categories_solved.get(category, 0) > 0

    @staticmethod
    def _category_count(categories_solved: dict, category: str) -> int:
        return categories_solved.get(category, 0)
