from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.models.user import ProgressData, UserPreferences


class UserResponse(BaseModel):
    id: Optional[str] = None
    email: str
    username: str
    avatar: Optional[str] = None
    provider: str
    fighter_progress: ProgressData
    sentinel_progress: ProgressData
    preferences: UserPreferences
    achievements: List[str] = []
    created_at: datetime
    last_login_at: datetime


class UserUpdate(BaseModel):
    username: Optional[str] = None
    avatar: Optional[str] = None


class UserPreferencesUpdate(BaseModel):
    default_language: Optional[str] = None
    timer_duration: Optional[int] = None
    theme: Optional[str] = None


class UserStatsResponse(BaseModel):
    total_problems_solved: int = 0
    fighter_progress: ProgressData
    sentinel_progress: ProgressData
    current_streak: int = 0
    best_streak: int = 0
    total_time_spent: float = 0  # hours
    achievements_count: int = 0
