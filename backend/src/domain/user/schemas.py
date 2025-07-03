from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class UserTypeEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    SUPERUSER = "superuser"


class UserCreateRequestSchema(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "sisat",
                "email": "sisat@example.com",
                "password": "automate123#"
            }
        }


class UserCreateResponseSchema(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    user_type: UserTypeEnum

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "sisat",
                "email": "sisat@example.com",
                "is_active": True,
                "user_type": "admin"
            }
        }


class UserAuthResponseSchema(BaseModel):
    user: UserCreateResponseSchema
    access_token: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "username": "sisat",
                    "email": "sisat@example.com",
                    "is_active": True,
                    "user_type": "admin"
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
            }
        }


class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "email": "sisat@example.com",
                "password": "automate123#"
            }
        }


class UserUpdateRequestSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    user_type: Optional[UserTypeEnum] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "novo_nome",
                "email": "novoemail@example.com",
                "password": "novaSenha123#",
                "is_active": True,
                "user_type": "admin"
            }
        }