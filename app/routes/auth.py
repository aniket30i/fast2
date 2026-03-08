from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.deps import get_db
from app.repositories import user_repository
from app.services import user_services
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.schemas.user_schemas import UserCreate, UserUpdate

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserUpdate)
def register(user: UserCreate, db: Session = Depends(get_db)):

    return user_services.register_user(
        db,
        user.email,
        user.password
    )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = user_repository.get_user_by_email(
        db,
        form_data.username
    )

    if not user:
        raise HTTPException(status_code=401)

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(status_code=401)

    token = create_access_token(
        {"user_id": user.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }