from pydantic import BaseModel, HttpUrl
from datetime import datetime


class BookmarkBase(BaseModel):
    original_url: HttpUrl


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkResponse(BookmarkBase):
    id: str
    short_code: str
    visit_count: int
    created_at: datetime
    user_id: str

    class Config:
        from_attributes = True
