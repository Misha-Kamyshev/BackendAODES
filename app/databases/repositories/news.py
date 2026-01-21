import json

from ..postgres_asyncpg import asyncpg_db
from ...schemas.news import NewsBlockSchema


async def get_news():
    query = """
            SELECT *
            FROM news
            ORDER BY id;
            """

    rows = await asyncpg_db.fetch(query)

    return [dict(row) for row in rows]


async def get_news_block(news_id: int):
    query = """
            SELECT *
            FROM news_block
            WHERE news_id = $1
            ORDER BY position
            """

    rows = await asyncpg_db.fetch(query, news_id)

    result = []
    for row in rows:
        row_dict = dict(row)
        # Преобразуем поле data из строки JSON в словарь
        if isinstance(row_dict["data"], str):
            row_dict["data"] = json.loads(row_dict["data"])
        result.append(NewsBlockSchema(**row_dict))

    return result


async def get_promotion_news(count: int):
    query = """
            SELECT *
            FROM news
            WHERE promotion = TRUE
            ORDER BY published_at
            LIMIT $1
            """

    rows = await asyncpg_db.fetch(query, count)

    return [dict(row) for row in rows]
