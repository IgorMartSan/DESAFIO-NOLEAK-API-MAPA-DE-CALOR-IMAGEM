from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from domain.user.schemas import UserTypeEnum
from domain.auth.use_cases import UseCases as AuthUserCases
from infra.db.database import get_db
from utils.auth import AuthUtils

router = APIRouter(prefix="/auth", tags=["Auth"])


# 🔑 Login - Gera Token
@router.post(
    "/token",
    summary="Login e geração de token",
    description="Autentica o usuário via `username` e `password` e retorna um token JWT válido."
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """
    Realiza autenticação do usuário com username/email e senha.

    Retorna um token JWT em caso de sucesso.
    """
    access_token = AuthUserCases.login(
        email_or_username=form_data.username,
        password=form_data.password,
        db_session=db
    )
    return access_token


# ✅ Rota Pública Teste
@router.get(
    "/test/public",
    summary="Rota pública de teste",
    description="Rota de teste acessível sem autenticação. Útil para verificar se a API está online."
)
def public_test():
    """
    Rota pública que retorna uma mensagem de teste.

    Não requer autenticação.
    """
    return {"message": "Rota pública funcionando ✅"}


# 🔒 Rota protegida - Qualquer usuário autenticado
@router.get(
    "/protected/general",
    summary="Rota protegida (usuários autenticados) (Teste)",
    description="Rota acessível a qualquer usuário autenticado com um token JWT válido."
)
def protected_general(
    current_data_from_token: dict = Depends(AuthUtils.get_current_data_from_token)):
    """
    Rota protegida que permite acesso a qualquer usuário autenticado.

    Requer token JWT válido.
    """
    return {"message": f"🔐 Acesso permitido. Bem-vindo {current_data_from_token['sub']}."}


# 🔒🔑 Rota protegida - ADMIN ou SUPERUSER
@router.get(
    "/protected/admin_or_superuser",
    summary="Rota protegida para Admin/Superuser (Teste)",
    description="Acesso restrito a usuários com papel `admin` ou `superuser`. Requer token JWT."
)
def admin_or_superuser(
    current_data_from_token: dict = Depends(AuthUtils.get_current_data_from_token)):
    """
    Rota protegida acessível apenas por usuários com papel:
    - admin
    - superuser

    Retorna erro 403 se o papel for diferente.
    """
    allowed_roles = ["superuser", "admin"]
    user_role = current_data_from_token.get("user_type")  
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este recurso.",
        )
    return {"message": f"🔐 Acesso permitido. Bem-vindo {current_data_from_token['sub']} (Admin/Superuser)."}

# 🔒👑 Rota protegida - SUPERUSER somente
@router.get(
    "/protected/superuser_only",
    summary="Rota protegida para Superuser (Teste)",
    description="Acesso exclusivo para usuários com papel `superuser`. Requer token JWT válido."
)
def superuser_only(current_data_from_token: dict = Depends(AuthUtils.get_current_data_from_token)):
    """
    Rota protegida acessível somente por usuários com papel `superuser`.

    Retorna erro 403 se outro tipo de usuário tentar acessar.
    """
    allowed_roles = ["superuser"]
    user_role = current_data_from_token.get("user_type")  
    
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"🚫 Acesso negado. Esta rota é restrita aos seguintes papéis: "
                f"{', '.join(allowed_roles)}. "
                f"Seu papel atual é: '{user_role}'."
            )
        )

    return {
        "message": (
            f"🔐 Acesso permitido. Bem-vindo, {current_data_from_token['sub']} "
            f"(papel: {user_role})."
        )
    }
