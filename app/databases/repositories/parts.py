from app.databases.postgres_asyncpg import asyncpg_db


async def get_parts_db(
        limit: int,
        last_id: str | None = None,
        last_name: str | None = None
) -> list:
    query = """
            SELECT *
            FROM parts p
            WHERE ($1::text IS NULL AND $2::uuid IS NULL)
               OR (p.name_part > $1::text)
               OR (p.name_part = $1::text AND p.id > $2::uuid)
            ORDER BY p.name_part, p.id
            LIMIT $3;
            """
    rows = await asyncpg_db.fetch(query, last_name, last_id, limit)

    return [dict(row) for row in rows]
