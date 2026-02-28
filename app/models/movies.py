from sqlalchemy import Column, Integer,String
from app.db.database import Base

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(100),unique=True,nullable=True)
    year = Column(String(100),unique=True,nullable=True)