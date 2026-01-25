from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    price: Optional[int]
    old_price: Optional[int]
    discount_date: Optional[date]
    stock: bool
    special_price: bool


class CategorySchema(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    products: Optional[List[ProductSchema]] = None
