from datetime import date
from typing import Optional

from pydantic import BaseModel


class NewsSchema(BaseModel):
    id: int
    title: str
    preview_text: str
    preview_image: str


class DataDetailTextSchema(BaseModel):
    type: str
    items: Optional[list[str]] = None
    text: Optional[str] = None
    url: Optional[str] = None
    preview_photo: Optional[str] = None
    link: Optional[str] = None
    text_link: Optional[str] = None


class NewsDetailSchema(BaseModel):
    title: str
    preview_image: str
    published_at: date
    data_detail_text: list[DataDetailTextSchema]
