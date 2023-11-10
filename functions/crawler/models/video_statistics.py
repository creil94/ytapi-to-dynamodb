from pydantic import BaseModel, Field
from datetime import datetime


class VideoStatistics(BaseModel):
    video_id: str = Field(alias='videoId', min_length=11, max_length=11)
    comment_count: int = Field(alias='commentCount', ge=0)
    favorite_count: int = Field(alias='favoriteCount', ge=0)
    like_count: int = Field(alias='likeCount', ge=0)
    view_count: int = Field(alias='viewCount', ge=0)

    entity_type: str = 'Statistic'
    identifier: str = f"STATS#{str(datetime.now())}"
