from app.repositories import movies_repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.movies import MovieUpdateModel


async def get_movies(db: AsyncSession, skip: int, limit: int, title: str | None, year: int | None,owner_id:int):
    return await movies_repository.get_all_movies(db, skip, limit, title, year,owner_id)

async def get_movies_by_genre(db:AsyncSession, genre:str, skip:int, limit:int, owner_id:int):
    return await movies_repository.get_movies_by_genre(db, genre, skip, limit, owner_id)

async def add_movies(db: AsyncSession, title, year,genres, user_id):
    if not title:
        raise ValueError("Movie title cannot be empty")
    if await movies_repository.exists(db,title):
        raise ValueError("Movie already exists")

    return await movies_repository.add_movie(db,title,year,genres,user_id)

async def update_movies(
    db: AsyncSession, movie_id: int, payload: MovieUpdateModel, owner_id: int
):
    movie = await movies_repository.get_by_id(db, movie_id, owner_id)

    if not movie:
        return None

    return await movies_repository.update_movie(db,payload,movie)

async def delete_movie(db: AsyncSession, movie_id: int, owner_id: int):
    return await movies_repository.delete_movie(db, movie_id, owner_id)

async def add_genre(db: AsyncSession, name: str):
    if not name:
        raise ValueError("Genre name cannot be empty")
    if await movies_repository.genre_exists(db, name):
        raise ValueError("Genre already exists")
    return await movies_repository.create_genre(db, name)

async def get_genres(db: AsyncSession):
    return await movies_repository.get_all_genres(db)

