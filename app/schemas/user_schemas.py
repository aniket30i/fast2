from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)