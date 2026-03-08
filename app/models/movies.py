from sqlalchemy import Column, Integer,String,ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(100),unique=True,nullable=True)
    year = Column(Integer,nullable=True)
    owner_id = Column(Integer,ForeignKey("users.id"))

