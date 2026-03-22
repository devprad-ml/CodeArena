from datetime import datetime

from app.core.security import create_access_token
from app.core.oauth import google_oauth, github_oauth
from app.db.repositories.user_repo import UserRepository
from app.models.user import User


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def handle_google_callback(self, code: str) -> str:
        """Handle Google OAuth callback and return JWT token"""
        token = await google_oauth.authorize_access_token(code)
        user_info = token.get("userinfo")

        user = await self._get_or_create_user(
            email=user_info["email"],
            username=user_info.get("name", user_info["email"]),
            avatar=user_info.get("picture"),
            provider="google",
            provider_id=user_info["sub"],
        )

        return self.create_token(user.id)

    async def handle_github_callback(self, code: str) -> str:
        """Handle GitHub OAuth callback and return JWT token"""
        token = await github_oauth.authorize_access_token(code)
        user_info = token.get("userinfo")

        user = await self._get_or_create_user(
            email=user_info.get("email", ""),
            username=user_info.get("login", ""),
            avatar=user_info.get("avatar_url"),
            provider="github",
            provider_id=str(user_info["id"]),
        )

        return self.create_token(user.id)

    async def _get_or_create_user(
        self,
        email: str,
        username: str,
        avatar: str,
        provider: str,
        provider_id: str,
    ) -> User:
        """Get existing user or create a new one"""
        existing_user = await self.user_repo.get_by_provider(provider, provider_id)

        if existing_user:
            await self.user_repo.update(
                existing_user.id,
                {"last_login_at": datetime.utcnow(), "avatar": avatar},
            )
            return existing_user

        new_user = User(
            email=email,
            username=username,
            avatar=avatar,
            provider=provider,
            provider_id=provider_id,
        )

        return await self.user_repo.create(new_user)

    def create_token(self, user_id: str) -> str:
        """Create JWT access token for a user"""
        return create_access_token(data={"sub": user_id})
