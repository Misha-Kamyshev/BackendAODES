from typing import Optional

from pydantic import BaseModel


class KeyValueRow(BaseModel):
    title: str
    description: str


class TableRow(BaseModel):
    items: list[str]


class Block(BaseModel):
    type: str
    title: Optional[str] = None
    items: Optional[list[str]] = None
    text: Optional[str] = None
    rows: Optional[list[KeyValueRow | TableRow]] = None
    header: Optional[list[str]] = None


class PolicyResponse(BaseModel):
    blocks: list[Block]
