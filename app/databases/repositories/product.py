import json
import re

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

    for field in ("description", "characteristics", "photos", "link_documentation"):
        value = product.get(field)

        if isinstance(value, str):
            product[field] = json.loads(value)

    return product


def _extract_product_lineage(name: str) -> tuple[str, str]:
    normalized_name = re.sub(r"\s+", " ", name.strip()).upper()
    tokens = normalized_name.split()

    if not tokens:
        return "", "BASE"

    if (
        len(tokens) >= 2
        and tokens[0] == "AODES"
        and re.fullmatch(r"UTV\d+(?:-\d+)?", tokens[1])
    ):
        family = f"{tokens[0]} {tokens[1]}"
    else:
        family = tokens[0]

    if re.search(r"\bMUD PRO\b", normalized_name):
        trim = "MUD PRO"
    elif re.search(r"\bPRO\b", normalized_name):
        trim = "PRO"
    else:
        trim = "BASE"

    return family, trim


def _get_related_sort_key(product_name: str) -> tuple[int, int, int, int, str]:
    normalized_name = product_name.upper()

    engine_match = re.search(r"\b(\d{3,4})[A-Z-]*\b", normalized_name)
    engine = int(engine_match.group(1)) if engine_match else 9999

    if re.search(r"\bS\b", normalized_name):
        body = 0
    elif re.search(r"\bL\b", normalized_name):
        body = 1
    elif re.search(r"\bSWT\b", normalized_name):
        body = 2
    elif re.search(r"\bWT\b", normalized_name):
        body = 3
    else:
        body = 9

    eps = 0 if re.search(r"\bEPS\b", normalized_name) else 1

    year_match = re.search(r"\b(20\d{2})\b", normalized_name)
    year = int(year_match.group(1)) if year_match else 9999

    return engine, body, eps, year, normalized_name


async def get_other_product_db(id_product: int):
    product_query = """
                    SELECT id,
                           name,
                           category_id
                    FROM products
                    WHERE id = $1
                    """

    current_product = await asyncpg_db.fetch_row(product_query, id_product)

    if current_product is None:
        return []

    current_family, current_trim = _extract_product_lineage(current_product["name"])

    query = """
            WITH product_colors AS (SELECT cp.id_product,

                                           array_agg(
                                                   cp.link_preview_image ORDER BY cp.id_color
                                           )
                                               FILTER (
                        WHERE cp.link_preview_image IS NOT NULL
                    ) AS link_preview_images,

                                           array_agg(
                                                   col.hex ORDER BY cp.id_color
                                           )
                                               FILTER (
                        WHERE col.hex IS NOT NULL
                    ) AS colors

                                    FROM colors_production cp

                                             LEFT JOIN colors col
                                                       ON col.id = cp.id_color

                                    GROUP BY cp.id_product)

            SELECT p.id            AS product_id,
                   p.name          AS product_name,
                   p.price         AS product_price,
                   p.old_price     AS old_product_price,
                   p.discount_date AS product_discount_date,
                   p.stock         AS product_stock,
                   p.special_price AS product_special_price,
                   c.name          AS category_name,

                   COALESCE(
                           pc.link_preview_images,
                           CASE
                               WHEN p.link_preview_image IS NOT NULL THEN ARRAY [p.link_preview_image]
                               ELSE '{}'
                               END
                   )               AS link_preview_images,

                   COALESCE(pc.colors, '{}') AS colors

            FROM products p

                     JOIN catalog_categories c
                          ON c.id = p.category_id

                     LEFT JOIN product_colors pc
                               ON pc.id_product = p.id

            WHERE p.category_id = $1
              AND p.id != $2
            """

    rows = await asyncpg_db.fetch(query, current_product["category_id"], id_product)

    products = []

    for row in rows:
        product = dict(row)
        family, trim = _extract_product_lineage(product["product_name"])

        if family != current_family or trim != current_trim:
            continue

        products.append(product)

    products.sort(key=lambda product: _get_related_sort_key(product["product_name"]))

    return products[:6]
