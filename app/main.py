from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routes.movies import router as movies_router
from app.db.database import engine,Base
from app.models.users import User
from app.models import movies
from app.routes import auth
from app.core.jwt import validate_jwt_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_jwt_settings()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Movies Storage", lifespan=lifespan)
app.include_router(movies_router)
app.include_router(auth.router)
