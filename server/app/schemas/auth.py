from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OAuthCallback(BaseModel):
    code: str
    state: str = ""
