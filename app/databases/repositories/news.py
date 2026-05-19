import json

from ..postgres_asyncpg import asyncpg_db
from ...schemas.news import NewsDetailSchema


async def get_news():
    query = """
            SELECT id,
                   title,
                   preview_text,
                   preview_image
            FROM news
            ORDER BY published_at DESC;
            """

    rows = await asyncpg_db.fetch(query)

    return [dict(row) for row in rows]


async def get_news_count(count: int):
    query = """
            SELECT id,
                   title,
                   preview_text,
                   preview_image
            FROM news
            ORDER BY published_at DESC
            LIMIT $1;
            """

    rows = await asyncpg_db.fetch(query, count)

    return [dict(row) for row in rows]


async def get_news_block(news_id: int):
    query = """
            SELECT *
            FROM news
            WHERE id = $1;
            """

    rows = await asyncpg_db.fetch(query, news_id)

    blocks_news = []
    for row in rows:
        blocks_news.append(dict(row))

    for block in blocks_news:
        value = block.get("data_detail_text")

        if isinstance(value, str):
            block["data_detail_text"] = json.loads(value)

    return blocks_news


async def get_promotion_news():
    query = """
            SELECT id,
                   title,
                   preview_text,
                   preview_image
            FROM news
            WHERE promotion = TRUE
            ORDER BY published_at DESC;
            """

    rows = await asyncpg_db.fetch(query)

    return [dict(row) for row in rows]
