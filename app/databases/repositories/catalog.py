from ..postgres_asyncpg import asyncpg_db


async def get_catalog():
    query = """
            SELECT c.id          AS category_id,
                   c.name        AS category_name,
                   c.description AS category_description,
                   c.icon        AS category_icon,

                   p.id          AS product_id,
                   p.name        AS product_name,
                   p.image       AS product_image,
                   p.price,
                   p.old_price,
                   p.discount_date,
                   p.stock,
                   p.special_price

            FROM catalog_categories c
                     LEFT JOIN products p ON p.category_id = c.id
            ORDER BY c.id, p.id
            """

    rows = await asyncpg_db.fetch(query)

    categories: dict[int, dict] = {}

    for row in rows:
        cat_id = row["category_id"]

        if cat_id not in categories:
            categories[cat_id] = {
                "id": cat_id,
                "name": row["category_name"],
                "description": row["category_description"],
                "icon": row["category_icon"],
                "products": [],
            }

        if row["product_id"] is not None:
            categories[cat_id]["products"].append(
                {
                    "id": row["product_id"],
                    "name": row["product_name"],
                    "image": row["product_image"],
                    "price": row["price"],
                    "old_price": row["old_price"],
                    "discount_date": row["discount_date"],
                    "stock": row["stock"],
                    "special_price": row["special_price"],
                    "category_name": row["category_name"],
                }
            )

    return list(categories.values())


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
