from pydantic import BaseModel
from typing import Optional
import uuid


class UserSchema(BaseModel):
    first_name: str  # mandatory field
    last_name: str  # mandatory field
    email: str  # mandatory field
    password: str


class UserReadSchema(BaseModel):
    id: uuid.UUID
    first_name: str  # mandatory field
    last_name: str  # mandatory field
    email: str  # mandatory field
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    class Config:
        orm_mode = True


class UserSignInSchema(BaseModel):
    email: str  # mandatory field
    password: str  # mandatory field


class RefreshTokenSchema(BaseModel):
    refresh_token: str  # mandatory field
