from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from jose import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def validate_jwt_settings() -> None:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY must be set in the environment before starting the API")


def create_access_token(data: dict):
    validate_jwt_settings()

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
