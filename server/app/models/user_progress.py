from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class CategoryPerformance(BaseModel):
    solved: int = 0
    accuracy: float = 0.0


class RecentSubmission(BaseModel):
    problem_id: str
    difficulty: str
    result: str  # 'accepted' | 'wrong'
    timestamp: datetime


class UserProgress(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str

    category_performance: Dict[str, CategoryPerformance] = {}

    recent_submissions: List[RecentSubmission] = []  # Last 20

    weak_areas: List[str] = []
    strong_areas: List[str] = []

    recommended_difficulty: str = "easy"

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
