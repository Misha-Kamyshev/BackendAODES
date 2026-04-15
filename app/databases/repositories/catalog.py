from ..postgres_asyncpg import asyncpg_db


async def get_catalog(category_id: int):
    query = """
            SELECT p.id            AS product_id,
                   p.name          AS product_name,
                   p.image         AS product_image,
                   p.price         AS product_price,
                   p.old_price     AS old_product_price,
                   p.discount_date AS product_discount_date,
                   p.stock         AS product_stock,
                   p.special_price AS product_special_price,
                   c.name          AS category_name
            FROM catalog_categories c
                     LEFT JOIN products p ON p.category_id = c.id
            WHERE c.id = $1
            ORDER BY c.id, p.id
            """

    rows = await asyncpg_db.fetch(query, category_id)

    return [dict(rows) for rows in rows]


async def get_categories():
    query = """
            SELECT *
            FROM catalog_categories;
            """

    rows = await asyncpg_db.fetch(query)

    return [dict(rows) for rows in rows]


async def get_promotion_catalog(count: int):
    query = """
            SELECT p.id,
                   p.name,
                   p.image,
                   p.price,
                   p.old_price,
                   p.discount_date,
                   p.stock,
                   p.special_price,
                   c.name as category_name
            FROM products p
                     LEFT JOIN catalog_categories c ON p.category_id = c.id
            WHERE (stock = TRUE OR special_price = TRUE)
              AND old_price IS NOT NULL
              AND discount_date >= CURRENT_DATE
            ORDER BY discount_date, id
                LIMIT $1;
            """

    rows = await asyncpg_db.fetch(query, count)

    return [dict(row) for row in rows]


async def get_regular_products(limit: int, exclude_ids: list[int]):
    query = """
            SELECT p.id,
                   p.name,
                   p.image,
                   p.price,
                   p.old_price,
                   p.discount_date,
                   p.stock,
                   p.special_price,
                   c.name AS category_name
            FROM products p
                     LEFT JOIN catalog_categories c ON p.category_id = c.id
            WHERE p.price IS NOT NULL
              AND p.id != ALL($1:: int [])
            ORDER BY id
                LIMIT $2;
            """

    rows = await asyncpg_db.fetch(query, exclude_ids, limit)

    return [dict(row) for row in rows]
