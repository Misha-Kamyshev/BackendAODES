from fastapi import APIRouter

from ..schemas.news import NewsSchema, NewsBlockSchema
from ..databases.repositories.news import get_news, get_news_block, get_promotion_news, get_news_count

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/", response_model=list[NewsSchema])
async def news():
    return await get_news()

@router.get("/latest/{count}", response_model=list[NewsSchema])
async def news_latest(count: int):
    return await get_news_count(count)

@router.get("/block{news_id}", response_model=list[NewsBlockSchema])
async def news_block(news_id: int):
    return await get_news_block(news_id)


@router.get("/promotion/{count}", response_model=list[NewsSchema])
async def news_promotion(count: int):
    return await get_promotion_news(count)
