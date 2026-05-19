from fastapi import APIRouter

from app.databases.repositories.product import get_detail_product_db
from app.schemas.product import ProductDetailSchema

router = APIRouter(prefix="/product", tags=["product"])

@router.get("/", response_model=ProductDetailSchema)
async def get_detail_product(product_id: int = ...):
    return await get_detail_product_db(product_id)
