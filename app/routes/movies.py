from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.movies import MovieModel
from app.services.movies_services import add_movies
from app.services import movies_services
from app.schemas.movies import MovieUpdateModel


router = APIRouter(prefix="/movies",tags=["Movies"])

@router.get("/show_movies_list")
def show_movies_list(db:Session=Depends(get_db)):
    return movies_services.get_all_movies(db)

@router.post("/add_movie")
def add_movie(movie:MovieModel,db:Session=Depends(get_db)):
    try:
        return add_movies(db,movie.title,movie.year)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.put("/update_movie/{movie_id}")
def movie_details_update(movie_id:int,payload:MovieUpdateModel,db:Session=Depends(get_db),):
    return movies_services.update_movies(db,movie_id,payload)

@router.delete("/delete_movie/{movie_id}")
def delete_movie(movie_id, db:Session=Depends(get_db)):
    result = movies_services.delete_movie(db,movie_id)

    if result is None:
        raise HTTPException(status_code=404,detail="Movie not found")
    return result

