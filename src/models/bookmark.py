import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Index
from sqlalchemy.dialects.mysql import CHAR, VARCHAR
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

from src.models.user import User
from src.utils.helper import generate_uuid


class BookmarkBase(DeclarativeBase):
    pass


class Bookmark(BookmarkBase):
    __tablename__ = "bookmarks"

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    original_url = Column(Text)
    short_code = Column(String(10), unique=True, index=True)
    visit_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(VARCHAR(512), ForeignKey(User.id))

    __table_args__ = (
        Index('ix_bookmarks_original_url', original_url,
              mysql_prefix='', mysql_length=100),
    )
