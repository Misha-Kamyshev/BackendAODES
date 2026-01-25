from app.databases.postgres_asyncpg import asyncpg_db


async def get_videos():
    query = """
    SELECT image, link 
    FROM videos
        ORDER BY id DESC
    """

    rows = await asyncpg_db.fetch(query)

    return [dict(row) for row in rows]
