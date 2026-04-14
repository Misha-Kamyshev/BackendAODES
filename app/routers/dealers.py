from fastapi import APIRouter

from app.databases.repositories.dealers import get_dealers_list
from app.schemas.dealers import RegionSchema

router = APIRouter(prefix="/dealers", tags=["dealers"])

@router.get("/", response_model=list[RegionSchema])
async def get_dealers():
    return await get_dealers_list()
