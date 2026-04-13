from datetime import date
from typing import Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str
    image: str
    price: Optional[int]
    old_price: Optional[int]
    discount_date: Optional[date]
    stock: bool
    special_price: bool
    category_name: Optional[str]


class CategorySchema(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    products: Optional[list[ProductSchema]] = None
