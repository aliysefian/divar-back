from typing import List, Optional

from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
import typing

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Posts(BaseModel):
    token: str
    id: int
    business_type: str
    price:  Optional[str] 
    brand_model:  Optional[str] 
    city:  Optional[str] 
    token: str
    Local_modified: datetime
    web_images:  Optional[str] 

    category:  Optional[str] 
    title:  Optional[str] 
    district:  Optional[str] 
    url: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
