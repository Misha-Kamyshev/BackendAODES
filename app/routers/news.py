from fastapi import APIRouter

from ..schemas.news import NewsSchema, NewsBlockSchema
from ..databases.repositories.news import get_news, get_news_block

router = APIRouter(prefix="/news", tags=["Catalog"])


@router.get("/", response_model=list[NewsSchema])
async def news():
    return await get_news()


@router.get("/{news_id}", response_model=list[NewsBlockSchema])
async def news_block(news_id: int):
    return await get_news_block(news_id)
