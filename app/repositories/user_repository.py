from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalars().first()

async def create_user(db:AsyncSession,username: str, hashed_password: str):

    new_user = User(
        email=username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

