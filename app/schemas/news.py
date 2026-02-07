from datetime import date
from enum import Enum
from typing import Union, List
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


class BaseBlockData(BaseModel):
    pass


class TitleBlockData(BaseBlockData):
    text: str
    level: int


class ParagraphBlockData(BaseBlockData):
    text: str


class ImageBlockData(BaseBlockData):
    url: str


class ListBlockData(BaseBlockData):
    items: List[str]


class CarouselBlockData(BaseBlockData):
    images: List[str]


class NewsBlockSchema(BaseModel):
    position: int
    type: BlockType
    data: Union[
        TitleBlockData,
        ParagraphBlockData,
        ImageBlockData,
        ListBlockData,
        CarouselBlockData,
    ]
