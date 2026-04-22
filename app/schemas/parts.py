from typing import Optional

from pydantic import BaseModel


class PartSchema(BaseModel):
    id_part: str
    name_part: str
    article_part: str


class LastPartSchema(BaseModel):
    id_part: str
    name_part: str


class PartsRequestSchema(BaseModel):
    items: list[PartSchema]
    last_part: Optional[LastPartSchema]
    is_next_data: bool
