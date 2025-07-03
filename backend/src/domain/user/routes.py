from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domain.user import schemas
from domain.user.use_cases import UserUseCases
from infra.db.database import get_db
from utils.auth import AuthUtils, oauth2_scheme


router = APIRouter(prefix="/users", tags=["Users"])


def get_current_user_data(token: str = Depends(oauth2_scheme)):
    return AuthUtils.get_current_data_from_token(token)


# 🚀 Create User
@router.post(
    "/",
    response_model=schemas.UserCreateResponseSchema,
    summary="Criar um novo usuário",
    description="Cria um novo usuário no sistema. Requer `username`, `email` e `password`. Retorna os dados do usuário criado."
)
def create_user(user: schemas.UserCreateRequestSchema, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no banco de dados.

    - Verifica se o username ou email já estão cadastrados.
    - Retorna o usuário criado caso tenha sucesso.
    """
    existing_user_username = UserUseCases.get_by_email_or_username(db, user.username) 
    if existing_user_username is not None:
        raise HTTPException(
            status_code=409,
            detail="Username already registered"
        )
    existing_user_email = UserUseCases.get_by_email_or_username(db, user.email) 
    if existing_user_email is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
    
    return UserUseCases.create(db, user)


# 🚀 Get All Users
@router.get(
    "/",
    response_model=list[schemas.UserCreateResponseSchema],
    summary="Listar todos os usuários",
    description="Retorna uma lista com todos os usuários cadastrados. Requer autenticação JWT."
)
def get_users(db: Session = Depends(get_db), token_data: dict = Depends(get_current_user_data)):
    """
    Lista todos os usuários cadastrados no sistema.

    Requer token de autenticação válido.
    """
    return UserUseCases.get_all(db)


# 🚀 Get User by ID
@router.get(
    "/{user_id}",
    response_model=schemas.UserCreateResponseSchema,
    summary="Obter usuário por ID",
    description="Retorna os dados de um usuário específico pelo seu ID. Requer autenticação JWT."
)
def get_user(user_id: int, db: Session = Depends(get_db), token_data: dict = Depends(get_current_user_data)):
    """
    Retorna um único usuário com base no ID fornecido.

    Se o usuário não existir, retorna erro 404.
    """
    user = UserUseCases.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 🚀 Update User
@router.put(
    "/{user_id}",
    response_model=schemas.UserCreateResponseSchema,
    summary="Atualizar um usuário",
    description="Atualiza os dados de um usuário existente com base no ID. Requer autenticação JWT."
)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdateRequestSchema,
    db: Session = Depends(get_db),
    token_data: dict = Depends(get_current_user_data)
):
    """
    Atualiza os dados de um usuário existente.

    Requer token de autenticação válido.
    """
    user = UserUseCases.update(db, user_id, user_update)
    return user


# 🚀 Delete User
@router.delete(
    "/{user_id}",
    summary="Deletar um usuário",
    description="Remove um usuário do sistema com base no ID fornecido. Requer autenticação JWT."
)
def delete_user(user_id: int, db: Session = Depends(get_db), token_data: dict = Depends(get_current_user_data)):
    """
    Deleta um usuário pelo seu ID.

    Se o usuário não for encontrado, retorna erro 404.
    """
    success = UserUseCases.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted successfully"}


