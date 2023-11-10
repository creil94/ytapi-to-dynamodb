from pydantic import BaseModel, Field


class VideoEvent(BaseModel):
    video_id: str = Field(alias='VideoId', min_length=11, max_length=11)
