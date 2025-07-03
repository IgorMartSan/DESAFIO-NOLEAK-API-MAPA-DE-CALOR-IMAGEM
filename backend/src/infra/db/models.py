from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func, Boolean, JSON, ARRAY, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAlchemyEnum
from enum import Enum
from infra.db.database import Base

class UserTypeEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    SUPERUSER = "superuser"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, comment="Username")
    email = Column(String, nullable=False, unique=True, comment="User email for login")
    hashed_password = Column(String, nullable=False, comment="Hashed password")
    is_active = Column(Boolean, default=False, comment="Indicates if the user account is active")
    user_type = Column(SQLAlchemyEnum(UserTypeEnum), nullable=False, comment="Type of user")  # Usando Enum corretamente!
    created_at = Column(DateTime, default=func.now(), comment="Account creation date")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="Last update timestamp")


