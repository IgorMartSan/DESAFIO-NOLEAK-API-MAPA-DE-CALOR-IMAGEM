from sqlalchemy.orm import Session
from sqlalchemy import or_
from infra.db.models import User,UserTypeEnum
from fastapi import HTTPException
from utils.auth import AuthUtils  # Certifique-se de importar a classe AuthUtils

class UseCases:
    
    @staticmethod
    def login(email_or_username, password, db_session: Session):
        user = db_session.query(User).filter(or_(User.email == email_or_username, User.username == email_or_username)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User/Email not found")
        print(type(user.is_active), user.is_active)

        if not user.is_active:
            print("Entrou no if")
            raise HTTPException(status_code=401, detail="User account is not active. Please contact an administrator for approval.")

        if not AuthUtils.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        access_token = AuthUtils.create_access_token(data={"sub": user.username, "user_type": user.user_type})
        return {"access_token": access_token, "token_type": "bearer"}