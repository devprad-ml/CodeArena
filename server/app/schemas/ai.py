from pydantic import BaseModel
from typing import Optional, List


class HintRequest(BaseModel):
    problem_id: str
    hint_level: int = 1  # 1=subtle, 2=moderate, 3=strong
    path: str  # 'pirate' | 'marine'


class HintResponse(BaseModel):
    hint: str
    hint_level: int
    points_deducted: int = 5


class ExplainRequest(BaseModel):
    problem_id: str
    user_code: str
    language: str


class ExplainResponse(BaseModel):
    explanation: str
    optimal_approach: str
    time_complexity: str
    space_complexity: str


class EvaluateRequest(BaseModel):
    problem_id: str
    answer: str
    criteria: List[str] = []


class CriterionScore(BaseModel):
    criterion: str
    score: float
    feedback: str


class EvaluateResponse(BaseModel):
    overall_score: float
    feedback: str
    criteria_scores: List[CriterionScore] = []
