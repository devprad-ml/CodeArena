import httpx
from typing import List

from app.config import settings
from app.models.problem import TestCase
from app.models.submission import TestResult
from app.schemas.submission import RunCodeResponse
from app.core.exceptions import CodeExecutionError


class CodeExecutor:
    LANGUAGE_IDS = {
        "python": 71,      # Python 3.8.1
        "javascript": 63,  # Node.js 12.14.0
        "java": 62,        # Java 13.0.1
        "cpp": 54,         # C++ 17
        "c": 50,           # C (GCC 9.2.0)
        "go": 60,          # Go 1.13.5
        "rust": 73,        # Rust 1.40.0
    }

    def __init__(self):
        self.api_url = settings.JUDGE0_API_URL
        self.api_key = settings.JUDGE0_API_KEY

    async def execute(
        self,
        code: str,
        language: str,
        test_cases: List[TestCase],
    ) -> RunCodeResponse:
        """Execute code against test cases using Judge0"""
        language_id = self.LANGUAGE_IDS.get(language)
        if not language_id:
            raise CodeExecutionError(f"Unsupported language: {language}")

        test_results = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            for i, test_case in enumerate(test_cases):
                result = await self._run_single_test(
                    client, code, language_id, test_case, i
                )
                test_results.append(result)

        return RunCodeResponse(test_results=test_results)

    async def _run_single_test(
        self,
        client: httpx.AsyncClient,
        code: str,
        language_id: int,
        test_case: TestCase,
        index: int,
    ) -> TestResult:
        """Run a single test case"""
        payload = {
            "source_code": code,
            "language_id": language_id,
            "stdin": test_case.input,
            "expected_output": test_case.expected_output,
        }

        headers = {
            "X-RapidAPI-Key": self.api_key,
            "Content-Type": "application/json",
        }

        try:
            response = await client.post(
                f"{self.api_url}/submissions?wait=true",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

            actual_output = (data.get("stdout") or "").strip()
            expected = test_case.expected_output.strip()

            return TestResult(
                test_case_id=index,
                passed=actual_output == expected,
                actual_output=actual_output,
                expected_output=expected,
                runtime=float(data.get("time", 0)) * 1000,
                memory=float(data.get("memory", 0)) / 1024,
            )

        except httpx.HTTPError as e:
            return TestResult(
                test_case_id=index,
                passed=False,
                actual_output=f"Execution error: {str(e)}",
                expected_output=test_case.expected_output,
                runtime=0,
                memory=0,
            )
