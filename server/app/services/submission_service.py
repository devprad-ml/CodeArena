from typing import Optional

from app.db.repositories.submission_repo import SubmissionRepository
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.problem_repo import ProblemRepository
from app.models.submission import Submission
from app.services.code_executor import CodeExecutor
from app.services.rank_service import RankService
from app.services.ai_judge import AIJudge


class SubmissionService:
    def __init__(self):
        self.submission_repo = SubmissionRepository()
        self.user_repo = UserRepository()
        self.problem_repo = ProblemRepository()
        self.code_executor = CodeExecutor()
        self.rank_service = RankService()
        self.ai_judge = AIJudge()

    async def create_submission(
        self,
        user_id: str,
        problem_id: str,
        code: str,
        language: str,
        path: str,
    ) -> Submission:
        """Create a new submission record"""
        attempt_number = await self.submission_repo.count_attempts(user_id, problem_id) + 1

        submission = Submission(
            user_id=user_id,
            problem_id=problem_id,
            path=path,
            code=code,
            language=language,
            status="pending",
            attempt_number=attempt_number,
        )

        return await self.submission_repo.create(submission)

    async def get_submission(self, submission_id: str) -> Optional[Submission]:
        """Get a submission by ID"""
        return await self.submission_repo.get_by_id(submission_id)

    async def process_submission(self, submission_id: str):
        """Process a submission: execute code, evaluate, update scores"""
        submission = await self.submission_repo.get_by_id(submission_id)
        if not submission:
            return

        # Update status to running
        await self.submission_repo.update(submission_id, {"status": "running"})

        problem = await self.problem_repo.get_by_id(submission.problem_id)
        if not problem:
            await self.submission_repo.update(submission_id, {"status": "error"})
            return

        if submission.path == "fighter":
            await self._process_dsa_submission(submission, problem)
        else:
            await self._process_design_submission(submission, problem)

    async def _process_dsa_submission(self, submission: Submission, problem):
        """Process DSA (fighter) submission with code execution"""
        try:
            results = await self.code_executor.execute(
                code=submission.code,
                language=submission.language,
                test_cases=problem.test_cases,
            )

            all_passed = all(r.passed for r in results.test_results)
            status = "accepted" if all_passed else "wrong"

            points = self.rank_service.calculate_submission_points(
                is_correct=all_passed,
                attempt_number=submission.attempt_number,
            )

            await self.submission_repo.update(
                submission.id,
                {
                    "status": status,
                    "test_results": [r.model_dump() for r in results.test_results],
                    "points_awarded": points,
                },
            )

            if all_passed:
                await self.rank_service.update_user_progress(
                    submission.user_id, submission.path, points, submission.attempt_number
                )

        except Exception:
            await self.submission_repo.update(submission.id, {"status": "error"})

    async def _process_design_submission(self, submission: Submission, problem):
        """Process system design (sentinel) submission with AI evaluation"""
        try:
            evaluation = await self.ai_judge.evaluate_system_design(
                problem_id=submission.problem_id,
                answer=submission.code,
                criteria=[c.criterion for c in problem.evaluation_criteria],
            )

            is_passing = evaluation.overall_score >= 0.6
            status = "accepted" if is_passing else "wrong"

            points = self.rank_service.calculate_submission_points(
                is_correct=is_passing,
                attempt_number=submission.attempt_number,
            )

            await self.submission_repo.update(
                submission.id,
                {
                    "status": status,
                    "ai_evaluation": {
                        "score": evaluation.overall_score,
                        "feedback": evaluation.feedback,
                        "criteria_scores": [
                            s.model_dump() for s in evaluation.criteria_scores
                        ],
                    },
                    "points_awarded": points,
                },
            )

            if is_passing:
                await self.rank_service.update_user_progress(
                    submission.user_id, submission.path, points, submission.attempt_number
                )

        except Exception:
            await self.submission_repo.update(submission.id, {"status": "error"})
