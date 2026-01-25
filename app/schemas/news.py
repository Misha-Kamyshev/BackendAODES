from datetime import date
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel

class BlockType(str, Enum):
    title = "title"
    paragraph = "paragraph"
    image = "image"
    list = "list"
    button = "button"
    link = "link"
    span = "span"
    warning_list = "warning_list"
    warning_text = "warning_text"
    disclaimer = "disclaimer"
    carousel = "carousel"
    tabel = "tabel"

class NewsSchema(BaseModel):
    id: int
    title: str
    preview_text: str
    preview_image: str
    published_at: date

class NewsBlockSchema(BaseModel):
    position: int
    type: BlockType
    data: dict[str, Any]
