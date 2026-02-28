from sqlalchemy.orm import Session
from app.models.movies import Movies
from app.schemas.movies import MovieModel
from app.schemas.movies import MovieUpdateModel

def get_all_movies(db:Session):
    return db.query(Movies).all()

def exists(db:Session,title:str)->bool:
    return db.query(Movies).filter(Movies.title==title).first() is not None

def get_by_id(db:Session, movie_id:int):
    return db.query(Movies).filter(Movies.id == movie_id).first()


def add_movie(db:Session,title:str,year:int):
    movie = Movies(year=year,title=title)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

def update_movie(db:Session, payload:MovieUpdateModel,movie:Movies):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(movie,key,value)

    db.commit()
    db.refresh(movie)
    return movie

def delete_movie(db:Session,movie_id:int):
    movie = db.query(Movies).filter(Movies.id == movie_id).first()

    if not movie:
        return None

    db.delete(movie)
    db.commit()
    return movie





