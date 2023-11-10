from pydantic import BaseModel, Field


class VideoStatistics(BaseModel):
    comment_count: int = Field(alias='commentCount', ge=0)
    favorite_count: int = Field(alias='favoriteCount', ge=0)
    like_count: int = Field(alias='likeCount', ge=0)
    view_count: int = Field(alias='viewCount', ge=0)
