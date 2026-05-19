import json
from ..postgres_asyncpg import asyncpg_db


async def get_detail_product_db(id_product: int):
    query = """
            SELECT p.price,
                   p.old_price,
                   p.discount_date,
                   p.stock,
                   p.special_price,
                   pc.*,
                   COALESCE(product_colors.colors, '{}')              AS colors,
                   COALESCE(product_colors.link_preview_images, '{}') AS link_preview_images

            FROM products p
                     JOIN product_characteristics pc
                          ON pc.id_product = p.id
                     LEFT JOIN (SELECT cp.id_product,
                                       array_agg(col.hex ORDER BY cp.id_color)
                                       FILTER (WHERE col.hex IS NOT NULL)               AS colors,
                                       array_agg(cp.link_preview_image ORDER BY cp.id_color)
                                       FILTER (WHERE cp.link_preview_image IS NOT NULL) AS link_preview_images
                                FROM colors_production cp
                                         LEFT JOIN colors col
                                                   ON col.id = cp.id_color
                                GROUP BY cp.id_product) AS product_colors
                               ON product_colors.id_product = p.id

            WHERE p.id = $1
            """

    row = await asyncpg_db.fetch_row(query, id_product)

    if row is None:
        return None

    product = dict(row)

    for field in ("description", "characteristics", "photos"):
        value = product.get(field)

        if isinstance(value, str):
            product[field] = json.loads(value)

    return product
