from app.db.database import AsyncSessionLocal
from sqlalchemy.orm import Session

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session