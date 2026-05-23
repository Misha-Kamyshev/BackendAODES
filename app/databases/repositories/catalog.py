from ..postgres_asyncpg import asyncpg_db

PRODUCT_BASE_SELECT = """
    p.id                 AS product_id,
    p.name               AS product_name,
    p.price              AS product_price,
    p.old_price          AS old_product_price,
    p.discount_date      AS product_discount_date,
    p.stock              AS product_stock,
    p.special_price      AS product_special_price,
    p.link_preview_image AS product_link_preview_image,
    c.name               AS category_name,

    COALESCE(pc.link_preview_images, '{}') AS link_preview_images,
    COALESCE(pc.colors, '{}') AS colors
"""

PRODUCT_COLOR_CTE = """
                    WITH product_colors AS (SELECT cp.id_product,

                                                   array_agg(
                                                           cp.link_preview_image ORDER BY cp.id_color
                                                   )
                                                       FILTER (
                WHERE cp.link_preview_image IS NOT NULL
            ) AS link_preview_images, array_agg(
                                col.hex ORDER BY cp.id_color
                                      )
                            FILTER (
                WHERE col.hex IS NOT NULL
            ) AS colors

                                            FROM colors_production cp

                                                     LEFT JOIN colors col
                                                               ON col.id = cp.id_color

                                            GROUP BY cp.id_product)
                    """


async def get_catalog(category_id: int):
    query = f"""
        {PRODUCT_COLOR_CTE}

        SELECT 
            {PRODUCT_BASE_SELECT}

        FROM products p

        JOIN catalog_categories c
            ON c.id = p.category_id

        LEFT JOIN product_colors pc
            ON pc.id_product = p.id

        WHERE c.id = $1

        ORDER BY p.id
    """

    rows = await asyncpg_db.fetch(query, category_id)

    return [dict(row) for row in rows]


async def get_categories():
    query = """
            SELECT *
            FROM catalog_categories
            ORDER BY id
            """

    rows = await asyncpg_db.fetch(query)

    return [dict(row) for row in rows]


async def get_promotion_catalog(count: int):
    query = f"""
        {PRODUCT_COLOR_CTE}

        SELECT 
            {PRODUCT_BASE_SELECT}

        FROM products p

        LEFT JOIN catalog_categories c
            ON p.category_id = c.id

        LEFT JOIN product_colors pc
            ON pc.id_product = p.id

        WHERE 
            (p.stock = TRUE OR p.special_price = TRUE)
            AND p.old_price IS NOT NULL
            AND p.discount_date >= CURRENT_DATE

        ORDER BY 
            p.discount_date,
            p.id

        LIMIT $1
    """

    rows = await asyncpg_db.fetch(query, count)

    return [dict(row) for row in rows]


async def get_regular_products(limit: int, exclude_ids: list[int]):
    query = f"""
        {PRODUCT_COLOR_CTE}

        SELECT 
            {PRODUCT_BASE_SELECT}

        FROM products p

        LEFT JOIN catalog_categories c
            ON p.category_id = c.id

        LEFT JOIN product_colors pc
            ON pc.id_product = p.id

        WHERE 
            p.price IS NOT NULL
            AND p.id != ALL($1::int[])

        ORDER BY p.id

        LIMIT $2
    """

    rows = await asyncpg_db.fetch(query, exclude_ids, limit)

    return [dict(row) for row in rows]
