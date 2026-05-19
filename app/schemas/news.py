from datetime import date
from pydantic import BaseModel


class NewsSchema(BaseModel):
    id: int
    title: str
    preview_text: str
    preview_image: str


class NewsDetailSchema(BaseModel):
    title: str
    preview_image: str
    published_at: date
    data_detail_text: dict
