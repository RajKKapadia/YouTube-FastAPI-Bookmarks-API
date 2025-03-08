from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Index
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from src.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    original_url = Column(Text)
    short_code = Column(String(10), unique=True, index=True)
    visit_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(CHAR(36), ForeignKey("users.id"))

    user = relationship("User")

    __table_args__ = (
        Index('ix_bookmarks_original_url', original_url,
              mysql_prefix='', mysql_length=100),
    )
