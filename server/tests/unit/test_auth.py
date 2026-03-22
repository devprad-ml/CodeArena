"""Unit tests for auth/security utilities"""

from app.core.security import create_access_token, decode_token


class TestSecurity:
    def test_create_and_decode_token(self):
        data = {"sub": "test_user_id"}
        token = create_access_token(data)
        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test_user_id"

    def test_invalid_token(self):
        decoded = decode_token("invalid.token.here")
        assert decoded is None
