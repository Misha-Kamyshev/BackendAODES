from fastapi import APIRouter

from app.databases.repositories.parts import get_parts_db, get_parts_search_db
from app.schemas.parts import PartsRequestSchema

router = APIRouter(prefix="/parts", tags=["parts"])


@router.get("/", response_model=PartsRequestSchema)
async def get_parts(
        limit: int = 100,
        last_id: str = None,
        last_name: str = None
):
    result: list = await get_parts_db(limit=limit, last_id=last_id, last_name=last_name)
    last_part = None if not result else result[-1]
    is_next_data = len(result) == limit

    return PartsRequestSchema(items=result, last_part=last_part, is_next_data=is_next_data)


@router.get("/search/", response_model=PartsRequestSchema)
async def get_parts_search(
        limit: int = 100,
        last_id: str = None,
        last_name: str = None,
        query: str = ...
):
    result: list = await get_parts_search_db(limit=limit, last_id=last_id, last_name=last_name, query=query)
    last_part = None if not result else result[-1]
    is_next_data = len(result) == limit

    return PartsRequestSchema(items=result, last_part=last_part, is_next_data=is_next_data)
