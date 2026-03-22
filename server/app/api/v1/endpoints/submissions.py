from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from app.schemas.submission import (
    SubmissionCreate,
    SubmissionResponse,
    RunCodeRequest,
    RunCodeResponse,
)
from app.services.submission_service import SubmissionService
from app.services.code_executor import CodeExecutor
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post("/", response_model=SubmissionResponse)
async def submit_code(
    submission: SubmissionCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """
    Submit code for evaluation.

    Scoring:
    - First correct: +25 points
    - Wrong submission: -5 points
    - Skip: -2 points
    """
    submission_service = SubmissionService()

    submission_record = await submission_service.create_submission(
        user_id=current_user.id,
        problem_id=submission.problem_id,
        code=submission.code,
        language=submission.language,
        path=submission.path,
    )

    background_tasks.add_task(
        submission_service.process_submission,
        submission_id=submission_record.id,
    )

    return submission_record


@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: str,
    current_user: User = Depends(get_current_user),
):
    """Get submission details and result"""
    submission_service = SubmissionService()
    submission = await submission_service.get_submission(submission_id)

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if submission.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return submission


@router.post("/run", response_model=RunCodeResponse)
async def run_code(
    request: RunCodeRequest,
    current_user: User = Depends(get_current_user),
):
    """Run code without submitting (no points affected)"""
    executor = CodeExecutor()
    result = await executor.execute(
        code=request.code,
        language=request.language,
        test_cases=request.test_cases,
    )
    return result


@router.get("/{submission_id}/status")
async def get_submission_status(
    submission_id: str,
    current_user: User = Depends(get_current_user),
):
    """Poll submission status"""
    submission_service = SubmissionService()
    submission = await submission_service.get_submission(submission_id)

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    return {"status": submission.status}
