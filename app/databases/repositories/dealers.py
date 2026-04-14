from app.databases.postgres_asyncpg import asyncpg_db


async def get_dealers_list() -> list:
    query = """
            SELECT dr.id     AS region_id,
                   dr.name   AS region_name,

                   d.id      AS dealer_id,
                   d.name    AS dealer_name,
                   d.phone   AS dealer_phone,
                   d.email   AS dealer_email,
                   d.address AS dealer_address,
                   d.link    AS dealer_link
            FROM dealers_region dr
                     LEFT JOIN dealers d ON d.region = dr.id
            ORDER BY dr.name
            """

    rows = await asyncpg_db.fetch(query)

    regions: dict[str, dict] = {}

    for row in rows:
        region_id = str(row["region_id"])

        if region_id not in regions:
            regions[region_id] = {
                "region_id": region_id,
                "region_name": row["region_name"],
                "dealers": []
            }

        if row["dealer_id"] is not None:
            regions[region_id]["dealers"].append({
                "dealer_id": str(row["dealer_id"]),
                "dealer_name": row["dealer_name"],
                "dealer_phone": row["dealer_phone"],
                "dealer_email": row["dealer_email"],
                "dealer_address": row["dealer_address"],
                "dealer_link": row["dealer_link"]
            })

    return list(regions.values())
