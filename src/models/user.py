from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mysql import CHAR
import uuid
from src.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    email = Column(String(100), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
