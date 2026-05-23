from datetime import date
from typing import Optional, Any
from pydantic import BaseModel


class ProductDetailSchema(BaseModel):
    price: Optional[int]
    old_price: Optional[int]
    discount_date: Optional[date]
    stock: bool
    special_price: bool
    full_name: str
    engine_capacity: str
    engine_capacity_text: str
    number_seats: str
    number_seats_text: str
    warranty: str
    warranty_text: str
    description: dict
    characteristics: Optional[dict]
    path_photo_dimensions: Optional[str]
    photos: list[str]
    length: Optional[str]
    height: Optional[str]
    clearance: Optional[str]
    wheel_base: Optional[str]
    width: Optional[str]
    video_link: str
    link_documentation: Optional[list]
    colors: list[str]
    link_preview_images: list[str]
    video_preview_image: str
