from datetime import date
from typing import Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    product_id: int
    product_name: str
    product_image: str
    product_price: Optional[int]
    old_product_price: Optional[int]
    product_discount_date: Optional[date]
    product_stock: bool
    product_special_price: bool
    category_name: str


class CategorySchema(BaseModel):
    id: int
    name: str
    description: str
    icon: str
