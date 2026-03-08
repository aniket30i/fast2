from fastapi import FastAPI
from app.routes.movies import router as movies_router
from app.db.database import engine,Base
from app.models.users import User
from app.models import movies
from app.routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movies Storage")
app.include_router(movies_router)
app.include_router(auth.router)