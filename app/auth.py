from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from app.config import Config

security = HTTPBearer(
    auto_error=False
)


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Vérifie le Bearer Token envoyé dans l'en-tête Authorization.

    Header attendu :

        Authorization: Bearer <API_TOKEN>
    """

    if credentials is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    token = credentials.credentials

    if token != Config.API_TOKEN:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return token