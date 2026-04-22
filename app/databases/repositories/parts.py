from app.databases.postgres_asyncpg import asyncpg_db


async def get_parts_db(
        limit: int,
        last_id: str | None = None,
        last_name: str | None = None
) -> list:
    query = """
            SELECT p.id::text AS id_part,
                   p.name_part,
                   p.article_part
            FROM parts p
            WHERE ($1::text IS NULL AND $2::uuid IS NULL)
               OR (p.name_part > $1::text)
               OR (p.name_part = $1::text AND p.id > $2::uuid)
            ORDER BY p.name_part, p.id
            LIMIT $3;
            """
    rows = await asyncpg_db.fetch(query, last_name, last_id, limit)

    return [dict(row) for row in rows]


async def get_parts_search_db(
        limit: int,
        last_id: str | None = None,
        last_name: str | None = None,
        query: str = ...
):
    sql = """
          SELECT p.id::text AS id_part,
                 p.name_part,
                 p.article_part
          FROM parts p
          WHERE (
              $4::text IS NULL
                  OR p.name_part ILIKE '%' || $4 || '%'
                  OR p.article_part ILIKE '%' || $4 || '%'
              )
            AND (
              ($1::text IS NULL AND $2::uuid IS NULL)
                  OR (p.name_part > $1)
                  OR (p.name_part = $1 AND p.id > $2::uuid)
              )
          ORDER BY p.name_part, p.id
          LIMIT $3;
          """
    rows = await asyncpg_db.fetch(sql, last_name, last_id, limit, query)

    return [dict(row) for row in rows]
