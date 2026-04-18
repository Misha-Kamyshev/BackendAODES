from fastapi import APIRouter

from ..databases.repositories.catalog import get_catalog, get_promotion_catalog, get_categories, get_regular_products
from ..schemas.catalog import CategorySchema, ProductSchema

router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/", response_model=list[ProductSchema])
async def catalog(category_id: int = ...):
    return await get_catalog(category_id)


@router.get("/categories", response_model=list[CategorySchema])
async def catalog_categories():
    return await get_categories()


@router.get("/promotion/{count}", response_model=list[ProductSchema])
async def promotion(count: int):
    promo = await get_promotion_catalog(count)
    if len(promo) == count:
        return promo

    missing = count - len(promo)
    promo_ids = [promo["product_id"] for promo in promo]

    regular = await get_regular_products(missing, promo_ids)

    return promo + regular
