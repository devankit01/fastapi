from pydantic import BaseModel
from typing import Optional
import uuid


class ProductSchema(BaseModel):
    name: str  # mandatory field
    price: int  # mandatory field
    stock: Optional[int] = 5  # default field
    sale: bool = False  # optional field
    image: Optional[str] = ""


class ProductReadSchema(ProductSchema):
    id: uuid.UUID

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[int]
    stock: Optional[int]
    sale: Optional[bool]
    image : Optional[str]
