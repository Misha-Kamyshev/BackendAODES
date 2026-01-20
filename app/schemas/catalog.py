from typing import List, Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    price: Optional[int]
    old_price: Optional[int]
    stock: bool
    special_price: bool


class CategorySchema(BaseModel):
    id: int
    slug: str
    name: str
    icon: Optional[str]
    products: List[ProductSchema]
