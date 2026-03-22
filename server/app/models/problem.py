from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class TestCase(BaseModel):
    input: str
    expected_output: str
    is_hidden: bool = False


class EvaluationCriterion(BaseModel):
    criterion: str
    weight: float


class ProblemMetadata(BaseModel):
    time_limit: int = 10000  # ms
    memory_limit: int = 256  # MB
    success_rate: float = 0.0
    total_attempts: int = 0


class Problem(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    slug: str
    description: str  # Markdown
    difficulty: str  # 'easy' | 'medium' | 'hard' | 'expert'
    path: str  # 'fighter' | 'sentinel'
    category: str  # 'arrays', 'trees', 'lld', etc.

    # For DSA (Fighter)
    test_cases: List[TestCase] = []

    # For System Design (Sentinel)
    evaluation_criteria: List[EvaluationCriterion] = []

    constraints: str = ""
    hints: List[str] = []
    solution: str = ""  # Markdown explanation

    solution_code: Dict[str, str] = {}  # {language: code}
    starter_code: Dict[str, str] = {}  # {language: code}

    tags: List[str] = []
    companies: List[str] = []

    metadata: ProblemMetadata = ProblemMetadata()

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
