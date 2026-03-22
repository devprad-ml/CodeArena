from typing import Optional

from app.db.repositories.problem_repo import ProblemRepository
from app.db.repositories.user_repo import UserRepository
from app.models.problem import Problem
from app.services.rag_service import RAGService
from app.services.question_generator import QuestionGenerator
from app.utils.constants import DSA_CATEGORIES, SYSTEM_DESIGN_CATEGORIES, SCORING


class ProblemService:
    def __init__(self):
        self.problem_repo = ProblemRepository()
        self.user_repo = UserRepository()
        self.rag_service = RAGService()
        self.question_generator = QuestionGenerator()

    async def get_next_problem(self, user_id: str, path: str) -> Optional[Problem]:
        """
        Get next problem using hybrid approach:
        - Pirate (DSA): pick from curated database
        - Marine (System Design): generate via LLM, fall back to database
        """
        recommended_difficulty = await self.rag_service.get_recommended_difficulty(
            user_id, path
        )

        if path == "pirate":
            return await self._get_dsa_problem(user_id, recommended_difficulty)
        else:
            return await self._get_design_problem(
                user_id, recommended_difficulty
            )

    async def _get_dsa_problem(
        self, user_id: str, difficulty: str
    ) -> Optional[Problem]:
        """Pick a curated DSA problem from the database"""
        return await self.problem_repo.get_random_by_criteria(
            path="pirate",
            difficulty=difficulty,
            exclude_solved_by=user_id,
        )

    async def _get_design_problem(
        self, user_id: str, difficulty: str
    ) -> Optional[Problem]:
        """Generate a system design problem via LLM, fall back to database"""
        # Get user's weak areas for targeted generation
        weak_areas = await self.rag_service.get_weak_areas(user_id)

        # Try LLM generation first
        generated = await self.question_generator.generate_system_design_problem(
            difficulty=difficulty,
            weak_areas=weak_areas,
        )

        if generated:
            # Save to DB so we can reference it for submissions/scoring
            saved = await self.problem_repo.create(generated)
            return saved

        # Fall back to curated database if LLM fails
        return await self.problem_repo.get_random_by_criteria(
            path="marine",
            difficulty=difficulty,
            exclude_solved_by=user_id,
        )

    async def get_problem(self, problem_id: str) -> Optional[Problem]:
        """Get a specific problem by ID"""
        return await self.problem_repo.get_by_id(problem_id)

    async def get_random_problem(
        self,
        path: str,
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Optional[Problem]:
        """Get a random problem with optional filters"""
        if path == "marine" and category:
            # Try LLM generation for marine with specific category
            generated = await self.question_generator.generate_system_design_problem(
                difficulty=difficulty or "medium",
                category=category,
            )
            if generated:
                saved = await self.problem_repo.create(generated)
                return saved

        return await self.problem_repo.get_random_by_criteria(
            path=path,
            difficulty=difficulty,
            category=category,
        )

    async def get_categories(self, path: str) -> dict:
        """Get problem categories for a path"""
        if path == "pirate":
            return {"categories": DSA_CATEGORIES}
        return {"categories": SYSTEM_DESIGN_CATEGORIES}

    async def skip_problem(self, user_id: str, problem_id: str) -> dict:
        """Skip a problem and apply penalty"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return {"error": "User not found"}

        problem = await self.problem_repo.get_by_id(problem_id)
        if not problem:
            return {"error": "Problem not found"}

        path = problem.path
        progress_field = f"{path}_progress"
        progress = getattr(user, progress_field)

        new_points = max(0, progress.points + SCORING["skip_penalty"])

        await self.user_repo.update(
            user_id,
            {f"{progress_field}.points": new_points},
        )

        return {
            "message": "Problem skipped",
            "points_deducted": abs(SCORING["skip_penalty"]),
            "current_points": new_points,
        }
