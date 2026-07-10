from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import Config

security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    if token != Config.API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Token"
        )

    return token