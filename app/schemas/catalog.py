from datetime import date
from typing import Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    product_id: int
    product_name: str
    product_price: Optional[int]
    old_product_price: Optional[int]
    product_discount_date: Optional[date]
    product_stock: bool
    product_special_price: bool
    product_link_preview_image: Optional[str]
    category_name: str
    link_preview_images: list[str]
    colors: list[str]


class CategorySchema(BaseModel):
    id: int
    name: str
    description: str
    icon: str
