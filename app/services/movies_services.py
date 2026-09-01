from app.repositories import movies_repository
from sqlalchemy.orm import Session
from app.schemas.movies import MovieUpdateModel


async def get_movies(db: Session, skip: int, limit: int, title: str | None, year: int | None,owner_id:int):
    return await movies_repository.get_all_movies(db, skip, limit, title, year,owner_id)

async def add_movies(db:Session,title,year,user_id):
    if not title:
        raise ValueError("Movie title cannot be empty")
    if await movies_repository.exists(db,title):
        raise ValueError("Movie already exists")

    return await movies_repository.add_movie(db,title,year,user_id)

async def update_movies(db:Session,movie_id:int,payload:MovieUpdateModel):
    movie=movies_repository.get_by_id(db,movie_id)

    if not movie:
        raise ValueError("Movie does not exist with the id")

    return await movies_repository.update_movie(db,payload,movie)

async def delete_movie(db:Session,movie_id:int):
    return await movies_repository.delete_movie(db,movie_id)

