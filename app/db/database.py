
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres123@localhost:5432/movies"
)
engine = create_async_engine(DATABASE_URL,echo=True)

AsyncSessionLocal = sessionmaker (
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()