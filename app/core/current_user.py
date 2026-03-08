from fastapi import Depends, HTTPException
from jose import jwt
from app.core.auth_dependency import oauth2_scheme
from app.core.jwt import SECRET_KEY, ALGORITHM


def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload["user_id"]

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )