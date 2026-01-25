from fastapi import APIRouter

from app.databases.repositories.videos import get_videos
from app.schemas.videos import VideoSchema

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.get("/", response_model=list[VideoSchema])
async def videos():
    return await get_videos()
