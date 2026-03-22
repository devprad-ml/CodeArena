from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

from app.models.problem import TestCase, EvaluationCriterion, ProblemMetadata


class ProblemResponse(BaseModel):
    id: Optional[str] = None
    title: str
    slug: str
    description: str
    difficulty: str
    path: str
    category: str
    test_cases: List[TestCase] = []
    evaluation_criteria: List[EvaluationCriterion] = []
    constraints: str = ""
    hints: List[str] = []
    starter_code: Dict[str, str] = {}
    tags: List[str] = []
    companies: List[str] = []
    metadata: ProblemMetadata = ProblemMetadata()


class ProblemCreate(BaseModel):
    title: str
    slug: str
    description: str
    difficulty: str
    path: str
    category: str
    test_cases: List[TestCase] = []
    evaluation_criteria: List[EvaluationCriterion] = []
    constraints: str = ""
    hints: List[str] = []
    solution: str = ""
    solution_code: Dict[str, str] = {}
    starter_code: Dict[str, str] = {}
    tags: List[str] = []
    companies: List[str] = []
