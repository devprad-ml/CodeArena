import json
import random
from typing import Optional, List

import httpx

from app.config import settings
from app.models.problem import Problem, EvaluationCriterion
from app.utils.constants import SYSTEM_DESIGN_CATEGORIES


SYSTEM_DESIGN_GENERATION_PROMPT = """You are an expert system design interviewer creating questions for a coding platform.

Generate a {sub_category} system design question at **{difficulty}** difficulty level.

Category: {category} ({sub_category})
Difficulty: {difficulty}

Difficulty guidelines:
- easy: Basic concepts, straightforward design with few components
- medium: Multiple components, trade-offs to consider, moderate scale
- hard: Large-scale systems, complex trade-offs, performance considerations
- expert: Industry-grade problems, distributed systems, extreme scale

{weak_areas_context}

Return your response as valid JSON with this exact structure:
{{
    "title": "Short descriptive title",
    "slug": "kebab-case-slug",
    "description": "Full problem description in Markdown. Include:\\n- Context/scenario\\n- Functional requirements (what the system should do)\\n- Non-functional requirements (scale, latency, availability)\\n- Any constraints",
    "constraints": "Key constraints and assumptions",
    "hints": ["hint 1 (subtle)", "hint 2 (moderate)", "hint 3 (detailed approach)"],
    "evaluation_criteria": [
        {{"criterion": "criteria name", "weight": 0.25}},
        {{"criterion": "criteria name", "weight": 0.25}},
        {{"criterion": "criteria name", "weight": 0.25}},
        {{"criterion": "criteria name", "weight": 0.25}}
    ],
    "tags": ["relevant", "tags"],
    "companies": ["companies that ask similar questions"]
}}

Return ONLY the JSON, no other text."""


class QuestionGenerator:
    """LLM-powered question generator for System Design (Marine) path"""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.anthropic_key = settings.ANTHROPIC_API_KEY

    async def generate_system_design_problem(
        self,
        difficulty: str,
        category: Optional[str] = None,
        weak_areas: Optional[List[str]] = None,
    ) -> Optional[Problem]:
        """Generate a system design problem using LLM"""
        # Pick category and sub-category
        if category and category in SYSTEM_DESIGN_CATEGORIES:
            cat = category
        else:
            cat = random.choice(["lld", "hld"])

        sub_categories = SYSTEM_DESIGN_CATEGORIES[cat]
        sub_category = random.choice(sub_categories)

        weak_areas_context = ""
        if weak_areas:
            weak_areas_context = (
                f"The student is weak in: {', '.join(weak_areas)}. "
                "Try to incorporate these areas into the question to help them improve."
            )

        prompt = SYSTEM_DESIGN_GENERATION_PROMPT.format(
            category=cat.upper(),
            sub_category=sub_category,
            difficulty=difficulty,
            weak_areas_context=weak_areas_context,
        )

        raw_json = await self._call_llm(prompt)
        if not raw_json:
            return None

        return self._parse_to_problem(raw_json, difficulty, cat)

    async def _call_llm(self, prompt: str) -> Optional[dict]:
        """Call LLM API (tries Anthropic first, falls back to OpenAI)"""
        if self.anthropic_key:
            result = await self._call_anthropic(prompt)
            if result:
                return result

        if self.api_key:
            result = await self._call_openai(prompt)
            if result:
                return result

        return None

    async def _call_anthropic(self, prompt: str) -> Optional[dict]:
        """Call Anthropic Claude API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 2048,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                response.raise_for_status()
                data = response.json()
                text = data["content"][0]["text"]
                return json.loads(text)
        except (httpx.HTTPError, json.JSONDecodeError, KeyError):
            return None

    async def _call_openai(self, prompt: str) -> Optional[dict]:
        """Call OpenAI API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-4o",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.8,
                        "response_format": {"type": "json_object"},
                    },
                )
                response.raise_for_status()
                data = response.json()
                text = data["choices"][0]["message"]["content"]
                return json.loads(text)
        except (httpx.HTTPError, json.JSONDecodeError, KeyError):
            return None

    def _parse_to_problem(
        self, data: dict, difficulty: str, category: str
    ) -> Optional[Problem]:
        """Parse LLM JSON response into a Problem model"""
        try:
            evaluation_criteria = [
                EvaluationCriterion(
                    criterion=c["criterion"],
                    weight=c.get("weight", 0.25),
                )
                for c in data.get("evaluation_criteria", [])
            ]

            return Problem(
                title=data["title"],
                slug=data.get("slug", data["title"].lower().replace(" ", "-")),
                description=data["description"],
                difficulty=difficulty,
                path="marine",
                category=category,
                evaluation_criteria=evaluation_criteria,
                constraints=data.get("constraints", ""),
                hints=data.get("hints", []),
                tags=data.get("tags", []),
                companies=data.get("companies", []),
            )
        except (KeyError, TypeError):
            return None
