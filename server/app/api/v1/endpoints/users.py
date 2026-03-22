from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import UserResponse, UserUpdate, UserPreferencesUpdate, UserStatsResponse
from app.services.user_service import UserService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get user profile"""
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update user profile"""
    user_service = UserService()
    updated_user = await user_service.update_user(current_user.id, update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.get("/stats", response_model=UserStatsResponse)
async def get_stats(current_user: User = Depends(get_current_user)):
    """Get user statistics"""
    user_service = UserService()
    return await user_service.get_user_stats(current_user.id)


@router.get("/submissions")
async def get_submissions(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
):
    """Get submission history"""
    user_service = UserService()
    return await user_service.get_submission_history(current_user.id, skip, limit)


@router.get("/achievements")
async def get_achievements(current_user: User = Depends(get_current_user)):
    """Get achievements"""
    user_service = UserService()
    return await user_service.get_achievements(current_user.id)


@router.put("/preferences")
async def update_preferences(
    preferences: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update user preferences"""
    user_service = UserService()
    return await user_service.update_preferences(current_user.id, preferences)
