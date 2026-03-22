from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TestResult(BaseModel):
    test_case_id: int
    passed: bool
    actual_output: str
    expected_output: str
    runtime: float  # ms
    memory: float  # MB


class CriteriaScore(BaseModel):
    criterion: str
    score: float
    feedback: str


class AIEvaluation(BaseModel):
    score: float
    feedback: str
    criteria_scores: List[CriteriaScore] = []


class Submission(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    problem_id: str
    path: str  # 'fighter' | 'sentinel'

    code: str
    language: str

    status: str  # 'pending' | 'running' | 'accepted' | 'wrong' | 'error' | 'timeout'

    test_results: List[TestResult] = []
    ai_evaluation: Optional[AIEvaluation] = None

    runtime: float = 0  # Average runtime in ms
    memory: float = 0  # Average memory in MB

    points_awarded: int = 0
    attempt_number: int = 1

    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
