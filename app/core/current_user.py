from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from app.core.auth_dependency import oauth2_scheme
from app.core.jwt import SECRET_KEY, ALGORITHM, validate_jwt_settings


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:

    try:
        validate_jwt_settings()
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["user_id"]

    except (JWTError, KeyError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
