from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user_repository
from app.core.security import hash_password

async def register_user(db: AsyncSession, email: str, password: str):

    existing = await user_repository.get_user_by_email(db, email)

    if existing:
        raise ValueError("User already exists")

    hashed_password = hash_password(password)

    return await user_repository.create_user(db, email, hashed_password)
