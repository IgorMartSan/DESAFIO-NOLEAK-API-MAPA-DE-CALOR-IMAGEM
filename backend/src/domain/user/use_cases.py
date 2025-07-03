from sqlalchemy.orm import Session
from infra.db.models import User
from domain.user import  schemas
from utils.auth import AuthUtils
from datetime import timedelta


class UserUseCases:

    @staticmethod
    def create(db: Session, request_schema: schemas.UserCreateRequestSchema) -> schemas.UserCreateResponseSchema:
        hashed_password = AuthUtils.get_password_hash(request_schema.password)
        user = User(
            username=request_schema.username,
            email=request_schema.email,
            hashed_password=hashed_password,
            user_type=schemas.UserTypeEnum.USER
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return schemas.UserCreateResponseSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            user_type=user.user_type
        )

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email_or_username(db: Session, email_or_username: str):
        return db.query(User).filter(
            (User.email == email_or_username) | (User.username == email_or_username)
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def delete(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    

    @staticmethod
    def update(db: Session, user_id: int, update_data: schemas.UserUpdateRequestSchema):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise Exception("User not found")

        if update_data.username:
            user.username = update_data.username
        if update_data.email:
            user.email = update_data.email
        if update_data.password:
            user.hashed_password = AuthUtils.get_password_hash(update_data.password)
        if update_data.is_active is not None:
            user.is_active = update_data.is_active
        if update_data.user_type:
            user.user_type = update_data.user_type

        db.commit()
        db.refresh(user)

        return schemas.UserCreateResponseSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            user_type=user.user_type
        )



