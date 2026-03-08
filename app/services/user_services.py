from sqlalchemy.orm import Session
from app.repositories import user_repository
from app.core.security import hash_password

def register_user(db:Session, email:str , password:str):

    existing = user_repository.get_user_by_email(db,email)

    if existing:
        raise ValueError("User already exists")

    hashed_password = hash_password(password)

    return user_repository.create_user(db,email,hashed_password)