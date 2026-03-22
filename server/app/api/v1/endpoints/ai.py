from fastapi import APIRouter, Depends

from app.schemas.ai import HintRequest, HintResponse, ExplainRequest, ExplainResponse, EvaluateRequest, EvaluateResponse
from app.services.ai_judge import AIJudge
from app.services.rank_service import RankService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["AI Services"])


@router.post("/hint", response_model=HintResponse)
async def get_hint(
    request: HintRequest,
    current_user: User = Depends(get_current_user),
):
    """Get hint for a problem (-5 points)"""
    rank_service = RankService()
    await rank_service.apply_hint_penalty(current_user.id, request.path)

    ai_judge = AIJudge()
    hint = await ai_judge.generate_hint(
        problem_id=request.problem_id,
        hint_level=request.hint_level,
    )
    return hint


@router.post("/explain", response_model=ExplainResponse)
async def explain_solution(
    request: ExplainRequest,
    current_user: User = Depends(get_current_user),
):
    """Get solution explanation post-submission"""
    ai_judge = AIJudge()
    explanation = await ai_judge.explain_solution(
        problem_id=request.problem_id,
        user_code=request.user_code,
        language=request.language,
    )
    return explanation


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_design(
    request: EvaluateRequest,
    current_user: User = Depends(get_current_user),
):
    """Evaluate system design answer (Sentinel path)"""
    ai_judge = AIJudge()
    evaluation = await ai_judge.evaluate_system_design(
        problem_id=request.problem_id,
        answer=request.answer,
        criteria=request.criteria,
    )
    return evaluation
