from sqlalchemy import Column, Integer, String, ForeignKey, Table
from app.db.database import Base
from sqlalchemy.orm import relationship

# Junction table for Many-to-Many relationship
movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    movies = relationship("Movies", secondary=movie_genres, back_populates="genres")

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=True)
    year = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer, nullable=True)

    director_id = Column(Integer, ForeignKey("directors.id"), nullable=True)
    director = relationship("Director", back_populates="movies")
    
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")




class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    movies = relationship("Movies", back_populates="director")

