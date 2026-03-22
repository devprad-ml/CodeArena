"""
Background worker for code execution tasks.
Can be run with Celery or ARQ for async task processing.
"""

from app.services.submission_service import SubmissionService


async def process_submission_task(submission_id: str):
    """Process a code submission in the background"""
    service = SubmissionService()
    await service.process_submission(submission_id)
