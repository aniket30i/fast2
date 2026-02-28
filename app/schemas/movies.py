from pydantic import BaseModel, ConfigDict
from typing import Optional

class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class MovieModel(StrictBaseModel):
    title:str
    year:int

class MovieUpdateModel(StrictBaseModel):
    title:Optional[str]=None
    year:Optional[int]=None