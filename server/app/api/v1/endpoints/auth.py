from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.config import settings
from app.schemas.auth import TokenResponse, OAuthCallback
from app.services.auth_service import AuthService
from app.core.oauth import google_oauth, github_oauth
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/google")
async def google_login(request: Request):
    """Redirect to Google OAuth"""
    redirect_uri = f"{settings.API_URL}/api/v1/auth/google/callback"
    return await google_oauth.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    auth_service = AuthService()
    token = await auth_service.handle_google_callback(request)

    return RedirectResponse(
        url=f"{settings.CLIENT_URL}/auth/callback?token={token}"
    )


@router.get("/github")
async def github_login(request: Request):
    """Redirect to GitHub OAuth"""
    redirect_uri = f"{settings.API_URL}/api/v1/auth/github/callback"
    return await github_oauth.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def github_callback(request: Request):
    """Handle GitHub OAuth callback"""
    auth_service = AuthService()
    token = await auth_service.handle_github_callback(request)

    return RedirectResponse(
        url=f"{settings.CLIENT_URL}/auth/callback?token={token}"
    )


@router.get("/me")
async def get_current_user_info(current_user=Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user


@router.post("/logout")
async def logout():
    """Logout user (client should delete token)"""
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(current_user=Depends(get_current_user)):
    """Refresh JWT token"""
    auth_service = AuthService()
    token = auth_service.create_token(current_user.id)
    return TokenResponse(access_token=token, token_type="bearer")
