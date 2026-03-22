from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, problems, submissions, ai

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(problems.router)
api_router.include_router(submissions.router)
api_router.include_router(ai.router)
