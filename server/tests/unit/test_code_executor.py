"""Unit tests for the CodeExecutor service"""


class TestCodeExecutor:
    def test_language_ids_mapping(self):
        from app.services.code_executor import CodeExecutor

        executor = CodeExecutor()
        assert executor.LANGUAGE_IDS["python"] == 71
        assert executor.LANGUAGE_IDS["javascript"] == 63
        assert executor.LANGUAGE_IDS["java"] == 62
        assert executor.LANGUAGE_IDS["cpp"] == 54
        assert executor.LANGUAGE_IDS["c"] == 50
        assert executor.LANGUAGE_IDS["go"] == 60
        assert executor.LANGUAGE_IDS["rust"] == 73

    def test_all_supported_languages(self):
        from app.services.code_executor import CodeExecutor

        executor = CodeExecutor()
        expected = {"python", "javascript", "java", "cpp", "c", "go", "rust"}
        assert set(executor.LANGUAGE_IDS.keys()) == expected
