from fastapi import Header
from fastapi import HTTPException

from app.config import Config


def verify_token(
    authorization: str = Header(...)
):

    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    if token != Config.API_TOKEN:

        raise HTTPException(
            status_code=401,
            detail="Invalid API Token"
        )