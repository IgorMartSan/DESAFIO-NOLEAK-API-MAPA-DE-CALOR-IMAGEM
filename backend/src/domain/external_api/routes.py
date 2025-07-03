from fastapi import APIRouter, HTTPException, Query, Depends, status
from utils.auth import AuthUtils
from typing import List, Dict
from domain.external_api.use_cases import UseCases

router = APIRouter(prefix="/embrapa", tags=["Embrapa"])

@router.get(
    "/producao",
    response_model=List[Dict],
    summary="Obter dados de produção",
    description="Retorna os dados de produção da uva coletados do site da Embrapa. Acesso permitido para usuários autenticados com papéis 'admin', 'superuser' ou 'user'."
)
def get_producao(current_user_token: dict = Depends(AuthUtils.get_current_data_from_token)):
    """
    🔒 Retorna os dados históricos de produção da uva, conforme disponibilizados pela Embrapa.

    Acesso permitido apenas para usuários com os seguintes papéis:
    - admin
    - superuser
    - user
    """
    allowed_roles = ["admin", "superuser", "user"]
    user_role = current_user_token.get("user_type")  
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este recurso.",
        )
    try:
        return UseCases.get_producao()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/processamento",
    response_model=List[Dict],
    summary="Obter dados de processamento",
    description="Retorna os dados de processamento de uva do Brasil conforme registros da Embrapa."
)
def get_processamento(current_user_token: dict = Depends(AuthUtils.get_current_data_from_token)):
    """
    🔒 Retorna os dados de processamento de uvas no Brasil, com base nas informações da Embrapa.

    Acesso permitido apenas para usuários autenticados.
    """
    try:
        return UseCases.get_processamento()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/comercializacao",
    response_model=List[Dict],
    summary="Obter dados de comercialização",
    description="Retorna os dados sobre a comercialização de uvas, conforme disponíveis nos relatórios da Embrapa."
)
def get_comercializacao(current_user_token: dict = Depends(AuthUtils.get_current_data_from_token)):
    """
    🔒 Retorna os dados de comercialização de uvas (quantidade, valores etc), conforme informações da Embrapa.

    Acesso permitido apenas para usuários autenticados.
    """
    try:
        return UseCases.get_comercializacao()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/importacao",
    response_model=List[Dict],
    summary="Obter dados de importação",
    description="Retorna os dados históricos de importação de uvas disponíveis nos relatórios da Embrapa."
)
def get_importacao(current_user_token: dict = Depends(AuthUtils.get_current_data_from_token)):
    """
    🔒 Retorna os dados de importação de uvas ao longo dos anos, conforme coletados pela Embrapa.

    Acesso permitido apenas para usuários autenticados.
    """
    try:
        return UseCases.get_importacao()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/exportacao",
    response_model=List[Dict],
    summary="Obter dados de exportação",
    description="Retorna os dados históricos de exportação de uvas do Brasil, conforme registros da Embrapa."
)
def get_exportacao(current_user_token: dict = Depends(AuthUtils.get_current_data_from_token)):
    """
    🔒 Retorna os dados de exportação de uvas do Brasil, com base nos relatórios da Embrapa.

    Acesso permitido apenas para usuários autenticados.
    """
    try:
        return UseCases.get_exportacao()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
