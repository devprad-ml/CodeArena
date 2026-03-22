from typing import List, Optional

from app.schemas.ai import HintResponse, ExplainResponse, EvaluateResponse, CriterionScore
from app.db.repositories.problem_repo import ProblemRepository


class AIJudge:
    """AI-powered code evaluation and hint generation"""

    def __init__(self):
        self.problem_repo = ProblemRepository()

    async def generate_hint(
        self,
        problem_id: str,
        hint_level: int = 1,
    ) -> HintResponse:
        """Generate a hint for a problem"""
        problem = await self.problem_repo.get_by_id(problem_id)
        if not problem:
            return HintResponse(hint="Problem not found", hint_level=hint_level)

        # Use pre-stored hints if available
        if problem.hints and hint_level <= len(problem.hints):
            return HintResponse(
                hint=problem.hints[hint_level - 1],
                hint_level=hint_level,
                points_deducted=5,
            )

        # TODO: Integrate with OpenAI/Claude for dynamic hint generation
        return HintResponse(
            hint="Think about the problem constraints and edge cases.",
            hint_level=hint_level,
            points_deducted=5,
        )

    async def explain_solution(
        self,
        problem_id: str,
        user_code: str,
        language: str,
    ) -> ExplainResponse:
        """Explain the solution to a problem"""
        problem = await self.problem_repo.get_by_id(problem_id)

        # TODO: Integrate with OpenAI/Claude for dynamic explanation
        return ExplainResponse(
            explanation=problem.solution if problem else "No explanation available.",
            optimal_approach="See the solution explanation above.",
            time_complexity="O(n)",
            space_complexity="O(1)",
        )

    async def evaluate_system_design(
        self,
        problem_id: str,
        answer: str,
        criteria: List[str],
    ) -> EvaluateResponse:
        """Evaluate a system design answer using AI"""
        # TODO: Integrate with OpenAI/Claude for AI evaluation
        criteria_scores = [
            CriterionScore(
                criterion=c,
                score=0.0,
                feedback="AI evaluation not yet configured.",
            )
            for c in criteria
        ]

        return EvaluateResponse(
            overall_score=0.0,
            feedback="AI evaluation service not yet configured. Please set up OpenAI or Claude API keys.",
            criteria_scores=criteria_scores,
        )
