from sqlalchemy.orm import Session
from app.models.users import User

def get_user_by_email(db:Session,email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session,username: str, hashed_password: str):

    new_user = User(
        email=username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

