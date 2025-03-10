from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import DeclarativeBase

from src.utils.helper import generate_uuid


class UserBase(DeclarativeBase):
    pass


class User(UserBase):
    __tablename__ = "users"

    id = Column(String(512), primary_key=True, default=generate_uuid)
    email = Column(String(100), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
