from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.current_user import get_current_user
from app.db.deps import get_db
from app.schemas.movies import MovieModel, MovieUpdateModel
from app.services import movies_services
from app.services.movies_services import add_movies

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/show_movies_list")
async def show_movies_list(
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await movies_services.get_movies(
        db,
        skip=skip,
        limit=limit,
        title=title,
        year=year,
        owner_id=current_user
    )

@router.get("/search_by_genre")
async def search_movies_by_genre(
        skip: int = 0,
        limit: int = 10,
        genre: Optional[str] = None,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user),
):
    return await movies_services.get_movies_by_genre(
        db,
        skip=skip,
        limit=limit,
        genre=genre,
        owner_id=current_user
    )

@router.post("/add_movie")
async def add_movie(
    movie: MovieModel,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return await add_movies(
            db,
            movie.title,
            movie.year,
            movie.genre,
            current_user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update_movie/{movie_id}")
async def movie_details_update(
    movie_id: int,
    payload: MovieUpdateModel,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    result = await movies_services.update_movies(db, movie_id, payload, current_user)

    if result is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return result


@router.delete("/delete_movie/{movie_id}")
async def delete_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    result = await movies_services.delete_movie(db, movie_id, current_user)

    if result is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return result


