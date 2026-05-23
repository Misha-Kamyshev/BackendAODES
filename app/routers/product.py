from fastapi import APIRouter

from app.databases.repositories.product import get_detail_product_db, get_other_product_db
from app.schemas.catalog import ProductSchema
from app.schemas.product import ProductDetailSchema

router = APIRouter(prefix="/product", tags=["product"])


@router.get("/", response_model=ProductDetailSchema)
async def get_detail_product(product_id: int = ...):
    return await get_detail_product_db(product_id)


@router.get("/other", response_model=list[ProductSchema])
async def get_other_product(product_id: int = ...):
    return await get_other_product_db(product_id)
