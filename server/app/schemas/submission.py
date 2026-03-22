from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.models.submission import TestResult, AIEvaluation
from app.models.problem import TestCase


class SubmissionCreate(BaseModel):
    problem_id: str
    code: str
    language: str
    path: str  # 'fighter' | 'sentinel'


class SubmissionResponse(BaseModel):
    id: Optional[str] = None
    user_id: str
    problem_id: str
    path: str
    code: str
    language: str
    status: str
    test_results: List[TestResult] = []
    ai_evaluation: Optional[AIEvaluation] = None
    runtime: float = 0
    memory: float = 0
    points_awarded: int = 0
    attempt_number: int = 1
    submitted_at: datetime


class RunCodeRequest(BaseModel):
    code: str
    language: str
    test_cases: List[TestCase] = []


class RunCodeResponse(BaseModel):
    test_results: List[TestResult] = []
    compile_error: Optional[str] = None
    runtime_error: Optional[str] = None
