from ..postgres_asyncpg import asyncpg_db


async def get_catalog():
    query = """
            SELECT c.id    AS category_id,
                   c.slug  AS category_slug,
                   c.name  AS category_name,
                   c.icon  AS category_icon,

                   p.id    AS product_id,
                   p.name  AS product_name,
                   p.image AS product_image,
                   p.price,
                   p.old_price,
                   p.stock,
                   p.special_price

            FROM catalog_categories c
                     LEFT JOIN products p ON p.category_id = c.id
            ORDER BY c.id, p.id \
            """

    rows = await asyncpg_db.fetch(query)

    categories: dict[int, dict] = {}

    for row in rows:
        cat_id = row["category_id"]

        if cat_id not in categories:
            categories[cat_id] = {
                "id": cat_id,
                "slug": row["category_slug"],
                "name": row["category_name"],
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
                    "stock": row["stock"],
                    "special_price": row["special_price"],
                }
            )

    return list(categories.values())


async def get_promotion_catalog(count: int):
    query = """
            SELECT id,
                   name,
                   image,
                   price,
                   old_price,
                   discount_date,
                   stock,
                   special_price
            FROM products
            WHERE (stock = TRUE OR special_price = TRUE)
              AND old_price IS NOT NULL
              AND discount_date >= CURRENT_DATE
                ORDER BY discount_date, id
                LIMIT $1;
            """

    rows = await asyncpg_db.fetch(query, count)

    return [dict(row) for row in rows]
