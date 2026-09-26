from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.movies import Movies, Genre, Director
from app.schemas.movies import MovieUpdateModel


# ==================== MOVIE REPOSITORY ====================

async def get_all_movies(
    db: AsyncSession,
    skip: int,
    limit: int,
    title: str | None,
    year: int | None,
    owner_id: int
):
    query = select(Movies).where(Movies.owner_id == owner_id)

    if title:
        query = query.where(Movies.title.ilike(f"%{title}%"))

    if year:
        query = query.where(Movies.year == year)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

async def get_movies_by_genre(db: AsyncSession, genre: str, skip: int, limit: int, owner_id: int):
    existing = await genre_exists(db, genre)

    if not existing:
        raise ValueError("Genre does not exist")

    query = select(Movies).join(Movies.genres).where(Genre.name == genre, Movies.owner_id == owner_id)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

async def exists(db: AsyncSession, title: str) -> bool:
    result = await db.execute(
        select(Movies).where(Movies.title == title)
    )
    return result.scalars().first() is not None

async def get_by_id(db: AsyncSession, movie_id: int, owner_id: int):
    result = await db.execute(
        select(Movies).where(
            Movies.id == movie_id,
            Movies.owner_id == owner_id,
        )
    )
    return result.scalars().first()

async def add_movie(db: AsyncSession, title: str, year: int, genres: list[str], owner_id: int, director:str | None = None):
    movie = Movies(year=year, title=title, owner_id=owner_id)


    for genre_name in genres:
        result = await db.execute(select(Genre).where(Genre.name == genre_name))
        genre_obj = result.scalars().first()

        if genre_obj:
            movie.genres.append(genre_obj)
        else:
            new_genre = Genre(name=genre_name)
            db.add(new_genre)
            movie.genres.append(new_genre)


    if director:
        query = await db.execute(select(Director).where(Director.name == director))
        director_obj = query.scalars().first()

        if director_obj:
            movie.director = director_obj
        else:
            new_director = Director(name=director)
            db.add(new_director)
            movie.director = new_director

    db.add(movie)
    await db.commit()
    await db.refresh(movie)

    return movie

async def update_movie(db: AsyncSession, payload: MovieUpdateModel, movie: Movies):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(movie, key, value)

    await db.commit()
    await db.refresh(movie)

    return movie

async def delete_movie(db: AsyncSession, movie_id: int, owner_id: int):
    result = await db.execute(
        select(Movies).where(
            Movies.id == movie_id,
            Movies.owner_id == owner_id,
        )
    )
    movie = result.scalars().first()

    if not movie:
        return None

    await db.delete(movie)
    await db.commit()

    return movie


# ==================== GENRE REPOSITORY ====================

async def create_genre(db: AsyncSession, genre: str) -> Genre:
    genre_obj = Genre(name=genre)
    db.add(genre_obj)
    await db.commit()
    await db.refresh(genre_obj)
    return genre_obj

async def get_all_genres(db: AsyncSession):
    result = await db.execute(select(Genre))
    return result.scalars().all()

async def genre_exists(db: AsyncSession, name: str) -> bool:
    result = await db.execute(select(Genre).where(Genre.name == name))
    return result.scalars().first() is not None


# ==================== DIRECTOR REPOSITORY ====================

async def create_director(db: AsyncSession, name: str) -> Director:

   director_obj = Director(name=name)
   db.add(director_obj)
   await db.commit()
   await db.refresh(director_obj)
   return director_obj


async def get_all_directors(db: AsyncSession):
    result = await db.execute(select(Director))
    return result.scalars().all()

async def director_exists(db: AsyncSession, name: str) -> bool:
    result = await db.execute(select(Director).where(Director.name == name))
    return result.scalars().first() is not None
