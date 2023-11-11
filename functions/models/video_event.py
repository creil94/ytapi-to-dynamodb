from pydantic import BaseModel, Field


class VideoEvent(BaseModel):
    video_id: str = Field(min_length=11, max_length=11)
