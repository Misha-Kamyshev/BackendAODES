from fastapi import APIRouter

from app.databases.repositories.parts import get_parts_db
from app.schemas.parts import PartsRequestSchema, LastPartSchema

router = APIRouter(prefix="/parts", tags=["parts"])


@router.get("/", response_model=PartsRequestSchema)
async def get_parts(
        limit: int = 100,
        last_id: str = None,
        last_name: str = None
):
    result: list = await get_parts_db(limit=limit, last_id=last_id, last_name=last_name)
    last_item = LastPartSchema(id_part=str(result[-1]["id"]), name_part=result[-1]["name_part"])
    is_next_data = len(result) == limit

    return PartsRequestSchema(items=result, last_part=last_item, is_next_data=is_next_data)
