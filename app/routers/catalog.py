from fastapi import APIRouter

from ..databases.repositories.catalog import get_catalog, get_promotion_catalog
from ..schemas.catalog import CategorySchema, ProductSchema

router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/", response_model=list[CategorySchema])
async def catalog():
    return await get_catalog()

@router.get("/promotion/{count}", response_model=list[ProductSchema])
async def promotion(count: int):
    return await get_promotion_catalog(count)