import json
from typing import List, Optional

import httpx

from app.config import settings
from app.schemas.ai import HintResponse, ExplainResponse, EvaluateResponse, CriterionScore
from app.db.repositories.problem_repo import ProblemRepository
from app.utils.prompts import HINT_PROMPT_TEMPLATE, EVALUATION_PROMPT_TEMPLATE


EXPLANATION_PROMPT_TEMPLATE = """You are a coding tutor explaining a solution.

Problem: {problem_title}
Description: {problem_description}

Student's Code ({language}):
{user_code}

Return a JSON object with exactly these keys:
{{
    "explanation": "explanation of what the student's code does and its approach",
    "optimal_approach": "the optimal/recommended approach to solve this problem",
    "time_complexity": "time complexity of the optimal approach, e.g. O(n log n)",
    "space_complexity": "space complexity of the optimal approach, e.g. O(n)"
}}

Return ONLY the JSON, no other text."""


class AIJudge:
    """AI-powered code evaluation and hint generation (Claude → OpenAI fallback)"""

    def __init__(self):
        self.problem_repo = ProblemRepository()
        self.anthropic_key = settings.ANTHROPIC_API_KEY
        self.openai_key = settings.OPENAI_API_KEY

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def generate_hint(
        self,
        problem_id: str,
        hint_level: int = 1,
        user_code: str = "",
    ) -> HintResponse:
        """Generate a contextual hint for a problem."""
        problem = await self.problem_repo.get_by_id(problem_id)
        if not problem:
            return HintResponse(hint="Problem not found.", hint_level=hint_level, points_deducted=0)

        # Use pre-stored hints first (no LLM call needed)
        if problem.hints and hint_level <= len(problem.hints):
            return HintResponse(
                hint=problem.hints[hint_level - 1],
                hint_level=hint_level,
                points_deducted=abs(settings.HINT_PENALTY) if hasattr(settings, "HINT_PENALTY") else 3,
            )

        # Fall back to LLM-generated hint
        prompt = HINT_PROMPT_TEMPLATE.format(
            problem_title=problem.title,
            problem_description=problem.description,
            difficulty=problem.difficulty,
            hint_level=hint_level,
        )
        hint_text = await self._call_llm_text(prompt)

        return HintResponse(
            hint=hint_text or "Consider the problem constraints carefully and think about edge cases.",
            hint_level=hint_level,
            points_deducted=3,
        )

    async def explain_solution(
        self,
        problem_id: str,
        user_code: str,
        language: str,
    ) -> ExplainResponse:
        """Explain the submitted solution and provide the optimal approach."""
        problem = await self.problem_repo.get_by_id(problem_id)
        if not problem:
            return ExplainResponse(
                explanation="Problem not found.",
                optimal_approach="N/A",
                time_complexity="N/A",
                space_complexity="N/A",
            )

        prompt = EXPLANATION_PROMPT_TEMPLATE.format(
            problem_title=problem.title,
            problem_description=problem.description,
            language=language,
            user_code=user_code,
        )

        data = await self._call_llm_json(prompt)
        if data:
            return ExplainResponse(
                explanation=data.get("explanation", ""),
                optimal_approach=data.get("optimal_approach", ""),
                time_complexity=data.get("time_complexity", "N/A"),
                space_complexity=data.get("space_complexity", "N/A"),
            )

        # Graceful fallback — use stored solution if available
        return ExplainResponse(
            explanation=problem.solution if problem.solution else "Explanation unavailable.",
            optimal_approach="See the solution above.",
            time_complexity="N/A",
            space_complexity="N/A",
        )

    async def evaluate_system_design(
        self,
        problem_id: str,
        answer: str,
        criteria: List[str],
    ) -> EvaluateResponse:
        """Evaluate a Sentinel system design answer with AI scoring."""
        problem = await self.problem_repo.get_by_id(problem_id)
        if not problem:
            return self._empty_evaluation(criteria, "Problem not found.")

        if not criteria:
            criteria = [c.criterion for c in (problem.evaluation_criteria or [])]

        prompt = EVALUATION_PROMPT_TEMPLATE.format(
            problem_title=problem.title,
            problem_description=problem.description,
            criteria="\n".join(f"- {c}" for c in criteria),
            answer=answer,
        )

        data = await self._call_llm_json(prompt)
        if not data:
            return self._empty_evaluation(criteria, "AI evaluation unavailable. Please configure API keys.")

        criteria_scores = [
            CriterionScore(
                criterion=cs.get("criterion", ""),
                score=float(cs.get("score", 0.0)),
                feedback=cs.get("feedback", ""),
            )
            for cs in data.get("criteria_scores", [])
        ]

        # Fill in any missing criteria
        scored_names = {cs.criterion for cs in criteria_scores}
        for c in criteria:
            if c not in scored_names:
                criteria_scores.append(CriterionScore(criterion=c, score=0.0, feedback="Not evaluated."))

        return EvaluateResponse(
            overall_score=float(data.get("overall_score", 0.0)),
            feedback=data.get("feedback", ""),
            criteria_scores=criteria_scores,
        )

    # ------------------------------------------------------------------
    # LLM helpers
    # ------------------------------------------------------------------

    async def _call_llm_json(self, prompt: str) -> Optional[dict]:
        """Call LLM expecting a JSON response. Tries Anthropic, then OpenAI."""
        if self.anthropic_key:
            result = await self._anthropic_json(prompt)
            if result:
                return result
        if self.openai_key:
            result = await self._openai_json(prompt)
            if result:
                return result
        return None

    async def _call_llm_text(self, prompt: str) -> Optional[str]:
        """Call LLM expecting plain text. Tries Anthropic, then OpenAI."""
        if self.anthropic_key:
            result = await self._anthropic_text(prompt)
            if result:
                return result
        if self.openai_key:
            result = await self._openai_text(prompt)
            if result:
                return result
        return None

    async def _anthropic_json(self, prompt: str) -> Optional[dict]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-haiku-4-5-20251001",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                resp.raise_for_status()
                text = resp.json()["content"][0]["text"]
                # Strip markdown code fences if present
                text = text.strip()
                if text.startswith("```"):
                    text = text.split("```")[1]
                    if text.startswith("json"):
                        text = text[4:]
                return json.loads(text.strip())
        except Exception:
            return None

    async def _anthropic_text(self, prompt: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-haiku-4-5-20251001",
                        "max_tokens": 512,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                resp.raise_for_status()
                return resp.json()["content"][0]["text"].strip()
        except Exception:
            return None

    async def _openai_json(self, prompt: str) -> Optional[dict]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3,
                        "response_format": {"type": "json_object"},
                    },
                )
                resp.raise_for_status()
                text = resp.json()["choices"][0]["message"]["content"]
                return json.loads(text)
        except Exception:
            return None

    async def _openai_text(self, prompt: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.5,
                        "max_tokens": 512,
                    },
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _empty_evaluation(self, criteria: List[str], message: str) -> EvaluateResponse:
        return EvaluateResponse(
            overall_score=0.0,
            feedback=message,
            criteria_scores=[
                CriterionScore(criterion=c, score=0.0, feedback=message)
                for c in criteria
            ],
        )
