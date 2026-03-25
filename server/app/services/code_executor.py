import httpx
from typing import List

from app.models.problem import TestCase
from app.models.submission import TestResult
from app.schemas.submission import RunCodeResponse
from app.core.exceptions import CodeExecutionError

PISTON_URL = "https://emkc.org/api/v2/piston/execute"

# Piston language slugs + pinned versions
LANGUAGE_MAP = {
    "python":     ("python",     "3.10.0"),
    "javascript": ("javascript", "18.15.0"),
    "java":       ("java",       "15.0.2"),
    "cpp":        ("c++",        "10.2.0"),
    "c":          ("c",          "10.2.0"),
    "go":         ("go",         "1.16.2"),
    "rust":       ("rust",       "1.50.0"),
}


class CodeExecutor:
    async def execute(
        self,
        code: str,
        language: str,
        test_cases: List[TestCase],
    ) -> RunCodeResponse:
        lang_entry = LANGUAGE_MAP.get(language)
        if not lang_entry:
            raise CodeExecutionError(f"Unsupported language: {language}")

        lang_slug, lang_version = lang_entry
        test_results = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            for i, test_case in enumerate(test_cases):
                result = await self._run_single_test(
                    client, code, lang_slug, lang_version, test_case, i
                )
                test_results.append(result)

        return RunCodeResponse(test_results=test_results)

    async def _run_single_test(
        self,
        client: httpx.AsyncClient,
        code: str,
        lang_slug: str,
        lang_version: str,
        test_case: TestCase,
        index: int,
    ) -> TestResult:
        payload = {
            "language": lang_slug,
            "version": lang_version,
            "files": [{"content": code}],
            "stdin": test_case.input,
        }

        try:
            response = await client.post(PISTON_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            run = data.get("run", {})
            actual_output = (run.get("stdout") or "").strip()
            stderr = (run.get("stderr") or "").strip()
            expected = test_case.expected_output.strip()

            # Non-zero exit or stderr with no stdout = runtime error
            if run.get("code", 0) != 0 and not actual_output:
                return TestResult(
                    test_case_id=index,
                    passed=False,
                    actual_output=stderr or "Runtime error",
                    expected_output=expected,
                    runtime=0,
                    memory=0,
                )

            return TestResult(
                test_case_id=index,
                passed=actual_output == expected,
                actual_output=actual_output,
                expected_output=expected,
                runtime=0,
                memory=0,
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
