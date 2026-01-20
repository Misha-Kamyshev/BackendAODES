from fastapi import APIRouter

from ..databases.repositories.catalog import get_catalog
from ..schemas.catalog import CategorySchema

router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/", response_model=list[CategorySchema])
async def catalog():
    return await get_catalog()
