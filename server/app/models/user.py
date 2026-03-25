from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProgressData(BaseModel):
    rank: int = 0
    points: int = 0
    total_points: int = 0
    problems_solved: int = 0
    current_streak: int = 0
    best_streak: int = 0
    wrong_submissions: int = 0
    first_try_successes: int = 0
    last_activity_date: Optional[datetime] = None


class UserPreferences(BaseModel):
    default_language: str = "python"
    timer_duration: int = 30  # minutes
    theme: str = "fighter"  # 'fighter' | 'sentinel' | 'auto'


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    email: str
    username: str
    avatar: Optional[str] = None
    provider: str  # 'google' | 'github'
    provider_id: str

    fighter_progress: ProgressData = ProgressData()
    sentinel_progress: ProgressData = ProgressData()

    preferences: UserPreferences = UserPreferences()
    achievements: List[str] = []

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
