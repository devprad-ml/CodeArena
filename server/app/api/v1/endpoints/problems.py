from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.problem import ProblemResponse
from app.services.problem_service import ProblemService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.get("/next", response_model=ProblemResponse)
async def get_next_problem(
    path: str = Query(..., regex="^(fighter|sentinel)$"),
    current_user: User = Depends(get_current_user),
):
    """Get next problem (AI-adjusted difficulty)"""
    problem_service = ProblemService()
    return await problem_service.get_next_problem(current_user.id, path)


@router.get("/categories")
async def get_categories(
    path: str = Query(..., regex="^(fighter|sentinel)$"),
):
    """List problem categories"""
    problem_service = ProblemService()
    return await problem_service.get_categories(path)


@router.get("/random", response_model=ProblemResponse)
async def get_random_problem(
    path: str = Query(..., regex="^(fighter|sentinel)$"),
    difficulty: str = Query(None),
    category: str = Query(None),
    current_user: User = Depends(get_current_user),
):
    """Get random problem"""
    problem_service = ProblemService()
    return await problem_service.get_random_problem(path, difficulty, category)


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
    problem_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get specific problem"""
    problem_service = ProblemService()
    problem = await problem_service.get_problem(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.post("/{problem_id}/skip")
async def skip_problem(
    problem_id: str,
    current_user: User = Depends(get_current_user),
):
    """Skip problem (-2 points)"""
    problem_service = ProblemService()
    return await problem_service.skip_problem(current_user.id, problem_id)
