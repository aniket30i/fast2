from pydantic import BaseModel, ConfigDict
from typing import Optional

class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class MovieModel(StrictBaseModel):
    title:str
    year:int
    genres:list[str] = []

class MovieResponse(StrictBaseModel):
    id: int
    title:str
    year:int
    genres:list[str]
    owner_id: int

class MovieUpdateModel(StrictBaseModel):
    title:Optional[str]=None
    year:Optional[int]=None